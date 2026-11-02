#!/usr/bin/env python3
"""Classify self-redefinition opportunities from existing passive GEM5 traces."""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass, field
import gzip
import json
from pathlib import Path
import re
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'register_reuse_analysis'))
from analyze import stat_blocks,write_csv
from run import file_sha256

RENAME=re.compile(r'^\s*(\d+):.*\[sn:(\d+)\] Renaming instruction with PC \((0x[0-9a-fA-F]+)=>')
SOURCE=re.compile(r'Looking up (IntRegClass|FloatRegClass) arch reg x(\d+), got \[phys: (\d+)\]')
DEST=re.compile(r'(Rename|Mov) arch reg x(\d+) \((\w+)\) from \[phys: (\d+)\] to \[phys: (\d+)\]')
FREE=re.compile(r'^\s*(\d+):.*Really free up p(\d+) on squash')
SQUASH=re.compile(r'^\s*(\d+):.*\[squash sn:(\d+)\] Squashing instructions')
EXEC=re.compile(r'FetchSeq=(\d+).*flags=\(([^)]*)\)')
BAD_FLAGS=frozenset(('IsLoad','IsStore','IsAtomic','IsControl','IsVector','IsMicroop',
                     'IsMov','IsNonSpeculative','IsFusion'))


@dataclass(slots=True)
class Instruction:
    seq:int
    rename:int=0
    pc:int=0
    sources:list=field(default_factory=list)
    dests:list=field(default_factory=list)
    flags:frozenset|None=None
    complete:int=0
    retire:int=0
    squash:int=0
    disasm:str=''
    micro:int=0


@dataclass(slots=True)
class Value:
    producer:int
    regclass:str
    arch:int
    readers:list=field(default_factory=list)
    aliased:bool=False
    release:int=0


def parse_trace(path):
    instructions={}
    values=[]
    physical={}
    alive={}
    current=None
    pipe=None
    flags_cache={}
    def value_for(tag,cls,arch):
        if tag not in physical:
            physical[tag]=len(values)
            values.append(Value(0,cls,arch))
        return physical[tag]
    with gzip.open(path,'rt') as handle:
        for line in handle:
            if line.startswith('O3PipeView:'):
                parts=line.rstrip().split(':',6)
                kind=parts[1]
                if kind=='fetch':
                    seq=int(parts[5]);pipe=instructions.get(seq)
                    if pipe:
                        pipe.micro=int(parts[4]);pipe.disasm=parts[6] if len(parts)>6 else ''
                elif pipe and kind=='complete':pipe.complete=int(parts[2])
                elif pipe and kind=='retire' and int(parts[2]):pipe.retire=int(parts[2])
                continue
            if 'Renaming instruction with PC' in line:
                match=RENAME.search(line)
                if match:
                    tick,seq,pc=int(match[1]),int(match[2]),int(match[3],16)
                    if seq in instructions:raise ValueError(f'duplicate dynamic rename seq {seq}')
                    current=Instruction(seq,rename=tick,pc=pc)
                    instructions[seq]=current;alive[seq]=current
                continue
            if 'Looking up ' in line:
                match=SOURCE.search(line)
                if current and match:
                    cls,arch,tag=match[1],int(match[2]),int(match[3])
                    vid=value_for(tag,cls,arch)
                    if vid not in current.sources:
                        current.sources.append(vid);values[vid].readers.append(current.seq)
                continue
            if ' arch reg ' in line and ('Rename arch' in line or 'Mov arch' in line):
                match=DEST.search(line)
                if current and match:
                    action,arch,cls,old,new=match[1],int(match[2]),match[3],int(match[4]),int(match[5])
                    oldvid=None
                    if cls in ('IntRegClass','FloatRegClass'):
                        oldvid=value_for(old,cls,arch)
                        if new!=old:
                            if action=='Mov':
                                newvid=value_for(new,cls,arch);values[newvid].aliased=True
                            else:
                                newvid=len(values);values.append(Value(current.seq,cls,arch))
                                physical[new]=newvid
                    current.dests.append((cls,arch,oldvid,old,new))
                continue
            if 'Really free up p' in line:
                match=FREE.search(line)
                if match:
                    vid=physical.get(int(match[2]))
                    if vid is not None:values[vid].release=int(match[1])
                continue
            if '[squash sn:' in line:
                match=SQUASH.search(line)
                if match:
                    tick,threshold=int(match[1]),int(match[2])
                    for seq in list(alive):
                        if seq>threshold:
                            inst=alive.pop(seq)
                            if not inst.squash:inst.squash=tick
                continue
            if 'FetchSeq=' in line and 'flags=(' in line:
                match=EXEC.search(line)
                if match:
                    seq=int(match[1]);inst=instructions.get(seq)
                    if inst:
                        text=match[2]
                        if text not in flags_cache:flags_cache[text]=frozenset(text.split('|'))
                        inst.flags=flags_cache[text]
                        alive.pop(seq,None)
    return instructions,values


def allowed(inst):
    return inst.flags is not None and not (inst.flags & BAD_FLAGS) and not inst.micro


def classify_prior(priors,rename_tick,writeback_tick):
    """Four nested opportunities: commit-proven, restricted-WB proxy, all-WB proxy."""
    committed=lambda i:bool(i.retire and i.retire<=rename_tick)
    complete=lambda i,t:bool(i.complete and i.complete<=t)
    return dict(committed_before_rename=all(committed(i) for i in priors),
                restricted_wb_before_rename=all(committed(i) or (allowed(i) and complete(i,rename_tick)) for i in priors),
                any_wb_before_rename=all(committed(i) or complete(i,rename_tick) for i in priors),
                any_wb_before_overwriter_wb=all((i.retire and i.retire<=writeback_tick) or
                                               complete(i,writeback_tick) for i in priors))


class Intervals:
    def __init__(self,intervals):
        merged=[]
        for start,end in sorted(intervals):
            if end<=start:continue
            if merged and start<=merged[-1][1]:merged[-1][1]=max(end,merged[-1][1])
            else:merged.append([start,end])
        self.intervals=merged
        self.starts=[s for s,e in merged]
        self.ends=[e for s,e in merged]
        self.prefix=[0]
        for s,e in merged:self.prefix.append(self.prefix[-1]+e-s)
    def before(self,t):
        index=bisect_right(self.ends,t)
        total=self.prefix[index]
        if index<len(self.starts) and self.starts[index]<t:
            total+=t-self.starts[index]
        return total
    def overlap(self,start,end):return max(0,self.before(end)-self.before(start))


def shortage_intervals(directory,epoch,period):
    selected=defaultdict(list)
    with (directory/'reg-pressure.csv').open() as handle:
        for row in csv.DictReader(handle):
            if row['kind']=='stall' and int(row['epoch'])==epoch:
                selected[int(row['class'])].append((int(row['start_cycle'])*period,
                                                   int(row['end_cycle'])*period))
    return [Intervals(selected[c]) for c in range(2)]


def summarize(directory):
    directory=Path(directory)
    meta=json.loads((directory/'run.json').read_text())
    if not meta.get('ok'):raise ValueError(f'unsuccessful simulation: {directory}')
    stats=stat_blocks(directory/'stats.txt')[-1]
    marker=json.loads((directory/'trace-window.json').read_text())
    if not marker['enabled']:raise ValueError('trace disabled')
    start_tick=marker['start_tick']
    import configparser
    cp=configparser.ConfigParser();cp.read(directory/'config.ini')
    period=int(cp['system.cpu_clk_domain']['clock'].split()[0])
    instructions,values=parse_trace(directory/'trace.gz')
    shortages=shortage_intervals(directory,int(stats['system.cpu.regPressure.epoch']),period)
    counters=Counter()
    candidate_rows=[]
    retired=[i for i in instructions.values() if i.retire]
    committed=[i for i in retired if i.flags is not None]
    counters['trace_retired']=len(retired)
    counters['trace_committed_with_flags']=len(committed)
    pcs=defaultdict(Counter)
    exposure=defaultdict(list)
    fields=('committed_before_rename','restricted_wb_before_rename','any_wb_before_rename')
    for inst in committed:
        if not allowed(inst) or len(inst.dests)!=1:continue
        cls,arch,vid,oldtag,newtag=inst.dests[0]
        if vid is None or vid not in inst.sources or oldtag==newtag:continue
        counters['self_redef_scalar']+=1
        value=values[vid]
        if not value.producer or value.producer not in instructions:
            counters['excluded_cross_window']+=1;continue
        producer=instructions[value.producer]
        if not producer.retire:
            counters['excluded_uncommitted_producer']+=1;continue
        if value.aliased:
            counters['excluded_aliased']+=1;continue
        if value.regclass!=cls or value.arch!=arch:
            counters['excluded_identity']+=1;continue
        prior=[instructions[s] for s in value.readers if s<inst.seq
               and not (instructions[s].squash and instructions[s].squash<=inst.rename)]
        counters['eligible_self_redef']+=1
        label='int' if cls=='IntRegClass' else 'fp';c=0 if label=='int' else 1
        counters[label+'_eligible_self_redef']+=1
        if not prior:
            counters['single_consumer_existing']+=1
            counters[label+'_single_consumer_existing']+=1
            continue
        counters['multiple_consumers']+=1;counters[label+'_multiple_consumers']+=1
        ready=classify_prior(prior,inst.rename,inst.complete)
        row=dict(seq=inst.seq,pc=hex(inst.pc),regclass=label,arch=arch,prior_consumers=len(prior),
                 rename_tick=inst.rename,complete_tick=inst.complete,release_tick=value.release,
                 **ready,disasm=inst.disasm)
        for name in fields:
            if ready[name]:
                counters[name]+=1;counters[label+'_'+name]+=1
                pcs[name][(row['pc'],inst.disasm)]+=1
                if value.release>inst.rename:
                    hold_start=inst.rename
                    overlap=shortages[c].overlap(hold_start,value.release)
                    counters[name+'_slot_shortage_ticks']+=overlap
                    exposure[name].append((hold_start,value.release,c))
                    if overlap:counters[name+'_overlap_values']+=1
                else:counters[name+'_missing_release']+=1
        if len(candidate_rows)<30 and (ready['committed_before_rename'] or ready['restricted_wb_before_rename']):
            row['prior_details']=[dict(seq=p.seq,retire=p.retire,complete=p.complete,
                                       flags=sorted(p.flags) if p.flags else None,disasm=p.disasm) for p in prior]
            candidate_rows.append(row)
    # Union of shortage cycles with any eligible value, not summed slot-cycles.
    for name in fields:
        overlaps=0
        for c in range(2):
            spans=Intervals((s,e) for s,e,cls in exposure[name] if cls==c)
            overlaps+=sum(shortages[c].overlap(s,e) for s,e in spans.intervals)
        counters[name+'_union_class_shortage_ticks']=overlaps
    for c,label in enumerate(('int','fp')):
        measured=shortages[c].prefix[-1]/period
        expected=stats['system.cpu.regPressure.shortageCycles::'+('int' if c==0 else 'float')]
        if measured!=expected:raise ValueError('CSV/stats shortage mismatch')
    result={k:meta[k] for k in ('workload','point','weight','int_regs','float_regs','warmup','measure')}
    result.update(analysis_sha256=file_sha256(__file__),
                  instructions=stats['simInsts'],cycles=stats['system.cpu.numCycles'],
                  decoded_fusion_pairs=stats.get('system.cpu.decode.numFusedInsts',0),
                  simulated_ops=stats.get('simOps',stats['simInsts']),
                  observer_schema=stats['system.cpu.regPressure.schemaVersion'],
                  standalone_stall_fraction=stats['system.cpu.regPressure.standaloneStallCycles']/stats['system.cpu.numCycles'],
                  int_shortage_cycles=stats['system.cpu.regPressure.shortageCycles::int'],
                  fp_shortage_cycles=stats['system.cpu.regPressure.shortageCycles::float'],
                  trace_start_tick=start_tick,period=period,counts=dict(counters),examples=candidate_rows,
                  top_pcs={k:[dict(pc=pc,disasm=asm,count=n) for (pc,asm),n in counts.most_common(10)]
                           for k,counts in pcs.items()})
    result['trace_coverage']=len(retired)/result['instructions']
    result['candidate_flags_coverage']=len(committed)/len(retired) if retired else 0
    for name in fields:
        result[name+'_per_1000_insts']=1000*counters[name]/result['instructions']
    for candidate in candidate_rows:
        candidate['rename_cycle']=candidate['rename_tick']//period
    assert counters['eligible_self_redef']==counters['single_consumer_existing']+counters['multiple_consumers']
    assert counters['committed_before_rename']<=counters['restricted_wb_before_rename']<=counters['any_wb_before_rename']<=counters['multiple_consumers']
    (directory/'opportunities.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def report(rows,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(dict(runs=rows),indent=2)+'\n')
    flat=[{k:v for k,v in row.items() if k not in ('examples','top_pcs','counts')}|row['counts'] for row in rows]
    write_csv(out/'per_run.csv',flat)
    lines=['# 最后消费者扩展：切片机会统计','',
           '被动观察现有 baseline，不改变分配、执行或释放。候选为单标量目的、同时读取同一逻辑旧值的重定义指令；排除别名、访存、控制、microop、move、非推测和 fusion 指令。',
           '只统计 trace 内生产者已提交、重定义也已提交的值，跨窗口样本排除。已有单消费者机会与新增多消费者机会分开。',
           '“已提交”要求所有此前仍有效的消费者在重定义实际 rename 前已提交；“受限 WB”额外允许普通标量消费者在此前完成最后一次 writeback，访存/控制等仍保守到提交；“全部 WB”允许所有类型，属于更乐观的时间代理。',
           'WB 不是硬件稳定 readDone 证明；统计也没有施加共享后的版本上限、shadow 容量、端口或调度反馈，所以是应用空间筛查，不能解读为性能增益。','',
           '| Workload | INT/FP | 原单消费者候选 | 新增：此前已提交 | 新增：受限WB | 新增：全部WB | 受限WB/千指令 |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for r in sorted(rows,key=lambda r:(r['int_regs'],r['float_regs'],r['workload'])):
        c=r['counts'];v=lambda k:c.get(k,0)
        lines.append(f'| {r["workload"]} | {r["int_regs"]}/{r["float_regs"]} | {v("single_consumer_existing")} | {v("committed_before_rename")} | {v("restricted_wb_before_rename")} | {v("any_wb_before_rename")} | {r["restricted_wb_before_rename_per_1000_insts"]:.3f} |')
    lines+=['','新增受限 WB 候选在 baseline 中的占位区间 `[rename, old-value release)` 与同类型容量不足的重叠：','',
            '| Workload | INT/FP | 独立容量阻塞 | 新增候选占位与不足重叠的寄存器周期 | 平均每次候选重叠周期 |',
            '|---|---:|---:|---:|---:|']
    for r in sorted(rows,key=lambda r:(r['int_regs'],r['float_regs'],r['workload'])):
        c=r['counts'];ticks=c.get('restricted_wb_before_rename_slot_shortage_ticks',0)
        count=c.get('restricted_wb_before_rename',0)
        lines.append(f'| {r["workload"]} | {r["int_regs"]}/{r["float_regs"]} | {r["standalone_stall_fraction"]:.2%} | {ticks/r["period"]:.0f} | {ticks/r["period"]/count if count else 0:.2f} |')
    lines+=['','占位重叠是寄存器周期，多个值可重复覆盖同一周期，不能当作可消除的停顿比例。',
            '每个 workload 仅一个最高权重切片；计数来自该切片的测量窗口，不是全 workload 或全 SPEC 分数。',
            '覆盖限制：现有 O3PipeView 在 Decode 新建的 fused DynInst 上缺少 fetch 时间，因此没有其完整流水线时间。fusion 候选及无法确认 producer/consumer 时间的样本排除。libquantum 的原始架构指令 trace 覆盖约 77.57%，gcc 约 99.7%，其他切片约 99.96% 以上；机会计数不外推到未覆盖部分。',
            '原始逐点计数见 `per_run.csv`；每个运行目录的 `opportunities.json` 含具体 PC、消费者完成时间和候选示例。']
    (out/'report.md').write_text('\n'.join(lines)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('results',type=Path)
    p.add_argument('--out',type=Path)
    p.add_argument('--refresh',action='store_true')
    args=p.parse_args()
    rows=[]
    paths=sorted(args.results.glob('*/*/*/run.json'))
    for n,path in enumerate(paths,1):
        directory=path.parent
        meta=json.loads(path.read_text())
        if not meta.get('ok'):raise ValueError(f'incomplete run: {directory}')
        start=time.monotonic();cached=directory/'opportunities.json'
        row=json.loads(cached.read_text()) if cached.exists() and not args.refresh else summarize(directory)
        rows.append(row)
        print(f'[{n}/{len(paths)}] {row["workload"]} {row["int_regs"]}/{row["float_regs"]} '
              f'extension={row["counts"].get("restricted_wb_before_rename",0)} '
              f'coverage={row["trace_coverage"]:.4%} {time.monotonic()-start:.1f}s',flush=True)
    if not rows:p.error('no successful run.json files')
    report(rows,args.out or args.results/'opportunity-summary')
    return 0


if __name__=='__main__':sys.exit(main())

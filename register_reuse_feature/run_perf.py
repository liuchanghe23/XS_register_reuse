#!/usr/bin/env python3
"""Pair reuse-off/certain/predicted runs on the same checkpoint and capacity."""
import argparse
import concurrent.futures
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT/'GEM5'
sys.path.insert(0,str(ROOT/'register_reuse_analysis'))
from analyze import stat_blocks
from run import file_sha256


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workloads',default='mcf,bzip2_combined,gcc_166,hmmer_nph3,libquantum,GemsFDTD,bwaves,leslie3d')
    p.add_argument('--capacities',default='224:256,192:208')
    p.add_argument('--modes',default='off,certain,predicted')
    p.add_argument('--warmup',type=int,default=1000000)
    p.add_argument('--measure',type=int,default=1000000)
    p.add_argument('--jobs',type=int,default=12)
    p.add_argument('--timeout',type=int,default=1800)
    p.add_argument('--out',type=Path,default=HERE/'performance')
    args=p.parse_args()
    args.out=args.out.absolute();args.out.mkdir(parents=True,exist_ok=True)
    binary=HERE/'build/RISCV/gem5.opt'
    binary_hash=file_sha256(binary)
    ref=os.environ.get('GCBV_REF_SO','/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so')
    meta=json.loads((ROOT/'zstd-checkpoint-0-0-0/cluster-0-0.json').read_text())
    tasks=[]
    for workload in args.workloads.split(','):
        point,weight=max(meta[workload]['points'].items(),key=lambda kv:float(kv[1]))
        checkpoint=next((ROOT/'zstd-checkpoint-0-0-0'/workload/point).glob('*.zstd'))
        for ni,nf in (map(int,item.split(':')) for item in args.capacities.split(',')):
            for mode in args.modes.split(','):
                if mode not in ('off','certain','predicted'):p.error('invalid mode')
                dest=args.out/workload/point/f'{ni}-{nf}'/mode
                command=[str(binary),'--outdir='+str(dest),str(REPO/'configs/example/kmhv3.py'),
                    '--generic-rv-cpt='+str(checkpoint),'--difftest-ref-so='+ref,
                    f'--warmup-insts-no-switch={args.warmup}',f'--maxinsts={args.warmup+args.measure}']
                params={'numPhysIntRegs':ni,'numPhysFloatRegs':nf,
                    'enableRegisterReuse':mode!='off','regReusePrediction':mode=='predicted',
                    'enableRegPressureStats':False}
                for key,value in params.items():command+=['--param',f'system.cpu[0].{key}={value}']
                tasks.append(dict(workload=workload,point=point,weight=float(weight),int_regs=ni,
                    float_regs=nf,mode=mode,out=str(dest),command=command,binary_sha256=binary_hash,
                    warmup=args.warmup,measure=args.measure))
    (args.out/'manifest.json').write_text(json.dumps(tasks,indent=2)+'\n')
    def run(task):
        dest=Path(task['out']);dest.mkdir(parents=True,exist_ok=True)
        result_file=dest/'result.json'
        if result_file.exists():
            old=json.loads(result_file.read_text())
            if old.get('ok') and old['command']==task['command'] and old['binary_sha256']==binary_hash:
                return old
            if old.get('ok'):raise ValueError(f'incompatible completed run: {dest}')
        start=time.monotonic()
        with (dest/'run.log').open('w') as log:
            try:rc=subprocess.run(task['command'],cwd=REPO,stdout=log,stderr=subprocess.STDOUT,timeout=args.timeout).returncode
            except subprocess.TimeoutExpired:rc=124
        text=(dest/'run.log').read_text(errors='replace')
        result=dict(task,returncode=rc,elapsed=time.monotonic()-start,
                    ok=rc==0 and 'because a thread reached the max instruction count' in text)
        if result['ok']:
            stats=stat_blocks(dest/'stats.txt')[-1]
            result['instructions']=stats['simInsts'];result['cycles']=stats['system.cpu.numCycles']
            result['ipc']=result['instructions']/result['cycles']
            result['reuse_stats']={key.split('.regReuse.')[1]:value for key,value in stats.items() if '.regReuse.' in key}
            result['ok'] &= result['instructions']>=.99*args.measure
        result_file.write_text(json.dumps(result,indent=2)+'\n')
        return result
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(run,task) for task in tasks]
        for i,future in enumerate(concurrent.futures.as_completed(futures),1):
            r=future.result();results.append(r)
            print(f"[{i}/{len(tasks)}] {'PASS' if r['ok'] else 'FAIL'} {r['workload']}/{r['int_regs']}-{r['float_regs']}/{r['mode']} IPC={r.get('ipc',0):.4f}",flush=True)
    results.sort(key=lambda r:(r['workload'],r['int_regs'],r['float_regs'],r['mode']))
    off={(r['workload'],r['int_regs'],r['float_regs']):r for r in results if r['mode']=='off' and r['ok']}
    ratios={}
    for r in results:
        base=off.get((r['workload'],r['int_regs'],r['float_regs']))
        if r['ok'] and base:
            r['speedup']=r['ipc']/base['ipc']
            ratios.setdefault((r['int_regs'],r['float_regs'],r['mode']),[]).append(r['speedup'])
    summary={'runs':results,'geomean':[
        dict(int_regs=ni,float_regs=nf,mode=mode,slices=len(values),speedup=math.exp(sum(map(math.log,values))/len(values)))
        for (ni,nf,mode),values in sorted(ratios.items())]}
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# Register reuse timing results','',
        'Single highest-weight checkpoint per workload; paired binary, capacity and instruction window. Uniform shadow storage, not equal-area comparisons.','',
        '| Workload | INT/FP | Mode | IPC | Speedup | Reuses | Repairs |',
        '|---|---:|---|---:|---:|---:|---:|']
    for r in results:
        st=r.get('reuse_stats',{})
        lines.append(f"| {r['workload']} | {r['int_regs']}/{r['float_regs']} | {r['mode']} | {r.get('ipc',0):.4f} | {r.get('speedup',0):.4f}x | {st.get('sharedVersions',0):.0f} | {st.get('repairCopies',0):.0f} |")
    lines+=['','Geometric means over these selected slices:','']
    for g in summary['geomean']:
        lines.append(f"- {g['int_regs']}/{g['float_regs']} {g['mode']}: {g['speedup']:.4f}x ({g['slices']} slices)")
    (args.out/'report.md').write_text('\n'.join(lines)+'\n')
    return 0 if all(r['ok'] for r in results) else 1


if __name__=='__main__':sys.exit(main())

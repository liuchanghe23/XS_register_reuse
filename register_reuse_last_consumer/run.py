#!/usr/bin/env python3
"""Collect passive traces for last-consumer opportunity screening on real slices."""
import argparse
import concurrent.futures
import configparser
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'register_reuse_analysis'))
from run import SCREEN, file_sha256, select_points
from analyze import stat_blocks


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=HERE/'slices-1m')
    p.add_argument('--workloads',default=','.join(SCREEN))
    p.add_argument('--capacities',default='224:256,192:208')
    p.add_argument('--warmup',type=int,default=1000000)
    p.add_argument('--measure',type=int,default=1000000)
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--timeout',type=int,default=3600)
    p.add_argument('--no-trace',action='store_true')
    p.add_argument('--raw',type=Path,help='bare-metal binary instead of checkpoint selection')
    args=p.parse_args()
    if min(args.warmup,args.measure,args.jobs,args.timeout)<=0:p.error('counts must be positive')
    args.out=args.out.absolute();args.out.mkdir(parents=True,exist_ok=True)
    binary=ROOT/'register_reuse_feature/build/RISCV/gem5.opt'
    reference=Path(os.environ.get('GCBV_REF_SO') or '/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so')
    if not reference.is_file():p.error('missing reference; set GCBV_REF_SO')
    metadata=json.loads((ROOT/'zstd-checkpoint-0-0-0/cluster-0-0.json').read_text())
    selected=[]
    if args.raw:
        selected=[('synthetic','0',1.,args.raw.absolute())]
    else:
        for workload in args.workloads.split(','):
            point,weight=select_points(metadata[workload]['points'],top=1)[0][0]
            checkpoint=next((ROOT/'zstd-checkpoint-0-0-0'/workload/point).glob('*.zstd'))
            selected.append((workload,point,weight,checkpoint))
    identity=dict(binary_sha256=file_sha256(binary),reference_sha256=file_sha256(reference),
                  wrapper_sha256=file_sha256(HERE/'trace_config.py'),warmup=args.warmup,
                  measure=args.measure,capacities=args.capacities,no_trace=args.no_trace,
                  selected=[(w,pt,weight,str(cpt)) for w,pt,weight,cpt in selected])
    manifest=args.out/'manifest.json'
    if manifest.exists() and json.loads(manifest.read_text())['identity']!=json.loads(json.dumps(identity)):
        p.error('experiment identity differs; use a new --out')
    tasks=[]
    for workload,point,weight,checkpoint in selected:
        for ni,nf in [map(int,c.split(':')) for c in args.capacities.split(',')]:
            dest=args.out/workload/point/f'{ni}-{nf}'
            command=[str(binary),'--debug-file=trace.gz','--outdir='+str(dest),str(HERE/'trace_config.py'),
                     '--generic-rv-cpt='+str(checkpoint),'--difftest-ref-so='+str(reference),
                     f'--warmup-insts-no-switch={args.warmup}',f'--maxinsts={args.warmup+args.measure}']
            if args.raw:command+=['--raw-cpt']
            for key,value in dict(enableRegisterReuse=False,enableRegPressureStats=True,
                                  regPressureTrace="'reg-pressure.csv'",numPhysIntRegs=ni,
                                  numPhysFloatRegs=nf,RobCompressPolicy="'none'").items():
                command+=['--param',f'system.cpu[0].{key}={value}']
            tasks.append(dict(workload=workload,point=point,weight=weight,int_regs=ni,float_regs=nf,
                              warmup=args.warmup,measure=args.measure,command=command,out=str(dest)))
    manifest.write_text(json.dumps(dict(identity=identity,tasks=tasks),indent=2)+'\n')
    def run(task):
        dest=Path(task['out']);dest.mkdir(parents=True,exist_ok=True)
        previous=dest/'run.json'
        if previous.exists():
            old=json.loads(previous.read_text())
            if old.get('ok') and old.get('command')==task['command']:
                return old,'SKIP'
        start=time.monotonic()
        env=os.environ.copy();env['LAST_CONSUMER_TRACE']='0' if args.no_trace else '1'
        with (dest/'run.log').open('w') as log:
            try:rc=subprocess.run(task['command'],cwd=ROOT/'GEM5',env=env,stdout=log,
                                  stderr=subprocess.STDOUT,timeout=args.timeout).returncode
            except subprocess.TimeoutExpired:rc=124
        info=dict(task,binary_sha256=identity['binary_sha256'],reference_sha256=identity['reference_sha256'],
                  returncode=rc,elapsed_seconds=round(time.monotonic()-start,3),ok=False)
        try:
            text=(dest/'run.log').read_text(errors='replace')
            assert rc==0 and 'because a thread reached the max instruction count' in text
            cp=configparser.ConfigParser();cp.read(dest/'config.ini');cpu=cp['system.cpu']
            assert cpu.getboolean('enable_difftest') and not cpu.getboolean('enableRegisterReuse')
            assert cpu.getboolean('enableRegPressureStats')
            assert cpu.getint('numPhysIntRegs')==task['int_regs'] and cpu.getint('numPhysFloatRegs')==task['float_regs']
            stats=stat_blocks(dest/'stats.txt')[-1]
            assert .99*args.measure<=stats['simInsts']<=args.measure+1024
            assert (dest/'trace-window.json').is_file()
            info.update(ok=True,instructions=stats['simInsts'],cycles=stats['system.cpu.numCycles'],
                        trace_bytes=(dest/'trace.gz').stat().st_size if (dest/'trace.gz').exists() else 0)
        except (AssertionError,KeyError,OSError,ValueError) as exc:info['error']=repr(exc)
        previous.write_text(json.dumps(info,indent=2)+'\n')
        return info,'OK' if info['ok'] else 'FAIL'
    all_ok=True
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for i,(info,status) in enumerate(pool.map(run,tasks),1):
            print(f'[{i}/{len(tasks)}] {status} {info["workload"]}/{info["int_regs"]}-{info["float_regs"]} '
                  f'{info["elapsed_seconds"]}s trace={info.get("trace_bytes",0)/1024**2:.1f}MB',flush=True)
            all_ok &= info['ok']
    return 0 if all_ok else 1


if __name__=='__main__':sys.exit(main())

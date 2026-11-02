#!/usr/bin/env python3
"""Run scalar reuse integration tests with NEMU difftest enabled."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT/'GEM5'
BINARY=HERE/'build/RISCV/gem5.opt'
REF=os.environ.get('GCBV_REF_SO','/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so')


def stats(path):
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('reuse_analysis',ROOT/'register_reuse_analysis/analyze.py')
    module=module_from_spec(spec);spec.loader.exec_module(module)
    return module.stat_blocks(path)[-1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--program',choices=['reuse','random'],default='reuse')
    args=parser.parse_args()
    program=args.program
    source=REPO/'tests/test-progs/register-reuse/reuse.S'
    if program=='random':
        subprocess.run([sys.executable,str(HERE/'generate_random.py')],check=True)
        source=HERE/'random.S'
    subprocess.run(['riscv64-linux-gnu-gcc','-nostdlib','-nostartfiles','-static',
        '-march=rv64gc','-mabi=lp64d','-Wl,-Ttext=0x80000000','-Wl,--build-id=none',
        '-o',str(HERE/(program+'.elf')),str(source)],check=True)
    subprocess.run(['riscv64-linux-gnu-objcopy','-O','binary',str(HERE/(program+'.elf')),str(HERE/(program+'.bin'))],check=True)
    cases=[('off',False,False,3,224,256),('certain',True,False,3,224,256),
           ('predicted',True,True,3,224,256),('one-shadow',True,True,1,224,256),
           ('small',True,True,3,64,64)]
    def run(case):
        name,enabled,predict,shadows,ni,nf=case
        out=HERE/(program+'-tests')/name;out.mkdir(parents=True,exist_ok=True)
        command=[str(BINARY),'--outdir='+str(out),str(REPO/'configs/example/kmhv3.py'),
            '--raw-cpt','--generic-rv-cpt='+str(HERE/(program+'.bin')),
            '--warmup-insts-no-switch=0','--maxinsts=100000',
            '--difftest-ref-so='+REF]
        params={'enableRegisterReuse':enabled,'regReusePrediction':predict,
                'regReuseShadowCopies':shadows,'numPhysIntRegs':ni,'numPhysFloatRegs':nf}
        for key,value in params.items():command+=['--param',f'system.cpu[0].{key}={value}']
        start=time.monotonic()
        with (out/'run.log').open('w') as log:
            try:rc=subprocess.run(command,cwd=REPO,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
            except subprocess.TimeoutExpired:rc=124
        text=(out/'run.log').read_text(errors='replace')
        result={'case':name,'command':command,'returncode':rc,'elapsed':time.monotonic()-start,
                'ok':rc==0 and 'because m5_exit instruction encountered' in text}
        if result['ok']:
            s=stats(out/'stats.txt')
            result['cycles']=s['system.cpu.numCycles'];result['instructions']=s['simInsts']
            result['reuse_stats']={key.split('regReuse.')[1]:value for key,value in s.items() if '.regReuse.' in key}
            if enabled:
                result['ok'] &= result['reuse_stats']['sharedVersions']>0
                result['ok'] &= result['reuse_stats']['deterministicReuses']>0
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(run,cases))
    (HERE/(program+'-correctness.json')).write_text(json.dumps(results,indent=2)+'\n')
    for result in results:
        print(result['case'],'PASS' if result['ok'] else 'FAIL',result.get('reuse_stats'),flush=True)
        if not result['ok']:
            print('\n'.join((HERE/(program+'-tests')/result['case']/'run.log').read_text(errors='replace').splitlines()[-15:]))
    return 0 if all(r['ok'] for r in results) else 1


if __name__=='__main__':sys.exit(main())

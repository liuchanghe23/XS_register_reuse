#!/usr/bin/env python3
"""Analyze completed passive traces in separate processes with bounded parallelism."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import time
from opportunities import summarize, report


def one(directory,refresh=False):
    start=time.monotonic()
    cached=directory/'opportunities.json'
    row=json.loads(cached.read_text()) if cached.exists() and not refresh else summarize(directory)
    return row,time.monotonic()-start


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('results',type=Path)
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--refresh',action='store_true')
    args=p.parse_args()
    expected=json.loads((args.results/'manifest.json').read_text())['tasks']
    directories=[]
    for task in expected:
        path=Path(task['out'])
        if (path/'run.json').exists() and json.loads((path/'run.json').read_text()).get('ok'):
            directories.append(path)
    rows=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        pending={pool.submit(one,d,args.refresh):d for d in directories}
        for future in concurrent.futures.as_completed(pending):
            row,seconds=future.result();rows.append(row)
            print(f'[{len(rows)}/{len(directories)}] {row["workload"]}/{row["int_regs"]}-{row["float_regs"]}: '
                  f'commit={row["counts"].get("committed_before_rename",0)} '
                  f'restrictedWB={row["counts"].get("restricted_wb_before_rename",0)} {seconds:.1f}s',flush=True)
    report(rows,args.results/'opportunity-summary')
    print(f'Analyzed {len(rows)}/{len(expected)} planned runs',flush=True)
    return 0 if len(rows)==len(expected) else 1


if __name__=='__main__':raise SystemExit(main())

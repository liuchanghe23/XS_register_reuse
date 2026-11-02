#!/usr/bin/env python3
"""Verify completed slice experiments against original OFF runs and analysis coverage."""
import argparse
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'register_reuse_analysis'))
from analyze import stat_blocks
from run import file_sha256


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--results',type=Path,default=HERE/'slices-1m')
    args=p.parse_args()
    root=args.results
    manifest=json.loads((root/'manifest.json').read_text())
    baseline=json.loads((ROOT/'register_reuse_feature/performance-validated/summary.json').read_text())
    refs={(r['workload'],r['point'],r['int_regs'],r['float_regs']):r for r in baseline['runs'] if r['mode']=='off'}
    binary=ROOT/'register_reuse_feature/build/RISCV/gem5.opt'
    assert file_sha256(binary)==manifest['identity']['binary_sha256']
    checks=[]
    for task in manifest['tasks']:
        path=Path(task['out'])
        meta=json.loads((path/'run.json').read_text())
        row=json.loads((path/'opportunities.json').read_text())
        stats=stat_blocks(path/'stats.txt')[-1]
        assert meta['ok'] and meta['returncode']==0
        assert row['analysis_sha256']==file_sha256(HERE/'opportunities.py')
        assert meta['binary_sha256']==manifest['identity']['binary_sha256']
        assert meta['reference_sha256']==manifest['identity']['reference_sha256']
        assert row['instructions']==meta['instructions']==stats['simInsts']
        assert row['cycles']==meta['cycles']==stats['system.cpu.numCycles']
        old=refs[meta['workload'],meta['point'],meta['int_regs'],meta['float_regs']]
        assert old['binary_sha256']==meta['binary_sha256']
        assert (old['warmup'],old['measure'])==(meta['warmup'],meta['measure'])
        assert old['instructions']==meta['instructions'] and old['cycles']==meta['cycles']
        counts=row['counts']
        assert counts['eligible_self_redef']==counts['single_consumer_existing']+counts['multiple_consumers']
        assert counts.get('committed_before_rename',0)<=counts.get('restricted_wb_before_rename',0)<=counts.get('any_wb_before_rename',0)<=counts['multiple_consumers']
        for c in row['examples']:
            if c['committed_before_rename']:
                assert all(0<r['retire']<=c['rename_tick'] for r in c['prior_details'])
        checks.append(dict(workload=meta['workload'],point=meta['point'],int_regs=meta['int_regs'],
                           float_regs=meta['float_regs'],difftest_passed=True,
                           baseline_instructions_equal=True,baseline_cycles_equal=True,
                           trace_coverage=row['trace_coverage'],decoded_fusion_pairs=row['decoded_fusion_pairs'],
                           conservative_new=counts.get('committed_before_rename',0),
                           restricted_wb_new=counts.get('restricted_wb_before_rename',0)))
    synthetic=HERE/'synthetic-validation/synthetic/0/224-256/opportunities.json'
    synthetic_row=json.loads(synthetic.read_text())
    assert synthetic_row['counts']['committed_before_rename']==34
    result=dict(ok=True,simulations=len(checks),planned=len(manifest['tasks']),
                all_baseline_cycles_and_instructions_equal=True,
                binary_sha256=manifest['identity']['binary_sha256'],
                reference_sha256=manifest['identity']['reference_sha256'],
                analyzer_sha256=file_sha256(HERE/'opportunities.py'),
                synthetic_conservative_opportunities=34,unit_tests=7,runs=checks)
    (root/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(checks)} difftest slice runs; original OFF cycles/instructions identical; synthetic=34')
    return 0


if __name__=='__main__':raise SystemExit(main())

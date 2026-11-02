#!/usr/bin/env python3
"""Run reproducible Kunminghu V3 physical-register pressure measurements."""
import argparse
import concurrent.futures
import configparser
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCREEN = ['mcf', 'bzip2_combined', 'gcc_166', 'hmmer_nph3',
          'libquantum', 'GemsFDTD', 'bwaves', 'leslie3d']


def positive(value):
    result = int(float(value))
    if result <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return result


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def select_points(points, top=1, coverage=None):
    """Select by weight; coverage=1 explicitly means every available point."""
    chosen, weight = [], 0.0
    for point, value in sorted(points.items(), key=lambda item: -float(item[1])):
        if coverage is None and len(chosen) >= top:
            break
        if coverage is not None and coverage < 1 and weight >= coverage:
            break
        weight += float(value)
        chosen.append((point, float(value)))
    return chosen, weight


def parse_reg_points(text):
    """Parse explicit label:integer_count:float_count capacity points."""
    points = []
    labels = set()
    for spec in text.split(','):
        parts = spec.split(':')
        if len(parts) != 3:
            raise ValueError('each capacity point must be label:INT:FP')
        label, int_text, fp_text = parts
        if not label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in label):
            raise ValueError('capacity point labels may contain only letters, digits, _ and -')
        if label in labels:
            raise ValueError(f'duplicate capacity label: {label}')
        nint, nfp = int(int_text), int(fp_text)
        if nint < 48 or nfp < 48:
            raise ValueError('use capacities >=48 to retain architectural registers and rename headroom')
        labels.add(label)
        points.append((label, nint, nfp))
    return points


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gem5', type=Path, default=ROOT / 'build/RISCV/gem5.opt')
    p.add_argument('--repo', type=Path, default=ROOT / 'GEM5')
    p.add_argument('--checkpoints', type=Path, default=ROOT / 'zstd-checkpoint-0-0-0')
    p.add_argument('--out', type=Path, default=HERE / 'results')
    p.add_argument('--suite', choices=['screen', 'all'], default='screen')
    p.add_argument('--workloads', help='comma-separated names, overrides suite')
    p.add_argument('--top', type=positive, default=1,
                   help='highest-weight slices per workload (default 1)')
    p.add_argument('--coverage', type=float, help='instead of --top, select slices to this weight coverage')
    p.add_argument('--variants', default='baseline,large',
                   help='comma-separated baseline,large,large-int,large-fp')
    p.add_argument('--reg-points', help='explicit label:INT:FP points, comma separated; overrides --variants')
    p.add_argument('--large-regs', type=positive, default=1024)
    p.add_argument('--small-regs', type=positive, default=96,
                   help='capacity for small/small-int/small-fp sensitivity variants')
    p.add_argument('--warmup', type=positive, default=1000000)
    p.add_argument('--measure', type=positive, default=2000000)
    p.add_argument('--jobs', type=positive, default=4)
    p.add_argument('--timeout', type=positive, default=7200, help='wall seconds per simulation')
    p.add_argument('--no-profile', action='store_true', help='disable the passive observer for a timing A/B check')
    p.add_argument('--disable-difftest', action='store_true')
    p.add_argument('--no-trace', action='store_true', help='omit interval CSV (stats remain available)')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    if args.coverage is not None and not 0 < args.coverage <= 1:
        p.error('--coverage must lie in (0,1]')
    variants = args.variants.split(',')
    if any(v not in ('baseline', 'large', 'large-int', 'large-fp', 'small', 'small-int', 'small-fp') for v in variants):
        p.error('invalid variant')
    try:
        if args.reg_points:
            reg_points = parse_reg_points(args.reg_points)
        else:
            reg_points = []
            for variant in variants:
                nint, nfp = 224, 256
                if variant in ('large', 'large-int'):
                    nint = args.large_regs
                if variant in ('large', 'large-fp'):
                    nfp = args.large_regs
                if variant in ('small', 'small-int'):
                    nint = args.small_regs
                if variant in ('small', 'small-fp'):
                    nfp = args.small_regs
                reg_points.append((variant, nint, nfp))
    except ValueError as exc:
        p.error(str(exc))
    args.out = args.out.absolute()
    args.repo = args.repo.resolve()
    args.gem5 = args.gem5.absolute()
    args.checkpoints = args.checkpoints.absolute()
    metadata = json.loads((args.checkpoints / 'cluster-0-0.json').read_text())
    workloads = args.workloads.split(',') if args.workloads else (
        SCREEN if args.suite == 'screen' else sorted(metadata))
    ref = os.environ.get('GCBV_REF_SO', '/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so')
    if not args.disable_difftest and not Path(ref).is_file():
        p.error(f'missing NEMU reference: {ref}; set GCBV_REF_SO')
    if not args.dry_run and not args.gem5.is_file():
        p.error(f'missing binary: {args.gem5}; run build.sh first')
    tasks = []
    for workload in workloads:
        if workload not in metadata:
            p.error(f'unknown workload: {workload}')
        selected, coverage = select_points(metadata[workload]['points'], args.top, args.coverage)
        for point, weight in selected:
            files = sorted((args.checkpoints / workload / point).glob('*.zstd'))
            if len(files) != 1:
                p.error(f'expected one checkpoint at {workload}/{point}: {files}')
            checkpoint = files[0]
            for variant, nint, nfp in reg_points:
                dest = args.out / workload / point / variant
                params = []
                if not args.no_profile:
                    params += ['system.cpu[0].enableRegPressureStats=True']
                    if not args.no_trace:
                        params += ["system.cpu[0].regPressureTrace='reg-pressure.csv'"]
                params += [f'system.cpu[0].numPhysIntRegs={nint}',
                           f'system.cpu[0].numPhysFloatRegs={nfp}']
                command = [str(args.gem5), f'--outdir={dest}',
                           str(args.repo / 'configs/example/kmhv3.py'),
                           f'--generic-rv-cpt={checkpoint}',
                           f'--warmup-insts-no-switch={args.warmup}',
                           f'--maxinsts={args.warmup + args.measure}']
                if args.disable_difftest:
                    command += ['--disable-difftest']
                else:
                    command += [f'--difftest-ref-so={ref}']
                for param in params:
                    command += ['--param', param]
                tasks.append(dict(workload=workload, point=point, weight=weight,
                                  selected_workload_coverage=coverage,
                                  variant=variant, int_regs=nint, float_regs=nfp,
                                  checkpoint=str(checkpoint),
                                  warmup=args.warmup, measure=args.measure,
                                  command=command, out=str(dest)))
    print(f'{len(tasks)} runs; {args.warmup:,} warmup + {args.measure:,} measured instructions; jobs={args.jobs}', flush=True)
    if args.dry_run:
        for task in tasks:
            print(shlex.join(task['command']))
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    binary_hash = file_sha256(args.gem5)
    revision = subprocess.check_output(['git', '-C', str(args.repo), 'rev-parse', 'HEAD'], text=True).strip()
    diff = subprocess.check_output(['git', '-C', str(args.repo), 'diff'], text=True)
    (args.out / 'source.diff').write_text(diff)
    # Include untracked observer sources in the provenance snapshot.
    for name in ('register_pressure.cc', 'register_pressure.hh'):
        src = args.repo / 'src/cpu/o3' / name
        if src.exists():
            (args.out / name).write_text(src.read_text())
    (args.out / 'manifest.json').write_text(json.dumps(tasks, indent=2) + '\n')

    def run(task):
        dest = Path(task['out'])
        dest.mkdir(parents=True, exist_ok=True)
        meta_path = dest / 'run.json'
        if meta_path.exists():
            old = json.loads(meta_path.read_text())
            matches = all(old.get(key) == task[key] for key in ('command', 'warmup', 'measure'))
            if old.get('ok') and matches and old.get('binary_sha256') == binary_hash:
                return f"SKIP {task['workload']}/{task['point']}/{task['variant']}", True
            if old.get('ok'):
                return f'REFUSE incompatible completed run: {dest}; select a new --out', False
        info = dict(task, binary_sha256=binary_hash, revision=revision,
                    started=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
        meta_path.write_text(json.dumps(info, indent=2) + '\n')
        start = time.monotonic()
        try:
            with (dest / 'run.log').open('w') as log:
                proc = subprocess.run(task['command'], cwd=args.repo,
                                      stdout=log, stderr=subprocess.STDOUT,
                                      timeout=args.timeout)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc = 124
        text = (dest / 'run.log').read_text(errors='replace')
        expected_exit = 'because a thread reached the max instruction count' in text
        cp = configparser.ConfigParser()
        cp.read(dest / 'config.ini')
        config_matches = ('system.cpu' in cp and
                          cp['system.cpu'].getint('numPhysIntRegs') == task['int_regs'] and
                          cp['system.cpu'].getint('numPhysFloatRegs') == task['float_regs'])
        info.update(returncode=rc, config_matches=config_matches, elapsed_seconds=round(time.monotonic() - start, 3),
                    ok=rc == 0 and expected_exit and config_matches and (dest / 'stats.txt').is_file())
        meta_path.write_text(json.dumps(info, indent=2) + '\n')
        status = 'OK' if info['ok'] else 'FAIL'
        return f"{status} {task['workload']}/{task['point']}/{task['variant']} {info['elapsed_seconds']:.1f}s", info['ok']

    success = True
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run, task) for task in tasks]
        for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
            line, ok = future.result()
            print(f'[{completed}/{len(tasks)}] {line}', flush=True)
            success &= ok
    if success:
        print(f'Analyze: python3 {HERE / "analyze.py"} {args.out}', flush=True)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

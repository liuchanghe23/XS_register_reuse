#!/usr/bin/env python3
"""Launch, resume, and summarize a large checkpoint capacity experiment."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

from run import file_sha256, parse_reg_points, select_points

HERE = Path(__file__).resolve().parent


def resolve_path(base, value):
    path = Path(value).expanduser()
    return Path(os.path.abspath(path if path.is_absolute() else base / path))


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def make_plan(config, config_dir, args):
    profile = args.profile or config['profile']
    if profile not in config['profiles']:
        raise ValueError(f'unknown profile {profile}; available: {list(config["profiles"])}')
    points = parse_reg_points(','.join(f'{name}:{ni}:{nf}' for name, ni, nf in config['profiles'][profile]))
    if ('baseline', 224, 256) not in points:
        raise ValueError('profile must include ["baseline", 224, 256]')
    paths = {key: resolve_path(config_dir, config[key])
             for key in ('repo', 'gem5', 'checkpoints', 'out')}
    if args.out:
        paths['out'] = args.out.absolute()
    settings = {name: getattr(args, name) if getattr(args, name) is not None else int(config[name])
                for name in ('warmup', 'measure', 'jobs', 'timeout')}
    if any(value <= 0 for value in settings.values()):
        raise ValueError('warmup, measure, jobs and timeout must be positive')
    coverage = args.coverage if args.coverage is not None else float(config['coverage'])
    if not 0 < coverage <= 1:
        raise ValueError('coverage must be in (0,1]')
    if args.top is not None and args.top <= 0:
        raise ValueError('top must be positive')
    coverage = None if args.top is not None else coverage
    metadata_path = paths['checkpoints'] / 'cluster-0-0.json'
    metadata = json.loads(metadata_path.read_text())
    workloads = args.workloads.split(',') if args.workloads else sorted(metadata)
    if not workloads or len(workloads) != len(set(workloads)):
        raise ValueError('workloads must be nonempty and unique')
    selected, per_workload = [], []
    for workload in workloads:
        if workload not in metadata:
            raise ValueError(f'unknown workload: {workload}')
        choices, weight = select_points(metadata[workload]['points'], args.top or 1, coverage)
        for point, value in choices:
            files = sorted((paths['checkpoints'] / workload / point).glob('*.zstd'))
            if len(files) != 1:
                raise ValueError(f'expected one checkpoint at {workload}/{point}, found {len(files)}')
            selected.append(dict(workload=workload, point=point, weight=value, checkpoint=str(files[0])))
        per_workload.append(dict(workload=workload, slices=len(choices), selected_weight=weight))
    difftest = bool(config.get('difftest', True))
    trace = bool(config.get('trace', False)) or args.trace
    reference = os.environ.get('GCBV_REF_SO') or config['reference']
    command = [sys.executable, str(HERE / 'run.py'),
               '--repo', str(paths['repo']), '--gem5', str(paths['gem5']),
               '--checkpoints', str(paths['checkpoints']), '--out', str(paths['out']),
               '--workloads', ','.join(workloads),
               '--reg-points', ','.join(f'{name}:{ni}:{nf}' for name, ni, nf in points)]
    if coverage is None:
        command += ['--top', str(args.top)]
    else:
        command += ['--coverage', str(coverage)]
    for name, value in settings.items():
        command += [f'--{name}', str(value)]
    if not trace:
        command += ['--no-trace']
    if not difftest:
        command += ['--disable-difftest']
    return dict(profile=profile, paths={k: str(v) for k, v in paths.items()},
                settings=settings, coverage=coverage, top=args.top,
                difftest=difftest, trace=trace, reference=reference,
                capacity_points=points, workloads=per_workload,
                selected=selected, selected_slices=len(selected),
                total_runs=len(selected) * len(points), command=command,
                metadata_path=str(metadata_path))


def simulation_identity(plan):
    return dict(repo=plan['paths']['repo'], gem5=plan['paths']['gem5'],
                binary_sha256=file_sha256(plan['paths']['gem5']),
                checkpoints=plan['paths']['checkpoints'],
                checkpoint_metadata_sha256=file_sha256(plan['metadata_path']),
                reference=plan['reference'] if plan['difftest'] else None,
                reference_sha256=file_sha256(plan['reference']) if plan['difftest'] else None,
                difftest=plan['difftest'], trace=plan['trace'],
                capacity_points=plan['capacity_points'], selected=plan['selected'],
                warmup=plan['settings']['warmup'], measure=plan['settings']['measure'])


def run_analysis(out):
    stages = [
        ([sys.executable, str(HERE / 'analyze.py'), str(out)], out / 'analysis.log'),
        ([sys.executable, str(HERE / 'capacity_report.py'), str(out),
          '--out', str(out / 'capacity-summary')], out / 'capacity-analysis.log'),
    ]
    for command, logfile in stages:
        print('Analyze:', shlex.join(command), flush=True)
        with logfile.open('w') as log:
            rc = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT).returncode
        if rc:
            print(f'Analysis failed ({rc}); see {logfile}', flush=True)
            print('\n'.join(logfile.read_text(errors='replace').splitlines()[-15:]), flush=True)
            return rc
    print(f'Results: {out / "capacity-summary/report.md"}', flush=True)
    print(f'Weighted per-workload stats: {out / "workload_weighted.csv"}', flush=True)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=HERE / 'large_test.json')
    p.add_argument('--profile', help='baseline, screen or threshold; default from config')
    p.add_argument('--out', type=Path)
    p.add_argument('--coverage', type=float)
    p.add_argument('--top', type=int, help='instead of weight coverage, top N slices per workload')
    p.add_argument('--workloads', help='comma-separated subset; default all 55 workloads')
    for name in ('jobs', 'warmup', 'measure', 'timeout'):
        p.add_argument(f'--{name}', type=int)
    p.add_argument('--trace', action='store_true', help='also save detailed overlap interval CSVs')
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='show compact plan; create no files or simulations')
    mode.add_argument('--analyze-only', action='store_true')
    args = p.parse_args()
    try:
        config_path = args.config.absolute()
        config = json.loads(config_path.read_text())
        plan = make_plan(config, config_path.parent, args)
    except (ValueError, KeyError, OSError) as exc:
        p.error(str(exc))
    print(f"Profile: {plan['profile']}; workloads: {len(plan['workloads'])}; "
          f"slices: {plan['selected_slices']}; capacity points: {len(plan['capacity_points'])}; "
          f"runs: {plan['total_runs']}", flush=True)
    print(f"Warmup: {plan['settings']['warmup']:,}; measured: {plan['settings']['measure']:,}; "
          f"jobs: {plan['settings']['jobs']}; timeout: {plan['settings']['timeout']}s", flush=True)
    print('Capacity points:', ', '.join(f'{name}={ni}/{nf}' for name, ni, nf in plan['capacity_points']), flush=True)
    print(f"Difftest: {plan['difftest']}; detailed trace: {plan['trace']}; "
          f"output: {plan['paths']['out']}", flush=True)
    if args.dry_run:
        print('Command:', shlex.join(plan['command']), flush=True)
        return 0
    out = Path(plan['paths']['out'])
    if args.analyze_only and not out.is_dir():
        p.error(f'output directory does not exist: {out}')
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.launcher.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            p.error(f'another launcher is using {out}; see .launcher.lock for PID')
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()) + '\n')
        lock.flush()
        if args.analyze_only:
            return run_analysis(out)
        try:
            identity = simulation_identity(plan)
        except OSError as exc:
            p.error(f'missing binary/reference: {exc}; build with register_reuse_analysis/build.sh')
        identity_path = out / 'experiment-identity.json'
        normalized_identity = json.loads(json.dumps(identity))
        if identity_path.exists():
            if json.loads(identity_path.read_text()) != normalized_identity:
                p.error('simulation config, selected slices or binary changed; use a new --out. '
                        'Changing --jobs or --timeout is allowed when resuming.')
        else:
            if (out / 'manifest.json').exists():
                p.error('existing output is not managed by this launcher; choose a new --out')
            write_json(identity_path, identity)
        write_json(out / 'launch-plan.json', plan)
        env = os.environ.copy()
        env['GCBV_REF_SO'] = plan['reference']
        start = time.monotonic()
        rc = subprocess.run(plan['command'], env=env).returncode
        # Complete simulations are still analyzed if other tasks failed. The
        # nonzero launch status remains visible, and retries skip successful runs.
        analysis_rc = run_analysis(out)
        write_json(out / 'launch-status.json', dict(simulation_returncode=rc,
                   analysis_returncode=analysis_rc, elapsed_seconds=time.monotonic()-start))
        if rc:
            print('Some simulations failed. Rerun the same command to retry failed tasks.', flush=True)
        return rc or analysis_rc


if __name__ == '__main__':
    sys.exit(main())

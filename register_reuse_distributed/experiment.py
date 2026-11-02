#!/usr/bin/env python3
"""Plan, run and validate sharded capacity and deterministic register-reuse tests."""
import argparse
from collections import Counter, defaultdict
import concurrent.futures
import configparser
import datetime
import fcntl
import hashlib
import heapq
import json
import math
import os
from pathlib import Path
import shlex
import shutil
import signal
import socket
import statistics
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'register_reuse_analysis'))
from analyze import aggregate, stat_blocks, summarize_run, write_csv
from capacity_report import minimum_safe, pressure_onset
from run import file_sha256, parse_reg_points, select_points

SCHEMA = 1
DEFAULT_REFERENCE = '/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so'
FEATURE_PARAMS = {
    'regReusePrediction': False, 'regReuseShadowCopies': 3,
    'regReusePredictorEntries': 512, 'regReuseRepairLatency': 2,
    'regReuseRecoveryLatency': 2,
}


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f'.{os.getpid()}.{threading.get_ident()}.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def absolute(path):
    return str(Path(path).expanduser().absolute())


def assign_shards(tasks, count):
    """Balance run counts; keep each off/certain pair on the same server."""
    grouped = defaultdict(list)
    for task in tasks:
        key = (task['suite'], task['workload'], task['point'], task['int_regs'], task['float_regs'])
        grouped[key].append(task)
    queue = [(0, i) for i in range(count)]
    heapq.heapify(queue)
    # Deterministic interleaving prevents workload-order clumping.
    groups = sorted(grouped.items(), key=lambda item: (-len(item[1]), digest(item[0])))
    for _, group in groups:
        load, shard = heapq.heappop(queue)
        for task in group:
            task['shard'] = shard
        heapq.heappush(queue, (load + len(group), shard))
    return [load for load, _ in sorted(queue, key=lambda item: item[1])]


def estimate(counts, jobs, seconds, factor):
    waves = max((math.ceil(n / jobs) for n in counts), default=0)
    return dict(max_runs_per_server=max(counts, default=0), waves=waves,
                nominal_hours=waves * seconds / 3600,
                budget_hours=waves * seconds * factor / 3600)


def runtime_paths(plan, args):
    saved = plan['paths']
    workspace = Path(getattr(args, 'workspace', None) or saved['workspace']).expanduser().absolute()
    return {
        'workspace': workspace,
        'repo': workspace / 'GEM5',
        'checkpoints': Path(getattr(args, 'checkpoints', None) or saved['checkpoints']).expanduser().absolute(),
        'capacity_gem5': Path(getattr(args, 'capacity_gem5', None) or
                              (workspace / saved['capacity_binary_relative'])).absolute(),
        'reuse_gem5': Path(getattr(args, 'reuse_gem5', None) or
                           (workspace / saved['reuse_binary_relative'])).absolute(),
        'reference': Path(getattr(args, 'reference', None) or os.environ.get('GCBV_REF_SO') or saved['reference']).expanduser().absolute(),
    }


def verify_components(plan, paths, suites):
    files = {
        'checkpoint_metadata': paths['checkpoints'] / 'cluster-0-0.json',
        'reference': paths['reference'],
        'config': paths['repo'] / 'configs/example/kmhv3.py',
    }
    for suite in suites:
        files[suite + '_binary'] = paths[suite + '_gem5']
        if not os.access(paths[suite + '_gem5'], os.X_OK):
            raise ValueError(f'gem5 binary is not executable: {paths[suite + "_gem5"]}')
    for name, path in files.items():
        if file_sha256(path) != plan['components'][name]:
            raise ValueError(f'{name} SHA256 differs from plan: {path}')
    for name, expected in plan['support_files'].items():
        if file_sha256(paths['repo'] / name) != expected:
            raise ValueError(f'configuration dependency differs from plan: {name}')


def make_command(plan, task, paths, destination):
    suite = task['suite']
    command = [str(paths[suite + '_gem5']), '--outdir=' + str(destination),
               str(paths['repo'] / 'configs/example/kmhv3.py'),
               '--generic-rv-cpt=' + str(paths['checkpoints'] / task['checkpoint_relative']),
               '--difftest-ref-so=' + str(paths['reference']),
               f"--warmup-insts-no-switch={plan['warmup']}",
               f"--maxinsts={plan['warmup'] + plan['measure']}"]
    params = {'numPhysIntRegs': task['int_regs'], 'numPhysFloatRegs': task['float_regs'],
              'enableRegPressureStats': suite == 'capacity', 'RobCompressPolicy': "'none'",
              'numThreads': 1, 'numROBEntries': 352}
    if suite == 'capacity':
        params['regPressureTrace'] = "''"
    else:
        params.update(FEATURE_PARAMS)
        params['enableRegisterReuse'] = task['mode'] == 'certain'
    for name, value in params.items():
        command += ['--param', f'system.cpu[0].{name}={value}']
    return command


def task_output(planfile, task):
    return planfile.parent / 'results' / task['suite'] / task['workload'] / task['point'] / task['variant']


def selected_tasks(plan, shard=None, suite='both'):
    return [t for t in plan['tasks'] if (shard is None or t['shard'] == shard)
            and (suite == 'both' or t['suite'] == suite)]


def plan_main(args):
    config = json.loads((ROOT / 'register_reuse_analysis/large_test.json').read_text())
    paths = {'workspace': absolute(args.workspace or ROOT),
             'checkpoints': absolute(args.checkpoints or ROOT / 'zstd-checkpoint-0-0-0'),
             'reference': absolute(args.reference or os.environ.get('GCBV_REF_SO') or DEFAULT_REFERENCE),
             'capacity_binary_relative': 'build/RISCV/gem5.opt',
             'reuse_binary_relative': 'register_reuse_feature/build/RISCV/gem5.opt'}
    metadata = json.loads((Path(paths['checkpoints']) / 'cluster-0-0.json').read_text())
    workloads = sorted(args.workloads.split(',')) if args.workloads else sorted(metadata)
    if len(workloads) != len(set(workloads)) or any(w not in metadata for w in workloads):
        raise ValueError('workloads must be unique names present in cluster-0-0.json')
    capacity_points = config['profiles'][args.capacity_profile]
    reuse_points = parse_reg_points(args.reuse_points)
    if len({(ni,nf) for _,ni,nf in reuse_points}) != len(reuse_points):
        raise ValueError('reuse capacity points must have unique INT/FP counts')
    chosen, tasks = [], []
    suites = ['capacity', 'reuse'] if args.suite == 'both' else [args.suite]
    for workload in workloads:
        points, coverage = select_points(metadata[workload]['points'], top=args.top or 1,
                                         coverage=None if args.top else args.coverage)
        for point, weight in points:
            files = sorted((Path(paths['checkpoints']) / workload / point).glob('*.zstd'))
            if len(files) != 1:
                raise ValueError(f'expected one checkpoint: {workload}/{point}, found {len(files)}')
            common = dict(workload=workload, point=point, weight=weight,
                          selected_workload_coverage=coverage,
                          checkpoint_relative=str(files[0].relative_to(paths['checkpoints'])))
            chosen.append(common)
            for suite in suites:
                entries = capacity_points if suite == 'capacity' else reuse_points
                for label, ni, nf in entries:
                    for mode in (['off'] if suite == 'capacity' else ['off', 'certain']):
                        variant = label if suite == 'capacity' else f'{label}-{mode}'
                        task = dict(common, suite=suite, variant=variant, mode=mode,
                                    int_regs=ni, float_regs=nf)
                        task['id'] = f'{suite}/{workload}/{point}/{variant}'
                        tasks.append(task)
    counts = assign_shards(tasks, args.servers)
    plan = dict(schema=SCHEMA, paths=paths, warmup=args.warmup, measure=args.measure,
                servers=args.servers, jobs=args.jobs, seconds_per_run=args.seconds_per_run,
                runtime_factor=args.runtime_factor, target_hours=args.target_hours,
                timeout=args.timeout, suites=suites, capacity_profile=args.capacity_profile,
                capacity_points=capacity_points, reuse_points=reuse_points,
                selected=chosen, selected_slices=len(chosen), tasks=tasks)
    actual_paths = runtime_paths(plan, args)
    for suite in suites:
        paths[suite + '_binary_relative'] = os.path.relpath(actual_paths[suite + '_gem5'], actual_paths['workspace'])
    components = {'reference': actual_paths['reference'],
                  'checkpoint_metadata': actual_paths['checkpoints'] / 'cluster-0-0.json',
                  'config': actual_paths['repo'] / 'configs/example/kmhv3.py'}
    components.update({s + '_binary': actual_paths[s + '_gem5'] for s in suites})
    plan['components'] = {k: file_sha256(v) for k, v in components.items()}
    # Config imports execute Python from these directories. Pin them as well.
    plan['support_files'] = {}
    for directory in ('configs', 'src/python'):
        for path in sorted((actual_paths['repo'] / directory).rglob('*.py')):
            plan['support_files'][str(path.relative_to(actual_paths['repo']))] = file_sha256(path)
    plan['plan_id'] = digest({k: v for k, v in plan.items() if k != 'paths'})
    print(f"{len(workloads)} workloads; {len(chosen)} slices; {len(tasks)} runs; "
          f"{args.servers} servers x {args.jobs} jobs", flush=True)
    print('Runs by suite:', dict(Counter(t['suite'] for t in tasks)), flush=True)
    print('Runs by server:', counts, flush=True)
    costs = estimate(counts, args.jobs, args.seconds_per_run, args.runtime_factor)
    print(f"Estimated slowest server: {costs['nominal_hours']:.2f}h nominal; "
          f"{costs['budget_hours']:.2f}h with x{args.runtime_factor:g} runtime margin.", flush=True)
    if costs['budget_hours'] > args.target_hours:
        print(f"WARNING: estimated budget exceeds {args.target_hours:g}h; add servers or reduce scope.", flush=True)
    if args.dry_run:
        return 0
    out = args.out.expanduser().absolute()
    planfile = out / 'plan.json'
    if planfile.exists():
        old = json.loads(planfile.read_text())
        if old['plan_id'] != plan['plan_id'] or old['paths'] != plan['paths']:
            raise ValueError('output already contains a different plan; choose a new --out')
        print(f'Existing identical plan retained: {planfile}')
        return 0
    if out.exists() and any(out.iterdir()):
        raise ValueError('planning output must be empty or contain an identical plan')
    out.mkdir(parents=True, exist_ok=True)
    write_json(planfile, plan)
    server_rows = []
    for shard, count in enumerate(counts):
        script = out / f'server-{shard:02d}.sh'
        script.write_text('#!/usr/bin/env bash\nset -euo pipefail\n'
                          'plan_dir=$(cd -- "$(dirname -- "$0")" && pwd)\n'
                          f'workspace=${{REGISTER_REUSE_WORKSPACE:-{shlex.quote(paths["workspace"])}}}\n'
                          'exec "${ANALYSIS_PYTHON:-python3}" '
                          '"$workspace/register_reuse_distributed/experiment.py" run '
                          f'--plan "$plan_dir/plan.json" --shard-id {shard} --workspace "$workspace" "$@"\n')
        script.chmod(0o755)
        suite_counts = Counter(t['suite'] for t in tasks if t['shard'] == shard)
        server_rows.append(dict(shard=shard, runs=count, capacity=suite_counts['capacity'],
                                reuse=suite_counts['reuse'], **estimate([count], args.jobs,
                                args.seconds_per_run, args.runtime_factor)))
    write_csv(out / 'server_plan.csv', server_rows)
    write_json(out / 'budget.json', dict(total_runs=len(tasks), shard_counts=counts,
               jobs_per_server=args.jobs, seconds_per_run=args.seconds_per_run,
               runtime_factor=args.runtime_factor, **costs))
    (out / 'PLAN.md').write_text('\n'.join([
        '# Distributed experiment plan', '',
        f'Plan ID: `{plan["plan_id"]}`',
        f'{len(chosen)} slices, {len(tasks)} runs, {args.servers} servers, {args.jobs} jobs/server.',
        f'{args.warmup:,} warmup + {args.measure:,} measured instructions; NEMU difftest enabled.',
        f'Estimated {costs["nominal_hours"]:.2f}h nominal / {costs["budget_hours"]:.2f}h with runtime margin.',
        f'{args.seconds_per_run:g} seconds/run is an input estimate; SMT, memory bandwidth and workload variation can change it.',
        '', 'Run exactly one distinct server-XX.sh per server. Paths default to this shared workspace.',
        'See register_reuse_distributed/README.md for relocation, cancellation, import and reporting.', '']) )
    print(f'Plan written: {planfile}; launch scripts: server-00.sh .. server-{args.servers-1:02d}.sh')
    return 0


def validate_run(plan, task, destination, reference):
    """Validate the actual config and the final measured stats, including resumes."""
    destination = Path(destination)
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(destination / 'config.ini')
    if 'system.cpu' not in cp:
        raise ValueError('missing system.cpu configuration')
    cpu = cp['system.cpu']
    expected_ints = dict(numPhysIntRegs=task['int_regs'], numPhysFloatRegs=task['float_regs'],
                         numThreads=1, numROBEntries=352,
                         max_insts_any_thread=plan['warmup'] + plan['measure'])
    for name, expected in expected_ints.items():
        if cpu.getint(name, fallback=-1) != expected:
            raise ValueError(f'config mismatch: {name}')
    if cpu.get('RobCompressPolicy') != 'none' or not cpu.getboolean('enable_difftest', fallback=False):
        raise ValueError('requires uncompressed ROB and active difftest')
    if Path(cpu.get('difftest_ref_so', '')).resolve() != Path(reference).resolve():
        raise ValueError('difftest reference path mismatch')
    is_capacity = task['suite'] == 'capacity'
    if cpu.getboolean('enableRegPressureStats', fallback=False) != is_capacity:
        raise ValueError('observer enable mismatch')
    if cpu.getboolean('enableRegisterReuse', fallback=False) != (task['mode'] == 'certain'):
        raise ValueError('register reuse enable mismatch')
    if not is_capacity:
        for name, value in FEATURE_PARAMS.items():
            actual = cpu.getboolean(name) if isinstance(value, bool) else cpu.getint(name)
            if actual != value:
                raise ValueError(f'feature config mismatch: {name}')
    elif cpu.get('regPressureTrace', ''):
        raise ValueError('unexpected interval trace in no-trace capacity run')
    text = (destination / 'run.log').read_text(errors='replace')
    if 'because a thread reached the max instruction count' not in text:
        raise ValueError('simulation did not reach instruction limit')
    blocks = stat_blocks(destination / 'stats.txt')
    if len(blocks) < 2:
        raise ValueError('missing warmup/final stats blocks')
    stats = blocks[-1]
    instructions, cycles = stats['simInsts'], stats['system.cpu.numCycles']
    high = plan['measure'] + max(1024, plan['measure'] * .001)
    if not (math.isfinite(instructions) and math.isfinite(cycles) and cycles > 0
            and .99 * plan['measure'] <= instructions <= high):
        raise ValueError(f'invalid measured instruction window: {instructions}, cycles={cycles}')
    if is_capacity and stats.get('system.cpu.regPressure.schemaVersion') != 2:
        raise ValueError('requires schema-2 capacity observer')
    reuse = {k.split('.regReuse.')[1]: v for k, v in stats.items() if '.regReuse.' in k}
    if not is_capacity:
        if 'sharedVersions' not in reuse:
            raise ValueError('missing reuse feature statistics')
        if task['mode'] == 'off' and reuse['sharedVersions'] != 0:
            raise ValueError('reuse activity in OFF baseline')
        if reuse.get('predictedReuses', -1) != 0 or reuse.get('repairCopies', -1) != 0:
            raise ValueError('deterministic experiment unexpectedly used prediction/repair')
        if reuse.get('deterministicReuses', -1) != reuse['sharedVersions']:
            raise ValueError('deterministic/shared version accounting mismatch')
    return dict(instructions=instructions, cycles=cycles, ipc=instructions/cycles,
                cpi=cycles/instructions, reuse_stats=reuse)


def base_metadata(plan, task, destination, paths):
    return dict(task, plan_id=plan['plan_id'], warmup=plan['warmup'], measure=plan['measure'],
                out=str(destination), command=make_command(plan, task, paths, destination),
                binary_sha256=plan['components'][task['suite'] + '_binary'],
                reference_sha256=plan['components']['reference'],
                config_sha256=plan['components']['config'],
                checkpoint_metadata_sha256=plan['components']['checkpoint_metadata'])


def metadata_matches(info, plan, task):
    return (info.get('plan_id') == plan['plan_id'] and info.get('id') == task['id']
            and info.get('binary_sha256') == plan['components'][task['suite'] + '_binary']
            and info.get('reference_sha256') == plan['components']['reference']
            and info.get('config_sha256') == plan['components']['config']
            and info.get('warmup') == plan['warmup'] and info.get('measure') == plan['measure'])


def terminate_process(proc):
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()


def run_one(plan, task, paths, destination, stop, timeout):
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / '.task.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 'LOCKED', task['id'], 'another process is running this task'
        result_path = destination / 'run.json'
        if result_path.exists():
            info = json.loads(result_path.read_text())
            if not metadata_matches(info, plan, task):
                return 'FAIL', task['id'], 'result identity differs; choose a new output'
            if info.get('ok'):
                try:
                    validate_run(plan, task, destination, info_reference(info))
                    return 'SKIP', task['id'], ''
                except (OSError, ValueError, KeyError, configparser.Error) as exc:
                    return 'FAIL', task['id'], f'completed result failed revalidation: {exc}'
        if stop.is_set():
            return 'CANCELLED', task['id'], 'not started'
        info = base_metadata(plan, task, destination, paths)
        info.update(started=now(), hostname=socket.gethostname(), state='running', ok=False)
        write_json(result_path, info)
        start = time.monotonic()
        rc, state, reason = None, 'failed', ''
        proc = None
        try:
            if not (paths['checkpoints'] / task['checkpoint_relative']).is_file():
                raise ValueError('checkpoint file missing')
            env = os.environ.copy()
            env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
            with (destination / 'run.log').open('w') as log:
                proc = subprocess.Popen(info['command'], cwd=paths['repo'], env=env,
                                        stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                info['child_pid'] = proc.pid
                write_json(result_path, info)
                while True:
                    if stop.is_set() or time.monotonic() - start >= timeout:
                        state = 'interrupted' if stop.is_set() else 'timeout'
                        terminate_process(proc)
                        break
                    if proc.poll() is not None:
                        break
                    stop.wait(.25)
                rc = proc.wait()
            if state not in ('interrupted', 'timeout'):
                if rc:
                    raise ValueError(f'gem5 exited with code {rc}')
                info.update(validate_run(plan, task, destination, paths['reference']))
                state = 'complete'
        except Exception as exc:
            if proc is not None:
                terminate_process(proc)
            reason = str(exc)
            state = 'failed'
        info.update(returncode=rc, state=state, ok=state == 'complete', error=reason,
                    ended=now(), elapsed_seconds=round(time.monotonic()-start, 3))
        write_json(result_path, info)
        return ('OK' if info['ok'] else 'FAIL'), task['id'], f"{info['elapsed_seconds']:.1f}s {reason}"


def run_main(args):
    planfile = args.plan.expanduser().absolute()
    plan = load_plan(planfile)
    if not 0 <= args.shard_id < plan['servers']:
        raise ValueError(f'shard-id must be 0..{plan["servers"]-1}')
    paths = runtime_paths(plan, args)
    tasks = selected_tasks(plan, args.shard_id, args.suite)
    jobs = args.jobs or plan['jobs']
    print(f"Shard {args.shard_id}/{plan['servers']}; {len(tasks)} runs; jobs={jobs}; "
          f"host={socket.gethostname()}; plan={plan['plan_id'][:12]}", flush=True)
    if args.dry_run:
        for task in tasks[:args.show_commands]:
            print(shlex.join(make_command(plan, task, paths, task_output(planfile, task))))
        print(f'{len(tasks)} commands selected; no simulations started.')
        return 0
    if not tasks:
        return 0
    verify_components(plan, paths, {t['suite'] for t in tasks})
    state_dir = planfile.parent / 'shards'
    state_dir.mkdir(parents=True, exist_ok=True)
    lockfile = state_dir / f'{args.shard_id:02d}.lock'
    with (planfile.parent / '.import.lock').open('a+') as import_guard, lockfile.open('a+') as lock:
        fcntl.flock(import_guard, fcntl.LOCK_SH | fcntl.LOCK_NB)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError(f'shard is already running; see {lockfile}')
        identity = dict(pid=os.getpid(), hostname=socket.gethostname(), started=now(),
                        shard=args.shard_id, suite=args.suite, plan_id=plan['plan_id'])
        lock.seek(0)
        lock.truncate()
        lock.write(json.dumps(identity) + '\n')
        lock.flush()
        state_path = state_dir / f'{args.shard_id:02d}.json'
        stop = threading.Event()
        old_handlers = {}
        def interrupted(signum, frame):
            stop.set()
        for sig in (signal.SIGINT, signal.SIGTERM):
            old_handlers[sig] = signal.signal(sig, interrupted)
        counts = Counter()
        start = time.monotonic()
        try:
            # Small queue: cancellation does not need to drain thousands of submitted futures.
            with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
                waiting = iter(tasks)
                pending = {}
                def submit():
                    if stop.is_set():
                        return False
                    task = next(waiting, None)
                    if task is None:
                        return False
                    future = pool.submit(run_one, plan, task, paths, task_output(planfile, task),
                                         stop, args.timeout or plan['timeout'])
                    pending[future] = task
                    return True
                for _ in range(jobs):
                    if not submit():
                        break
                write_json(state_path, dict(identity, state='running', total=len(tasks), counts=dict(counts)))
                last_heartbeat = time.monotonic()
                while pending:
                    done, _ = concurrent.futures.wait(pending, timeout=1,
                                return_when=concurrent.futures.FIRST_COMPLETED)
                    for future in done:
                        task = pending.pop(future)
                        try:
                            status, task_id, detail = future.result()
                        except Exception as exc:
                            status, task_id, detail = 'FAIL', task['id'], repr(exc)
                        counts[status] += 1
                        print(f'[{sum(counts.values())}/{len(tasks)}] {status} {task_id} {detail}', flush=True)
                        submit()
                    if done or time.monotonic()-last_heartbeat >= 60:
                        elapsed = time.monotonic()-start
                        write_json(state_path, dict(identity, state='stopping' if stop.is_set() else 'running',
                                   total=len(tasks), counts=dict(counts), active=len(pending),
                                   elapsed_seconds=round(elapsed, 1), heartbeat=now()))
                        if not done:
                            print(f'Heartbeat: completed={sum(counts.values())}/{len(tasks)}, '
                                  f'active={len(pending)}, elapsed={elapsed/3600:.2f}h', flush=True)
                        last_heartbeat = time.monotonic()
            failed = counts['FAIL'] + counts['LOCKED']
            state = 'interrupted' if stop.is_set() else ('failed' if failed else 'complete')
            write_json(state_path, dict(identity, state=state, total=len(tasks), counts=dict(counts),
                                       ended=now(), elapsed_seconds=round(time.monotonic()-start, 1)))
            return 130 if stop.is_set() else (1 if failed else 0)
        finally:
            for sig, handler in old_handlers.items():
                signal.signal(sig, handler)


def load_plan(path):
    plan = json.loads(Path(path).read_text())
    if plan.get('schema') != SCHEMA:
        raise ValueError('unsupported plan schema')
    expected = digest({k:v for k,v in plan.items() if k not in ('paths', 'plan_id')})
    if expected != plan.get('plan_id'):
        raise ValueError('plan checksum failed: do not edit plan.json; generate a new plan')
    return plan


def status_main(args):
    planfile = args.plan.expanduser().absolute()
    plan = load_plan(planfile)
    rows, durations = [], []
    for shard in range(plan['servers']):
        counts = Counter()
        for task in selected_tasks(plan, shard, args.suite):
            meta = task_output(planfile, task) / 'run.json'
            if not meta.exists():
                counts['pending'] += 1
                continue
            try:
                info = json.loads(meta.read_text())
                state = info.get('state', 'unknown')
                if not metadata_matches(info, plan, task):
                    state = 'identity_mismatch'
                elif info.get('ok'):
                    state = 'complete'
                    if info.get('elapsed_seconds'):
                        durations.append(info['elapsed_seconds'])
                counts[state] += 1
            except (OSError, ValueError):
                counts['unreadable'] += 1
        rows.append(dict(shard=shard, **dict(counts)))
        print(f'Shard {shard:02d}: ' + ', '.join(f'{k}={v}' for k,v in sorted(counts.items())))
    if durations:
        values = sorted(durations)
        print(f'Completed runtime: median={statistics.median(values):.1f}s; '
              f'p90={values[min(len(values)-1, math.ceil(.9*len(values))-1)]:.1f}s; '
              f'max={max(values):.1f}s')
    return 0


def weighted_reuse_rows(plan, rows):
    expected = defaultdict(dict)
    for task in plan['tasks']:
        if task['suite'] == 'reuse':
            expected[task['workload'], task['int_regs'], task['float_regs']][task['point']] = task['weight']
    keyed = {(r['workload'],r['point'],r['int_regs'],r['float_regs'],r['mode']):r for r in rows}
    paired, weighted = [], []
    for (workload, ni, nf), points in sorted(expected.items()):
        matches = []
        for point, weight in points.items():
            off = keyed.get((workload, point, ni, nf, 'off'))
            certain = keyed.get((workload, point, ni, nf, 'certain'))
            if off is None or certain is None:
                continue
            if off['binary_sha256'] != certain['binary_sha256']:
                raise ValueError('OFF/certain binary mismatch')
            pair = dict(workload=workload, point=point, weight=weight, int_regs=ni, float_regs=nf,
                        off_cpi=off['cpi'], certain_cpi=certain['cpi'],
                        speedup=off['cpi']/certain['cpi'],
                        change_percent=100*(off['cpi']/certain['cpi']-1),
                        deterministic_reuses=certain['reuse_stats'].get('deterministicReuses',0),
                        repair_wait_cycles=certain['reuse_stats'].get('repairWaitCycles',0),
                        restored_groups=certain['reuse_stats'].get('restoredGroups',0))
            matches.append(pair)
            paired.append(pair)
        if not matches:
            continue
        coverage = sum(r['weight'] for r in matches)
        off_cpi = sum(r['weight']*r['off_cpi'] for r in matches)/coverage
        certain_cpi = sum(r['weight']*r['certain_cpi'] for r in matches)/coverage
        weighted.append(dict(workload=workload, int_regs=ni, float_regs=nf,
                             matched_slices=len(matches), expected_slices=len(points),
                             selected_weight=coverage, expected_selected_weight=sum(points.values()),
                             complete=len(matches)==len(points), off_cpi=off_cpi, certain_cpi=certain_cpi,
                             speedup=off_cpi/certain_cpi, change_percent=100*(off_cpi/certain_cpi-1)))
    # Compare reduced-capacity certain with default-capacity OFF on identical points.
    retained = []
    for row in weighted:
        workload,ni,nf = row['workload'],row['int_regs'],row['float_regs']
        if (ni,nf)==(224,256):
            continue
        points = expected[workload,ni,nf]
        pairs = [(weight,keyed.get((workload,point,224,256,'off')),
                  keyed.get((workload,point,ni,nf,'certain'))) for point,weight in points.items()]
        pairs = [(weight,off,certain) for weight,off,certain in pairs if off and certain]
        if not pairs:
            continue
        coverage = sum(w for w,_,_ in pairs)
        baseline = sum(w*off['cpi'] for w,off,_ in pairs)/coverage
        smaller = sum(w*certain['cpi'] for w,_,certain in pairs)/coverage
        retained.append(dict(workload=workload, int_regs=ni, float_regs=nf, matched_slices=len(pairs),
                             expected_slices=len(points), complete=len(pairs)==len(points),
                             selected_weight=coverage, default_off_cpi=baseline,
                             reduced_certain_cpi=smaller, ipc_ratio_to_default_off=baseline/smaller,
                             change_percent=100*(baseline/smaller-1)))
    return paired, weighted, retained


def capacity_weighted_report(plan, rows):
    expected = defaultdict(set)
    for task in plan['tasks']:
        if task['suite']=='capacity':
            expected[task['workload'],task['variant']].add(task['point'])
    weighted = aggregate(rows)
    actual = defaultdict(set)
    for row in rows:
        actual[row['workload'],row['variant']].add(row['point'])
    baseline = {row['workload']:row for row in weighted if row['variant']=='baseline'}
    weighted_points = []
    for row in weighted:
        key = (row['workload'],row['variant'])
        row['expected_slices'] = len(expected[key])
        row['complete'] = actual[key] == expected[key]
        base = baseline.get(row['workload'])
        if base and actual[key] == actual[row['workload'],'baseline']:
            row['ipc_ratio_to_default'] = base['weighted_cpi']/row['weighted_cpi']
            row['ipc_loss'] = 1-row['ipc_ratio_to_default']
        source = next(r for r in rows if (r['workload'],r['variant'])==key)
        row['int_regs'],row['float_regs'] = source['int_regs'],source['float_regs']
        if row['complete'] and base and base['complete']:
            weighted_points.append(row)
    thresholds = []
    for workload in sorted({r['workload'] for r in weighted_points}):
        group = [r for r in weighted_points if r['workload']==workload]
        for axis,fixed,count,field in [('int','float_regs','int_regs','weighted_int_standalone_shortage_fraction'),
                                       ('float','int_regs','float_regs','weighted_float_standalone_shortage_fraction')]:
            fixed_value = 256 if axis=='int' else 224
            points = [(r[count],r) for r in group if r[fixed]==fixed_value]
            if len(points)<2:
                continue
            bad,good = pressure_onset(points,field)
            thresholds.append(dict(workload=workload,axis=axis,safe_1pct=minimum_safe(points,.01),
                                   safe_5pct=minimum_safe(points,.05),
                                   largest_tested_count_with_1pct_pressure=bad,
                                   next_larger_count_under_1pct_pressure=good,
                                   tested_counts=','.join(str(n) for n,_ in sorted(points))))
    return weighted,thresholds


def report_main(args):
    planfile = args.plan.expanduser().absolute()
    plan = load_plan(planfile)
    out = (args.out or planfile.parent / 'report').expanduser().absolute()
    out.mkdir(parents=True, exist_ok=True)
    capacity, reuse, missing, invalid = [], [], [], []
    for task in selected_tasks(plan, suite=args.suite):
        destination = task_output(planfile,task)
        file = destination/'run.json'
        if not file.exists():
            missing.append(task['id'])
            continue
        try:
            info = json.loads(file.read_text())
            if not metadata_matches(info,plan,task) or not info.get('ok') or info.get('returncode') != 0:
                raise ValueError('not complete or metadata differs from plan')
            data = validate_run(plan,task,destination,info_reference(info))
            local = dict(info,out=str(destination))
            if task['suite']=='capacity':
                row = summarize_run(local)
                row['binary_sha256'] = info['binary_sha256']
                capacity.append(row)
            else:
                reuse.append(dict(local,**data))
        except (OSError,ValueError,KeyError,configparser.Error) as exc:
            invalid.append(dict(id=task['id'],error=str(exc)))
    paired,weighted,retained = weighted_reuse_rows(plan,reuse)
    capacity_weighted,thresholds = capacity_weighted_report(plan,capacity)
    write_csv(out/'capacity_per_run.csv',capacity)
    write_csv(out/'capacity_workload_weighted.csv',capacity_weighted)
    write_csv(out/'capacity_workload_thresholds.csv',thresholds)
    write_csv(out/'reuse_pairs.csv',paired)
    write_csv(out/'reuse_workload_weighted.csv',weighted)
    write_csv(out/'reuse_retained_vs_default.csv',retained)
    reuse_flat = []
    for row in reuse:
        reuse_flat.append({k:v for k,v in row.items() if k not in ('command','reuse_stats')}
                          | {f'reuse_{k}':v for k,v in row['reuse_stats'].items()})
    write_csv(out/'reuse_per_run.csv',reuse_flat)
    gm = []
    expected_workloads = {t['workload'] for t in plan['tasks'] if t['suite']=='reuse'}
    for ni,nf in sorted({(r['int_regs'],r['float_regs']) for r in weighted}):
        group = [r for r in weighted if (r['int_regs'],r['float_regs'])==(ni,nf)]
        complete = all(r['complete'] for r in group) and {r['workload'] for r in group}==expected_workloads
        gm.append(dict(int_regs=ni,float_regs=nf,workloads=len(group),complete=complete,
                       speedup=math.exp(sum(math.log(r['speedup']) for r in group)/len(group))))
    complete = not missing and not invalid
    summary = dict(plan_id=plan['plan_id'],suite=args.suite,complete=complete,capacity_runs=len(capacity),reuse_runs=len(reuse),
                   missing=missing,invalid=invalid,reuse_geomean=gm,
                   reuse_pairs=len(paired),components=plan['components'],generated=now())
    write_json(out/'validation.json',summary)
    report = ['# 容量扫描与确定性寄存器复用验证','',
              f'Plan `{plan["plan_id"][:16]}`；范围 `{args.suite}`；状态：**{"完整" if complete else "未完整，仅供排查"}**。',
              f'容量运行 {len(capacity)}；复用运行 {len(reuse)}；缺失 {len(missing)}；失败/校验不通过 {len(invalid)}。',
              f'每片预热 {plan["warmup"]:,} + 测量 {plan["measure"]:,} 指令，NEMU difftest 开启。','',
              '## 确定性复用','',
              'off/certain 使用相同 feature 二进制、相同容量、切片和指令窗口，显式关闭跨寄存器预测。',
              'workload 内按所选 SimPoint 权重加权 CPI，再计算 off_CPI/certain_CPI；部分覆盖只在所选切片内归一化。',
              '下面是 workload 级比值的等权几何平均，不是官方 SPEC 分数。','',
              '| INT/FP | Workloads | 完整 | IPC 变化 |','|---|---:|---|---:|']
    for row in gm:
        report.append(f'| {row["int_regs"]}/{row["float_regs"]} | {row["workloads"]} | {row["complete"]} | {(row["speedup"]-1)*100:+.3f}% |')
    report += ['','| Workload | INT/FP | 配对切片/计划 | 覆盖权重 | IPC 变化 |',
               '|---|---:|---:|---:|---:|']
    for row in weighted:
        report.append(f'| {row["workload"]} | {row["int_regs"]}/{row["float_regs"]} | {row["matched_slices"]}/{row["expected_slices"]} | {row["selected_weight"]:.6f} | {row["change_percent"]:+.3f}% |')
    report += ['','## 容量扫描','',
               '使用 schema-2 直接容量检查；阻塞比例不等于可回收的性能收益。',
               'workload 级阈值仅纳入同一组切片全部完成的容量点；safe 容量要求该点及所有更大已测点满足损失上限。',
               '默认参照 224/256。只改 INT 时固定 FP=256；只改 FP 时固定 INT=224。','',
               '| Workload | 轴 | IPC损失≤1%最小已测容量 | IPC损失≤5%最小已测容量 |',
               '|---|---|---:|---:|']
    for row in thresholds:
        report.append(f'| {row["workload"]} | {row["axis"]} | {row["safe_1pct"]} | {row["safe_5pct"]} |')
    report += ['','`capacity_workload_weighted.csv`：容量和直接阻塞统计；',
               '`reuse_pairs.csv`、`reuse_workload_weighted.csv`：同容量配对收益；',
               '`reuse_retained_vs_default.csv`：收紧容量 certain 相对默认容量 OFF 的性能保留；',
               '`validation.json`：缺失/失败清单和实验身份。','',
               '模型仍为统一 shadow 存储，无等面积、频率、能耗或逐端口争用结论。']
    (out/'report.md').write_text('\n'.join(report)+'\n')
    print(f'Report: {out/"report.md"}; complete={complete}; missing={len(missing)}; invalid={len(invalid)}')
    return 0 if complete else 1


def info_reference(info):
    for arg in info['command']:
        if arg.startswith('--difftest-ref-so='):
            return arg.split('=',1)[1]
    raise ValueError('missing difftest reference in recorded command')


def import_capacity_main(args):
    """Import only strictly matching completed observer runs from the old batch."""
    planfile = args.plan.expanduser().absolute()
    plan = load_plan(planfile)
    source = args.source.expanduser().absolute()
    identity = json.loads((source/'experiment-identity.json').read_text())
    expected = {'binary_sha256':plan['components'].get('capacity_binary'),
                'reference_sha256':plan['components']['reference'],
                'checkpoint_metadata_sha256':plan['components']['checkpoint_metadata'],
                'warmup':plan['warmup'],'measure':plan['measure'],'difftest':True,'trace':False}
    if any(identity.get(k)!=v for k,v in expected.items()):
        raise ValueError('old experiment identity differs in binary/reference/window/metadata/trace')
    oldplan = json.loads((source/'launch-plan.json').read_text())
    oldrepo = Path(oldplan['paths']['repo'])
    if file_sha256(oldrepo/'configs/example/kmhv3.py')!=plan['components']['config']:
        raise ValueError('old/current config mismatch')
    paths = runtime_paths(plan,args)
    verify_components(plan,paths,{'capacity'})
    counts = Counter()
    # Workers also hold this guard in shared mode; importing requires exclusivity.
    with (planfile.parent/'.import.lock').open('a+') as guard:
        fcntl.flock(guard,fcntl.LOCK_EX | fcntl.LOCK_NB)
        for task in selected_tasks(plan,suite='capacity'):
            olddir = source/task['workload']/task['point']/task['variant']
            oldmeta = olddir/'run.json'
            if not oldmeta.exists():
                counts['not_available']+=1
                continue
            info = json.loads(oldmeta.read_text())
            if not info.get('ok'):
                counts['unfinished']+=1
                continue
            destination = task_output(planfile,task)
            if destination.exists():
                counts['already_present']+=1
                continue
            try:
                if info.get('binary_sha256')!=expected['binary_sha256']:
                    raise ValueError('run binary mismatch')
                if info.get('checkpoint')!=str(paths['checkpoints']/task['checkpoint_relative']):
                    raise ValueError('checkpoint path mismatch')
                if any(info.get(k)!=v for k,v in [('warmup',plan['warmup']),('measure',plan['measure']),
                                                 ('int_regs',task['int_regs']),('float_regs',task['float_regs'])]):
                    raise ValueError('per-run window/capacity mismatch')
                values=validate_run(plan,task,olddir,identity['reference'])
                summarize_run(dict(info,out=str(olddir)))
            except (OSError,ValueError,KeyError,configparser.Error) as exc:
                print(f'REJECT {task["id"]}: {exc}')
                counts['rejected']+=1
                continue
            counts['importable']+=1
            if args.dry_run:
                continue
            destination.mkdir(parents=True)
            for name in ('config.ini','config.json','stats.txt','run.log'):
                if (olddir/name).exists():
                    shutil.copy2(olddir/name,destination/name)
            meta=base_metadata(plan,task,destination,paths)
            # Retain the actual recorded command/reference for validation provenance.
            meta.update(values,command=info['command'],state='complete',ok=True,returncode=0,
                        imported_from=str(olddir),imported_at=now(),
                        elapsed_seconds=info.get('elapsed_seconds'),
                        hostname='imported',started=info.get('started'))
            write_json(destination/'run.json',meta)
            counts['imported']+=1
    print('Capacity import:',dict(counts))
    return 0


def stop_main(args):
    planfile = args.plan.expanduser().absolute()
    plan = load_plan(planfile)
    if not 0 <= args.shard_id < plan['servers']:
        raise ValueError('invalid shard-id')
    lockfile = planfile.parent / 'shards' / f'{args.shard_id:02d}.lock'
    if not lockfile.exists():
        print('Shard has no running record.')
        return 0
    with lockfile.open('r+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            pass
        else:
            print('Shard is already stopped.')
            return 0
        identity = json.loads(lock.read())
        if identity['hostname'] != socket.gethostname():
            raise ValueError(f'run stop on {identity["hostname"]}, where this shard is running')
        if identity['plan_id'] != plan['plan_id']:
            raise ValueError('runner plan identity differs')
        pid = int(identity['pid'])
        command = Path(f'/proc/{pid}/cmdline').read_bytes().decode().split('\0')
        if 'run' not in command or '--shard-id' not in command:
            raise ValueError('runner PID no longer matches; refusing to signal')
        if command[command.index('--shard-id')+1] != str(args.shard_id):
            raise ValueError('runner PID has a different shard')
        os.kill(pid, signal.SIGTERM)
        print(f'SIGTERM sent to shard {args.shard_id}, runner PID {pid}; active gem5 groups will be stopped.')
    return 0


def positive(text):
    value=int(text)
    if value<=0:
        raise argparse.ArgumentTypeError('must be positive')
    return value


def positive_float(text):
    value=float(text)
    if not math.isfinite(value) or value<=0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return value


def add_runtime_arguments(parser):
    parser.add_argument('--workspace',type=Path)
    parser.add_argument('--checkpoints',type=Path)
    parser.add_argument('--capacity-gem5',type=Path)
    parser.add_argument('--reuse-gem5',type=Path)
    parser.add_argument('--reference',type=Path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='action',required=True)
    p=subs.add_parser('plan',help='generate immutable task assignments and server launchers')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--servers',type=positive,default=6)
    p.add_argument('--jobs',type=positive,default=64)
    p.add_argument('--suite',choices=['both','capacity','reuse'],default='both')
    p.add_argument('--capacity-profile',choices=['baseline','screen','threshold'],default='threshold')
    p.add_argument('--reuse-points',default='baseline:224:256,mixed192_208:192:208')
    p.add_argument('--coverage',type=positive_float,default=.8)
    p.add_argument('--top',type=positive)
    p.add_argument('--workloads')
    p.add_argument('--warmup',type=positive,default=20000000)
    p.add_argument('--measure',type=positive,default=20000000)
    p.add_argument('--timeout',type=positive,default=7200)
    p.add_argument('--seconds-per-run',type=positive_float,default=800)
    p.add_argument('--runtime-factor',type=positive_float,default=1.25)
    p.add_argument('--target-hours',type=positive_float,default=12)
    p.add_argument('--dry-run',action='store_true')
    add_runtime_arguments(p)
    p.set_defaults(func=plan_main)
    p=subs.add_parser('run',help='run exactly one shard; interrupt safely with SIGTERM')
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--shard-id',type=int,required=True)
    p.add_argument('--jobs',type=positive)
    p.add_argument('--timeout',type=positive)
    p.add_argument('--suite',choices=['both','capacity','reuse'],default='both')
    p.add_argument('--dry-run',action='store_true')
    p.add_argument('--show-commands',type=positive,default=2)
    add_runtime_arguments(p)
    p.set_defaults(func=run_main)
    for action,func in [('status',status_main),('report',report_main)]:
        p=subs.add_parser(action)
        p.add_argument('--plan',type=Path,required=True)
        p.add_argument('--suite',choices=['both','capacity','reuse'],default='both')
        if action=='report':
            p.add_argument('--out',type=Path)
        p.set_defaults(func=func)
    p=subs.add_parser('stop',help='stop one shard on its current server, including gem5 children')
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--shard-id',type=int,required=True)
    p.set_defaults(func=stop_main)
    p=subs.add_parser('import-capacity',help='copy matching old results without modifying the old batch')
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--dry-run',action='store_true')
    add_runtime_arguments(p)
    p.set_defaults(func=import_capacity_main)
    args=parser.parse_args()
    if hasattr(args,'coverage') and not 0<args.coverage<=1:
        parser.error('coverage must lie in (0,1]')
    try:
        return args.func(args)
    except (OSError,ValueError,KeyError,configparser.Error) as exc:
        parser.error(str(exc))


if __name__=='__main__':
    sys.exit(main())

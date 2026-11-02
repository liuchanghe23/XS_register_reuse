#!/usr/bin/env python3
"""Summarize pressure stats and intersect completed single-use lifetimes with RegFull."""
import argparse
from collections import defaultdict
import csv
import configparser
import json
from pathlib import Path


def stat_blocks(path):
    blocks, block = [], None
    for line in path.read_text().splitlines():
        if 'Begin Simulation Statistics' in line:
            block = {}
        elif 'End Simulation Statistics' in line:
            if block:
                blocks.append(block)
            block = None
        elif block is not None:
            parts = line.split()
            if len(parts) >= 2 and not parts[0].startswith('#'):
                try:
                    block[parts[0]] = float(parts[1])
                except ValueError:
                    pass
    return blocks


def sweep(intervals):
    """Half-open intervals; four channels: stall, single-use, eligible, self-redef."""
    events = defaultdict(lambda: [0, 0, 0, 0])
    for start, end, channel in intervals:
        if end <= start:
            continue
        events[start][channel] += 1
        events[end][channel] -= 1
    active = [0, 0, 0, 0]
    totals = dict(stall_cycles=0, single_overlap_cycles=0,
                  eligible_overlap_cycles=0, self_redef_overlap_cycles=0,
                  single_exposure=0, eligible_exposure=0, self_redef_exposure=0,
                  max_single_held_at_stall=0)
    previous = None
    for point in sorted(events):
        if previous is not None and active[0] > 0:
            dt = point - previous
            totals['stall_cycles'] += dt
            for channel, label in ((1, 'single'), (2, 'eligible'), (3, 'self_redef')):
                if active[channel] > 0:
                    totals[f'{label}_overlap_cycles'] += dt
                totals[f'{label}_exposure'] += dt * active[channel]
            totals['max_single_held_at_stall'] = max(totals['max_single_held_at_stall'], active[1])
        for channel in range(4):
            active[channel] += events[point][channel]
            if active[channel] < 0:
                raise ValueError('negative interval occupancy')
        previous = point
    return totals


def trace_metrics(path, epoch):
    intervals = [[] for _ in range(4)]
    with path.open(newline='') as handle:
        for row in csv.DictReader(handle):
            if int(row['epoch']) != epoch:
                continue
            cls = int(row['class'])
            start, end = int(row['start_cycle']), int(row['end_cycle'])
            if row['kind'] == 'stall':
                intervals[cls].append((start, end, 0))
            elif row['kind'] == 'value':
                intervals[cls].append((start, end, 1))
                if int(row['eligible']):
                    intervals[cls].append((start, end, 2))
                if int(row['self_redef']):
                    intervals[cls].append((start, end, 3))
    return [sweep(group) for group in intervals]


def ratio(a, b):
    return a / b if b else 0.0


def summarize_run(meta):
    path = Path(meta['out'])
    blocks = stat_blocks(path / 'stats.txt')
    if not blocks:
        raise ValueError(f'no complete stats: {path}')
    stats = blocks[-1]
    cycles = stats['system.cpu.numCycles']
    instructions = stats['simInsts']
    if cycles <= 0 or instructions < 0.99 * meta['measure']:
        raise ValueError(f'incomplete measurement block: {path}: {instructions} insts')
    result = {key: meta[key] for key in ('workload', 'point', 'weight', 'variant', 'warmup', 'measure')}
    cp = configparser.ConfigParser()
    cp.read(path / 'config.ini')
    result['int_regs'] = cp['system.cpu'].getint('numPhysIntRegs')
    result['float_regs'] = cp['system.cpu'].getint('numPhysFloatRegs')
    result.update(instructions=instructions, cycles=cycles, ipc=ratio(instructions, cycles),
                  cpi=ratio(cycles, instructions),
                  regfull_cycles=stats.get('system.cpu.rename.stallEvents::RegFull', 0),
                  elapsed_seconds=meta.get('elapsed_seconds'), out=str(path))
    result['regfull_fraction'] = ratio(result['regfull_cycles'], cycles)
    prefix = 'system.cpu.regPressure.'
    profiled = any('enableRegPressureStats=True' in x for x in meta['command'])
    result['profiled'] = profiled
    if not profiled:
        return result
    result['observer_schema'] = int(stats.get(prefix + 'schemaVersion', 1))
    for stat, label in (('standaloneStallCycles', 'standalone_stall'),
                        ('otherBlockedStallCycles', 'other_blocked_stall')):
        result[label + '_cycles'] = stats.get(prefix + stat, 0)
        result[label + '_fraction'] = ratio(result[label + '_cycles'], cycles)
    result['demand_stall_cycles'] = stats[prefix + 'demandStallCycles']
    result['demand_stall_fraction'] = ratio(result['demand_stall_cycles'], cycles)
    if result['observer_schema'] >= 2 and result['demand_stall_cycles'] != (
            result['standalone_stall_cycles'] + result['other_blocked_stall_cycles']):
        raise ValueError(f'capacity/block split mismatch: {path}')
    epoch = int(stats[prefix + 'epoch'])
    overlaps = trace_metrics(path / 'reg-pressure.csv', epoch) if (path / 'reg-pressure.csv').exists() else None
    for cls, name in enumerate(('int', 'float', 'vector', 'misc')):
        shortage = stats[prefix + 'shortageCycles::' + name]
        result[f'{name}_shortage_cycles'] = shortage
        result[f'{name}_shortage_fraction'] = ratio(shortage, cycles)
        standalone = stats.get(prefix + 'standaloneShortageCycles::' + name, 0)
        result[f'{name}_standalone_shortage_cycles'] = standalone
        result[f'{name}_standalone_shortage_fraction'] = ratio(standalone, cycles)
        result[f'{name}_mean_free_when_short'] = ratio(stats[prefix + 'freeAtShortage::' + name], shortage)
        if overlaps is not None:
            sweep_result = overlaps[cls]
            if sweep_result['stall_cycles'] != shortage:
                raise ValueError(f'trace/stats stall mismatch: {path}, {name}')
            for key, value in sweep_result.items():
                result[f'{name}_{key}'] = value
            for kind in ('single', 'eligible', 'self_redef'):
                result[f'{name}_{kind}_overlap_fraction_of_shortage'] = ratio(sweep_result[f'{kind}_overlap_cycles'], shortage)
        if cls >= 2:
            continue
        for stat in ('allocations', 'completedValues', 'unaliasedValues', 'aliasedValues',
                     'zeroConsumerValues', 'singleConsumerValues', 'multiConsumerValues',
                     'eligibleSingleValues', 'selfRedefSingleValues', 'singleHoldCycles',
                     'singleStallExposure', 'eligibleStallExposure', 'selfRedefStallExposure',
                     'singleValuesOverlappingStall', 'squashedValues', 'liveValues'):
            result[f'{name}_{stat}'] = stats[prefix + stat + '::' + name]
        complete = result[f'{name}_completedValues']
        unaliased = result[f'{name}_unaliasedValues']
        single = result[f'{name}_singleConsumerValues']
        if complete != unaliased + result[f'{name}_aliasedValues']:
            raise ValueError(f'classification mismatch: {path}, {name}')
        if unaliased != sum(result[f'{name}_{stat}'] for stat in ('zeroConsumerValues', 'singleConsumerValues', 'multiConsumerValues')):
            raise ValueError(f'consumer-count mismatch: {path}, {name}')
        result[f'{name}_single_fraction_unaliased'] = ratio(single, unaliased)
        result[f'{name}_mean_single_hold_cycles'] = ratio(result[f'{name}_singleHoldCycles'], single)
        result[f'{name}_mean_single_held_at_shortage'] = ratio(result[f'{name}_singleStallExposure'], shortage)
        if overlaps is not None:
            for stat, key in (('singleStallExposure', 'single_exposure'),
                              ('eligibleStallExposure', 'eligible_exposure'),
                              ('selfRedefStallExposure', 'self_redef_exposure')):
                if result[f'{name}_{stat}'] != overlaps[cls][key]:
                    raise ValueError(f'trace/stats exposure mismatch: {path}, {name}, {stat}')
    return result


def write_csv(path, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['workload'], row['variant']].append(row)
    result = []
    for (workload, variant), group in sorted(groups.items()):
        coverage = sum(row['weight'] for row in group)
        cpi = sum(row['weight'] * row['cpi'] for row in group) / coverage
        rpi = sum(row['weight'] * row['regfull_cycles'] / row['instructions'] for row in group) / coverage
        row = dict(workload=workload, variant=variant, slices=len(group),
                   selected_weight=coverage, weighted_cpi=cpi,
                   weighted_ipc=1/cpi, weighted_regfull_fraction=rpi/cpi)
        for field in ('demand_stall_cycles', 'standalone_stall_cycles',
                      'other_blocked_stall_cycles', 'int_shortage_cycles',
                      'float_shortage_cycles', 'int_standalone_shortage_cycles',
                      'float_standalone_shortage_cycles'):
            if all(field in point for point in group):
                per_inst = sum(point['weight'] * point[field] / point['instructions']
                               for point in group) / coverage
                row['weighted_' + field.replace('_cycles', '_fraction')] = per_inst / cpi
        result.append(row)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results', type=Path)
    args = p.parse_args()
    rows, failed = [], []
    for filename in sorted(args.results.glob('*/*/*/run.json')):
        meta = json.loads(filename.read_text())
        if not meta.get('ok'):
            failed.append(str(filename.parent))
            continue
        rows.append(summarize_run(meta))
    if not rows:
        p.error('no successful runs')
    write_csv(args.results / 'per_run.csv', rows)
    write_csv(args.results / 'workload_weighted.csv', aggregate(rows))
    comparisons = []
    keyed = {(r['workload'], r['point'], r['variant']): r for r in rows}
    for baseline in rows:
        if baseline['variant'] != 'baseline':
            continue
        for variant in sorted({r['variant'] for r in rows} - {'baseline'}):
            other = keyed.get((baseline['workload'], baseline['point'], variant))
            if other:
                comparisons.append(dict(workload=baseline['workload'], point=baseline['point'],
                                        variant=variant, ipc_speedup=other['ipc']/baseline['ipc'],
                                        baseline_regfull_fraction=baseline['regfull_fraction'],
                                        variant_regfull_fraction=other['regfull_fraction']))
    write_csv(args.results / 'comparison.csv', comparisons)
    (args.results / 'summary.json').write_text(json.dumps(dict(runs=rows, comparisons=comparisons, failed=failed), indent=2) + '\n')
    report = ['# Kunminghu V3 register-pressure screening', '',
              'These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.', '',
              'Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.', '',
              '| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |',
              '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        def percent(key):
            return f"{100*r[key]:.2f}%" if key in r else 'N/A'
        report.append(f"| {r['workload']}/{r['point']} | {r['variant']} | {r['int_regs']}/{r['float_regs']} | {r['ipc']:.3f} | {percent('regfull_fraction')} | {percent('demand_stall_fraction')} | {percent('standalone_stall_fraction')} | {percent('int_shortage_fraction')} | {percent('float_shortage_fraction')} |")
    report += ['', '| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |',
               '|---|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        if ('int_single_overlap_fraction_of_shortage' not in r and
                'float_single_overlap_fraction_of_shortage' not in r):
            continue
        report.append(f"| {r['workload']}/{r['point']}/{r['variant']} | {100*r.get('int_single_overlap_fraction_of_shortage', 0):.2f}% | {100*r.get('int_eligible_overlap_fraction_of_shortage', 0):.2f}% | {r.get('int_mean_single_held_at_shortage', 0):.2f} | {100*r.get('float_single_overlap_fraction_of_shortage', 0):.2f}% | {100*r.get('float_eligible_overlap_fraction_of_shortage', 0):.2f}% | {r.get('float_mean_single_held_at_shortage', 0):.2f} |")
    report += ['', 'The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper\'s predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.', '', '| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |', '|---|---|---:|---:|---:|']
    for r in comparisons:
        report.append(f"| {r['workload']}/{r['point']} | {r['variant']} | {r['ipc_speedup']:.3f}x | {100*r['baseline_regfull_fraction']:.2f}% | {100*r['variant_regfull_fraction']:.2f}% |")
    if failed:
        report += ['', f'{len(failed)} unsuccessful runs excluded; see summary.json.']
    (args.results / 'report.md').write_text('\n'.join(report) + '\n')
    print('\n'.join(report))


if __name__ == '__main__':
    main()

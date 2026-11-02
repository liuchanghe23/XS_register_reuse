#!/usr/bin/env python3
"""Combine schema-2 capacity scans and report per-slice pressure/performance knees."""
import argparse
from collections import defaultdict
import csv
import json
import math
from pathlib import Path


def minimum_safe(points, loss_limit):
    """Smallest tested count for which all larger tested points meet the limit."""
    for count, row in sorted(points):
        if all(r['ipc_loss'] <= loss_limit for n, r in points if n >= count):
            return count
    return None


def pressure_onset(points, field, limit=0.01):
    bad = sorted(n for n, r in points if r[field] >= limit)
    if not bad:
        return None, min((n for n, _ in points), default=None)
    largest_bad = max(bad)
    larger_good = [n for n, r in points if n > largest_bad and r[field] < limit]
    return largest_bad, min(larger_good, default=None)


def axis_points(rows, axis):
    if axis == 'joint':
        return [(r['int_regs'], r) for r in rows if r['int_regs'] == r['float_regs']]
    if axis == 'int':
        return [(r['int_regs'], r) for r in rows if r['float_regs'] == 256]
    return [(r['float_regs'], r) for r in rows if r['int_regs'] == 224]


def dump_csv(path, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', newline='') as handle:
        out = csv.DictWriter(handle, fields)
        out.writeheader()
        out.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results', nargs='+', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--plot', action='store_true', help='requires matplotlib')
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    unique, hashes, windows = {}, set(), set()
    failed, unfinished = [], []
    for root in args.results:
        summary = json.loads((root / 'summary.json').read_text())
        failed.extend(summary.get('failed', []))
        for row in summary['runs']:
            if row.get('observer_schema', 1) < 2:
                raise ValueError(f'legacy observer schema: {root}')
            meta = json.loads((Path(row['out']) / 'run.json').read_text())
            hashes.add(meta['binary_sha256'])
            windows.add((row['warmup'], row['measure']))
            key = (row['workload'], row['point'], row['int_regs'], row['float_regs'])
            if key in unique:
                old = unique[key]
                for field in ('cycles', 'instructions', 'demand_stall_cycles', 'standalone_stall_cycles'):
                    if row[field] != old[field]:
                        raise ValueError(f'non-reproducible duplicate: {key}, {field}')
                # Prefer a result with detailed interval tracing.
                if 'int_single_overlap_fraction_of_shortage' in row:
                    unique[key] = row
            else:
                unique[key] = row
    if len(hashes) != 1 or len(windows) != 1:
        raise ValueError('cannot combine different binaries or measurement windows')
    grouped = defaultdict(list)
    for row in unique.values():
        grouped[row['workload'], row['point']].append(row)
    normalized, thresholds, baseline_rows = [], [], []
    for (workload, point), group in sorted(grouped.items()):
        baselines = [r for r in group if (r['int_regs'], r['float_regs']) == (224, 256)]
        if not baselines:
            unfinished.append((workload, point))
            continue
        baseline = baselines[0]
        baseline_rows.append(baseline)
        for row in group:
            row['ipc_ratio'] = row['ipc'] / baseline['ipc']
            row['ipc_loss'] = 1 - row['ipc_ratio']
            normalized.append(row)
        for axis in ('joint', 'int', 'float'):
            points = axis_points(group, axis)
            # A baseline alone does not constitute a one-axis scan.
            if len(points) < 2:
                continue
            pressure_field = ('standalone_stall_fraction' if axis == 'joint' else
                              f"{'int' if axis == 'int' else 'float'}_standalone_shortage_fraction")
            bad, good = pressure_onset(points, pressure_field)
            thresholds.append(dict(workload=workload, point=point, axis=axis,
                                   safe_1pct=minimum_safe(points, .01),
                                   safe_5pct=minimum_safe(points, .05),
                                   largest_tested_count_with_1pct_pressure=bad,
                                   next_larger_count_under_1pct_pressure=good,
                                   pressure_field=pressure_field,
                                   tested_counts=','.join(str(n) for n, _ in sorted(points))))
    normalized.sort(key=lambda r: (r['workload'], r['point'], r['int_regs'], r['float_regs']))
    dump_csv(args.out / 'all_points.csv', normalized)
    dump_csv(args.out / 'thresholds.csv', thresholds)
    (args.out / 'combined.json').write_text(json.dumps(dict(runs=normalized, thresholds=thresholds,
        failed=failed, unfinished=unfinished, binary_sha256=next(iter(hashes)),
        measurement_window=next(iter(windows))), indent=2) + '\n')
    report = ['# 昆明湖 V3 物理寄存器容量扫描', '',
              '**统计修正：旧 `rename.stallEvents::RegFull` 会把容量不足归因到 ROB/LSQ 头部等待，不能用其为 0 来证明没有寄存器压力。本报告只使用 schema 2 的直接容量检查。**', '',
              '容量失败率：有等待指令时 `canRename()` 因寄存器不足而失败的周期占比。独立阻塞率：这些周期中没有同时收到下游 `blockRename` 的占比；这仍不是可无条件回收的加速比例。当前模型对 INT/FP/Vector/RMisc 均要求至少 8 个空闲寄存器。', '',
              f"本报告包含 {len(grouped)} 个切片、{len({w for w, _ in grouped})} 个 workload；预热 {next(iter(windows))[0]:,}、测量 {next(iter(windows))[1]:,} 条指令。单线程、默认 kmhv3.py，只改物理寄存器数量，不改变时钟、端口和流水线，也不实现论文的复用机制。默认参照为 INT=224、FP=256。切片选择和权重见批次 manifest.json。", '',
              '| 默认配置切片 | IPC | 容量失败率 | 独立容量阻塞率 | INT 不足 | FP 不足 | Legacy RegFull |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for r in baseline_rows:
        report.append(f"| {r['workload']}/{r['point']} | {r['ipc']:.3f} | {r['demand_stall_fraction']:.2%} | {r['standalone_stall_fraction']:.2%} | {r['int_shortage_fraction']:.2%} | {r['float_shortage_fraction']:.2%} | {r['regfull_fraction']:.2%} |")
    report += ['', '阈值是本次离散采样的界限，不是所有 workload 通用的最小硬件容量。“≤1%/≤5% IPC 损失”的容量，要求该采样点及所有更大的已测容量均满足该损失上限。联合扫描的容量表示 INT 和 FP 各有这么多个。', '',
               '| 切片 | 扫描轴 | IPC 损失≤1%的最小已测容量 | IPC 损失≤5%的最小已测容量 | 独立阻塞≥1%的最大已测容量 | 再大一级且阻塞<1%的容量 |',
               '|---|---|---:|---:|---:|---:|']
    for r in thresholds:
        cell = lambda k: str(r[k]) if r[k] is not None else '未界定'
        report.append(f"| {r['workload']}/{r['point']} | {r['axis']} | {cell('safe_1pct')} | {cell('safe_5pct')} | {cell('largest_tested_count_with_1pct_pressure')} | {cell('next_larger_count_under_1pct_pressure')} |")
    report += ['', '| 切片 | INT/FP | IPC | 相对默认 IPC 变化 | 容量失败率 | 独立容量阻塞率 | INT 不足 | FP 不足 |',
               '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in normalized:
        report.append(f"| {r['workload']}/{r['point']} | {r['int_regs']}/{r['float_regs']} | {r['ipc']:.3f} | {100*(r['ipc_ratio']-1):+.2f}% | {r['demand_stall_fraction']:.2%} | {r['standalone_stall_fraction']:.2%} | {r['int_shortage_fraction']:.2%} | {r['float_shortage_fraction']:.2%} |")
    # Equal-weight geometric mean over the selected workload slices, not SPEC score.
    aggregates = defaultdict(list)
    for r in normalized:
        aggregates[r['int_regs'], r['float_regs']].append(r)
    aggregate_rows = []
    for (ni, nf), group in sorted(aggregates.items()):
        if len(group) != len(grouped):
            continue
        gm = math.exp(sum(math.log(r['ipc_ratio']) for r in group) / len(group))
        aggregate_rows.append(dict(int_regs=ni, float_regs=nf, slices=len(group),
                                   geometric_mean_ipc_ratio=gm,
                                   max_ipc_loss=max(r['ipc_loss'] for r in group),
                                   mean_standalone_fraction=sum(r['standalone_stall_fraction'] for r in group)/len(group)))
    dump_csv(args.out / 'selected_slice_aggregate.csv', aggregate_rows)
    report += ['', '覆盖限制：只代表所选切片和测量窗口，不作全 SPEC 外推。单消费者统计只包含窗口内完整释放且未发生别名的 INT/FP 值。大容量实验不计面积、时序和能耗成本。', '',
               f'完整原始点：`all_points.csv`；阈值：`thresholds.csv`；失败任务：{len(failed)}；缺少默认参照：{len(unfinished)}。']
    if args.plot:
        make_plot(normalized, args.out)
        report += ['', '图：`joint_capacity.png`、`joint_capacity.pdf`（联合扫描）；`separate_capacity.png`、`separate_capacity.pdf`（只改一类）。']
    (args.out / 'report.md').write_text('\n'.join(report) + '\n')
    print('\n'.join(report[:18]))
    print(f'Wrote {len(normalized)} points and {len(thresholds)} thresholds to {args.out}')


def make_plot(rows, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    series = defaultdict(list)
    for r in rows:
        if r['int_regs'] == r['float_regs'] or (r['int_regs'], r['float_regs']) == (224, 256):
            key = (r['int_regs'], r['float_regs'])
            series[r['workload']].append((key, r))
    counts = sorted({n for group in series.values() for n, _ in group})
    labels = ['224/256\ndefault' if n == (224, 256) else str(n[0]) for n in counts]
    x = {n: i for i, n in enumerate(counts)}
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True, constrained_layout=True)
    for workload, group in sorted(series.items()):
        group.sort()
        axes[0].plot([x[n] for n, _ in group], [100*r['ipc_ratio'] for _, r in group], marker='o', markersize=4, label=workload)
        axes[1].plot([x[n] for n, _ in group], [100*r['standalone_stall_fraction'] for _, r in group], marker='o', markersize=4)
    axes[0].axhline(95, color='gray', linestyle='--', linewidth=1)
    axes[0].axhline(99, color='gray', linestyle=':', linewidth=1)
    axes[0].set_ylabel('IPC relative to default (%)')
    axes[0].set_title('Kunminghu V3: physical register capacity sweep (selected slices)')
    axes[0].legend(ncol=4, fontsize=8, loc='lower right')
    axes[1].set_ylabel('Standalone capacity blocked cycles (%)')
    axes[1].set_xlabel('Physical registers per class (INT = FP, except default)')
    axes[1].set_xticks(range(len(counts)), labels)
    for axis in axes:
        axis.grid(alpha=.25)
    fig.savefig(out / 'joint_capacity.png', dpi=180)
    fig.savefig(out / 'joint_capacity.pdf')
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['workload']].append(row)
    for col, which in enumerate(('int', 'float')):
        class_name = 'int' if which == 'int' else 'float'
        for workload, group in sorted(grouped.items()):
            points = sorted(axis_points(group, which))
            if len(points) < 2:
                continue
            axes[0, col].plot([n for n, _ in points], [100*r['ipc_ratio'] for _, r in points], marker='o', markersize=3, label=workload)
            axes[1, col].plot([n for n, _ in points], [100*r[f'{class_name}_standalone_shortage_fraction'] for _, r in points], marker='o', markersize=3)
        axes[0, col].axhline(95, color='gray', linestyle='--', linewidth=1)
        axes[0, col].set_title('INT sweep (FP=256)' if which == 'int' else 'FP sweep (INT=224)')
        axes[0, col].set_ylabel('IPC relative to default (%)')
        axes[1, col].set_ylabel(f'{which.upper()} standalone shortage cycles (%)')
        axes[1, col].set_xlabel(f'Physical {which.upper()} registers')
        axes[0, col].legend(fontsize=7, ncol=2)
        for row in range(2):
            axes[row, col].grid(alpha=.25)
    fig.savefig(out / 'separate_capacity.png', dpi=180)
    fig.savefig(out / 'separate_capacity.pdf')
    plt.close(fig)


if __name__ == '__main__':
    main()

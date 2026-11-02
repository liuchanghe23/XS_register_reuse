#!/usr/bin/env python3
"""Analyze validated distributed results without rerunning simulations.

Run experiment.py report first. This script writes derived CSV/JSON and optional
figures to report/analysis; it does not change run data or simulator sources.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys


def read_csv(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def number(row, key):
    return float(row[key])


def geomean(values):
    values = list(values)
    return math.exp(statistics.mean(math.log(value) for value in values))


def write_csv(path, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def describe(values):
    values = list(values)
    return dict(n=len(values), geomean=geomean(values), median=statistics.median(values),
                minimum=min(values), maximum=max(values),
                above_1pct=sum(x > 1.01 for x in values),
                below_minus_1pct=sum(x < .99 for x in values),
                below_minus_5pct=sum(x < .95 for x in values))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, default=Path(__file__).resolve().parent/'batch-6servers')
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()
    batch = args.batch.resolve()
    report = batch/'report'
    out = report/'analysis'
    out.mkdir(parents=True, exist_ok=True)
    plan = json.loads((batch/'plan.json').read_text())
    validation = json.loads((report/'validation.json').read_text())
    capacity = read_csv(report/'capacity_workload_weighted.csv')
    raw_capacity = read_csv(report/'capacity_per_run.csv')
    raw_reuse = read_csv(report/'reuse_per_run.csv')
    reuse = read_csv(report/'reuse_workload_weighted.csv')
    thresholds = read_csv(report/'capacity_workload_thresholds.csv')
    pairs = read_csv(report/'reuse_pairs.csv')
    assert validation['plan_id'] == plan['plan_id']
    assert len(raw_capacity) == validation['capacity_runs']
    assert len(raw_reuse) == validation['reuse_runs']
    assert len(pairs) == validation['reuse_pairs']
    keyed = {(r['workload'], r['point'], int(r['int_regs']), r['mode']): r for r in raw_reuse}
    selected = defaultdict(list)
    for row in plan['selected']:
        selected[row['workload']].append(row)
    combined = []
    counters = []
    for workload, points in sorted(selected.items()):
        common = [p for p in points if all((workload, p['point'], ni, mode) in keyed
                  for ni in (192, 224) for mode in ('off', 'certain'))]
        weight = sum(p['weight'] for p in common)
        def cpi(ni, mode):
            return sum(p['weight']*number(keyed[workload,p['point'],ni,mode], 'cpi')
                       for p in common)/weight
        default_off, default_certain = cpi(224,'off'), cpi(224,'certain')
        reduced_off, reduced_certain = cpi(192,'off'), cpi(192,'certain')
        loss = reduced_off-default_off
        recovered = reduced_off-reduced_certain
        combined.append(dict(workload=workload, matched_slices=len(common), expected_slices=len(points),
                             complete=len(common)==len(points), selected_weight=weight,
                             expected_selected_weight=sum(p['weight'] for p in points),
                             default_off_cpi=default_off, default_certain_cpi=default_certain,
                             reduced_off_cpi=reduced_off, reduced_certain_cpi=reduced_certain,
                             default_reuse_speedup=default_off/default_certain,
                             reduced_reuse_speedup=reduced_off/reduced_certain,
                             reduced_off_vs_default=default_off/reduced_off,
                             reduced_certain_vs_default=default_off/reduced_certain,
                             added_cpi_from_reduction=loss, recovered_cpi=recovered,
                             recovered_fraction_of_added_cpi=recovered/loss if loss>0 else ''))
    for row in reuse:
        workload, ni = row['workload'], int(row['int_regs'])
        matched = [p for p in selected[workload] if all((workload,p['point'],ni,mode) in keyed
                   for mode in ('off','certain'))]
        weight = sum(p['weight'] for p in matched)
        def per_inst(field):
            return sum(p['weight']*number(keyed[workload,p['point'],ni,'certain'], field)/
                       number(keyed[workload,p['point'],ni,'certain'],'instructions') for p in matched)/weight
        counter = dict(workload=workload, int_regs=ni, float_regs=int(row['float_regs']),
                       complete=row['complete'], speedup=number(row,'speedup'))
        for field in ['sharedVersions','allocatedSlots','restoredGroups','squashEvents','aliasRejects','versionLimitRejects']:
            counter[field+'_per_ki']=1000*per_inst('reuse_'+field)
        counter['shared_fraction_of_scalar_destinations'] = counter['sharedVersions_per_ki'] / (
            counter['sharedVersions_per_ki']+counter['allocatedSlots_per_ki'])
        counters.append(counter)
    capacity_key = {(r['workload'], r['variant']):r for r in capacity}
    variants = {r['variant'] for r in capacity}
    all_capacity_workloads = [w for w in selected if all(
        (w,v) in capacity_key and capacity_key[w,v]['complete']=='True' for v in variants)]
    capacity_summary = []
    for variant in sorted({r['variant'] for r in capacity}):
        group=[r for r in capacity if r['variant']==variant and r['complete']=='True'
               and r.get('ipc_ratio_to_default')]
        values=[number(r,'ipc_ratio_to_default') for r in group]
        capacity_summary.append(dict(variant=variant,int_regs=int(group[0]['int_regs']),
                                     float_regs=int(group[0]['float_regs']),**describe(values),
                                     common_n=len(all_capacity_workloads),
                                     common_geomean=geomean(number(capacity_key[w,variant],'ipc_ratio_to_default') for w in all_capacity_workloads),
                                     common_minimum=min(number(capacity_key[w,variant],'ipc_ratio_to_default') for w in all_capacity_workloads)))
    opportunity=[]
    for workload in sorted(selected):
        group=[r for r in raw_capacity if r['workload']==workload and r['variant']=='baseline']
        weight=sum(number(r,'weight') for r in group)
        def weighted(field):
            return sum(number(r,'weight')*number(r,field)/number(r,'instructions') for r in group)/weight
        row=dict(workload=workload)
        for cls in ('int','float'):
            for name, numerator,denominator in [
                ('single_fraction_unaliased','singleConsumerValues','unaliasedValues'),
                ('eligible_fraction_single','eligibleSingleValues','singleConsumerValues'),
                ('self_redef_fraction_single','selfRedefSingleValues','singleConsumerValues'),
                ('mean_single_held_at_shortage','singleStallExposure',None),
                ('mean_eligible_held_at_shortage','eligibleStallExposure',None),
                ('mean_self_redef_held_at_shortage','selfRedefStallExposure',None)]:
                a=weighted(cls+'_'+numerator)
                b=weighted(cls+'_'+denominator) if denominator else weighted(cls+'_shortage_cycles')
                row[cls+'_'+name]=a/b if b else None
        opportunity.append(row)
    failures=[]
    for invalid in validation['invalid']:
        p=batch/'results'/invalid['id']
        info=json.loads((p/'run.json').read_text())
        text=(p/'run.log').read_text(errors='replace')
        failures.append(dict(id=invalid['id'],state=info['state'],returncode=info['returncode'],
                             elapsed_seconds=info['elapsed_seconds'],hostname=info['hostname'],
                             difftest_error_text='difftest failed' in text.lower()))
    # Independently compare the observer binary with feature-OFF for available paired runs.
    cap_key={(r['workload'],r['point'],int(r['int_regs']),int(r['float_regs'])):r for r in raw_capacity}
    equivalence=[]
    for ni,nf in [(224,256),(192,208)]:
        group=[r for r in raw_reuse if int(r['int_regs'])==ni and r['mode']=='off']
        matches=[(r,cap_key.get((r['workload'],r['point'],ni,nf))) for r in group]
        matches=[(a,b) for a,b in matches if b]
        equivalence.append(dict(int_regs=ni,float_regs=nf,compared=len(matches),
            exact_instructions_and_cycles=sum(number(a,'instructions')==number(b,'instructions')
                and number(a,'cycles')==number(b,'cycles') for a,b in matches),
            max_relative_cpi_difference=max(abs(number(a,'cpi')/number(b,'cpi')-1) for a,b in matches)))
    pressure=[r for r in capacity if r['variant']=='baseline']
    # Preserve the strongest regression's raw counters across four configurations.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'register_reuse_analysis'))
    from analyze import stat_blocks
    case_study=[]
    worst=sorted((r for r in pairs if r['workload']=='soplex_ref' and int(r['int_regs'])==192),
                 key=lambda r:number(r,'speedup'))[:5]
    for pair in worst:
        for mode in ['baseline-off','baseline-certain','mixed192_208-off','mixed192_208-certain']:
            stats=stat_blocks(batch/'results'/'reuse'/'soplex_ref'/pair['point']/mode/'stats.txt')[-1]
            row=dict(workload='soplex_ref',point=pair['point'],variant=mode,weight=pair['weight'])
            for stat in ['simInsts','system.cpu.numCycles','system.cpu.lsq0.RAWQueueFullCycles',
                         'system.cpu.lsq0.RAWQueueReplay','system.cpu.lsq0.RARQueueReplay',
                         'system.cpu.commit.squashDueToBranch','system.cpu.regReuse.repairCopies',
                         'system.cpu.regReuse.repairWaitCycles','system.cpu.regReuse.restoredGroups']:
                row[stat]=stats.get(stat,0)
            case_study.append(row)
    write_csv(out/'soplex_raw_queue_case.csv',case_study)
    result=dict(plan_id=plan['plan_id'],capacity_runs=len(raw_capacity),reuse_runs=len(raw_reuse),
                expected_runs=len(plan['tasks']),failures=failures,
                coverage=dict(minimum=min(r['expected_selected_weight'] for r in combined),
                              maximum=max(r['expected_selected_weight'] for r in combined)),
                reuse={},common_slices={},capacity=capacity_summary,
                all_capacity_workloads=all_capacity_workloads,off_equivalence=equivalence,
                input_sha256={name:hashlib.sha256((report/name).read_bytes()).hexdigest() for name in
                    ['validation.json','capacity_per_run.csv','capacity_workload_weighted.csv',
                     'reuse_per_run.csv','reuse_pairs.csv','reuse_workload_weighted.csv']})
    for ni in (224,192):
        group=[r for r in reuse if int(r['int_regs'])==ni]
        result['reuse'][str(ni)]=dict(all_available=describe(number(r,'speedup') for r in group),
            complete_workloads=describe(number(r,'speedup') for r in group if r['complete']=='True'),
            incomplete_workloads=[r['workload'] for r in group if r['complete']!='True'])
    result['slice_reuse']={}
    for ni in (224,192):
        group=[r for r in pairs if int(r['int_regs'])==ni]
        ordered=sorted(group,key=lambda r:number(r,'speedup'))
        result['slice_reuse'][str(ni)]=dict(
            pairs=len(group),below_minus_1pct=sum(number(r,'speedup')<.99 for r in group),
            below_minus_5pct=sum(number(r,'speedup')<.95 for r in group),
            worst=[{k:r[k] for k in ['workload','point','speedup','weight']} for r in ordered[:5]],
            best=[{k:r[k] for k in ['workload','point','speedup','weight']} for r in ordered[-5:]])
    result['reuse_total_counters']={field:sum(number(r,'reuse_'+field) for r in raw_reuse)
        for field in ['predictedReuses','predictionMisses','repairCopies','repairWaitCycles']}
    for field in ['default_reuse_speedup','reduced_reuse_speedup','reduced_off_vs_default','reduced_certain_vs_default']:
        result['common_slices'][field]=dict(all_available=describe(r[field] for r in combined),
            complete_workloads=describe(r[field] for r in combined if r['complete']))
    for field in ['weighted_standalone_stall_fraction','weighted_int_standalone_shortage_fraction',
                  'weighted_float_standalone_shortage_fraction']:
        vals=[number(r,field) for r in pressure]
        result[field]=dict(mean=statistics.mean(vals),median=statistics.median(vals),
                          maximum=max(vals),at_least_1pct=sum(v>=.01 for v in vals),
                          at_least_10pct=sum(v>=.1 for v in vals))
    result['family_weight_sensitivity']={}
    for ni in (224,192):
        families=defaultdict(list)
        for row in reuse:
            if int(row['int_regs'])==ni:
                families[row['workload'].split('_')[0]].append(number(row,'speedup'))
        result['family_weight_sensitivity'][str(ni)]=dict(
            families=len(families),geomean=geomean(geomean(values) for values in families.values()),
            note='Equal weight per named benchmark family, equal weight per input within family; not official SPEC scores')
    result['recovery_of_reduction_cpi']=dict(
        positive_reduction_cost_workloads=sum(r['added_cpi_from_reduction']>0 for r in combined),
        ratio_of_equal_workload_summed_cpi=sum(r['recovered_cpi'] for r in combined)/sum(r['added_cpi_from_reduction'] for r in combined),
        median_fraction_for_positive_cost=statistics.median(r['recovered_fraction_of_added_cpi'] for r in combined if r['added_cpi_from_reduction']>0))
    result['threshold_counts']={axis:{limit:dict(Counter(r[limit] or 'none' for r in thresholds if r['axis']==axis))
                              for limit in ['safe_1pct','safe_5pct']} for axis in ['int','float']}
    write_csv(out/'four_way_comparison.csv',combined)
    write_csv(out/'reuse_counter_rates.csv',counters)
    write_csv(out/'capacity_summary.csv',capacity_summary)
    write_csv(out/'baseline_opportunities.csv',opportunity)
    write_csv(out/'failures.csv',failures)
    (out/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    if args.plot:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
        ordered=sorted(combined,key=lambda r:r['reduced_reuse_speedup'])
        fig,axes=plt.subplots(1,2,figsize=(14,17),sharey=True,gridspec_kw={'width_ratios':[1,1]})
        yy=list(range(len(ordered)))
        axes[0].barh([v-.19 for v in yy],[100*(r['default_reuse_speedup']-1) for r in ordered],height=.37,label='224 INT / 256 FP')
        axes[0].barh([v+.19 for v in yy],[100*(r['reduced_reuse_speedup']-1) for r in ordered],height=.37,label='192 INT / 208 FP')
        axes[0].set_yticks(yy,[r['workload']+(' *' if not r['complete'] else '') for r in ordered])
        axes[0].set_xlabel('Certain reuse vs OFF at the same capacity (%)')
        axes[0].legend(loc='lower right')
        axes[1].barh([v-.19 for v in yy],[100*(r['reduced_off_vs_default']-1) for r in ordered],height=.37,label='192/208 OFF',color='#969696')
        axes[1].barh([v+.19 for v in yy],[100*(r['reduced_certain_vs_default']-1) for r in ordered],height=.37,label='192/208 certain',color='#2a9d8f')
        axes[1].set_xlabel('Reduced capacity vs 224/256 OFF (%)')
        axes[1].legend(loc='lower right')
        for ax in axes:
            ax.axvline(0,color='black',linewidth=.8)
            ax.grid(axis='x',alpha=.2)
        fig.suptitle('Deterministic register reuse: weighted CPI within each workload\n55 workloads; 20M warmup + 20M measure; * mcf uses 8/9 matched slices')
        fig.tight_layout(rect=(0,0,1,.97))
        fig.savefig(out/'reuse_workloads.png',dpi=170)
        fig.savefig(out/'reuse_workloads.svg')
        plt.close(fig)
        fig,axes=plt.subplots(1,2,figsize=(13,4.5))
        for axis,ax,selector in [('INT',axes[0],lambda r:r['float_regs']==256 and r['variant']!='large'),
                                  ('FP',axes[1],lambda r:r['int_regs']==224 and r['variant']!='large')]:
            points=sorted((r for r in capacity_summary if selector(r)),key=lambda r:r['int_regs'] if axis=='INT' else r['float_regs'])
            xx=[r['int_regs'] if axis=='INT' else r['float_regs'] for r in points]
            for field,label,style in [('common_geomean','Workload geomean','-o'),('common_minimum','Worst workload','--s')]:
                ax.plot(xx,[100*(r[field]-1) for r in points],style,label=label)
            ax.axhline(-5,color='gray',linestyle=':',label='-5%')
            ax.axhline(0,color='black',linewidth=.7)
            ax.set_xlabel(axis+' physical base slots')
            ax.set_ylabel('IPC change vs default (%)')
            ax.grid(alpha=.2)
            ax.legend()
        fig.suptitle(f'Capacity sensitivity, same {len(all_capacity_workloads)} complete workloads at every point')
        fig.tight_layout()
        fig.savefig(out/'capacity_curves.png',dpi=170)
        fig.savefig(out/'capacity_curves.svg')
        plt.close(fig)
        case=[r for r in case_study if r['point']=='6948']
        if case:
            fig,axes=plt.subplots(1,2,figsize=(11,4.5))
            xx=list(range(4))
            labels=['224/256 OFF','224/256 certain','192/208 OFF','192/208 certain']
            colors=['#969696','#457b9d','#b5b5b5','#2a9d8f']
            axes[0].bar(xx,[r['system.cpu.numCycles']/1e6 for r in case],color=colors)
            axes[0].set_ylabel('Measured cycles (millions)')
            axes[1].bar(xx,[r['system.cpu.lsq0.RAWQueueReplay']/1e6 for r in case],color=colors)
            axes[1].set_ylabel('RAW queue full replay events (millions)')
            for ax in axes:
                ax.set_xticks(xx,labels,rotation=25,ha='right')
                ax.grid(axis='y',alpha=.2)
            fig.suptitle('soplex_ref / 6948: reuse removes the reduced-capacity throttling benefit')
            fig.tight_layout()
            fig.savefig(out/'soplex_case.png',dpi=170)
            fig.savefig(out/'soplex_case.svg')
            plt.close(fig)
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()

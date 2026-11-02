# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

| Workload/slice | Variant | IPC | RegFull/cycles | INT shortage/cycles | FP shortage/cycles | INT single-use | FP single-use |
|---|---|---:|---:|---:|---:|---:|---:|
| mcf/12253 | small | 0.217 | 0.00% | 0.00% | 0.00% | 70.96% | 0.00% |

| Baseline workload/slice | INT shortage cycles with held single-use value | With eligible consumer | Mean held single-use INT values during shortage |
|---|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

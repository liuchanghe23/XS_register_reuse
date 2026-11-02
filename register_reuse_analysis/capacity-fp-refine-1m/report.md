# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | fp208 | 224/208 | 4.556 | 0.00% | 36.93% | 36.49% | 0.00% | 36.93% |
| GemsFDTD/30385 | fp240 | 224/240 | 4.630 | 0.00% | 32.66% | 32.54% | 0.00% | 32.66% |
| bwaves/37801 | fp208 | 224/208 | 3.316 | 0.00% | 54.92% | 54.76% | 0.00% | 54.92% |
| bwaves/37801 | fp240 | 224/240 | 3.421 | 0.00% | 45.57% | 39.25% | 0.00% | 45.57% |
| leslie3d/68289 | fp208 | 224/208 | 4.212 | 0.00% | 29.00% | 27.65% | 0.10% | 28.91% |
| leslie3d/68289 | fp240 | 224/240 | 4.335 | 0.00% | 11.83% | 11.18% | 0.05% | 11.78% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

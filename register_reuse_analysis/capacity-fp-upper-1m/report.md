# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | fp272 | 224/272 | 4.592 | 0.00% | 3.48% | 0.21% | 0.00% | 3.48% |
| GemsFDTD/30385 | fp288 | 224/288 | 4.547 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| bwaves/37801 | fp272 | 224/272 | 3.411 | 0.00% | 23.43% | 12.12% | 0.00% | 23.43% |
| bwaves/37801 | fp288 | 224/288 | 3.441 | 0.00% | 6.53% | 0.04% | 0.00% | 6.53% |
| leslie3d/68289 | fp272 | 224/272 | 4.366 | 0.00% | 4.58% | 3.97% | 0.25% | 4.34% |
| leslie3d/68289 | fp288 | 224/288 | 4.313 | 0.00% | 0.14% | 0.08% | 0.08% | 0.06% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

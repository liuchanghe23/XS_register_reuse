# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| bwaves/37801 | baseline | 224/256 | 3.176 | 0.00% | 41.87% | 39.18% | 0.00% | 41.87% |
| bwaves/37801 | both64 | 64/64 | 1.574 | 0.00% | 77.68% | 77.46% | 2.33% | 76.29% |
| mcf/12253 | baseline | 224/256 | 0.436 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| mcf/12253 | both64 | 64/64 | 0.233 | 0.00% | 82.06% | 80.73% | 82.06% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|
| bwaves/37801/baseline | 0.00% | 0.00% | 0.00 | 99.92% | 99.92% | 159.73 |
| bwaves/37801/both64 | 100.00% | 98.18% | 5.73 | 99.98% | 99.98% | 24.11 |
| mcf/12253/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| mcf/12253/both64 | 98.64% | 96.45% | 5.95 | 0.00% | 0.00% | 0.00 |

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|
| bwaves/37801 | both64 | 0.496x | 0.00% | 0.00% |
| mcf/12253 | both64 | 0.533x | 0.00% | 0.00% |

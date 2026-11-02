# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| bzip2_combined/7116 | int256 | 256/256 | 1.210 | 0.00% | 1.19% | 1.13% | 1.19% | 0.00% |
| bzip2_combined/7116 | int320 | 320/256 | 1.204 | 0.00% | 0.21% | 0.00% | 0.21% | 0.00% |
| gcc_166/2766 | int256 | 256/256 | 1.678 | 0.00% | 19.37% | 7.22% | 19.37% | 0.00% |
| gcc_166/2766 | int320 | 320/256 | 1.677 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| hmmer_nph3/2887 | int256 | 256/256 | 6.339 | 0.00% | 2.00% | 1.87% | 2.00% | 0.00% |
| hmmer_nph3/2887 | int320 | 320/256 | 6.357 | 0.00% | 0.20% | 0.20% | 0.20% | 0.00% |
| libquantum/64624 | int256 | 256/256 | 5.660 | 0.00% | 0.03% | 0.03% | 0.03% | 0.00% |
| libquantum/64624 | int320 | 320/256 | 5.597 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

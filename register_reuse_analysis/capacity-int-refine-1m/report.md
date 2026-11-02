# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| bzip2_combined/7116 | int112 | 112/256 | 1.165 | 0.00% | 24.54% | 23.04% | 24.54% | 0.00% |
| bzip2_combined/7116 | int144 | 144/256 | 1.193 | 0.00% | 16.55% | 15.78% | 16.55% | 0.00% |
| bzip2_combined/7116 | int176 | 176/256 | 1.209 | 0.00% | 12.55% | 12.25% | 12.55% | 0.00% |
| bzip2_combined/7116 | int208 | 208/256 | 1.204 | 0.00% | 9.97% | 9.84% | 9.97% | 0.00% |
| gcc_166/2766 | int112 | 112/256 | 1.452 | 0.00% | 71.29% | 71.02% | 71.29% | 0.00% |
| gcc_166/2766 | int144 | 144/256 | 1.484 | 0.00% | 65.61% | 65.44% | 65.61% | 0.00% |
| gcc_166/2766 | int176 | 176/256 | 1.550 | 0.00% | 66.00% | 65.86% | 66.00% | 0.00% |
| gcc_166/2766 | int208 | 208/256 | 1.618 | 0.00% | 53.15% | 50.39% | 53.15% | 0.00% |
| hmmer_nph3/2887 | int112 | 112/256 | 4.607 | 0.00% | 37.80% | 37.79% | 37.80% | 0.00% |
| hmmer_nph3/2887 | int144 | 144/256 | 5.534 | 0.00% | 25.46% | 25.44% | 25.46% | 0.00% |
| hmmer_nph3/2887 | int176 | 176/256 | 6.074 | 0.00% | 16.31% | 16.12% | 16.31% | 0.00% |
| hmmer_nph3/2887 | int208 | 208/256 | 6.276 | 0.00% | 13.14% | 13.10% | 13.14% | 0.00% |
| libquantum/64624 | int112 | 112/256 | 5.507 | 0.00% | 24.41% | 24.13% | 24.41% | 0.00% |
| libquantum/64624 | int144 | 144/256 | 5.659 | 0.00% | 1.85% | 1.71% | 1.85% | 0.00% |
| libquantum/64624 | int176 | 176/256 | 5.653 | 0.00% | 0.33% | 0.31% | 0.33% | 0.00% |
| libquantum/64624 | int208 | 208/256 | 5.674 | 0.00% | 0.01% | 0.01% | 0.01% | 0.00% |
| mcf/12253 | int112 | 112/256 | 0.389 | 0.00% | 62.62% | 60.82% | 62.62% | 0.00% |
| mcf/12253 | int144 | 144/256 | 0.435 | 0.00% | 39.41% | 35.04% | 39.41% | 0.00% |
| mcf/12253 | int176 | 176/256 | 0.454 | 0.00% | 19.13% | 16.91% | 19.13% | 0.00% |
| mcf/12253 | int208 | 208/256 | 0.470 | 0.00% | 8.49% | 1.31% | 8.49% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

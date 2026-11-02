# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

| Workload/slice | Variant | IPC | RegFull/cycles | INT shortage/cycles | FP shortage/cycles | INT single-use | FP single-use |
|---|---|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | small | 1.341 | 0.06% | 0.01% | 0.05% | 46.15% | 90.00% |
| bwaves/37801 | small | 0.932 | 0.06% | 0.00% | 0.06% | 20.42% | 99.16% |
| bzip2_combined/7116 | small | 0.724 | 0.00% | 0.00% | 0.00% | 64.72% | 0.00% |
| gcc_166/2766 | small | 0.732 | 0.00% | 0.00% | 0.00% | 63.28% | 0.00% |
| hmmer_nph3/2887 | small | 1.059 | 0.00% | 0.00% | 0.00% | 77.14% | 0.00% |
| leslie3d/68289 | small | 0.854 | 0.04% | 0.00% | 0.04% | 51.24% | 92.89% |
| libquantum/64624 | small | 1.164 | 0.02% | 0.02% | 0.00% | 73.05% | 0.00% |
| mcf/12253 | small | 0.217 | 0.00% | 0.00% | 0.00% | 70.96% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385/small | 100.00% | 0.00% | 6.00 | 100.00% | 100.00% | 5.64 |
| bwaves/37801/small | 0.00% | 0.00% | 0.00 | 100.00% | 100.00% | 21.02 |
| bzip2_combined/7116/small | 100.00% | 66.67% | 7.33 | 0.00% | 0.00% | 0.00 |
| gcc_166/2766/small | 100.00% | 100.00% | 8.00 | 0.00% | 0.00% | 0.00 |
| hmmer_nph3/2887/small | 100.00% | 100.00% | 7.00 | 0.00% | 0.00% | 0.00 |
| leslie3d/68289/small | 100.00% | 0.00% | 3.00 | 100.00% | 100.00% | 11.47 |
| libquantum/64624/small | 100.00% | 100.00% | 4.00 | 0.00% | 0.00% | 0.00 |
| mcf/12253/small | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

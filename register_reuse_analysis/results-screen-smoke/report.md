# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

| Workload/slice | Variant | IPC | RegFull/cycles | INT shortage/cycles | FP shortage/cycles | INT single-use | FP single-use |
|---|---|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | baseline | 4.093 | 0.00% | 0.00% | 0.00% | 46.15% | 90.01% |
| GemsFDTD/30385 | large | 4.124 | 0.00% | 0.00% | 0.00% | 46.15% | 90.00% |
| bwaves/37801 | baseline | 3.176 | 0.00% | 0.00% | 0.00% | 20.44% | 99.16% |
| bwaves/37801 | large | 3.245 | 0.00% | 0.00% | 0.00% | 20.44% | 99.16% |
| bzip2_combined/7116 | baseline | 1.362 | 0.00% | 0.00% | 0.00% | 64.78% | 0.00% |
| bzip2_combined/7116 | large | 1.400 | 0.00% | 0.00% | 0.00% | 64.79% | 0.00% |
| gcc_166/2766 | baseline | 1.535 | 0.00% | 0.00% | 0.00% | 63.28% | 0.00% |
| gcc_166/2766 | large | 1.564 | 0.00% | 0.00% | 0.00% | 63.28% | 0.00% |
| hmmer_nph3/2887 | baseline | 6.139 | 0.00% | 0.00% | 0.00% | 77.14% | 0.00% |
| hmmer_nph3/2887 | large | 6.181 | 0.00% | 0.00% | 0.00% | 77.14% | 0.00% |
| leslie3d/68289 | baseline | 2.402 | 0.00% | 0.00% | 0.00% | 51.22% | 92.90% |
| leslie3d/68289 | large | 2.427 | 0.00% | 0.00% | 0.00% | 51.22% | 92.90% |
| libquantum/64624 | baseline | 5.624 | 0.00% | 0.00% | 0.00% | 72.86% | 0.00% |
| libquantum/64624 | large | 5.528 | 0.00% | 0.00% | 0.00% | 72.86% | 0.00% |
| mcf/12253 | baseline | 0.436 | 0.00% | 0.00% | 0.00% | 70.96% | 0.00% |
| mcf/12253 | large | 0.440 | 0.00% | 0.00% | 0.00% | 70.96% | 0.00% |

| Baseline workload/slice | INT shortage cycles with held single-use value | With eligible consumer | Mean held single-use INT values during shortage |
|---|---:|---:|---:|
| GemsFDTD/30385 | 0.00% | 0.00% | 0.00 |
| bwaves/37801 | 0.00% | 0.00% | 0.00 |
| bzip2_combined/7116 | 0.00% | 0.00% | 0.00 |
| gcc_166/2766 | 0.00% | 0.00% | 0.00 |
| hmmer_nph3/2887 | 0.00% | 0.00% | 0.00 |
| leslie3d/68289 | 0.00% | 0.00% | 0.00 |
| libquantum/64624 | 0.00% | 0.00% | 0.00 |
| mcf/12253 | 0.00% | 0.00% | 0.00 |

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|
| GemsFDTD/30385 | large | 1.007x | 0.00% | 0.00% |
| bwaves/37801 | large | 1.022x | 0.00% | 0.00% |
| bzip2_combined/7116 | large | 1.028x | 0.00% | 0.00% |
| gcc_166/2766 | large | 1.019x | 0.00% | 0.00% |
| hmmer_nph3/2887 | large | 1.007x | 0.00% | 0.00% |
| leslie3d/68289 | large | 1.010x | 0.00% | 0.00% |
| libquantum/64624 | large | 0.983x | 0.00% | 0.00% |
| mcf/12253 | large | 1.008x | 0.00% | 0.00% |

# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

| Workload/slice | Variant | IPC | RegFull/cycles | INT shortage/cycles | FP shortage/cycles | INT single-use | FP single-use |
|---|---|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | baseline | 4.554 | 0.00% | 0.00% | 0.00% | 46.15% | 90.00% |
| bwaves/37801 | baseline | 3.480 | 0.00% | 0.00% | 0.00% | 20.37% | 99.16% |
| bzip2_combined/7116 | baseline | 1.202 | 0.00% | 0.00% | 0.00% | 61.49% | 0.00% |
| gcc_166/2766 | baseline | 1.662 | 0.00% | 0.00% | 0.00% | 63.34% | 0.00% |
| hmmer_nph3/2887 | baseline | 6.315 | 0.00% | 0.00% | 0.00% | 77.12% | 0.00% |
| leslie3d/68289 | baseline | 4.408 | 0.00% | 0.00% | 0.00% | 50.25% | 94.26% |
| libquantum/64624 | baseline | 5.630 | 0.00% | 0.00% | 0.00% | 71.77% | 0.00% |
| mcf/12253 | baseline | 0.470 | 0.00% | 0.00% | 0.00% | 70.84% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| bwaves/37801/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| bzip2_combined/7116/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| gcc_166/2766/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| hmmer_nph3/2887/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| leslie3d/68289/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| libquantum/64624/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |
| mcf/12253/baseline | 0.00% | 0.00% | 0.00 | 0.00% | 0.00% | 0.00 |

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

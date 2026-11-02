# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | baseline | 224/256 | 4.554 | 0.00% | 32.71% | 32.13% | 0.00% | 32.71% |
| GemsFDTD/30385 | both128 | 128/128 | 4.411 | 0.00% | 38.57% | 38.46% | 0.00% | 38.57% |
| GemsFDTD/30385 | both160 | 160/160 | 4.393 | 0.00% | 41.91% | 41.83% | 0.00% | 41.91% |
| GemsFDTD/30385 | both192 | 192/192 | 4.540 | 0.00% | 38.70% | 38.47% | 0.00% | 38.70% |
| GemsFDTD/30385 | both64 | 64/64 | 2.715 | 0.00% | 58.50% | 57.98% | 0.23% | 58.27% |
| GemsFDTD/30385 | both96 | 96/96 | 3.927 | 0.00% | 43.71% | 43.42% | 0.00% | 43.71% |
| GemsFDTD/30385 | large | 512/512 | 4.547 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| bwaves/37801 | baseline | 224/256 | 3.480 | 0.00% | 37.31% | 35.30% | 0.00% | 37.31% |
| bwaves/37801 | both128 | 128/128 | 2.542 | 0.00% | 66.08% | 66.07% | 0.00% | 66.08% |
| bwaves/37801 | both160 | 160/160 | 2.925 | 0.00% | 60.83% | 60.66% | 0.00% | 60.83% |
| bwaves/37801 | both192 | 192/192 | 3.128 | 0.00% | 57.55% | 57.19% | 0.00% | 57.55% |
| bwaves/37801 | both64 | 64/64 | 1.581 | 0.00% | 77.61% | 77.40% | 2.33% | 76.22% |
| bwaves/37801 | both96 | 96/96 | 2.228 | 0.00% | 69.41% | 69.31% | 0.13% | 69.29% |
| bwaves/37801 | large | 512/512 | 3.542 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| bzip2_combined/7116 | baseline | 224/256 | 1.202 | 0.00% | 7.01% | 6.87% | 7.01% | 0.00% |
| bzip2_combined/7116 | both128 | 128/128 | 1.187 | 0.00% | 19.97% | 18.69% | 19.97% | 0.00% |
| bzip2_combined/7116 | both160 | 160/160 | 1.204 | 0.00% | 14.07% | 13.57% | 14.07% | 0.00% |
| bzip2_combined/7116 | both192 | 192/192 | 1.207 | 0.00% | 11.14% | 10.96% | 11.14% | 0.00% |
| bzip2_combined/7116 | both64 | 64/64 | 1.019 | 0.00% | 50.39% | 46.99% | 50.39% | 0.00% |
| bzip2_combined/7116 | both96 | 96/96 | 1.143 | 0.00% | 30.10% | 27.94% | 30.10% | 0.00% |
| bzip2_combined/7116 | large | 512/512 | 1.210 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| gcc_166/2766 | baseline | 224/256 | 1.662 | 0.00% | 44.69% | 42.19% | 44.69% | 0.00% |
| gcc_166/2766 | both128 | 128/128 | 1.470 | 0.00% | 69.57% | 69.40% | 69.57% | 0.00% |
| gcc_166/2766 | both160 | 160/160 | 1.508 | 0.00% | 65.78% | 65.64% | 65.78% | 0.00% |
| gcc_166/2766 | both192 | 192/192 | 1.598 | 0.00% | 62.24% | 61.42% | 62.24% | 0.00% |
| gcc_166/2766 | both64 | 64/64 | 1.154 | 0.00% | 81.00% | 79.90% | 81.00% | 0.00% |
| gcc_166/2766 | both96 | 96/96 | 1.409 | 0.00% | 74.72% | 74.17% | 74.72% | 0.00% |
| gcc_166/2766 | large | 512/512 | 1.677 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| hmmer_nph3/2887 | baseline | 224/256 | 6.315 | 0.00% | 11.85% | 11.63% | 11.85% | 0.00% |
| hmmer_nph3/2887 | both128 | 128/128 | 5.119 | 0.00% | 30.73% | 30.72% | 30.73% | 0.00% |
| hmmer_nph3/2887 | both160 | 160/160 | 5.859 | 0.00% | 20.94% | 20.56% | 20.94% | 0.00% |
| hmmer_nph3/2887 | both192 | 192/192 | 6.213 | 0.00% | 14.13% | 14.11% | 14.13% | 0.00% |
| hmmer_nph3/2887 | both64 | 64/64 | 2.211 | 0.00% | 72.10% | 72.06% | 72.10% | 0.00% |
| hmmer_nph3/2887 | both96 | 96/96 | 3.909 | 0.00% | 47.73% | 47.70% | 47.73% | 0.00% |
| hmmer_nph3/2887 | large | 512/512 | 6.319 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| leslie3d/68289 | baseline | 224/256 | 4.408 | 0.00% | 6.10% | 5.63% | 0.13% | 5.97% |
| leslie3d/68289 | both128 | 128/128 | 3.609 | 0.00% | 48.85% | 48.40% | 6.35% | 45.14% |
| leslie3d/68289 | both160 | 160/160 | 4.026 | 0.00% | 39.12% | 38.69% | 2.51% | 36.72% |
| leslie3d/68289 | both192 | 192/192 | 4.178 | 0.00% | 32.51% | 31.37% | 0.41% | 32.09% |
| leslie3d/68289 | both64 | 64/64 | 2.216 | 0.00% | 69.52% | 68.39% | 6.12% | 68.05% |
| leslie3d/68289 | both96 | 96/96 | 3.237 | 0.00% | 52.87% | 52.44% | 5.73% | 50.97% |
| leslie3d/68289 | large | 512/512 | 4.408 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| libquantum/64624 | baseline | 224/256 | 5.630 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| libquantum/64624 | both128 | 128/128 | 5.667 | 0.00% | 13.15% | 12.36% | 13.15% | 0.00% |
| libquantum/64624 | both160 | 160/160 | 5.650 | 0.00% | 0.36% | 0.34% | 0.36% | 0.00% |
| libquantum/64624 | both192 | 192/192 | 5.626 | 0.00% | 0.31% | 0.24% | 0.31% | 0.00% |
| libquantum/64624 | both64 | 64/64 | 2.701 | 0.00% | 63.76% | 63.24% | 63.76% | 0.00% |
| libquantum/64624 | both96 | 96/96 | 4.862 | 0.00% | 32.73% | 32.38% | 32.73% | 0.00% |
| libquantum/64624 | large | 512/512 | 5.597 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| mcf/12253 | baseline | 224/256 | 0.470 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| mcf/12253 | both128 | 128/128 | 0.414 | 0.00% | 54.82% | 50.64% | 54.82% | 0.00% |
| mcf/12253 | both160 | 160/160 | 0.453 | 0.00% | 28.41% | 25.36% | 28.41% | 0.00% |
| mcf/12253 | both192 | 192/192 | 0.457 | 0.00% | 12.30% | 10.83% | 12.30% | 0.00% |
| mcf/12253 | both64 | 64/64 | 0.274 | 0.00% | 79.86% | 78.29% | 79.86% | 0.00% |
| mcf/12253 | both96 | 96/96 | 0.360 | 0.00% | 69.75% | 67.79% | 69.75% | 0.00% |
| mcf/12253 | large | 512/512 | 0.454 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|
| GemsFDTD/30385 | both128 | 0.969x | 0.00% | 0.00% |
| GemsFDTD/30385 | both160 | 0.965x | 0.00% | 0.00% |
| GemsFDTD/30385 | both192 | 0.997x | 0.00% | 0.00% |
| GemsFDTD/30385 | both64 | 0.596x | 0.00% | 0.00% |
| GemsFDTD/30385 | both96 | 0.862x | 0.00% | 0.00% |
| GemsFDTD/30385 | large | 0.999x | 0.00% | 0.00% |
| bwaves/37801 | both128 | 0.731x | 0.00% | 0.00% |
| bwaves/37801 | both160 | 0.840x | 0.00% | 0.00% |
| bwaves/37801 | both192 | 0.899x | 0.00% | 0.00% |
| bwaves/37801 | both64 | 0.454x | 0.00% | 0.00% |
| bwaves/37801 | both96 | 0.640x | 0.00% | 0.00% |
| bwaves/37801 | large | 1.018x | 0.00% | 0.00% |
| bzip2_combined/7116 | both128 | 0.987x | 0.00% | 0.00% |
| bzip2_combined/7116 | both160 | 1.001x | 0.00% | 0.00% |
| bzip2_combined/7116 | both192 | 1.004x | 0.00% | 0.00% |
| bzip2_combined/7116 | both64 | 0.847x | 0.00% | 0.00% |
| bzip2_combined/7116 | both96 | 0.951x | 0.00% | 0.00% |
| bzip2_combined/7116 | large | 1.007x | 0.00% | 0.00% |
| gcc_166/2766 | both128 | 0.884x | 0.00% | 0.00% |
| gcc_166/2766 | both160 | 0.908x | 0.00% | 0.00% |
| gcc_166/2766 | both192 | 0.961x | 0.00% | 0.00% |
| gcc_166/2766 | both64 | 0.694x | 0.00% | 0.00% |
| gcc_166/2766 | both96 | 0.848x | 0.00% | 0.00% |
| gcc_166/2766 | large | 1.009x | 0.00% | 0.00% |
| hmmer_nph3/2887 | both128 | 0.811x | 0.00% | 0.00% |
| hmmer_nph3/2887 | both160 | 0.928x | 0.00% | 0.00% |
| hmmer_nph3/2887 | both192 | 0.984x | 0.00% | 0.00% |
| hmmer_nph3/2887 | both64 | 0.350x | 0.00% | 0.00% |
| hmmer_nph3/2887 | both96 | 0.619x | 0.00% | 0.00% |
| hmmer_nph3/2887 | large | 1.001x | 0.00% | 0.00% |
| leslie3d/68289 | both128 | 0.819x | 0.00% | 0.00% |
| leslie3d/68289 | both160 | 0.913x | 0.00% | 0.00% |
| leslie3d/68289 | both192 | 0.948x | 0.00% | 0.00% |
| leslie3d/68289 | both64 | 0.503x | 0.00% | 0.00% |
| leslie3d/68289 | both96 | 0.735x | 0.00% | 0.00% |
| leslie3d/68289 | large | 1.000x | 0.00% | 0.00% |
| libquantum/64624 | both128 | 1.007x | 0.00% | 0.00% |
| libquantum/64624 | both160 | 1.004x | 0.00% | 0.00% |
| libquantum/64624 | both192 | 0.999x | 0.00% | 0.00% |
| libquantum/64624 | both64 | 0.480x | 0.00% | 0.00% |
| libquantum/64624 | both96 | 0.864x | 0.00% | 0.00% |
| libquantum/64624 | large | 0.994x | 0.00% | 0.00% |
| mcf/12253 | both128 | 0.880x | 0.00% | 0.00% |
| mcf/12253 | both160 | 0.963x | 0.00% | 0.00% |
| mcf/12253 | both192 | 0.972x | 0.00% | 0.00% |
| mcf/12253 | both64 | 0.582x | 0.00% | 0.00% |
| mcf/12253 | both96 | 0.766x | 0.00% | 0.00% |
| mcf/12253 | large | 0.966x | 0.00% | 0.00% |

# Kunminghu V3 register-pressure screening

These are sampled slice results, not full-workload conclusions. Single-use lifetimes include only unaliased INT/FP values allocated and actually freed within the measurement epoch. Consumer uniqueness is determined from the committed path. Last execution attempt approximates operand consumption. Unfinished lifetimes are censored.

Observer schema 2 measures capacity independently of root-cause attribution. Schema 1 measurements undercount capacity shortages and cannot establish a capacity threshold.

| Workload/slice | Variant | INT/FP | IPC | Legacy RegFull | Capacity failure | Standalone capacity block | INT shortage | FP shortage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| GemsFDTD/30385 | fp128 | 224/128 | 4.411 | 0.00% | 38.57% | 38.46% | 0.00% | 38.57% |
| GemsFDTD/30385 | fp160 | 224/160 | 4.393 | 0.00% | 41.91% | 41.83% | 0.00% | 41.91% |
| GemsFDTD/30385 | fp192 | 224/192 | 4.540 | 0.00% | 38.70% | 38.47% | 0.00% | 38.70% |
| GemsFDTD/30385 | fp224 | 224/224 | 4.573 | 0.00% | 34.18% | 33.54% | 0.00% | 34.18% |
| GemsFDTD/30385 | fp320 | 224/320 | 4.547 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| GemsFDTD/30385 | int128 | 128/256 | 4.608 | 0.00% | 34.23% | 34.13% | 34.23% | 0.00% |
| GemsFDTD/30385 | int160 | 160/256 | 4.554 | 0.00% | 32.71% | 32.13% | 0.00% | 32.71% |
| bwaves/37801 | fp128 | 224/128 | 2.542 | 0.00% | 66.08% | 66.07% | 0.00% | 66.08% |
| bwaves/37801 | fp160 | 224/160 | 2.925 | 0.00% | 60.83% | 60.66% | 0.00% | 60.83% |
| bwaves/37801 | fp192 | 224/192 | 3.128 | 0.00% | 57.55% | 57.19% | 0.00% | 57.55% |
| bwaves/37801 | fp224 | 224/224 | 3.376 | 0.00% | 53.46% | 51.59% | 0.00% | 53.46% |
| bwaves/37801 | fp320 | 224/320 | 3.542 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| bwaves/37801 | int128 | 128/256 | 3.480 | 0.00% | 37.31% | 35.30% | 0.00% | 37.31% |
| bwaves/37801 | int160 | 160/256 | 3.480 | 0.00% | 37.31% | 35.30% | 0.00% | 37.31% |
| leslie3d/68289 | fp128 | 224/128 | 3.673 | 0.00% | 47.66% | 47.22% | 0.00% | 47.66% |
| leslie3d/68289 | fp160 | 224/160 | 3.955 | 0.00% | 40.70% | 40.30% | 0.00% | 40.70% |
| leslie3d/68289 | fp192 | 224/192 | 4.217 | 0.00% | 31.56% | 30.44% | 0.16% | 31.40% |
| leslie3d/68289 | fp224 | 224/224 | 4.311 | 0.00% | 18.17% | 15.44% | 0.20% | 17.97% |
| leslie3d/68289 | fp320 | 224/320 | 4.406 | 0.00% | 0.13% | 0.13% | 0.13% | 0.00% |
| leslie3d/68289 | int128 | 128/256 | 4.105 | 0.00% | 34.49% | 33.87% | 33.33% | 3.74% |
| leslie3d/68289 | int160 | 160/256 | 4.337 | 0.00% | 19.61% | 17.25% | 13.61% | 6.00% |

| Run | INT shortage with held single-use | INT with eligible consumer | Mean held INT values | FP shortage with held single-use | FP with eligible consumer | Mean held FP values |
|---|---:|---:|---:|---:|---:|---:|

The overlap fraction counts each shortage cycle once. Register-cycle exposures count each simultaneously held value and can exceed cycle counts. Eligibility assumes perfect knowledge and a fresh destination in the same register class; it does not implement the paper's predictor, shadow banks, version limits, or recovery. Co-occurrence alone is not causal proof of achievable speedup. Capacity A/B changes only register counts and ignores physical area/timing costs.

| Workload/slice | Capacity variant | IPC speedup | RegFull before | RegFull after |
|---|---|---:|---:|---:|

# Register reuse timing results

Single highest-weight checkpoint per workload; paired binary, capacity and instruction window. Uniform shadow storage, not equal-area comparisons.

| Workload | INT/FP | Mode | IPC | Speedup | Reuses | Repairs |
|---|---:|---|---:|---:|---:|---:|
| GemsFDTD | 224/256 | certain | 3.1899 | 0.9939x | 36237 | 0 |
| GemsFDTD | 224/256 | off | 3.2096 | 1.0000x | 0 | 0 |
| GemsFDTD | 224/256 | predicted | 3.4455 | 1.0735x | 42552 | 1023 |
| bwaves | 224/256 | certain | 2.5507 | 1.0339x | 27153 | 0 |
| bwaves | 224/256 | off | 2.4670 | 1.0000x | 0 | 0 |
| bwaves | 224/256 | predicted | 2.5686 | 1.0412x | 43231 | 13 |
| bzip2_combined | 224/256 | certain | 1.1670 | 1.0218x | 39235 | 0 |
| bzip2_combined | 224/256 | off | 1.1421 | 1.0000x | 0 | 0 |
| bzip2_combined | 224/256 | predicted | 1.1555 | 1.0117x | 40282 | 585 |
| gcc_166 | 224/256 | certain | 0.9916 | 0.9868x | 8871 | 0 |
| gcc_166 | 224/256 | off | 1.0049 | 1.0000x | 0 | 0 |
| gcc_166 | 224/256 | predicted | 0.9807 | 0.9759x | 10672 | 643 |
| hmmer_nph3 | 224/256 | certain | 5.0958 | 0.9713x | 31457 | 0 |
| hmmer_nph3 | 224/256 | off | 5.2464 | 1.0000x | 0 | 0 |
| hmmer_nph3 | 224/256 | predicted | 5.0647 | 0.9654x | 35454 | 1 |
| leslie3d | 224/256 | certain | 1.9711 | 0.9569x | 27325 | 0 |
| leslie3d | 224/256 | off | 2.0600 | 1.0000x | 0 | 0 |
| leslie3d | 224/256 | predicted | 2.0177 | 0.9795x | 30817 | 907 |
| libquantum | 224/256 | certain | 4.5477 | 1.0000x | 2 | 0 |
| libquantum | 224/256 | off | 4.5477 | 1.0000x | 0 | 0 |
| libquantum | 224/256 | predicted | 2.4045 | 0.5287x | 9909 | 2512 |
| mcf | 224/256 | certain | 0.3103 | 0.9384x | 81951 | 0 |
| mcf | 224/256 | off | 0.3307 | 1.0000x | 0 | 0 |
| mcf | 224/256 | predicted | 0.3431 | 1.0376x | 81315 | 0 |

Geometric means over these selected slices:

- 224/256 certain: 0.9874x (8 slices)
- 224/256 off: 1.0000x (8 slices)
- 224/256 predicted: 0.9326x (8 slices)

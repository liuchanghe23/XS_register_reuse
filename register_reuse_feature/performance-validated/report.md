# Register reuse timing results

Single highest-weight checkpoint per workload; paired binary, capacity and instruction window. Uniform shadow storage, not equal-area comparisons.

| Workload | INT/FP | Mode | IPC | Speedup | Reuses | Repairs |
|---|---:|---|---:|---:|---:|---:|
| GemsFDTD | 192/208 | certain | 4.5474 | 0.9981x | 361000 | 0 |
| GemsFDTD | 192/208 | off | 4.5559 | 1.0000x | 0 | 0 |
| GemsFDTD | 192/208 | predicted | 4.6131 | 1.0126x | 424781 | 217 |
| GemsFDTD | 224/256 | certain | 4.5474 | 0.9986x | 361000 | 0 |
| GemsFDTD | 224/256 | off | 4.5537 | 1.0000x | 0 | 0 |
| GemsFDTD | 224/256 | predicted | 4.6131 | 1.0131x | 424781 | 217 |
| bwaves | 192/208 | certain | 3.4524 | 1.0411x | 271374 | 0 |
| bwaves | 192/208 | off | 3.3161 | 1.0000x | 0 | 0 |
| bwaves | 192/208 | predicted | 3.3979 | 1.0246x | 431826 | 0 |
| bwaves | 224/256 | certain | 3.5424 | 1.0179x | 271367 | 0 |
| bwaves | 224/256 | off | 3.4800 | 1.0000x | 0 | 0 |
| bwaves | 224/256 | predicted | 3.3979 | 0.9764x | 431826 | 0 |
| bzip2_combined | 192/208 | certain | 1.2154 | 1.0072x | 384679 | 0 |
| bzip2_combined | 192/208 | off | 1.2066 | 1.0000x | 0 | 0 |
| bzip2_combined | 192/208 | predicted | 1.1953 | 0.9906x | 395754 | 1057 |
| bzip2_combined | 224/256 | certain | 1.2118 | 1.0079x | 384510 | 0 |
| bzip2_combined | 224/256 | off | 1.2023 | 1.0000x | 0 | 0 |
| bzip2_combined | 224/256 | predicted | 1.2088 | 1.0054x | 394687 | 1066 |
| gcc_166 | 192/208 | certain | 1.6232 | 1.0159x | 43650 | 0 |
| gcc_166 | 192/208 | off | 1.5977 | 1.0000x | 0 | 0 |
| gcc_166 | 192/208 | predicted | 1.6410 | 1.0271x | 58292 | 555 |
| gcc_166 | 224/256 | certain | 1.6823 | 1.0122x | 44182 | 0 |
| gcc_166 | 224/256 | off | 1.6620 | 1.0000x | 0 | 0 |
| gcc_166 | 224/256 | predicted | 1.6994 | 1.0225x | 58444 | 555 |
| hmmer_nph3 | 192/208 | certain | 6.3478 | 1.0217x | 314449 | 0 |
| hmmer_nph3 | 192/208 | off | 6.2132 | 1.0000x | 0 | 0 |
| hmmer_nph3 | 192/208 | predicted | 6.3264 | 1.0182x | 354438 | 0 |
| hmmer_nph3 | 224/256 | certain | 6.3551 | 1.0064x | 314439 | 0 |
| hmmer_nph3 | 224/256 | off | 6.3150 | 1.0000x | 0 | 0 |
| hmmer_nph3 | 224/256 | predicted | 6.3316 | 1.0026x | 354447 | 0 |
| leslie3d | 192/208 | certain | 4.3508 | 1.0364x | 279406 | 0 |
| leslie3d | 192/208 | off | 4.1978 | 1.0000x | 0 | 0 |
| leslie3d | 192/208 | predicted | 4.3263 | 1.0306x | 301907 | 1014 |
| leslie3d | 224/256 | certain | 4.4078 | 1.0000x | 279405 | 0 |
| leslie3d | 224/256 | off | 4.4077 | 1.0000x | 0 | 0 |
| leslie3d | 224/256 | predicted | 4.3263 | 0.9816x | 301907 | 1014 |
| libquantum | 192/208 | certain | 5.6394 | 1.0024x | 31 | 0 |
| libquantum | 192/208 | off | 5.6262 | 1.0000x | 0 | 0 |
| libquantum | 192/208 | predicted | 4.3478 | 0.7728x | 82263 | 6423 |
| libquantum | 224/256 | certain | 5.6295 | 1.0000x | 34 | 0 |
| libquantum | 224/256 | off | 5.6295 | 1.0000x | 0 | 0 |
| libquantum | 224/256 | predicted | 4.3351 | 0.7701x | 79077 | 6491 |
| mcf | 192/208 | certain | 0.4676 | 1.0235x | 686384 | 0 |
| mcf | 192/208 | off | 0.4568 | 1.0000x | 0 | 0 |
| mcf | 192/208 | predicted | 0.4738 | 1.0373x | 689612 | 0 |
| mcf | 224/256 | certain | 0.4541 | 0.9661x | 701193 | 0 |
| mcf | 224/256 | off | 0.4700 | 1.0000x | 0 | 0 |
| mcf | 224/256 | predicted | 0.4773 | 1.0155x | 694260 | 0 |

Geometric means over these selected slices:

- 192/208 certain: 1.0182x (8 slices)
- 192/208 off: 1.0000x (8 slices)
- 192/208 predicted: 0.9853x (8 slices)
- 224/256 certain: 1.0010x (8 slices)
- 224/256 off: 1.0000x (8 slices)
- 224/256 predicted: 0.9698x (8 slices)

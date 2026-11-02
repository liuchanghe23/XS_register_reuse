# 容量扫描与确定性寄存器复用验证

Plan `e37c5c85366b7d9e`；范围 `both`；状态：**未完整，仅供排查**。
容量运行 11673；复用运行 2334；缺失 0；失败/校验不通过 9。
每片预热 20,000,000 + 测量 20,000,000 指令，NEMU difftest 开启。

## 确定性复用

off/certain 使用相同 feature 二进制、相同容量、切片和指令窗口，显式关闭跨寄存器预测。
workload 内按所选 SimPoint 权重加权 CPI，再计算 off_CPI/certain_CPI；部分覆盖只在所选切片内归一化。
下面是 workload 级比值的等权几何平均，不是官方 SPEC 分数。

| INT/FP | Workloads | 完整 | IPC 变化 |
|---|---:|---|---:|
| 192/208 | 55 | False | +1.235% |
| 224/256 | 55 | True | +0.528% |

| Workload | INT/FP | 配对切片/计划 | 覆盖权重 | IPC 变化 |
|---|---:|---:|---:|---:|
| GemsFDTD | 192/208 | 12/12 | 0.812163 | +5.747% |
| GemsFDTD | 224/256 | 12/12 | 0.812163 | +3.502% |
| astar_biglakes | 192/208 | 4/4 | 0.806285 | +0.532% |
| astar_biglakes | 224/256 | 4/4 | 0.806285 | +0.031% |
| astar_rivers | 192/208 | 4/4 | 0.809343 | +0.539% |
| astar_rivers | 224/256 | 4/4 | 0.809343 | +0.050% |
| bwaves | 192/208 | 3/3 | 0.808140 | +5.209% |
| bwaves | 224/256 | 3/3 | 0.808140 | +0.535% |
| bzip2_chicken | 192/208 | 7/7 | 0.813716 | +0.180% |
| bzip2_chicken | 224/256 | 7/7 | 0.813716 | +0.117% |
| bzip2_combined | 192/208 | 12/12 | 0.815916 | +0.273% |
| bzip2_combined | 224/256 | 12/12 | 0.815916 | +0.074% |
| bzip2_html | 192/208 | 8/8 | 0.820488 | +0.275% |
| bzip2_html | 224/256 | 8/8 | 0.820488 | -0.036% |
| bzip2_liberty | 192/208 | 7/7 | 0.807712 | +0.527% |
| bzip2_liberty | 224/256 | 7/7 | 0.807712 | +0.182% |
| bzip2_program | 192/208 | 11/11 | 0.811499 | +0.453% |
| bzip2_program | 224/256 | 11/11 | 0.811499 | +0.317% |
| bzip2_source | 192/208 | 11/11 | 0.801749 | +0.207% |
| bzip2_source | 224/256 | 11/11 | 0.801749 | +0.154% |
| cactusADM | 192/208 | 2/2 | 0.951362 | +0.907% |
| cactusADM | 224/256 | 2/2 | 0.951362 | -0.017% |
| calculix | 192/208 | 11/11 | 0.818502 | +11.955% |
| calculix | 224/256 | 11/11 | 0.818502 | +6.753% |
| dealII | 192/208 | 10/10 | 0.805056 | +0.584% |
| dealII | 224/256 | 10/10 | 0.805056 | +0.171% |
| gamess_cytosine | 192/208 | 13/13 | 0.809428 | +3.507% |
| gamess_cytosine | 224/256 | 13/13 | 0.809428 | +1.096% |
| gamess_gradient | 192/208 | 13/13 | 0.816288 | +6.139% |
| gamess_gradient | 224/256 | 13/13 | 0.816288 | +1.810% |
| gamess_triazolium | 192/208 | 13/13 | 0.813049 | +6.632% |
| gamess_triazolium | 224/256 | 13/13 | 0.813049 | +2.011% |
| gcc_166 | 192/208 | 9/9 | 0.841906 | +0.377% |
| gcc_166 | 224/256 | 9/9 | 0.841906 | +0.226% |
| gcc_200 | 192/208 | 10/10 | 0.830479 | +0.540% |
| gcc_200 | 224/256 | 10/10 | 0.830479 | +0.366% |
| gcc_cpdecl | 192/208 | 9/9 | 0.810044 | +0.314% |
| gcc_cpdecl | 224/256 | 9/9 | 0.810044 | +0.281% |
| gcc_expr | 192/208 | 9/9 | 0.816558 | +0.159% |
| gcc_expr | 224/256 | 9/9 | 0.816558 | +0.450% |
| gcc_expr2 | 192/208 | 11/11 | 0.827805 | +0.580% |
| gcc_expr2 | 224/256 | 11/11 | 0.827805 | +0.121% |
| gcc_g23 | 192/208 | 9/9 | 0.815219 | +0.210% |
| gcc_g23 | 224/256 | 9/9 | 0.815219 | +0.203% |
| gcc_s04 | 192/208 | 11/11 | 0.823795 | +0.575% |
| gcc_s04 | 224/256 | 11/11 | 0.823795 | +0.401% |
| gcc_scilab | 192/208 | 11/11 | 0.816882 | +0.276% |
| gcc_scilab | 224/256 | 11/11 | 0.816882 | +0.309% |
| gcc_typeck | 192/208 | 9/9 | 0.802595 | +0.305% |
| gcc_typeck | 224/256 | 9/9 | 0.802595 | +0.211% |
| gobmk_13x13 | 192/208 | 10/10 | 0.807535 | +0.936% |
| gobmk_13x13 | 224/256 | 10/10 | 0.807535 | +0.360% |
| gobmk_nngs | 192/208 | 9/9 | 0.823022 | +1.028% |
| gobmk_nngs | 224/256 | 9/9 | 0.823022 | +0.157% |
| gobmk_score2 | 192/208 | 11/11 | 0.817318 | +0.476% |
| gobmk_score2 | 224/256 | 11/11 | 0.817318 | +0.282% |
| gobmk_trevorc | 192/208 | 13/13 | 0.810505 | +0.540% |
| gobmk_trevorc | 224/256 | 13/13 | 0.810505 | +0.352% |
| gobmk_trevord | 192/208 | 11/11 | 0.826228 | +0.653% |
| gobmk_trevord | 224/256 | 11/11 | 0.826228 | +0.248% |
| gromacs | 192/208 | 26/26 | 0.803484 | +0.036% |
| gromacs | 224/256 | 26/26 | 0.803484 | +0.041% |
| h264ref_foreman.baseline | 192/208 | 11/11 | 0.825948 | +2.157% |
| h264ref_foreman.baseline | 224/256 | 11/11 | 0.825948 | +0.373% |
| h264ref_foreman.main | 192/208 | 14/14 | 0.809373 | +1.838% |
| h264ref_foreman.main | 224/256 | 14/14 | 0.809373 | +0.322% |
| h264ref_sss | 192/208 | 13/13 | 0.827950 | +2.193% |
| h264ref_sss | 224/256 | 13/13 | 0.827950 | +0.533% |
| hmmer_nph3 | 192/208 | 4/4 | 0.800178 | +1.858% |
| hmmer_nph3 | 224/256 | 4/4 | 0.800178 | +0.292% |
| hmmer_retro | 192/208 | 10/10 | 0.813433 | +1.600% |
| hmmer_retro | 224/256 | 10/10 | 0.813433 | +0.186% |
| lbm | 192/208 | 4/4 | 0.841062 | +0.055% |
| lbm | 224/256 | 4/4 | 0.841062 | +0.060% |
| leslie3d | 192/208 | 12/12 | 0.810373 | +2.673% |
| leslie3d | 224/256 | 12/12 | 0.810373 | +0.560% |
| libquantum | 192/208 | 9/9 | 0.808054 | +0.546% |
| libquantum | 224/256 | 9/9 | 0.808054 | +0.077% |
| mcf | 192/208 | 8/9 | 0.703468 | +0.145% |
| mcf | 224/256 | 9/9 | 0.841044 | +0.110% |
| milc | 192/208 | 15/15 | 0.815104 | +2.583% |
| milc | 224/256 | 15/15 | 0.815104 | +2.307% |
| namd | 192/208 | 20/20 | 0.815157 | +0.091% |
| namd | 224/256 | 20/20 | 0.815157 | +0.008% |
| omnetpp | 192/208 | 3/3 | 0.809479 | -0.192% |
| omnetpp | 224/256 | 3/3 | 0.809479 | +0.406% |
| perlbench_checkspam | 192/208 | 9/9 | 0.844889 | +0.136% |
| perlbench_checkspam | 224/256 | 9/9 | 0.844889 | +0.075% |
| perlbench_diffmail | 192/208 | 2/2 | 0.818418 | +0.022% |
| perlbench_diffmail | 224/256 | 2/2 | 0.818418 | +0.166% |
| perlbench_splitmail | 192/208 | 4/4 | 0.850668 | -0.054% |
| perlbench_splitmail | 224/256 | 4/4 | 0.850668 | -0.081% |
| povray | 192/208 | 14/14 | 0.830838 | +0.238% |
| povray | 224/256 | 14/14 | 0.830838 | +0.118% |
| sjeng | 192/208 | 8/8 | 0.830691 | +0.535% |
| sjeng | 224/256 | 8/8 | 0.830691 | +0.331% |
| soplex_pds-50 | 192/208 | 14/14 | 0.826817 | -0.226% |
| soplex_pds-50 | 224/256 | 14/14 | 0.826817 | -0.114% |
| soplex_ref | 192/208 | 13/13 | 0.803383 | -5.166% |
| soplex_ref | 224/256 | 13/13 | 0.803383 | -0.138% |
| sphinx3 | 192/208 | 12/12 | 0.811178 | +2.293% |
| sphinx3 | 224/256 | 12/12 | 0.811178 | +1.826% |
| tonto | 192/208 | 15/15 | 0.827537 | +1.250% |
| tonto | 224/256 | 15/15 | 0.827537 | +0.163% |
| wrf | 192/208 | 16/16 | 0.818451 | +1.163% |
| wrf | 224/256 | 16/16 | 0.818451 | +0.195% |
| xalancbmk | 192/208 | 27/27 | 0.805779 | +0.255% |
| xalancbmk | 224/256 | 27/27 | 0.805779 | +0.083% |
| zeusmp | 192/208 | 17/17 | 0.825133 | +2.682% |
| zeusmp | 224/256 | 17/17 | 0.825133 | +0.703% |

## 容量扫描

使用 schema-2 直接容量检查；阻塞比例不等于可回收的性能收益。
workload 级阈值仅纳入同一组切片全部完成的容量点；safe 容量要求该点及所有更大已测点满足损失上限。
默认参照 224/256。只改 INT 时固定 FP=256；只改 FP 时固定 INT=224。

| Workload | 轴 | IPC损失≤1%最小已测容量 | IPC损失≤5%最小已测容量 |
|---|---|---:|---:|
| GemsFDTD | int | 176 | 160 |
| GemsFDTD | float | 224 | 176 |
| astar_biglakes | int | 192 | 128 |
| astar_biglakes | float | 160 | 160 |
| astar_rivers | int | 176 | 128 |
| astar_rivers | float | 160 | 160 |
| bwaves | int | 128 | 128 |
| bwaves | float | 240 | 208 |
| bzip2_chicken | int | 160 | 128 |
| bzip2_chicken | float | 160 | 160 |
| bzip2_combined | int | 160 | 128 |
| bzip2_combined | float | 160 | 160 |
| bzip2_html | int | 176 | 160 |
| bzip2_html | float | 160 | 160 |
| bzip2_liberty | int | 320 | 160 |
| bzip2_liberty | float | 160 | 160 |
| bzip2_program | int | 160 | 128 |
| bzip2_program | float | 160 | 160 |
| bzip2_source | int | 160 | 128 |
| bzip2_source | float | 160 | 160 |
| cactusADM | int | 128 | 128 |
| cactusADM | float | 208 | 176 |
| calculix | int | 128 | 128 |
| calculix | float | 240 | 208 |
| dealII | int | 192 | 160 |
| dealII | float | 176 | 160 |
| gamess_cytosine | int | 224 | 176 |
| gamess_cytosine | float | 176 | 160 |
| gamess_gradient | int | 224 | 192 |
| gamess_gradient | float | 176 | 160 |
| gamess_triazolium | int | 224 | 192 |
| gamess_triazolium | float | 192 | 160 |
| gcc_166 | int | 176 | 128 |
| gcc_166 | float | 160 | 160 |
| gcc_200 | int | 192 | 160 |
| gcc_200 | float | 160 | 160 |
| gcc_cpdecl | int | 160 | 128 |
| gcc_cpdecl | float | 160 | 160 |
| gcc_expr | int | 160 | 128 |
| gcc_expr | float | 160 | 160 |
| gcc_expr2 | int | 176 | 128 |
| gcc_expr2 | float | 160 | 160 |
| gcc_g23 | int | 160 | 128 |
| gcc_g23 | float | 160 | 160 |
| gcc_s04 | int | 192 | 128 |
| gcc_s04 | float | 160 | 160 |
| gcc_scilab | int | 160 | 128 |
| gcc_scilab | float | 160 | 160 |
| gcc_typeck | int | 160 | 128 |
| gcc_typeck | float | 160 | 160 |
| gobmk_13x13 | int | 192 | 128 |
| gobmk_13x13 | float | 160 | 160 |
| gobmk_nngs | int | 192 | 128 |
| gobmk_nngs | float | 160 | 160 |
| gobmk_score2 | int | 160 | 128 |
| gobmk_score2 | float | 160 | 160 |
| gobmk_trevorc | int | 176 | 128 |
| gobmk_trevorc | float | 160 | 160 |
| gobmk_trevord | int | 176 | 128 |
| gobmk_trevord | float | 160 | 160 |
| gromacs | int | 128 | 128 |
| gromacs | float | 192 | 176 |
| h264ref_foreman.baseline | int | 208 | 176 |
| h264ref_foreman.baseline | float | 160 | 160 |
| h264ref_foreman.main | int | 208 | 160 |
| h264ref_foreman.main | float | 160 | 160 |
| h264ref_sss | int | 208 | 176 |
| h264ref_sss | float | 160 | 160 |
| hmmer_nph3 | int | 208 | 176 |
| hmmer_nph3 | float | 160 | 160 |
| hmmer_retro | int | 208 | 176 |
| hmmer_retro | float | 160 | 160 |
| lbm | int | 128 | 128 |
| lbm | float | 160 | 160 |
| leslie3d | int | 160 | 128 |
| leslie3d | float | 240 | 176 |
| libquantum | int | 176 | 160 |
| libquantum | float | 160 | 160 |
| mcf | int | 192 | 192 |
| mcf | float | 176 | 176 |
| milc | int | 128 | 128 |
| milc | float | 240 | 176 |
| namd | int | 128 | 128 |
| namd | float | 176 | 160 |
| omnetpp | int | 192 | 160 |
| omnetpp | float | 160 | 160 |
| perlbench_checkspam | int | 160 | 128 |
| perlbench_checkspam | float | 160 | 160 |
| perlbench_diffmail | int | 160 | 128 |
| perlbench_diffmail | float | 160 | 160 |
| perlbench_splitmail | int | 128 | 128 |
| perlbench_splitmail | float | 160 | 160 |
| povray | int | 160 | 128 |
| povray | float | 176 | 160 |
| sjeng | int | 192 | 160 |
| sjeng | float | 160 | 160 |
| soplex_pds-50 | int | 160 | 128 |
| soplex_pds-50 | float | 160 | 160 |
| soplex_ref | int | 128 | 128 |
| soplex_ref | float | 160 | 160 |
| sphinx3 | int | 128 | 128 |
| sphinx3 | float | 192 | 160 |
| tonto | int | 192 | 160 |
| tonto | float | 192 | 160 |
| wrf | int | 160 | 128 |
| wrf | float | 208 | 176 |
| xalancbmk | int | 160 | 128 |
| xalancbmk | float | 160 | 160 |
| zeusmp | int | 160 | 128 |
| zeusmp | float | 240 | 176 |

`capacity_workload_weighted.csv`：容量和直接阻塞统计；
`reuse_pairs.csv`、`reuse_workload_weighted.csv`：同容量配对收益；
`reuse_retained_vs_default.csv`：收紧容量 certain 相对默认容量 OFF 的性能保留；
`validation.json`：缺失/失败清单和实验身份。

模型仍为统一 shadow 存储，无等面积、频率、能耗或逐端口争用结论。

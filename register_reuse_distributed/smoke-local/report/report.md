# 容量扫描与确定性寄存器复用验证

Plan `f4267c536222599d`；范围 `both`；状态：**完整**。
容量运行 4；复用运行 4；缺失 0；失败/校验不通过 0。
每片预热 10,000 + 测量 20,000 指令，NEMU difftest 开启。

## 确定性复用

off/certain 使用相同 feature 二进制、相同容量、切片和指令窗口，显式关闭跨寄存器预测。
workload 内按所选 SimPoint 权重加权 CPI，再计算 off_CPI/certain_CPI；部分覆盖只在所选切片内归一化。
下面是 workload 级比值的等权几何平均，不是官方 SPEC 分数。

| INT/FP | Workloads | 完整 | IPC 变化 |
|---|---:|---|---:|
| 192/208 | 1 | True | +3.649% |
| 224/256 | 1 | True | +2.311% |

| Workload | INT/FP | 配对切片/计划 | 覆盖权重 | IPC 变化 |
|---|---:|---:|---:|---:|
| bwaves | 192/208 | 1/1 | 0.706046 | +3.649% |
| bwaves | 224/256 | 1/1 | 0.706046 | +2.311% |

## 容量扫描

使用 schema-2 直接容量检查；阻塞比例不等于可回收的性能收益。
workload 级阈值仅纳入同一组切片全部完成的容量点；safe 容量要求该点及所有更大已测点满足损失上限。
默认参照 224/256。只改 INT 时固定 FP=256；只改 FP 时固定 INT=224。

| Workload | 轴 | IPC损失≤1%最小已测容量 | IPC损失≤5%最小已测容量 |
|---|---|---:|---:|
| bwaves | int | 192 | 192 |
| bwaves | float | 208 | 208 |

`capacity_workload_weighted.csv`：容量和直接阻塞统计；
`reuse_pairs.csv`、`reuse_workload_weighted.csv`：同容量配对收益；
`reuse_retained_vs_default.csv`：收紧容量 certain 相对默认容量 OFF 的性能保留；
`validation.json`：缺失/失败清单和实验身份。

模型仍为统一 shadow 存储，无等面积、频率、能耗或逐端口争用结论。

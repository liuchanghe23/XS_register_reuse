# 大规模 Kunminghu V3 寄存器容量测试

启动入口是 `run_large.sh`，参数文件是同目录的 `large_test.json`。只使用 Python 标准库；长测和自动汇总不依赖绘图库。

## 默认配置

| 项目 | 默认值 |
|---|---|
| CPU 配置 | `GEM5/configs/example/kmhv3.py` |
| checkpoint | 工作区 `zstd-checkpoint-0-0-0` |
| workload | 全部 55 个 |
| 切片选择 | 每个 workload 按 SimPoint 权重降序选到至少 80% |
| 本地切片数量 | 584 |
| profile | `threshold`，20 个容量点，总计 11680 次模拟 |
| 单片指令区间 | 预热 20M + 测量 20M，`maxinsts=40M` |
| 并发 | 16，可通过 `--jobs` 调整 |
| 单次超时 | 21600 秒（6 小时），可通过 `--timeout` 调整 |
| 正确性检查 | NEMU difftest 开启 |
| 观测 | schema 2 直接容量检查、INT/FP 完整生命周期单消费者统计 |
| 详细区间 CSV | 默认关闭；累计统计仍保留，可通过 `--trace` 开启 |
| 输出目录 | `register_reuse_analysis/large-capacity-coverage80` |

## 启动和查看进度

```bash
cd /nfs/home/liuchanghe/register_reuse

# 查看实际切片数、容量点和命令；不启动模拟。
./register_reuse_analysis/run_large.sh --dry-run

# 长时间运行。日志有已完成/总任务数以及每个任务的退出状态。
nohup ./register_reuse_analysis/run_large.sh \
  > register_reuse_analysis/large-test.log 2>&1 &

# 查看进度。
tail -f register_reuse_analysis/large-test.log
```

当前构建产物为 `build/RISCV/gem5.opt`。若缺少，先运行 `./register_reuse_analysis/build.sh`。普通 `.zstd` 切片使用内置 restorer，脚本不传 `--raw-cpt` 或 `--gcpt-restorer`。NEMU 默认路径已写入配置；设置 `GCBV_REF_SO` 可以覆盖它。

## 三种规模

| profile | 容量点 | 80% 权重覆盖下的运行数量 |
|---|---:|---:|
| `baseline` | 仅默认 224 INT / 256 FP | 584 |
| `screen` | 默认、512/512、192/256、224/208 | 2336 |
| `threshold` | 默认和高容量参照、INT 与 FP 分别扫描、192/208 组合 | 11680 |

如果先进行较小规模的大样本确认：

```bash
nohup ./register_reuse_analysis/run_large.sh \
  --profile screen --jobs 8 \
  --out register_reuse_analysis/large-screen-coverage80 \
  > register_reuse_analysis/large-screen.log 2>&1 &
```

`threshold` 的 20 个容量点：

- 参照：224/256、512/512。
- 只改 INT、固定 FP=256：128、160、176、192、208、256、288、320。
- 只改 FP、固定 INT=224：160、176、192、208、224、240、272、288、320。
- 联合缩减：INT=192、FP=208。

全切片覆盖使用 `--coverage 1`，明确选取全部 1169 个切片，不因权重的小数舍入提前停止；完整阈值 profile 共 23380 次模拟：

```bash
nohup ./register_reuse_analysis/run_large.sh \
  --coverage 1 --jobs 16 \
  --out register_reuse_analysis/large-capacity-all \
  > register_reuse_analysis/large-all.log 2>&1 &
```

## 续跑与修改参数

重新执行相同命令即可续跑。配置和二进制一致的已成功任务会跳过，失败或未完成任务会重跑。并发数和超时可以改变，例如：

```bash
nohup ./register_reuse_analysis/run_large.sh --jobs 8 --timeout 28800 \
  >> register_reuse_analysis/large-test.log 2>&1 &
```

启动器对输出目录加进程锁，同一目录不能同时运行两个启动器。输出中保存实验身份，包括二进制 SHA256、NEMU reference SHA256、切片和权重、容量点、指令区间；这些内容改变时应使用新的 `--out`，脚本会在启动模拟前检查。

配置文件中的路径相对于 JSON 文件的位置解释；命令行 `--out` 相对于当前工作目录解释。调整大部分参数可直接使用命令行：

```bash
./register_reuse_analysis/run_large.sh \
  --workloads gcc_166,bwaves --coverage 0.8 \
  --warmup 20000000 --measure 20000000 --jobs 4 \
  --out register_reuse_analysis/large-gcc-bwaves
```

## 输出

完成后自动执行统计和容量报告。失败任务不会阻止其他模拟继续运行；脚本最终保留非零状态，汇总中列出失败，续跑会重试。

- `launch-plan.json`：解析后的配置、完整命令、584 个已选切片及权重。
- `experiment-identity.json`：续跑一致性检查。
- `launch-status.json`：模拟、分析退出状态。
- `manifest.json`：全部模拟任务及其精确命令。
- `workload/point/variant/`：每次模拟的 `run.json`、`run.log`、`config.ini/json`、`stats.txt`。
- `per_run.csv`、`comparison.csv`、`summary.json`：逐切片统计与相对默认配置的比较。
- `workload_weighted.csv`：每个 workload、每个容量点按 SimPoint 权重加权的 CPI/IPC、直接容量失败率、独立容量阻塞率、INT/FP 分类不足率。百分比按加权每指令周期除以加权 CPI 计算。
- `capacity-summary/report.md`、`all_points.csv`、`thresholds.csv`：逐切片容量阈值。阈值是已测点范围，1%/5% IPC 损失与容量阻塞率分别计算。
- `analysis.log`、`capacity-analysis.log`：汇总详细日志。

部分覆盖时只在所选切片内归一化，实际覆盖权重会保留。`selected_slice_aggregate.csv` 是所选切片的等权几何平均，不能视为 SimPoint 加权结果或官方 SPEC 分数；大规模分析优先使用 `workload_weighted.csv` 和配对的逐切片数据。只有所有相关容量点覆盖同一组切片时，才能将其直接用于 workload 级阈值比较。

只重新分析而不启动模拟：

```bash
./register_reuse_analysis/run_large.sh --analyze-only

# 自定义输出目录：
./register_reuse_analysis/run_large.sh --analyze-only \
  --out register_reuse_analysis/large-screen-coverage80
```

短跑验证可用：

```bash
./register_reuse_analysis/run_large.sh --profile baseline \
  --workloads bwaves --top 1 --warmup 10000 --measure 20000 \
  --jobs 1 --timeout 300 \
  --out register_reuse_analysis/large-launcher-smoke
```

该路径已完成真实切片验证，启动、difftest、统计及自动报告均正常；再次运行会跳过已有成功模拟。

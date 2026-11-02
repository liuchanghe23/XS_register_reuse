# 多服务器容量扫描与确定性复用验证

已生成可直接启动的计划：`batch-6servers/plan.json` 和 `batch-6servers/server-00.sh` 至 `server-05.sh`。这里只生成计划，不会自动登录或启动其他服务器。

## 规模与 12 小时预算

默认保留原长测口径：55 个 workload、各自至少 80% SimPoint 权重覆盖、584 个切片，每片预热 20M + 测量 20M 指令，开启 NEMU difftest。

| 实验 | 配置 | 运行次数 |
|---|---|---:|
| 容量扫描 | 原 threshold profile，20 个 INT/FP 容量点 | 11,680 |
| 确定性复用 | 224/256 和 192/208 两种容量，各跑 off/certain | 2,336 |
| 合计 | 同一份计划同时分发两类任务 | 14,016 |

容量扫描使用原 `build/RISCV/gem5.opt` 和 schema-2 被动观察器；确定性复用的 off/certain 都使用 `register_reuse_feature/build/RISCV/gem5.opt`，显式指定 `regReusePrediction=False`。不同二进制的结果不作为复用收益的配对基线。

单次 800 秒、每台 64 并发的估算如下，按最慢分片的完整执行批次计算：

| 服务器数 | 每台最多运行数 | 预计耗时 | 单次耗时增加 25% 后 |
|---:|---:|---:|---:|
| 4 | 3,504 | 12.22 小时 | 15.28 小时 |
| 5 | 2,804 | 9.78 小时 | 12.22 小时 |
| **6** | **2,336** | **8.22 小时** | **10.28 小时** |
| 7 | 2,003 | 7.11 小时 | 8.89 小时 |
| 8 | 1,752 | 6.22 小时 | 7.78 小时 |

建议 **6 台，每台 64 并发**。如果希望把两类实验放到不同服务器，容量扫描 5 台、复用验证 1 台，也各为约 8.22 小时、含余量约 10.28 小时。256 个逻辑核不按 256 个独立物理核估算；64 并发下的实际单次耗时仍需观察。800 秒若是在低并发测得，带宽、内存和 I/O 竞争可能使它增加。12 小时是预算，不是完成保证。

预算按全量任务计算，没有扣除可导入的旧结果。正式计划已导入当前旧容量扫描中通过严格校验的 160 个成功运行，不会修改旧目录。

## 直接使用已生成的六台计划（共享 NFS）

以下命令都在 `/nfs/home/liuchanghe/register_reuse` 执行。每台服务器只启动自己的一个编号；编号从 0 开始，不要在多台重复启动同一编号。

第 1 台：

```bash
cd /nfs/home/liuchanghe/register_reuse
nohup ./register_reuse_distributed/batch-6servers/server-00.sh \
  > register_reuse_distributed/batch-6servers/server-00.log 2>&1 &
```

其他五台分别执行相同命令，将脚本和日志的 `00` 同时替换为 `01`、`02`、`03`、`04`、`05`。六个脚本共用同一份计划，各自只跑自己的任务。每个 off/certain 配对固定在同一分片。

查看所有服务器的进度：

```bash
python3 register_reuse_distributed/experiment.py status \
  --plan register_reuse_distributed/batch-6servers/plan.json

tail -f register_reuse_distributed/batch-6servers/server-00.log
```

`status` 显示完成、待运行、失败和历史运行耗时；worker 每分钟更新心跳。强制断电等情况可能留下 `running` 记录，是否仍活跃应结合 `shards/XX.json` 的心跳判断。

结束后汇总：

```bash
python3 register_reuse_distributed/experiment.py report \
  --plan register_reuse_distributed/batch-6servers/plan.json
```

输出在 `batch-6servers/report/`。缺少任务或校验失败时，汇总会退出非零并将报告标记为未完整。中途也可以汇总，用于排查。

## 自定义服务器数量与实验范围

重新生成另一份计划，例如 8 台：

```bash
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/batch-8servers \
  --servers 8 --jobs 64
```

生成计划时会打印任务量、每台负载和预算。`--dry-run` 只计算，不生成文件或启动模拟。服务器数、指令窗口、覆盖率或实验配置改变后使用新的 `--out`；不要编辑 `plan.json`。计划校验和可防止各台使用不一致的分片。

可选范围：

```bash
# 四个容量点的初筛；仍包含两种容量的确定性 A/B。
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/batch-screen \
  --servers 2 --jobs 64 --capacity-profile screen

# 只生成容量扫描：5 台。
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/capacity-5servers \
  --suite capacity --servers 5 --jobs 64

# 只生成确定性复用验证：1 台。
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/reuse-1server \
  --suite reuse --servers 1 --jobs 64

# 复用容量可扩展，例如加入单类容量点；每点都自动生成 OFF/certain。
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/reuse-extra \
  --suite reuse --servers 2 --jobs 64 \
  --reuse-points baseline:224:256,int192:192:256,fp208:224:208,mixed192_208:192:208
```

公共选择参数为 `--workloads mcf,bwaves`、`--coverage 0.8`、`--top 1`、`--warmup`、`--measure`。`--top` 替代覆盖率；`--coverage 1` 明确包含所有切片。默认单次超时 7200 秒，可通过 `--timeout` 调整。

也提供单独入口，使用同一计划和分片：

```bash
./register_reuse_distributed/run_capacity.sh \
  --plan register_reuse_distributed/batch-6servers/plan.json --shard-id 0
./register_reuse_distributed/run_deterministic.sh \
  --plan register_reuse_distributed/batch-6servers/plan.json --shard-id 0
```

同一分片的两个入口应先后执行；完整的 `server-XX.sh` 默认两类都跑。每个分片有进程锁，每个任务另有锁，避免重复覆盖结果。

## 停止、续跑和复用旧结果

在运行对应分片的服务器上终止，例如编号 0：

```bash
python3 register_reuse_distributed/experiment.py stop \
  --plan register_reuse_distributed/batch-6servers/plan.json --shard-id 0
```

脚本校验服务器、PID 和分片身份后发送 SIGTERM；worker 停止派发，终止活跃 GEM5 进程组并记录 `interrupted`。也可直接对 worker PID 发送 SIGTERM。不要只杀 GEM5 子进程，否则 worker 会继续派发。

续跑时重复原 `server-XX.sh` 命令即可；成功运行会重新校验配置和统计后跳过，失败/超时/中断任务会重跑。`--jobs 48`、`--timeout 10800` 可直接附在启动脚本后，不改变实验身份。

在所有新分片尚未启动或已停止时，导入原长测目录的成功结果：

```bash
python3 register_reuse_distributed/experiment.py import-capacity \
  --plan register_reuse_distributed/batch-6servers/plan.json \
  --source register_reuse_analysis/large-capacity-coverage80 --dry-run

# 去掉 --dry-run 才复制匹配结果；已存在的新结果会跳过。
```

只导入二进制、reference、checkpoint 元数据、容量、指令窗口、observer schema 和实际统计都匹配的成功任务。只复制必要日志、配置和统计，不改旧目录。原扫描应先停止，避免继续占用相同服务器的预算。

## 不共享目录的服务器

推荐共享 NFS。独立磁盘也支持：把**同一份** `plan.json`、对应 `server-XX.sh`、脚本、GEM5 配置/Python 依赖及两份二进制放到各服务器，checkpoint 与 reference 必须可访问。不要各台独立生成计划。

```bash
REGISTER_REUSE_WORKSPACE=/local/register_reuse \
  /local/batch-6servers/server-00.sh \
  --checkpoints /data/checkpoints \
  --reference /data/riscv64-nemu-interpreter-so
```

可用 `--capacity-gem5`、`--reuse-gem5` 指向本地二进制。worker 启动前检查二进制、reference、checkpoint 元数据和配置依赖的 SHA256，与中央计划一致才运行。输出位于各服务器本地计划旁的 `results/`。

跑完将每台 `results/` 的内容合并回同一份中央计划旁的 `results/`，例如在中央服务器执行：

```bash
rsync -a serverA:/local/batch-6servers/results/ \
  register_reuse_distributed/batch-6servers/results/
```

各分片任务互斥，目录不会互相覆盖；然后在中央运行 `report`。汇总按实际收集目录定位统计，不依赖另一台服务器的绝对输出路径。两份 binary 各约 1 GB；各台必须有对应的运行时依赖。

## 汇总口径与输出

- `capacity_per_run.csv`：直接容量不足、单消费者生命周期等逐片数据。
- `capacity_workload_weighted.csv`：按 SimPoint 权重加权的 CPI、IPC 和容量阻塞率。
- `capacity_workload_thresholds.csv`：workload 级 1%/5% IPC 损失及直接阻塞阈值；只用相同切片集完整覆盖的点。
- `reuse_pairs.csv`：每个切片、每种容量的 off/certain 收益与关键复用计数。
- `reuse_workload_weighted.csv`：同容量、配对切片上的加权收益与覆盖率。
- `reuse_retained_vs_default.csv`：192/208 certain 相对 224/256 OFF 的性能保留，回答缩容后能否维持默认性能。
- `validation.json`：缺失/失败列表、完整状态、SHA256、workload 级收益的几何平均。
- `report.md`：可读汇总。

只对成功配对的相同切片计算收益，不把两边不同的已完成切片集合直接比较。部分覆盖显式报告 selected_weight；总体为 workload 等权几何平均，不是官方 SPEC 分数。相同容量比较仍不代表相同面积；当前均匀 shadow 模型未建立 SRAM、端口、频率或能耗成本。

## 验证脚本

```bash
python3 -m unittest discover -s register_reuse_distributed -p 'test_*.py' -v
python3 -m unittest discover -s register_reuse_analysis -p 'test_*.py' -v

# 小规模真实切片预检：8 个任务，不启动长测。
python3 register_reuse_distributed/experiment.py plan \
  --out register_reuse_distributed/my-smoke \
  --servers 1 --jobs 2 --workloads bwaves --top 1 \
  --capacity-profile screen --warmup 10000 --measure 20000
./register_reuse_distributed/my-smoke/server-00.sh
python3 register_reuse_distributed/experiment.py report \
  --plan register_reuse_distributed/my-smoke/plan.json
```

工作区 `smoke-local/` 已完成上述 8 个真实切片预检；全部通过 difftest、配置与测量窗口验证，重复运行全部跳过，汇总标记完整。

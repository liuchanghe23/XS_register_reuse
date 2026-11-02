# 昆明湖 V3 单消费者寄存器占用与容量阈值实验

**统计修正（schema 2）：早期 `results-screen-*` 使用的 RegFull 归因统计会把寄存器容量不足归因到 ROB/LSQ 头部等待，因此“RegFull=0”不能证明没有容量压力。容量阈值以 `capacity-*` 目录和 `schemaVersion=2` 的直接 `canRename()` 检查为准。早期单消费者生命周期比例仍可参考，但不足周期与其交集并不完整。**

## 大规模测试入口

已准备好 [run_large.sh](run_large.sh)、[large_test.json](large_test.json) 和 [大规模运行说明](LARGE_TEST.md)。默认是 55 个 workload、80% SimPoint 权重覆盖（584 个切片）、20 个容量点、预热 20M + 测量 20M、16 并发，共 11680 次模拟，结束后自动汇总。

```bash
./register_reuse_analysis/run_large.sh --dry-run
nohup ./register_reuse_analysis/run_large.sh > register_reuse_analysis/large-test.log 2>&1 &
```

更小的四容量点大样本配置用 `--profile screen`，并指定新的 `--out`；完整细节、续跑和结果路径见 LARGE_TEST.md。

## 已完成结果

已完成 121 组百万指令容量实验，详见 [capacity-summary/findings.md](capacity-summary/findings.md)、[完整逐点报告](capacity-summary/report.md) 和 [单类容量曲线](capacity-summary/separate_capacity.png)。所有运行的指令数、二进制 SHA256、状态和时序开关验证保存在 [experiment-validation.json](capacity-summary/experiment-validation.json)。

复算当前完整汇总（这些目录使用同一二进制和指令区间）：

```bash
register_reuse_analysis/.venv-plot/bin/python \
  register_reuse_analysis/capacity_report.py \
  register_reuse_analysis/capacity-*-1m \
  --out register_reuse_analysis/capacity-summary --plot
```

## 容量扫描

```bash
cd /nfs/home/liuchanghe/register_reuse
./register_reuse_analysis/build.sh

# 第一阶段：8 个 workload，各一个最高权重切片，7 种配置，56 次模拟。
python3 register_reuse_analysis/sweep.py --axis joint \
  --counts 192,160,128,96,64 --high 512 \
  --warmup 1000000 --measure 1000000 --jobs 12 --no-trace \
  --out register_reuse_analysis/capacity-joint-1m

# 第二阶段：分别只扫描 INT 或 FP，保持另一类为默认值。
python3 register_reuse_analysis/sweep.py --axis int \
  --counts 192,176,160,144,128 --warmup 1000000 --measure 1000000 \
  --jobs 12 --no-trace --out register_reuse_analysis/capacity-int-1m
python3 register_reuse_analysis/sweep.py --axis float \
  --counts 256,240,224,208,192,176,160 --warmup 1000000 --measure 1000000 \
  --jobs 12 --no-trace --out register_reuse_analysis/capacity-fp-1m

# 指定任意少量配置进行精查；省略 --no-trace 会保存区间 CSV。
python3 register_reuse_analysis/run.py --workloads bwaves \
  --reg-points baseline:224:256,fp224:224:224,fp192:224:192 \
  --warmup 1000000 --measure 1000000 --jobs 3 \
  --out register_reuse_analysis/capacity-bwaves-refine
```

`sweep.py` 完成模拟后会自动调用 `analyze.py`。`--axis joint` 同时改变 INT/FP，`int` 固定 FP=256，`float` 固定 INT=224；512/512 作为高容量参照。`--workloads`、`--suite`、`--coverage`、`--timeout` 等选项与 `run.py` 相同。`--no-trace` 只关闭详细区间输出，保留单消费者及容量累计统计。

合并多组相同二进制、相同指令区间的扫描并生成阈值报告：

```bash
python3 register_reuse_analysis/capacity_report.py \
  register_reuse_analysis/capacity-joint-1m \
  register_reuse_analysis/capacity-int-1m \
  register_reuse_analysis/capacity-fp-1m \
  --out register_reuse_analysis/capacity-summary

# 可选绘图依赖仅安装在 .venv-plot，不影响构建环境。
register_reuse_analysis/.venv-plot/bin/python \
  register_reuse_analysis/capacity_report.py \
  register_reuse_analysis/capacity-joint-1m \
  --out register_reuse_analysis/capacity-summary --plot
```

阈值定义：一是独立容量阻塞占总周期达到 1% 的容量范围；二是相对默认配置 IPC 损失达到 1%/5% 的容量范围。两者独立报告。`minimum_safe` 要求一个点及所有更大已测点都在性能损失上限内，避免把不单调曲线中的一个偶然点误报成安全阈值。仅有离散采样时报告采样点/区间，不宣称一个精确且适用于所有程序的硬件阈值。失败任务、二进制或窗口不一致、重复配置结果不一致均不会被静默混入。


使用本工作区的 XS-GEM5 `configs/example/kmhv3.py`，回答两个独立问题：寄存器容量是否限制重命名，以及这些停顿发生时是否有单消费者值已经被使用、却仍占着物理寄存器。新增观测参数默认为关闭，不实现复用，也不改变分配、释放、执行和恢复行为。

## 运行

```bash
cd /nfs/home/liuchanghe/register_reuse
./register_reuse_analysis/build.sh

# 初筛：8 个 workload，各选权重最大的一个切片；每个切片比较默认容量与大容量。
python3 register_reuse_analysis/run.py \
  --out register_reuse_analysis/results-screen \
  --warmup 1000000 --measure 2000000 --jobs 4
python3 register_reuse_analysis/analyze.py register_reuse_analysis/results-screen

# 正式筛查：55 个 workload，按权重从高到低选择到至少 80% 覆盖率。
# 每个切片预热 20M、统计 20M 指令；规模较大，可由用户长时间运行。
python3 register_reuse_analysis/run.py \
  --suite all --coverage 0.8 \
  --warmup 20000000 --measure 20000000 --jobs 8 \
  --out register_reuse_analysis/results-coverage80
python3 register_reuse_analysis/analyze.py register_reuse_analysis/results-coverage80

# 全部 1169 个切片：用 --suite all --coverage 1 替换上面的选择参数。
# 单独确认瓶颈类型，可用 --variants baseline,large-int,large-fp,large。
# 仅跑一个 workload，可用 --workloads mcf；也可用逗号列出多个名字。
```

默认 `baseline` 使用 kmhv3.py 原始配置：224 个整数、256 个浮点物理寄存器。`large` 只把这两个数量改为 1024；`large-int`、`large-fp` 只增加对应一类。`small`、`small-int`、`small-fp` 默认把对应容量降到 96（可用 `--small-regs` 修改），只用于制造容量敏感性，不用于声称 V3 的真实参数。大容量实验用于隔离容量瓶颈，不计面积、频率和访问延迟成本，因此其 IPC 变化不是论文方案可直接获得的收益。

程序默认开启 difftest，优先采用环境变量 `GCBV_REF_SO`，否则使用 `/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so`。普通 `.zstd` 切片使用自带 restorer，不传 `--raw-cpt` 或 `--gcpt-restorer`。构建脚本在缺少 DRAMsim3 时链接服务器已有的 `/nfs/home/share/gem5_ci/DRAMsim3`，不会修改共享依赖。构建产物位于工作区 `build/RISCV/gem5.opt`。

`--dry-run` 只显示命令。成功且配置、二进制 SHA256 一致的任务会跳过，可以重新执行同一命令续跑；配置或二进制改变后，请使用新的 `--out`。超时或失败任务会重跑，完整日志保存在每次运行目录的 `run.log`。只有正常达到指令上限且统计完整的结果会纳入分析。默认单次超时两小时，可用 `--timeout` 修改。

## 统计口径

- `system.cpu.rename.stallEvents::RegFull` 是原模型的停顿周期统计，不能解释成“free list 为零”。`canRename()` 对 INT/FP/Vector/RMisc 至少要求保留一个 renameWidth（默认 8）的余量；前面没有等待指令时也可能产生资源检查失败。
- schema 2 的 `system.cpu.regPressure.demandStallCycles` 直接记录有非 squash 等待指令且 `canRename()` 容量检查失败的周期，独立于原模型的根因归类。`standaloneStallCycles` 为其中没有下游显式 `blockRename` 的周期，`otherBlockedStallCycles` 为同时有下游阻塞的周期；两者之和等于 demandStallCycles。`shortageCycles::{int,float,vector,misc}` 区分不足类别；`standaloneShortageCycles` 为无显式其他阻塞的分类版本；同周期多个类别不足时可以重叠。`freeAtShortage / shortageCycles` 为不足时平均剩余数量。无其他显式阻塞不等于可以无条件回收这些周期，实际性能影响由相同区间的容量 A/B 确定。
- 只跟踪在当前统计窗口内新分配、生产者已提交、并最终实际释放的 INT/FP 物理值。预热末尾 reset 时丢弃跨窗口值；测量结束仍未释放的值计入 `liveValues`，不强行归类。
- 消费者数量按已提交路径统计，同一条动态指令重复读取同一个物理值只算一个消费者。错误路径指令不算消费者。正常释放前，所有正确路径消费者应已提交，因此能区分零、一、多个消费者。
- 任意时刻发生过寄存器别名共享的值（move elimination 等，包括随后被 squash 的别名）保守地归入 `aliasedValues`，不混入单消费者样本。单消费者比例的分母是 `unaliasedValues`；这是物理值的保守子集，不直接等于论文的全部架构值比例。
- store 拆分会移除父指令的数据源，因此在 rename 后保存原始源寄存器，并把 STD 的执行时间回传父指令。只在父指令提交时统计一次消费者。最后一次 Execute 作为操作数被使用的近似时间；它不是逐端口的精确读时刻，也没有执行重放安全性的证明。无 Execute 的指令使用提交时刻作保守替代。
- `eligibleSingleValues` 要求唯一消费者真正新分配了同类型目的物理寄存器；`selfRedefSingleValues` 进一步要求重定义生产者的同一架构寄存器。跨类型消费和没有目的寄存器的 store 不计入可复用候选。
- 在上述完整生命周期样本内，从唯一消费者最后执行到源物理寄存器实际释放，称为读后占用区间。`singleHoldCycles` 是这些区间的寄存器周期之和。
- `singleStallExposure` 只累加该值的读后占用区间与同类型 RegFull 周期的交集。同周期有多个值时会累计多次，**不能直接作为停顿周期占比**。除以该类型不足周期数，得到不足时平均有多少个已使用的单消费者值仍在占位。
- 可选 `reg-pressure.csv` 只输出压缩的不足周期区间，以及与不足重叠且已完成分类的单消费者区间。分析器按时间扫描合并，得到“至少存在一个已使用的单消费者值”的不足周期占比，不重复计算同一个周期；还分别统计 eligible 和 self-redef 子集，并与在线累计值校验。

完美获知已提交路径、已完成生命周期的统计，不能直接代表在线单消费者预测器能识别多少机会。未完成生命周期会低估覆盖；忽略预测准确率、版本上限、shadow bank 容量等又会使候选集合比实际可利用的集合乐观。结果应作为共现与容量敏感性的证据，不将全部 RegFull 因果归给单消费者占用。

## 输出与复核

每个任务都有 `run.json`（精确命令、权重、时间、退出状态、二进制 SHA256 和基础提交号）、`config.ini`、`config.json`、`stats.txt`、`reg-pressure.csv`、`run.log`。批次根目录还保存 manifest、源码 diff 和新增观察器源码快照。

分析器读取最后一个完整的统计块（预热后），并验证指令量、消费者分类恒等式、CSV 与 stats 的周期及曝光量一致。输出 `per_run.csv`、`comparison.csv`、`workload_weighted.csv`、`summary.json`、`report.md`。未完成或失败任务单独列出。预热、测量指令数可有流水线批次造成的少量偏差，以实际 simInsts 为准。

每个 workload 的切片权重来自 `cluster-0-0.json`。部分覆盖时只在已选切片内部归一化，并显式输出 selected_weight；不会把一个高权重短切片冒充整个 workload。加权 CPI 按指令份额加权，停顿比例通过加权每指令停顿周期除以加权 CPI 得到，不对 IPC 或百分比直接做不正确的算术平均。

```bash
# 离线统计的边界、去重、epoch 隔离与最后统计块测试
python3 -m unittest discover -s register_reuse_analysis -p 'test_*.py' -v

# 观测开关的时间一致性：使用单独目录，和完全相同的 profile 开启任务比较。
python3 register_reuse_analysis/run.py --workloads mcf --variants baseline \
  --warmup 100000 --measure 200000 --no-profile \
  --out register_reuse_analysis/validation-off
```

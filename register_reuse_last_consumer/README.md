# 最后消费者扩展的应用空间筛查

本实验回答：对于“重定义自身且同时读取旧值”的普通标量指令，如果允许此前存在消费者，有多少次能在它实际 rename 时确认先前消费者已经使用完旧值？

沿用现有二进制，开启其已有的 Rename、O3PipeView、ExecFlags 调试探针和被动 schema-2 容量观察器。复用 feature 关闭。没有修改 C++、分配、执行或释放协议，没有重新构建，也没有改动此前分布式长测的二进制、配置或输出目录。

## 已完成的实验

- 8 个 workload 各取最高权重切片；INT/FP=224/256 和 192/208 两种容量，共 16 次。
- 每次预热 1M + 测量 1M 指令；预热结束后才开始 trace。
- 16/16 通过 NEMU difftest，实际指令数和周期数与此前同二进制、同切片/容量/窗口的 OFF 运行完全一致。
- 一个定向程序通过 difftest，识别出 34 次“先前消费者已提交”的扩展机会。
- 7 个分析单元测试覆盖乱序读值、commit/WB 区别、访存边界、来源去重、物理槽位代数、错误路径及区间并集。

结果入口：`slices-1m/opportunity-summary/report.md`、`per_run.csv`、`summary.json`、`slices-1m/validation.json`。各任务目录的 `opportunities.json` 保存实际 PC、指令和先前消费者时间。

## 三种统计口径

1. `committed_before_rename`：新增多消费者机会，所有先前仍有效的消费者均在重定义实际 rename 前已提交。属于读取完成的保守证据；仍需要原有版本和 shadow 机制保护异常/恢复。
2. `restricted_wb_before_rename`：包含第一类；另外允许普通、非访存/非控制/非 microop 的标量消费者在此前完成最后一次 writeback。writeback 是取得操作数的代理，不是硬件稳定 readDone 证明。
3. `any_wb_before_rename`：允许所有类型的先前消费者使用 WB 时间代理，更乐观，尤其不能据此放开 load/store replay 安全约束。

`single_consumer_existing` 是此前无消费者的自重定义机会，与新增机会分开。所有候选要求同逻辑寄存器、源/旧目的指向同一个物理值；同一指令重复源只算一次。值通过物理标签加每次新分配的代数区分，避免 free list 复用造成 ABA 混淆。

实际 rename 时间来自 `Renaming instruction with PC`，不是 O3PipeView 的 rename-buffer 入队时间。提交时间来自 O3PipeView retire 字段；Exec 行前缀是执行时生成的时间，不能误用为 commit 时间。错误路径消费者仅在其 squash 已发生时从先前消费者集合排除。

## 与寄存器不足的关系

对新增候选取 baseline 的 `[重定义 rename, 旧值常规释放)` 区间，与同类型 shortage 周期求交。它表示潜在重叠，不是已实现的槽位节省或可回收周期。

`*_slot_shortage_ticks` 是寄存器占位时间，可重复计同一周期；除以 `period=333` 得到寄存器周期。`*_union_class_shortage_ticks` 在每类内部去重，再相加，跨 INT/FP 仍可能重叠，不能直接当作全局停顿比例。

该筛查没有施加复用后的版本上限、shadow 容量和端口成本，也没有模拟调度反馈，不能将新增候选百分比称为 IPC 收益。逐个切片的代表权重保存在结果中，结果不外推为完整 workload 或 SPEC 分数。

## 覆盖边界

候选排除访存/控制/vector/microop/move/非推测/fusion 指令；曾出现别名的值保守排除，trace 前已经存在的物理值不计。最后仍未释放的值可以计候选，但不会捏造其结束时间和不足曝光量。

现有 Decode 的 `applyFusion()` 会新建 DynInst，未给新对象复制 O3PipeView 的 fetchTick，故其完整流水线记录缺失。缺少 producer/consumer 时间时保守不计相应机会；fusion 指令也不作为候选。libquantum 原始架构指令 trace 覆盖约 77.57%，gcc 约 99.7%，其余约 99.95% 以上。每点的 `trace_coverage` 和 `decoded_fusion_pairs` 明确记录此边界；不把缺失样本外推到全量。

## 复现

```bash
cd /nfs/home/liuchanghe/register_reuse
python3 register_reuse_last_consumer/run.py --jobs 8
python3 register_reuse_last_consumer/analyze_batch.py \
  register_reuse_last_consumer/slices-1m --jobs 4
python3 register_reuse_last_consumer/validate.py
python3 -m unittest discover -s register_reuse_last_consumer -p 'test_*.py' -v
```

默认已有完整成功运行会跳过。改变切片、容量或窗口时使用新的 `--out`，例如：

```bash
python3 register_reuse_last_consumer/run.py \
  --workloads mcf,gcc_166 --capacities 192:208 \
  --warmup 1000000 --measure 2000000 --jobs 2 \
  --out register_reuse_last_consumer/refine-2m
```

`trace.gz` 是压缩的原始证据，这轮 16 组约数 GB。分析支持独立进程并行；`--refresh` 可重新分析，不重新模拟。所有参数、命令和 SHA256 在 manifest/run JSON 中。

# 寄存器复用：实现、正确性和性能结果

已在 XS-GEM5 上实现默认关闭的单线程标量 INT/FP 寄存器槽位复用，支持最多三次复用、独立版本依赖标签、旧版本数据、精确状态读回、分支/异常 squash、单消费者预测及额外消费者修正。代码入口为 `GEM5/src/cpu/o3/register_reuse.cc`，开启参数为 `enableRegisterReuse`。

## 正确性验证

- 6 个版本状态单元测试通过 ASAN/UBSAN：版本容量、旧版本存活、squash 后避免标签 ABA、首次消费者、已提交消费者标记。
- 10 个真实裸机测试通过 NEMU difftest：定向程序和固定随机种子程序，各运行 off/certain/predicted/one-shadow/small 五种配置。
- 定向程序检查整数/浮点链、同指令重复源、move alias、额外消费者修正、store-data、延迟 store 对年轻 load 的别名冲突、错误路径和 64 次非法指令精确异常中的 INT/FP 状态。默认启用复用的用例实际发生 308 次 nuke replay。
- 随机程序含 4000 个算术/访存操作，检查所有最终寄存器和内存值，并逐条执行 difftest。
- 四个不支持参数组合（非法 shadow 数、空预测器、压缩 ROB、同时启用旧观察器）均在启动时被拒绝。
- 新二进制关闭 feature 后，与旧二进制在定向程序及 8 个默认容量 SPEC 切片上的指令数、周期数完全一致。
- 最终性能实验 48/48 正常达到指令上限并通过 difftest；配置文件逐项校验了开关、容量、未压缩 ROB 和 reference。
- 这些结果未发现覆盖范围内的功能错误，不是不存在所有 bug 的形式证明。

## 性能

8 个 workload 各取最高权重切片，每组预热 1M + 测量 1M 指令，off/certain/predicted 使用同一最终二进制、同一容量和指令区间。下表为这 8 个切片的等权几何平均，不是全 SPEC 分数。

| INT/FP 物理槽位数 | 仅确定性复用 | 启用跨寄存器预测 |
|---|---:|---:|
| 224/256 | +0.10% | -3.02% |
| 192/208 | +1.82% | -1.47% |

确定性模式在 192/208 容量下，bwaves 约 +4.11%、leslie3d 约 +3.64%、mcf 约 +2.35%、hmmer 约 +2.17%。默认容量下存在收益和退化，mcf 确定性模式约 -3.39%，因此不能从复用次数直接推导加速。

预测模式在 libquantum 上约 -23%，百万指令测量段发生约 6.4K 次修正复制；修正等待、额外临时槽位和动态调度反馈可能抵消分配节省。当前建议显式使用 `regReusePrediction=False` 先评估确定性模式，预测模式保留为实验开关。

## 模型与适用边界

- 当前均匀地给每个 INT/FP 槽位配置 1..3 份影子数据，没有实现论文异构 0/1/2/3-shadow bank 的预测分配，因此不作等面积、功耗和频率收益声明。
- 发现额外消费者后，等待原生产者就绪和复制延迟，分配真实 free-list 临时槽位供该消费者读取，提交/冲刷后释放。它比论文的持久重映射方案更保守，后续消费者可能重复修正。
- 旧版本按版本地址保存；恢复通过旧 RAT 版本重新可见并施加配置的 rename 恢复间隔建模，没有模拟 SRAM cell 的具体复制电路和逐端口争用。
- 禁止 memory/control/non-speculative/vector/microop 自身成为源槽位覆盖者；它们仍可读取修正后的标量源。
- 支持单线程、未压缩 ROB 的 kmhv3.py；SMT、ROB compression、value prediction、constant folding、立即数消除及旧观察器组合暂不支持。
- 默认关闭整个 feature。已有大规模容量测试继续使用原二进制；其 SHA256 已核对未改变。

## 复现与文件

```bash
cd /nfs/home/liuchanghe/register_reuse
./register_reuse_feature/build.sh
./register_reuse_feature/test_state.sh
python3 register_reuse_feature/run_tests.py
python3 register_reuse_feature/run_tests.py --program random
python3 register_reuse_feature/run_perf.py --jobs 12
```

最终数据：`performance-validated/report.md`、`performance-validated/summary.json`；配置验证：`validation.json`；旧二进制一致性：`baseline-equivalence.json`、`spec-baseline-equivalence.json`；源码快照与 SHA256：`source-manifest.json`、`source-snapshot/`；工作区完整补丁：`workspace-source.patch`（包含此前观察器改动）。

`spec-smoke`、`performance-final` 属于较早实现/中断实验，不用于上述最终结论。

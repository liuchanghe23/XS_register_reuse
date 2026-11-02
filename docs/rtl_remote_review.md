# XiangShan 远端 RTL 核对（2026-11-01）

通过官方 origin 的 `git ls-remote --symref` 查询分支，再下载源码核对。这里的“主线最新”指查询时默认分支 `kunminghu-v3` 的 HEAD，不表示仓库所有实验分支按时间排序的最后一个提交。

| 分支或快照 | 提交 | 提交时间（+0800） | 结论 |
|---|---|---|---|
| 原 xs-env 固定的 RTL | `16ae9ddcda54fc9a2fddffad73174cf793ac7814` | 2025-04-03 22:44:20 | 旧快照，不适合作为本次 V3 落地配置依据 |
| `kunminghu-v3`（远端默认分支） | `a0c2a26cbe3c862175174bad03a1a23c406315ed` | 2026-10-30 17:46:44 | 当前主线；源码中未发现文档描述的 IntSparseUCA/IntER |
| `fix-gsim-compile` | `673bc98a11a7e5357b65292cd3c38ca202db60ce` | 2026-08-05 09:37:27 | 有完整 IntER 实验代码，主线以外的参考实现 |
| 文档评测 feature 提交 | `3f395c6f9dbdf69a9d73262153a64e63d1bf0af8` | 2026-07-22 11:19:41 | 标题 `backend: resolve IntER integer entries at writeback`；已在原本地完整历史中确认属于上述实验分支历史 |
| `agentic-new-er-try` | `0ff7a1886c4dd04610a94d12b680a424b8206da5` | 2026-06-27 19:41:40 | 含 IntSparseUCA、readDone、ST 等较早实验 |
| `new-er` | `d3c358867d849719b99f712b99fa80eacf7a5c9c` | 2026-05-24 20:14:05 | 另一套 EarlyRelease/UserCountTable 实验，不能与 IntSparseUCA 方案混成同一版本 |

已在工作区准备两个源代码目录：

- `../XiangShan-RTL/`：独立浅克隆，位于 `kunminghu-v3` 的 `a0c2a26c`。
- `../XiangShan-IntER/`：上述仓库的独立 worktree，detached 于实验提交 `673bc98a`。

旧 `/nfs/home/liuchanghe/xs-env/XiangShan` 的工作树和 HEAD 未修改；现有 GEM5、大规模实验的二进制和参数也未修改。两个新目录都尚未初始化 submodule、编译或运行 RTL，源码检查不等于实现已经验证。

## 新 V3 与 GEM5 的配置关系

| 资源 | 新 V3 RTL DefaultConfig | 当前 GEM5 kmhv3.py |
|---|---|---|
| INT 物理寄存器 | 224 | 224 |
| FP 物理寄存器 | 256 | 256 |
| Decode / Rename | 8 / 8 | 8 / 8 |
| Virtual LQ | 120 | 120 |
| Physical SQ / multiple | 64 / 2 | 64 / 2 |
| RAR / RAW queue | 96 / 56 | 96 / 56 |
| ROB | 160，默认启用压缩 | 352，`RobCompressPolicy=none` |
| RAB | 352 | 不可将其直接当作 RTL ROB 容量 |
| INT PRF bank | 4 | scheduler 参数为 1，且禁用寄存器仲裁 |

RTL 参数入口是 `XiangShan-RTL/src/main/scala/xiangshan/Parameters.scala` 和 `top/Configs.scala`。`NoRobCompressionConfig` 只关闭压缩，未把 RobSize 自动改成 352。数字接近不等于逐周期行为等价；实现 feature 前需明确压缩、释放、寄存器端口和 replay 的建模口径。

## IntER 实验版本的开关与源码入口

`fix-gsim-compile` 最新提交的 `DefaultConfig` 中 `WithIntEarlyReleaseFunctional` 已被注释；`IntEarlyReleaseParams` 默认 `enable=false`。不能拿该分支的 DefaultConfig 运行，就宣称启用了提前释放。

可用配置：

- `IntERFunctionalConfig`：显式开启 functional IntER。
- `IntERDisabledConfig`：显式关闭，用于同一提交上的 A/B。
- `IntERFunctionalIntPreg128Config` / `IntPreg128Config`：128 个整数寄存器的配对配置。

最新 functional 配置为 `trackEntries=256`、`earlyFreeWidth=8`、`stWalkWidth=8`、`enableOtherIntegerWritebackResolve=true`；文档对应 `3f395c6f9` 为 `trackEntries=128`、`stWalkWidth=4`，且当时 DefaultConfig 默认开启。复现文档数值应固定文档提交和配置，不能套用实验分支的最新参数。

主要代码入口（相对于 `XiangShan-IntER/`）：

- `src/main/scala/xiangshan/backend/IntSparseUCA.scala`
- `src/main/scala/xiangshan/backend/IntEarlyReleaseBundles.scala`
- `src/main/scala/xiangshan/backend/rename/Rename.scala`
- `src/main/scala/xiangshan/backend/datapath/DataPath.scala`、`WbArbiter.scala`
- `src/main/scala/xiangshan/backend/rob/Rob.scala`、`Rab.scala`
- `src/main/scala/xiangshan/backend/rename/freelist/MEFreeList.scala`
- `src/test/scala/xiangshan/backend/IntSparseUCATest.scala` 和 `IntEarlyRelease*Test.scala`

这也解开了组内文档的版本歧义：`3f395c6f9` 确实已经有普通整数 writeback-resolve 路径，“所有类型只在 normal commit 才 resolved”的段落不适用于该功能开启后的版本。

## 面向 RTL 的后续路线

建议将当前 V3 主线固定提交作为最终集成目标，将实验分支作为正确性机制和对照参考：

1. 在 IntER 实验提交上，使用同一提交的 Functional/Disabled 配置复现结果，确认 readDone、guard、late writeback 和 commit suppress 的机制。
2. 以 V3 主线的压缩 ROB、RAB 和新 FreeList 接口明确集成点。主线 INT 已使用 StdFreeList，旧实验围绕 MEFreeList 的修改不能机械套用。
3. 为 GEM5 机会统计逐步加入实际 RTL 约束：replay-prone consumer、store-data、move alias、压缩组及多 uop、有限 UCA/版本容量、释放带宽。
4. 再确定优化是扩展现有非推测提前释放，还是实现论文的单消费者直接复用。后者还需要版本依赖匹配与可综合的旧值恢复存储，不是只改一次 FreeList 入队时机。
5. 正确性验证覆盖 redirect、load replay、异常、counter/identity 复用、late writeback、double-free；性能比较用相同提交、相同容量和相同切片。

原始远端版本记录见 `rtl_remote_review.json`。上述路线是基于已查源码的建议，尚未开始 RTL 功能修改。

# XiangShan 非推测整数寄存器提前释放方案精要
本文提取当前 IntER（Integer Early Register Release）方案中最关键的设计、边界和性能结论，用于快速理解当前实现。

> 当前方案只处理整数物理寄存器。FP、Vector、V0 和 VL 寄存器仍完全使用原有提交释放协议。
>



# 核心方案总览
| 项目 | 当前方案 |
| --- | --- |
| 优化目标 | 在旧整数物理寄存器已不会再被正确路径读取、也不会因恢复重新成为有效映射后，早于 conventional release 将其归还 `MEFreeList`。 |
| 追踪对象 | producer 新分配的整数 `pdest`，每个 UCA entry 对应一个物理寄存器 owner。 |
| consumer 证明 | Rename 统计 unique consumer；DataPath 确认源值已稳定取得；ROB 校验动态指令和 source identity 后才减计数。 |
| producer 证明 | 必须观察到真正获胜的整数 RF writeback，防止旧 producer 的晚写回覆盖已复用寄存器。 |
| redefiner 证明 | 后续 redefiner 已出现，且 speculation tracker 已确认它跨过当前定义的安全边界。 |
| 恢复策略 | 无法证明安全时立即放弃优化，回到原有 commit、RAB、RAT 和 FreeList 协议。 |
| 防止重复释放 | early-free 后保留完整 entry identity，等 redefiner commit 时 suppress conventional free。 |
| 当前功能模式 | `DefaultConfig` 中 `enable=true`、`observeOnly=false`，会真实执行 early-free。 |


传统路径中，旧物理寄存器通常要等 redefiner 提交并经过 RAB/RAT 对齐路径后才释放：

```plain
x5 -> p80
ADD x5, x7, x8       // x5 -> p81，p80 成为 oldPdest

传统路径：ADD commit -> RAB/RAT conventional free(p80)
IntER：   安全条件满足 -> earlyFree(p80) -> ADD commit 时 suppress free(p80)
```

IntER 只改变物理寄存器进入 free list 的时间，不改变 ROB 的程序序提交，也不让 redefiner 提前提交。



# 提前释放的安全条件
对一个正在追踪的整数物理寄存器 `p`，只有以下条件全部成立才能提前释放：

```plain
EarlyFree(p) =
    entry.state == counting
 && !entry.fallback
 && producerReady(p)
 && redefinerSeen(p)
 && redefinerNonSpeculative(p)
 && allCountedConsumersReadDone(p)
 && !earlyFreeIssued(p)
```

| 条件 | 保护的风险 |
| --- | --- |
| `producerReady` | 原 producer 晚到的 writeback 在 `p` 被复用后覆盖新 owner 的值。 |
| `allCountedConsumersReadDone` | 尚未取得旧值的 consumer 在 `p` 被复用后读到新 owner 的值。 |
| `redefinerNonSpeculative` | redefiner 被冲刷后，`p` 本应重新成为有效映射，但已经被复用。 |
| 完整 identity 和 generation 匹配 | UCA entry 或物理寄存器复用后，旧事件误更新新 owner。 |
| `commitSuppress` | 同一个 `p` 先 early-free、后 conventional-free，造成 double-free。 |


## 当前“非推测”的真实边界
ROB entry 入队时，不区分指令类型，统一初始化为：

```plain
entry.intER.resolved = false
```

当前 `commitSafeNow` 也不是“已经执行完成”的泛化信号，而是该 entry 本周期真的被某条 commit lane 选中：

```plain
commitSafeNow(entry) =
    io.commits.isCommit
 && exists lane:
      io.commits.commitValid(lane)
   && io.commits.robIdx(lane) == entry.robIdx
```

其中，单独的 `commitValid(lane)` 只表示该 lane 通过了逐 lane 的完成和顺序检查；它还必须与全局 `io.commits.isCommit` 同时为 true，并且 lane 的 `robIdx` 命中该 entry，才构成该 entry 的实际 normal commit。因此：

```plain
commitSafeNow(entry) == actualNormalCommit(entry)
```

ROB speculation tracker 使用：

```plain
safeToCross(entry) = entry.intER.resolved || commitSafeNow(entry)
```

`commitSafeNow` 为真时，ST 可以通过上式在同周期越过该 entry；在该周期末，RTL 将 entry 中保存的 `resolved` 置为 true。这里不是两个先后发生的安全边界：实际 normal commit、`commitSafeNow` 和 ST 的同周期放行描述的是同一个事件，寄存的 `resolved` 只是该事件在时钟沿后的状态记录。

```plain
周期 T 组合逻辑：actualNormalCommit -> commitSafeNow -> safeToCross
周期 T 时钟沿：entry.resolved := true，同时该 entry 按正常提交路径退休
```

也就是说，当前所有指令类型只有在实际 normal commit 时才被视为 resolved，没有按指令类型连接更早的 resolve event。

必须区分以下三个状态：

```plain
isWritebacked(entry) = (entry.uopNum == 0)

isWritebacked != resolved
resolved       => 该 entry 已经达到过实际 normal-commit 边界
```

一条指令即使已经 writeback，只要还没有轮到它提交，仍然是 unresolved，并会挡住 ST。实际 commit 还要求 ROB 处于 idle、没有全局 `blockCommit`、entry 有效且所有 uop 已完成、没有 head exception/flush 阻塞，也没有更老 lane 阻止提交。ST 还会在 redirect、walk、interrupt、exception、`flushPipe`、replay 或 WFI 等条件下全局停止。



### 各类指令当前如何判定 resolved
| 指令分类 | 当前 resolved 时刻 | 在此之前的典型阻塞 |
| --- | --- | --- |
| 简单 ALU、MUL/DIV、其它整数运算（`other_integer`） | 执行和 writeback `uopNum` 归零。 | 未 writeback、等待更老指令、全局 commit block。 |
| Branch / JAL / JALR（`branch_jump`） | BJU writeback、redirect/mispredict 处理完成后，仍要等实际 normal commit 才 resolved。 | 分支未 writeback、redirect、mispredict drain、被更老指令阻塞。 |
| Scalar Load（`scalar_load`） | Load 完成 writeback，且没有 exception、replay 或 flush 后，最终在实际 normal commit 时 resolved。 | cache/TLB/重放、访问异常、Load replay、等待更老指令。 |
| Scalar Store（`scalar_store`） | 地址和数据相关 uop 完成，并满足正常提交条件后，在实际 commit 时 resolved。 | STA/STD 未完成、内存异常或 replay、等待更老指令。 |
| AMO（`amo`） | 原子访存完成且没有 exception/replay 后，在实际 normal commit 时 resolved。 | 原子操作未完成、内存异常、replay、序列化等待。 |
| CSR / System（`csr`） | CSR 执行完成且没有 exception/`flushPipe` 等精确状态事件后，在实际 normal commit 时 resolved。 | CSR 序列化、异常、`flushPipe`、等待更老指令。 |
| Fence（`fence`） | Fence 的序列化和完成条件满足后，在实际 normal commit 时 resolved。 | 内存序约束、flush/序列化、等待更老指令。 |
| Vector Load / Store | 所有相关 uop 完成且没有 vector-memory exception/replay 后，在实际 normal commit 时 resolved。 | 多 uop 未完成、VLS 异常处理、内存 replay。 |
| 其它 FP / Vector 指令 | 所有 uop 完成后，仍在实际 normal commit 时 resolved。它们不产生 IntER destination，但可以阻塞 ST frontier。 | 多 uop/writeback 未完成、等待更老指令。 |
| ROB-compressed、fusion、multi-uop entry（`other`） | 整个 ROB entry 的 `uopNum` 归零并实际 commit 时 resolved。 | 任一成员 uop 未完成都会阻塞整个 entry；当前也不保存可提前释放所需的 per-instruction resolved identity。 |


这里的 `scalar_load`、`branch_jump` 等 `instClass` 目前只用于性能计数器归因，不参与 `resolved` 的功能判定。因此，不能把“计数器能区分指令类别”理解成“RTL 已为不同类别实现不同 resolve 条件”。



### 按指令类型提前 resolved 的可用边界
下面是后续如果要扩大提前释放窗口，各类指令至少需要证明的边界；这些条件当前尚未接入 `entry.intER.resolved`：

| 指令类型 | 可考虑的更早 resolved 边界 | 仍需保护的风险 |
| --- | --- | --- |
| 简单 ALU、MUL/DIV | 最终 writeback 成功，且确认不会再产生 exception/redirect。 | late writeback、执行异常和取消事件。 |
| Branch / JAL / JALR | 方向和目标已确定，redirect 已完成仲裁，且 ST 的程序序保证所有更老 redirect 风险已经关闭。 | 当前或更老分支随后冲刷 redefiner。 |
| Scalar Load | 最终成功返回数据，并完成地址翻译、异常、replay、memory-order violation 等检查。 | Load replay、TLB/page fault、内存违例重执行。 |
| Scalar Store | 地址和数据均被可靠接收，异常检查完成，且不会再因 memory-order violation 触发恢复。 | Store 地址/数据重取、访问异常、内存序恢复。 |
| AMO | 原子操作已不可撤销地完成，异常和 replay 风险全部关闭。 | 原子访存重试、异常和序列化恢复。 |
| CSR / Fence / flush-sensitive System | 继续保守到 normal commit，除非能为每种副作用建立独立的不可回滚证明。 | 特权状态、副作用、流水线 flush 和精确异常。 |
| Vector / multi-uop / compressed entry | 建立 per-uop 或 per-segment resolved 状态，并证明 entry 内所有更老成员安全。 | 只用一个 entry-level bit 会错误越过尚未完成的成员。 |


因此，当前 ST 实际接近 commit-safe frontier：

+ 普通 ALU 并没有在执行完成后立即 resolved；
+ Branch 并没有只因方向和目标已经确定就立即 resolved；
+ Load/Store 也没有建立比 commit-safe 更早的精确 resolved 条件；
+ early-free 的主要提前量来自早于后续 RAB/RAT conventional-free 对齐路径，而不是大幅早于 ROB commit。

这是理解当前收益有限的第一关键点。当前实现的恢复证明较简单，但可利用的提前释放窗口也较短。



# User Counter Array
`IntSparseUCA` 是一个稀疏 User Counter Array。每个 entry 追踪一个 producer 分配的整数 `pdest`，并保存：

| 字段 | 含义 |
| --- | --- |
| `state` | `invalid`、`counting`、`fallbackWaitCommit` 或 `releasedWaitCommit`。 |
| `pdest` | 被追踪的整数物理寄存器。 |
| `producerRobIdx` | producer 的 ROB identity，用于验证真实整数 RF writeback。 |
| `redefinerRobIdx` | 把该 `pdest` 变成 oldPdest 的 redefiner identity。 |
| `userCounter` | 1 个 redefiner guard token，加尚未完成读值的 unique consumer token。 |
| `trackId + trackGen` | entry identity 和复用代数，隔离 stale event。 |
| `producedReady` | producer 已经通过真实整数 RF 写口。 |
| `redefinerSeen/redefinerNS` | redefiner 已发现，且已通过 ST 安全边界。 |
| `earlyFreeIssued/releasedReused` | 是否已提前释放，以及 commit 前是否发生过物理寄存器复用。 |


## Counter 规则
producer 分配 entry 时，counter 初始为 1，而不是 0：

```plain
UC = 1                        // redefiner guard token
UC = 1 + pending unique consumers
```

+ consumer 在 Rename 首次命中该 entry 时加 1；
+ consumer 在 DataPath 稳定取得源值、且 ROB 完整校验通过后减 1；
+ redefiner 被 ST 判定为 non-speculative 后，guard 再减 1；
+ `UC == 0` 表示所有已计数 consumer 都已 readDone，且 redefiner guard 已消耗。

同一动态指令的两个 source 指向同一个 `psrc` 时只计一次：

```plain
ADD x6, x5, x5       // 对 x5 对应 entry 只产生一个 token
```

若 4-bit counter 将超过 15，entry 进入 fallback，而不是饱和后继续尝试 early-free。



## Entry 状态机
| 当前状态 | 主要事件 | 下一状态 | 释放行为 |
| --- | --- | --- | --- |
| `invalid` | eligible producer 分配成功 | `counting` | 建立 identity，`UC=1+` 同周期 unique consumer 数。 |
| `counting` | 所有安全条件成立 | `releasedWaitCommit` | functional 模式发出 early-free。 |
| `counting` | unsafe source/redefiner、read-path fallback 或 counter 饱和 | `fallbackWaitCommit` | 禁止 early-free，等待常规提交释放。 |
| `counting` | redefiner 已常规释放而未 early-free | `invalid` | conventional free 正常执行。 |
| `fallbackWaitCommit` | redefiner commit | `invalid` | conventional free 正常执行。 |
| `releasedWaitCommit` | redefiner commit 且 identity 全匹配 | `invalid` | suppress conventional free，防止 double-free。 |
| 未释放状态 | redirect、ROB/RAB walk recovery | `invalid` | 放弃 tracking，由原恢复路径接管。 |
| `releasedWaitCommit` | recovery kill | 保持 | 已进入 FreeList 的操作不能撤销，必须等 commit suppress。 |


# 端到端模块协同
```plain
Decode / RAT old-dest read
          |
          v
Rename: producer alloc + source match + redefiner match
          |
          +--------------------------> IntSparseUCA
          |                                  ^
          v                                  |
Dispatch -> IssueQueue -> DataPath ---- readDone / fallback
          |                                  ^
          v                                  |
       EXU / WbArbiter ---------------- producerReady
                                             ^
                                             |
ROB: readDone validation + ordered ST guard--+
          |
          v
RAB commit identity -> commitSuppress -> MEFreeList
```

| 模块 | 关键责任 |
| --- | --- |
| Decode / RenameTable | 为 destination 额外读取当前整数 RAT old mapping，使 redefiner 能关联旧 `pdest`。 |
| Rename | 生成 producer、source、redefiner probe，执行 eligibility/fallback 判断，实例化 UCA，并连接 commit 与 FreeList。 |
| IntSparseUCA | 聚合 source increment、read decrement、guard decrement、fallback、early-free 和 commit suppress。 |
| Bundles / Dispatch / IssueQueue / Region | 让 `trackId + trackGen + psrc + robIdx + srcIdx` 随动态指令和 source 一直传播。 |
| DataPath | 在 OG1 的真实操作数边界区分稳定 `readDone` 与可能重读的 `fallback`。 |
| WbArbiter | 只从真正获胜的整数 RF writeback port 产生 `producerReady`。 |
| ROB | 验证 raw readDone/fallback，记录每个 source 是否已完成，并按程序序推进 ST guard。 |
| RAB | 保存并提交 redefiner 的完整 identity，与 conventional-free lane 对齐。 |
| MEFreeList | 合并 conventional-free 与 early-free lane，并检查重复释放。 |
| Difftest shadow | 保存提交态整数值，避免 Difftest 读取已经 early-free 并被复用的 PRF 位置。 |


成功路径为：

```plain
producer alloc
 -> consumer token increment
 -> producerReady
 -> consumer readDone
 -> redefinerSeen
 -> ST guard decrement
 -> UC == 0
 -> earlyFree
 -> redefiner commitSuppress
 -> UCA entry clear
```



# 各类指令的处理方式
分析一条指令时必须分开看三个角色：

+ 它的新整数 destination 能否成为 tracked producer；
+ 它读取已 tracked `psrc` 时能否成为可完成的 consumer；
+ 它覆盖逻辑寄存器旧映射时能否成为 redefiner。

例如 Load 的整数结果可以成为新的 tracked producer，但 Load 使用 base register 的路径可能 replay，因此会让 base 对应的另一个 UCA entry fallback。



## 通用 producer 条件
新整数 destination 只有同时满足以下条件才尝试分配 UCA entry：

+ Rename output 真正 fire；
+ 当前没有 redirect 或 RAB walk；
+ `firstUop && lastUop && numUops == 1`；
+ 没有 exception、debug trigger、`flushPipe` 或 single-step；
+ 确实写整数 destination，且 `ldest != x0`；
+ 不是 move elimination；
+ UCA 有空 entry。

UCA full 时只是不追踪新 producer，不会阻塞 Rename，也不影响正确性。



## 指令分类
| 指令类型 | Destination 处理 | Source 处理 | 当前结果 |
| --- | --- | --- | --- |
| 简单 ALU | single-uop、single-entry 时可追踪。 | RF、RegCache、已支持的 forward/bypass 可 readDone。 | 最适合 fast path；但连续简单 ALU 被 ROB compression 合并后通常失去 eligibility。 |
| MUL/DIV | producer 条件与普通 ALU 相同。 | uncertain-latency source path 会 fallback。 | destination 和 source 独立判断。 |
| Scalar Load | 单 entry、写整数且无异常/flush 时，load result 可追踪。 | base 位于 replay-prone load-address path，命中 tracked source 时 fallback。 | “结果可追踪”与“base consumer 回退”可同时发生。 |
| Scalar Store | 通常没有整数 destination。 | Rename 对非零 store-data 保守 fallback；当前按整条 uop 影响命中的 tracked sources。DataPath store path 也 replay-prone。 | 不走当前 fast consumer path。 |
| Branch | 通常无整数 destination。 | 非 replay、非 uncertain 且数据源受支持时可 readDone。 | 仍可能在 ST frontier 等待 writeback/commit-safe。 |
| JAL/JALR | link destination 满足通用条件时可追踪。 | JALR base 按实际 BJU DataPath 判断。 | destination 与 source 分别判断。 |
| CSR/System | 没有按类别完全禁用，满足通用条件时整数 destination 理论上可追踪。 | exception、trigger、`flushPipe` 或 unsupported path 会 fallback。 | 多数序列化 CSR 仍走保守路径。 |
| Fence | 通常无整数 destination/source。 | 不直接贡献 consumer token。 | 自身不触发 early-free，但可能阻塞 ST。 |
| AMO | 严格满足 single-entry 和整数 destination 条件时才可追踪。 | 内存 replay 或 multi-uop 形态通常回退。 | 典型走保守路径。 |
| Move elimination | 不分配新物理寄存器，不作为 producer。 | 读取 tracked source 时使对应 entry fallback。 | 仍可作为另一个 old mapping 的 redefiner。 |
| FP/Vector | FP、Vector、V0、VL destination 不属于本 feature。 | 只有实际配置为整数 `IntData` 的 x-source 才可能参与。 | 纯 FP/Vector 寄存器沿用 conventional release。 |
| 立即数、PC、x0 | 不产生 tracked source；写 x0 不分配 entry。 | 忽略。 | 不影响 UCA。 |
| ROB-compressed、fusion、multi-uop | 新 destination 不追踪。 | 若读取已 tracked `psrc`，对应 entry fallback。 | 当前覆盖率的重要限制。 |
| exception、flushPipe、single-step | 新 destination 不追踪。 | 命中 active entry 时 fallback。 | 精确状态优先。 |
| redirect / RAB walk 同周期 | 不产生新 tracking probe。 | 未 released entry 在 recovery 中清除。 | 完全交回原有恢复协议。 |


# ReadDone 与 Fallback 边界
IQ 选择成功并不等于 consumer 已永久取得旧值。DataPath 在 OG1 观察实际 source path 后才决定：

| Source path / 状态 | 当前行为 |
| --- | --- |
| integer RF `readRegOH` | 支持 `readDone`。 |
| integer RegCache | 支持 `readDone`。 |
| forward | `DefaultConfig` 支持，且 EXU 必须是 wakeup sink。 |
| bypass | `DefaultConfig` 支持，且 EXU 必须是 wakeup sink。 |
| bypass2 | 默认关闭，产生 `unsupportedReadPath` fallback。 |
| load/store/hybrid/vector replay-prone IQ | 产生 `replayProneReadPath` fallback。 |
| uncertain-latency path | 产生 `uncertainReadPath` fallback。 |
| OG1 failed / 尚未完成 | 本拍不 decrement，也不立即 fallback，等待后续成功观察。 |
| 非整数 RF、立即数、PC | 不属于本 feature 的 consumer token。 |


ROB 只有在以下检查全部通过后才把 event 送给 UCA：

```plain
ROB entry live
 && not killed by redirect
 && srcIdx valid
 && stored source valid
 && trackId / trackGen / psrc match
 && source not already readDone
 && no duplicate event in the same cycle
```

只要一条指令的执行路径需要 fallback，当前实现会保守地回退该指令命中的相关 UCA entry，而不是冒险遗漏一次可能的源重读。



# Speculation Tracker
ST 从较老到较年轻按程序序推进，每周期最多跨越 `stWalkWidth=4` 个连续 ROB entry：

```plain
cursor = max(ROB deqPtr, previous specCursor)

repeat up to 4 entries:
  global stop / invalid / needFlush / !safeToCross -> stop
  redefiner metadata valid && guard not emitted   -> emit guard decrement
  advance cursor
```

commit block、walk、flush、interrupt、异常、replay、WFI 等 global stop 会停止推进。ST 的指令分类计数只用于归因，不能让某一类指令绕过相同安全条件。

当前性能计数器把 frontier 指令分为：

```plain
scalar_load / scalar_store / vector_load / vector_store / amo
branch_jump / csr / fence
other_integer / other_fp / other_vector / other
```

并区分 `not_writebacked`、commit-safe 条件不满足、walk width、global stop 等原因。因此可以同时回答“队头被哪类指令卡住”和“为什么卡住”。



# 简单情况举例
下面的 fast-path 例子假设每条指令都是 single-uop、single-entry，且没有 exception、flush 或 single-step。



## 一个 consumer，成功提前释放
```plain
I0: ADD x5, x1, x2     // x5 -> p80，UC=1
I1: XOR x6, x5, x3     // consumer of p80，UC=2
I2: SUB x5, x7, x8     // x5 -> p81，p80 成为 oldPdest
```

```plain
UC = 1
 -> I1 Rename:        2
 -> I1 readDone:      1
 -> I2 ST guard:      0
 -> earlyFree(p80)
 -> I2 commit: suppress conventional free(p80)
```

此外还必须满足 I0 的 `producerReady`。若 producer 尚未真正写入整数 RF，即使 `UC==0` 也不能释放 p80。



## 没有 consumer
```plain
I0: ADD x5, x1, x2     // p80，UC=1
I1: SUB x5, x3, x4     // redefiner of p80
```

I0 producerReady 且 I1 guard 消耗后，`UC` 可直接从 1 变为 0。不能在 I0 Rename 后立即释放，因为 I1 出现并安全以前，p80 仍是 x5 的当前映射。



# 复杂情况举例
## Load consumer 导致 fallback
```plain
I0: ADD x5, x1, x2     // p80 tracked
I1: LD  x6, 0(x5)      // base source = p80
I2: SUB x5, x7, x8     // redefiner of p80
```

I1 在 Rename 命中 p80 并增加 consumer token，但 load-address path 可能 replay。DataPath 因此产生 `replayProneReadPath` fallback，p80 对应 entry 进入 `fallbackWaitCommit`，最终由 I2 的 conventional release 释放。

I1 自己产生的 load result `x6` 若满足通用条件，仍可作为另一个独立 tracked producer。



## 其它典型复杂情况
| 情况 | 当前处理 |
| --- | --- |
| `ADD x6, x5, x5` | 相同 `psrc` 只计一个 consumer token，也只允许一次 decrement。 |
| 多个 consumer 乱序完成 | readDone 可乱序到达；每个 token 只需恰好减一次。 |
| Store-data 读取 tracked source | Rename 立即 fallback；当前整条 uop 命中的其它 tracked source 也可能受影响。 |
| Move elimination 读取 tracked source | move 不产生新 tracked destination，并使读取的旧 entry fallback。 |
| ROB compression 合并连续 ALU | 因 `numUops != 1`，组内 destination 不追踪；读取既有 tracked source 时回退。 |
| UCA full | 新 producer 不分配 entry，直接沿用 conventional release。 |
| Counter 将溢出 | entry 进入 fallback，不能带着不完整 consumer 数提前释放。 |
| Redirect 时 `counting` entry | 清除 tracking，原 recovery 接管。 |
| Redirect 时 `releasedWaitCommit` entry | 保留到原 redefiner commit suppress，避免再次 free。 |


# 混合情况举例
```plain
I0: ADD x10, x1, x2       // x10 -> p70，分配 E0
I1: ADD x11, x3, x4       // x11 -> p71，分配 E1
I2: XOR x12, x10, x5      // p70 的 safe consumer
I3: LD  x13, 0(x11)       // p71 的 replay-prone consumer
I4: SUB x10, x6, x7       // p70 的 redefiner
I5: BEQ x8, x9, target    // ST frontier blocker
I6: AND x11, x14, x15     // p71 的 redefiner
```

| 路径 | 事件 | 结果 |
| --- | --- | --- |
| `p70 / E0` | I2 readDone；I0 producerReady；I4 成为 redefiner。 | I4 到 commit-safe 后 guard 归零，p70 可以 early-free。 |
| `p71 / E1` | I3 在 load replay-prone path 产生 fallback；I6 成为 redefiner。 | E1 等 I6 conventional commit free。 |
| ST cursor | 必须依次跨越 I4、I5、I6；I5 未 writeback/未 commit-safe 时停止。 | 即使 E1 未 fallback，I6 guard 也不能绕过更老的 I5。 |


这说明 tracking 以 `pdest` 为粒度：p70 和 p71 独立演化；但 ST 又使用全局程序序 frontier，因此一条无关的较老指令也可能推迟年轻 redefiner 的 guard。



# Recovery、提交与正确性
当前方案必须保持以下不变量：

+ x0 不能分配 tracking entry，也不能被 early-free；
+ source token 不能重复 increment/decrement，counter 不能 underflow；
+ producerReady 必须同时匹配 `pdest + producerRobIdx`；
+ source event 必须匹配 `trackId + trackGen + psrc + robIdx + srcIdx`；
+ ST guard 必须匹配 `trackId + trackGen + oldPdest + redefinerRobIdx`；
+ guard 已发出的 redefiner 不能再被 redirect flush；
+ early-free 后 entry 必须保留到 commit suppress；
+ conventional-free 与 early-free 不能在同周期重复释放同一个 `pdest`；
+ redirect/walk 后 RAT、RAB 和 FreeList 仍由原有精确恢复协议收敛；
+ Difftest 不能从可能已经复用的 PRF 位置推导提交态整数值。

commit suppress 只有在以下 identity 全部匹配时才生效：

```plain
entry.state == releasedWaitCommit
trackId && trackGen match
RAB oldPdest == conventional oldPdest == UCA pdest
redefinerRobIdx match
```



# 当前默认配置
`DefaultConfig` 当前开启 functional IntER，相关硬件和 feature-specific 性能计数器会随 feature 生成：

| 参数 | 当前值 | 含义 |
| --- | --- | --- |
| `enable` | `true` | 生成并启用 IntER。 |
| `observeOnly` | `false` | early-free 会真实进入整数 FreeList。 |
| `trackEntries` | `128` | 最多追踪 128 个 producer。 |
| `counterBits` | `4` | `UC` 最大值为 15。 |
| `genBits` | `4` | generation 宽度。 |
| `earlyFreeWidth` | `8` | 每周期最多 8 个 early-free。 |
| `stWalkWidth` | `4` | ST 每周期最多跨越 4 个 ROB entry。 |
| `enableForwardReadDone` | `true` | 支持满足条件的 forward source。 |
| `enableBypassReadDone` | `true` | 支持满足条件的 bypass source。 |
| `enableBypass2ReadDone` | `false` | bypass2 仍走保守 fallback。 |
| `enableDiffShadowXRF` | `true` | 使用 ROB 侧整数架构 shadow。 |


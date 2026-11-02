Table of Contents



# 1	SPEC06 当前寄存器提前释放性能计数器说明
## 1.1	1. 文档目的
本文档基于当前寄存器提前释放 feature 的 SPEC06 perf run，对性能收益不明显的原因进行归因说明。文档使用两类图：

+ spec06-er-vs-baseline-percent-change.svg：当前 feature 相对 baseline 的 SPEC06 score 百分比增减图。
+ spec06-current-feature-bottleneck-charts/*.svg：当前 feature 版本中 IntER/ROB/ST/UCA/DataPath/Rename/FreeList 相关性能计数器的原因占比图。

本文档关注的是“为什么当前 feature 局部有效，但 SPEC06 总体收益很小”。结论不是 feature 未生效，而是主要端到端瓶颈已经不在当前 feature 覆盖的普通整数 writeback-resolved 窗口。

## 1.2	2. 数据来源与解析口径
当前 feature perf 目录：

/nfs/home/cirunner/perf-report-custom/cr260722-3f395c6f9-DefaultConfig

baseline perf 目录：

/nfs/home/cirunner/perf-report-custom/cr260612-be3c06aa4-DefaultConfig

每个 checkpoint 的性能计数器来自对应子目录的 simulator_err.txt。每个日志中存在两次 [PERF] dump：

1. warmup 结束前 dump，用于 reset 前观测；
2. final dump，用于实际测量区间。

本报告只聚合每个 checkpoint 最大 time= 的 final dump，避免 warmup 数据污染归因。

聚合结果：

| 项目 | 值 |
| --- | ---: |
| checkpoint 数 | 143 |
| 聚合指令数 | 5,720,000,398 |
| 聚合周期数 | 2,176,348,848 |
| 聚合 IPC | 2.628255 |


## 1.3	3. SPEC06 分数变化
下图展示当前 feature 相对 baseline 的 SPEC06 score 百分比变化。score 越高越好，计算公式为：

(current score / baseline score - 1) * 100%

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789240976-e0ac969d-d3c4-4b1e-bcc5-2c70fbcb58da.png" title="" crop="0,0,1,1" id="TxN24" class="ne-image">

SPEC06 score percentage change

汇总项如下：

| 项目 | Baseline score | 当前 feature score | 增减百分比 |
| --- | ---: | ---: | ---: |
| SPECint2006/GHz | 19.056 | 19.074 | +0.094% |
| SPECfp2006/GHz | 21.933 | 21.939 | +0.027% |
| SPEC2006 total | 20.693 | 20.705 | +0.058% |


结论：当前 feature 对 SPEC06 有轻微正收益，但 total 只有 +0.058%，属于非常小的提升。因此需要结合性能计数器判断收益被哪些剩余瓶颈限制。

## 1.4	4. 总体归因结论
当前 feature 中的 WB-resolve 子路径是有效的：final accepted writeback 后提前 resolved 的 entry 很多，WB-resolve candidate 的绝大多数也成功 resolved。但 SPEC06 总体性能提升不明显，主要原因如下：

| 归因点 | 证据 | 解释 |
| --- | ---: | --- |
| WB-resolve 成功率高 | 97.810% | feature 内部的 WB-resolve 子路径没有被安全检查大量拒绝。 |
| ST pending-work 仍被 valid frontier 阻塞 | 58.309% | ST 有待处理工作时，最大阻塞仍是队头/frontier entry 无法跨越。 |
| 队头 blocker 多数还没 writeback | not_writebacked 92.851% | 当前 feature 主要优化“已经 writeback 但尚未 resolved”的窗口；但当前主要 blocker 尚未到达 writeback。 |
| 队头 blocker 主要不是普通整数 | load 53.422%，store 14.317%，other_fp 15.235%，branch 8.848% | load/store/FP/branch 不是当前普通整数 WB-resolve 的主要覆盖范围。 |
| other_integer 剩余直接机会很小 | other_integer/not_resolved 0.784% | 本轮优化后，最直接可优化的 other_integer resolved 等待窗口已经不是主瓶颈。 |
| ST walk width 形成二级瓶颈 | pending-work 中 34.212% | 即使减少 blocker，ST 每周期扫描/跨越宽度仍限制 guard 推进速度。 |
| global stop 多数来自 recovery/walk | global-stop 中 recovery_walk 83.476% | 与普通整数 writeback-resolved 基本无直接关系。 |
| UCA/DataPath/Rename fallback 很多 | UCA first fallback 653,904,450 | 很多 source/consumer/read-path 无法证明 usersDone/readDone，导致提前释放链条不能闭合。 |
| FreeList 压力窗口有限 | enough free regs 93.868% | early-free 机会只有一部分正好落在 rename/free-list 紧张窗口。 |


因此，当前 feature 的性能不明显不是因为 WB-resolve 没生效，而是主要剩余瓶颈集中在未 writeback 的 load/store/FP/branch、ST walk-width、recovery/global stop、UCA/DataPath/Rename conservative fallback，以及 FreeList 压力窗口不重合。

## 1.5	5. ST run-state split
该图展示测量周期中 ST 相关计数覆盖情况。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789241428-cfe86a24-5cfb-4e24-897d-cfdd422f5815.png" title="" crop="0,0,1,1" id="AoOH8" class="ne-image">

ST run-state split

| 状态 | 值 | 占 measured cycles |
| --- | ---: | ---: |
| ST has pending work | 996,668,564 | 45.795% |
| ST no work | 44,551,014 | 2.047% |
| outside ST accounted window | 1,135,129,270 | 52.158% |


这里的 outside ST accounted window 表示总测量周期中没有落入 int_er_rob_st_cycle 的部分。后续 ST 归因主要针对 ST 已经开始计数并且存在 pending work 的窗口。

## 1.6	6. ST pending-work outcomes
该图是 ST 有 pending work 时的 exclusive outcome 闭包。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789241756-d3da5516-cea9-4125-a873-1a146f5778a7.png" title="" crop="0,0,1,1" id="tqGEu" class="ne-image">

ST pending-work outcomes

| 原因 | 值 | 占 pending-work |
| --- | ---: | ---: |
| valid-frontier blocker | 581,146,208 | 58.309% |
| walk-width limited | 340,984,982 | 34.212% |
| global stop | 68,589,314 | 6.882% |
| caught up after scan | 5,948,060 | 0.597% |


结论：最大瓶颈仍然是 valid-frontier blocker；第二大瓶颈是 ST walk width。也就是说，就算减少了一部分普通整数 resolved 等待，ST 推进仍可能被队头其它类型指令或扫描宽度限制。

## 1.7	7. ST global-stop reasons
该图展示 ST pending work 被全局状态阻挡时的原因。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789242172-d2392ab9-04f6-4784-9dd4-68606260be56.png" title="" crop="0,0,1,1" id="UYrEU" class="ne-image">

ST global-stop reasons

| 原因 | 值 | 占 global-stop |
| --- | ---: | ---: |
| recovery_walk | 57,255,619 | 83.476% |
| mispredict_drain | 10,988,098 | 16.020% |
| commit_flush | 212,139 | 0.309% |
| other | 131,384 | 0.192% |
| interrupt_exception_replay | 2,074 | 0.003% |


结论：global stop 中绝大多数是 recovery/walk，当前普通整数 writeback-resolved 无法直接减少这些周期。

## 1.8	8. ST valid-frontier blocker by instruction class
这是当前最关键的归因图，展示 speculation tracker 队头/frontier 被哪类指令卡住。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789242571-3881abf0-ca09-4594-b2da-03fdaf6035c9.png" title="" crop="0,0,1,1" id="ROOSP" class="ne-image">

ST valid-frontier blocker by instruction class

| 指令类型 | 值 | 占 valid-frontier blocker |
| --- | ---: | ---: |
| scalar_load | 310,460,275 | 53.422% |
| other_fp | 88,537,893 | 15.235% |
| scalar_store | 83,199,863 | 14.317% |
| branch_jump | 51,416,953 | 8.848% |
| other_integer | 42,517,190 | 7.316% |
| other | 1,964,478 | 0.338% |
| csr | 1,156,024 | 0.199% |
| fence | 1,024,094 | 0.176% |
| amo | 869,438 | 0.150% |


结论：队头 blocker 主要不是本轮优化覆盖的普通整数。scalar_load + scalar_store + branch_jump 合计超过 76%。

## 1.9	9. ST valid-frontier blocker by status reason
该图展示队头 blocker 处于哪种状态。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789242864-2b1c7841-c264-454d-9afb-67788efce167.png" title="" crop="0,0,1,1" id="wbHFa" class="ne-image">

ST valid-frontier blocker by status reason

| 状态原因 | 值 | 占 valid-frontier blocker |
| --- | ---: | ---: |
| not_writebacked | 539,599,395 | 92.851% |
| not_resolved | 40,516,646 | 6.972% |
| need_flush | 1,030,167 | 0.177% |


结论：当前 blocker 的 92.851% 还没有 writeback。说明绝大多数属于自然卡顿。

## 1.10	10. ST valid-frontier top class × reason cells
该图把指令类型和阻塞状态组合起来，定位最具体的剩余瓶颈。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789243299-2a3d80f0-d4e8-46f1-8b3c-50de2b70c1a2.png" title="" crop="0,0,1,1" id="a7zSZ" class="ne-image">

ST valid-frontier top class reason cells

| 组合 | 值 | 占 valid-frontier blocker |
| --- | ---: | ---: |
| scalar_load / not_writebacked | 298,318,739 | 51.333% |
| other_fp / not_writebacked | 85,338,738 | 14.685% |
| scalar_store / not_writebacked | 74,946,062 | 12.896% |
| branch_jump / not_writebacked | 39,404,802 | 6.781% |
| other_integer / not_writebacked | 37,960,649 | 6.532% |
| scalar_load / not_resolved | 12,141,535 | 2.089% |
| branch_jump / not_resolved | 12,012,151 | 2.067% |
| scalar_store / not_resolved | 8,251,895 | 1.420% |
| other_integer / not_resolved | 4,556,541 | 0.784% |
| other_fp / not_resolved | 3,199,155 | 0.550% |


关键点是 other_integer / not_resolved 只占 0.784%。这说明本轮普通整数 writeback-resolved 后，直接可优化的 remaining window 已经很小；真正大的 cell 是 load/store/FP/branch 的 not_writebacked。

## 1.11	11. Writeback-resolve final-candidate outcomes
该图说明 feature 内部的 WB-resolve 子路径是否被 safety check 大量拒绝。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789243628-8ce6ff7a-76e3-437d-ac9e-8fbe6294a1d2.png" title="" crop="0,0,1,1" id="iN7jl" class="ne-image">

Writeback-resolve final candidate outcomes

| 结果 | 值 | 占 final candidate |
| --- | ---: | ---: |
| resolved_by_writeback | 1,042,686,821 | 97.810% |
| blocked_redirect_recovery | 23,347,255 | 2.190% |
| blocked_need_flush | 0 | 0.000% |


结论：WB-resolve 子路径成功率很高，因此性能不明显不是因为该子路径经常被 reject。

## 1.12	12. Writeback-resolved entries by class
该图展示成功提前 resolved 的 entry 类型。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789243920-7ef2e39f-861c-4bb6-add6-3de2e0b416bc.png" title="" crop="0,0,1,1" id="ZBSQO" class="ne-image">

Writeback-resolved entries by class

| 类型 | 值 | 占 resolved_by_writeback |
| --- | ---: | ---: |
| ALU | 1,026,719,074 | 98.469% |
| MUL | 10,654,473 | 1.022% |
| other_integer (bku/i2f/i2v) | 4,861,555 | 0.466% |
| DIV | 451,719 | 0.043% |


结论：提前 resolved 的绝大多数是 ALU。MUL/DIV/other_integer 的覆盖量较小。ALU resolved 很多，但它要转化成 end-to-end 性能收益，还必须满足 ST 能跨过更老指令、UCA 能证明 usersDone、FreeList 正好有压力等条件。

## 1.13	13. UCA first fallback reasons
该图解释 UCA 中候选项第一次进入 conservative fallback 的原因。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789244248-06b9ab70-d1ae-44f9-bcae-7abb8a4024d7.png" title="" crop="0,0,1,1" id="Lxpal" class="ne-image">

UCA first fallback reasons

| 原因 | 值 | 占 UCA first fallback |
| --- | ---: | ---: |
| replay_prone | 298,297,141 | 45.618% |
| store_data | 253,879,033 | 38.825% |
| move | 56,929,437 | 8.706% |
| unsupported_consumer | 29,224,044 | 4.469% |
| multiple | 13,003,987 | 1.989% |
| counter_saturated | 1,950,892 | 0.298% |
| uncertain | 593,970 | 0.091% |
| unsupported_read_path | 25,946 | 0.004% |


结论：大量候选因为 replay-prone 或 store-data consumer 进入保守路径。即使 producer 已经 writeback-resolved，如果 consumer/usersDone 无法安全证明，early-free 仍不能释放。

## 1.14	14. UCA entry blocker event/cycle counters
该图展示 UCA entry 级别 readiness blocker 的归因。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789244615-374ca3d8-b29a-4dc6-9239-8b5642dead9c.png" title="" crop="0,0,1,1" id="V0xH3" class="ne-image">

UCA entry blocker events

| 原因 | 值 | 占 listed UCA blocker |
| --- | ---: | ---: |
| multiple blockers | 28,454,416,883 | 64.414% |
| guard not done | 15,650,943,793 | 35.430% |
| consumer/users not done | 68,903,703 | 0.156% |


结论：UCA 层面常见多个条件同时未闭合，尤其 guard not done 占比较高。这说明 ST 侧 guard 推进速度和 UCA 侧 readiness 闭合速度仍是收益转化路径上的关键限制。

## 1.15	15. DataPath primary fallback reasons
该图展示 DataPath 侧不能给出精确 readDone 证明的主因。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789244936-055810f1-d679-46d5-a1db-c8d32fb6b5c5.png" title="" crop="0,0,1,1" id="RGQ0E" class="ne-image">

DataPath primary fallback reasons

| 原因 | 值 | 占 DataPath primary fallback |
| --- | ---: | ---: |
| replay_prone | 572,435,823 | 89.271% |
| unsupported_read_path | 68,240,860 | 10.642% |
| uncertain | 459,034 | 0.072% |
| multiple | 98,407 | 0.015% |


结论：DataPath fallback 主要由 replay-prone read path 造成。这类路径不能简单地当作 source 已安全使用完，否则会破坏 replay/redirect 下的正确性。

## 1.16	16. Rename fallback reasons
该图展示 Rename 侧 conservative fallback 的原因。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789245241-46d5a61a-d39a-4c9d-a0ec-d2c7534194be.png" title="" crop="0,0,1,1" id="xWw2O" class="ne-image">

Rename fallback reasons

| 原因 | 值 | 占 Rename fallback |
| --- | ---: | ---: |
| store_data_consumer | 238,702,538 | 71.467% |
| move | 72,438,911 | 21.688% |
| unsupported_consumer | 22,863,971 | 6.845% |


结论：store-data consumer 是 Rename/UCA fallback 中非常明显的残余瓶颈。如果后续要继续扩大收益，store-data consumer 的安全证明路径值得单独建模。

## 1.17	17. Integer free-list pressure states
该图展示整数 free-list 压力窗口。

<img src="https://cdn.nlark.com/yuque/0/2026/png/47565320/1784789245641-58792af7-59d3-4ead-9faa-245afb89cc8e.png" title="" crop="0,0,1,1" id="fBfRE" class="ne-image">

Integer free-list pressure states

| 状态 | 值 | 占 measured cycles |
| --- | ---: | ---: |
| enough free regs (>= 2×rename width) | 2,042,900,542 | 93.868% |
| low: [rename width, 2×rename width) | 61,674,329 | 2.834% |
| very low: (0, rename width) | 71,296,067 | 3.276% |
| empty | 477,910 | 0.022% |


相关 counter：

| 指标 | 值 | 占比 |
| --- | ---: | ---: |
| int_er_rename_int_freelist_stall_cycle | 65,215,369 | 占 measured cycles 2.997% |
| int_er_me_freelist_early_free_req_when_cannot_allocate | 44,644,482 | 占 early-free req 6.811% |


结论：early-free 的机会很多，但 FreeList 绝大多数周期并不紧张。只有当 early-free 与 rename allocation pressure 重合时，才会转化成直接性能收益。

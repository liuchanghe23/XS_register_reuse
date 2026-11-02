# XS-GEM5 scalar register reuse

The implementation lives in `GEM5/src/cpu/o3/register_reuse.{hh,cc}` and `register_reuse_state.hh`; the default CPU behavior keeps reuse disabled. The separate binary below leaves the ongoing capacity scan's binary intact.

```bash
cd /nfs/home/liuchanghe/register_reuse
./register_reuse_feature/build.sh
./register_reuse_feature/test_state.sh
python3 register_reuse_feature/run_tests.py
python3 register_reuse_feature/run_tests.py --program random
python3 register_reuse_feature/run_perf.py --jobs 12
```

CPU parameters:

| Parameter | Default | Meaning |
|---|---:|---|
| enableRegisterReuse | false | Enable scalar INT/FP sharing |
| regReuseShadowCopies | 3 | Uniform copies per slot, 1..3; maximum 4 version tags |
| regReusePrediction | true | Enable confidence-based cross-register reuse |
| regReusePredictorEntries | 512 | PC-indexed two-bit saturating counters; predict at >=2 |
| regReuseRepairLatency | 2 | Rename cycles per repaired shadow source, plus producer-ready wait |
| regReuseRecoveryLatency | 2 | Rename recovery interval when a squash discards shared versions |

Example:

```bash
register_reuse_feature/build/RISCV/gem5.opt --outdir=/tmp/reuse-example \
  GEM5/configs/example/kmhv3.py \
  --generic-rv-cpt=/path/to/checkpoint.zstd \
  --difftest-ref-so=/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so \
  --param 'system.cpu[0].enableRegisterReuse=True' \
  --param 'system.cpu[0].regReusePrediction=False'
```

Only base slots enter the free list. Shadow version IDs participate in normal dependency matching, wakeup, speculative/committed RAT mapping and recovery. Older committed values remain available for precise traps and difftest. All owners must release before the slot is returned; version numbers never wrap while the slot is live, even after a squash.

The Read bit is represented by a consumer count so wrong-path source registrations can be undone precisely. A first consumer that redefines the same logical register can reuse deterministically. Cross-logical sharing requires a confident predictor. Additional consumers wait for the old value and a copy latency, then receive a normal free-list temporary source until commit/squash. Duplicate operands in one instruction count once. Move aliases, pinned sources, vectors, microops, memory/control and non-speculative reusing instructions are excluded. Memory instructions can consume repaired sources, including split stores and replayed loads.

This is a bounded functional/timing reference. Uniform shadow capacity differs from the paper's mixed banks, and repair temporaries repeat per consumer rather than permanently remapping the old logical register. The model does not establish SRAM area/energy/clock cost or charge per-port copy contention. Equal-capacity performance measurements are not equal-area claims. Replay sources retain their version identity; actual RTL must separately prove stable readDone and cancellation behavior.

Supported initial configuration: single-thread RISC-V kmhv3.py with an uncompressed ROB. Unsupported combinations fail at construction: SMT, ROB compression, value prediction, constant folding, immediate elimination, and simultaneous passive `enableRegPressureStats` tracking. Baseline runs in `run_perf.py` use the same new binary and the same capacities and instruction windows as feature runs.

`reuse.S` tests deterministic INT/FP chains, source deduplication, prediction training followed by an extra consumer, move aliases, split store data, memory consumers, wrong-path updates and 64 precise illegal-instruction traps. `random.S` is generated reproducibly with 4000 integer/memory operations and checks every final register/memory value. Both run with NEMU difftest. `register_reuse_state.test.cc` additionally exercises version saturation, squash tag identity and ownership release under ASAN/UBSAN.

Validation and performance JSON/Markdown outputs are stored alongside this file. Passing these checks establishes the tested coverage, not a proof that the implementation contains no bugs.

Completed results: see [RESULTS.md](RESULTS.md),
[validation.json](validation.json), and
[performance-validated/report.md](performance-validated/report.md).
The recommended initial mode explicitly sets `regReusePrediction=False`.
The speculative predictor is implemented and passes difftest, but regresses
libquantum in the selected performance slice; it remains an experiment.

## 定向证明复用机制生效

```bash
python3 register_reuse_feature/run_mechanism.py
# 只复核已有配置、统计与 Rename trace：
python3 register_reuse_feature/run_mechanism.py --analyze-only
```

测试源为 `GEM5/tests/test-progs/register-reuse/mechanism.S`。运行同一个二进制的五组配置：单消费者 off/1-shadow/3-shadow，多消费者 off/3-shadow。全部固定 INT/FP=224/256、关闭预测和 move elimination，并开启 NEMU difftest。

正例连续执行 64 次 `addi s1,s1,1` 和 16 次 `fadd.d f8,f8,f8`，自检整数 17→81、FP 1.0→65536.0。负例在每次运算前先用 store 消费旧值，最终检查内存保留的旧值为 80 和 32768.0。

脚本从 ELF 符号确定测试区间，在 Rename trace 中逐条检查基槽位和版本：旧/新依赖标签不同、基槽位相同、版本增加一才算复用；版本容量耗尽则必须分配新的基槽位。预期 INT/FP 复用数为 off=0/0、1-shadow=32/8、3-shadow=48/12；多消费者负例即使开启 feature 也必须为 0/0。重复 FP 源操作数作为一个消费者得到覆盖。

已运行的五组全部通过；在这 80 次测试运算中，3-shadow 将新槽位分配从 80 次降至 20 次。全程序 counters 包含初始化等指令，不能直接当作测试区间计数。结果与逐条证据在 `mechanism-proof/report.md`、`proof.json` 和各用例的 `rename.log`。这是机制验证，应用性能收益仍用配对切片实验评估。

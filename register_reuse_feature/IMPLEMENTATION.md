# Register reuse implementation and validation notes

Work in progress: scalar INT/FP source-slot sharing in GEM5, default disabled.

- Separate build: register_reuse_feature/build/RISCV/gem5.opt. The ongoing capacity batch keeps its original build/RISCV/gem5.opt.
- Independent dependency tags for 0..3 shadow versions. Only base physical slots enter the free list; every version must lose its ownership reference before a slot is returned.
- Per-value first-consumer tracking at rename, including squash rollback. Same logical source/destination gives deterministic reuse; cross-logical reuse uses a 512-entry, 2-bit saturating PC predictor.
- Values are retained in bounded scalar shadow storage. Architectural/difftest reads use the committed version, which preserves precise exceptions and branch recovery. Squashing shared versions incurs configurable rename recovery latency.
- A later consumer of a predicted-dead value waits for the original producer and repair latency, then copies the saved version into a real free-list temporary source. This temporary is held until that consumer commits or is squashed. This is more conservative than the paper's persistent remapping repair: later consumers repeat the repair.
- This first implementation uses uniform shadow capacity per INT/FP slot, rather than the paper's predicted 0/1/2/3-shadow bank selection. It is a functional and timing reference, not an equal-area reproduction or a claim about synthesizable bit cells.
- Replay-prone loads/stores, vectors, microops, control/non-speculative instructions cannot themselves overwrite their source slots. They can consume repaired scalar values. Move aliases disqualify a value from sharing.
- Unsupported combinations fail fast: SMT, constant folding, immediate elimination, value prediction, and the earlier passive register-pressure observer. Default kmhv3.py is supported.

Progress checkpoint:

- Build succeeded and initial synthetic + random correctness tests passed with NEMU in off/certain/predicted/one-shadow/small configurations.
- Initial 24 SPEC smoke runs (8 workloads x 3 modes, 10K warmup +100K measure) all passed. See spec-smoke; this used the earlier prediction threshold and is not the final performance result.
- The 2-bit predictor now predicts at >=2. Consumer metadata is bounded: in-flight reads plus a saturated committed-read count. Repair temporaries do not train producer-PC confidence.
- Six version-state ASAN/UBSAN tests pass (state-tests-final.log).
- Added FP state verification in the precise trap handler and a delayed-store/younger-load alias test to reuse.S; final full synthetic runs must be repeated after the last build.
- Last source tweak is fresh repair temporary producer=0 (skip predictor training). Final incremental build is logs/build-ready.log, exec session 75137. No further source changes are planned absent failures.
- Preliminary performance-final was deliberately stopped to avoid mixing binaries before the bounded-counter cleanup; do not use it as final data. Final paired performance should use a new output directory performance-validated with run_perf.py (default 8 workloads, capacities224/256 +192/208, modesoff/certain/predicted, 1M+1M instructions, 48 runs).
- After build: rerun run_tests.py and --program random; rerun old original binary on the same newly compiled reuse.bin and compare OFF cycles/instructions; run unsupported-config negative tests; then run_perf.py. Existing user's large-capacity-coverage80 jobs and original build/RISCV/gem5.opt have not been changed/stopped.

Implementation limits: uniform shadow banks, per-consumer repair temporaries, no equal-area port/energy model; these must be disclosed in final documentation/results. Single-thread RISC-V, uncompressed ROB; passive old observer disabled with this feature.


Final completion: all 10 synthetic integration cases, 6 ASAN/UBSAN state tests,
4 negative configuration tests, and 48 paired 1M+1M SPEC runs passed. Final
performance is in performance-validated, not the stopped performance-final.
Validation JSON confirms all eight default OFF results match the prior original
binary exactly. See RESULTS.md and validation.json for evidence and limits.

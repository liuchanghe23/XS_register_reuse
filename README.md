# XS Register Reuse

在 XS-GEM5 / Kunminghu V3 模拟配置中研究标量 INT/FP 物理寄存器复用，包含容量压力观测、确定性与预测复用、正确性测试、分布式容量扫描及结果分析。

## 阅读入口

- [大规模实验分析与图表](register_reuse_distributed/batch-6servers/report/analysis/findings.md)：55 个 workload、584 个切片、20M 预热 + 20M 测量；包含超时任务和配对覆盖边界。
- [批次汇总](register_reuse_distributed/batch-6servers/report/report.md) 与 [运行校验](register_reuse_distributed/batch-6servers/report/validation.json)。
- [复用功能与参数](register_reuse_feature/README.md)、[正确性及早期性能结果](register_reuse_feature/RESULTS.md)。
- [容量观测与统计口径](register_reuse_analysis/README.md)。
- [分布式实验启动、续跑与汇总](register_reuse_distributed/README.md)。
- [最后消费者扩展机会筛查](register_reuse_last_consumer/README.md)。

## 目录

| 目录 | 内容 |
|---|---|
| `GEM5/` | 包含本项目改动的完整模拟器源码；上游许可证保留在该目录中 |
| `register_reuse_feature/` | 独立构建、定向/随机测试、复用机制证明及性能验证 |
| `register_reuse_analysis/` | schema-2 被动容量观察器的运行与分析脚本 |
| `register_reuse_distributed/` | 多服务器任务计划、worker、汇总与大规模分析 |
| `register_reuse_last_consumer/` | 基于 trace 的最后消费者机会分析 |
| `docs/` | 设计背景和 RTL 对照笔记 |

`GEM5/` 以普通源码文件纳入本仓库，不需要另外下载它的源码。工作区原有的内层 GEM5 Git 元数据没有被修改或删除。源码来源及参考版本见 [UPSTREAMS.json](UPSTREAMS.json)。

## 构建与测试

在仓库根目录执行。构建依赖参见 [GEM5 文档](GEM5/README.md)；需要 C++ 工具链、SCons 及 DRAMsim3。本地 DRAMsim3 可通过 `GEM5/ext/dramsim3/DRAMsim3` 指向其安装目录；构建脚本中的共享服务器默认路径需按环境调整。定向程序还需要 `riscv64-linux-gnu-gcc` / `objcopy`；执行 NEMU difftest 需要可访问的 reference shared library。

```bash
# 根据实际机器设置，不同环境应使用自己的 reference。
export GCBV_REF_SO=/path/to/riscv64-nemu-interpreter-so

# 观察器与 feature 使用独立输出目录。
./register_reuse_analysis/build.sh
./register_reuse_feature/build.sh

./register_reuse_feature/test_state.sh
python3 register_reuse_feature/run_tests.py
python3 register_reuse_feature/run_tests.py --program random
python3 register_reuse_feature/run_mechanism.py

python3 -m unittest discover -s register_reuse_analysis -p 'test_*.py' -v
python3 -m unittest discover -s register_reuse_distributed -p 'test_*.py' -v
python3 -m unittest discover -s register_reuse_last_consumer -p 'test_*.py' -v
```

SPEC 切片不随仓库发布。重跑实验前，将 checkpoint 数据放到本地，并按对应脚本的参数设置路径；默认入口使用根目录 `zstd-checkpoint-0-0-0`。已有六服务器计划记录的是原工作区的实验身份和路径；迁移机器或改变配置时，按分布式说明生成新的计划。

## 结果与模型边界

本轮大规模长测评估 `regReusePrediction=False` 的确定性复用。54 个配对完整 workload 的等权几何平均：默认容量复用约 +0.54%；192/208 同容量复用约 +1.26%；192/208 开启复用相对默认 OFF 约 +0.40%。mcf 仍有 9 项超时，完整情况见报告。

当前模型为每个基础槽位统一配置 shadow，未建立异构 bank、逐端口争用、面积、能耗或频率模型。缩减基础槽位不等于相同比例的硬件面积节省。结果限于所选切片和模拟配置，不是官方 SPEC 分数。

仓库保留源代码、实验计划、汇总 CSV/JSON、验证记录和分析图表；构建产物、checkpoint、原始逐运行 stats/trace、外部 RTL/xs-env checkout 和本机虚拟环境由 `.gitignore` 排除。已有大规模计划及统计中的绝对路径用于保留原始实验出处。

## 复算已有产物

```bash
# 需要本地保留完整的 results/ 原始目录；仓库中的汇总 CSV 可直接阅读。
python3 register_reuse_distributed/experiment.py report \
  --plan register_reuse_distributed/batch-6servers/plan.json

# 利用汇总 CSV 及案例原始 stats 复算；加 --plot 需要 matplotlib。
python3 register_reuse_distributed/analyze_results.py
python3 register_reuse_distributed/analyze_results.py --plot
```

第一步在存在未完成任务时退出非零，但仍写出有效结果与失败清单。第二步也会读取 soplex_ref 案例的原始 stats，原始产物需自行提供；已生成的结果和图表包含在仓库中。

# 旧统计口径说明

本目录的 observer schema 为 1。Legacy RegFull 会把很多寄存器容量检查失败归因到 ROB/LSQ 头部等待；因此 RegFull=0 不能证明没有容量压力，原有 shortage 与交集统计也不完整。请使用新 `capacity-*` 目录中 schema=2 的直接检查结果。单消费者完整生命周期比例没有因这次归因修正而失效。

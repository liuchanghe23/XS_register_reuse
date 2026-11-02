/*
 * Copyright (c) 2026
 * All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 */
#ifndef __CPU_O3_REGISTER_PRESSURE_HH__
#define __CPU_O3_REGISTER_PRESSURE_HH__

#include <array>
#include <cstdint>
#include <iosfwd>
#include <vector>

#include "base/statistics.hh"
#include "cpu/inst_seq.hh"
#include "cpu/reg_class.hh"

namespace gem5
{
struct BaseO3CPUParams;
namespace o3
{
class CPU;
class DynInst;

/** Passive, single-thread physical-value lifetime measurements. */
class RegisterPressure : public statistics::Group
{
  public:
    struct ReadPoint
    {
        uint64_t epoch = 0;
        uint64_t cycle = 0;
        std::array<uint64_t, 2> stalls{};
    };

    RegisterPressure(CPU *cpu, const BaseO3CPUParams &params);
    const bool enabled;
    void allocate(PhysRegIdPtr reg, const RegId &arch, InstSeqNum producer);
    void alias(PhysRegIdPtr reg);
    void renamed(DynInst &inst);
    void execute(DynInst &inst);
    void commit(const DynInst &inst);
    void release(PhysRegIdPtr reg);
    void stall(const std::array<unsigned, 4> &free,
               const std::array<unsigned, 4> &demand);
    void resetStats() override;
    void preDumpStats() override;

  private:
    struct Value
    {
        bool active = false;
        bool committed = false;
        bool aliased = false;
        bool eligible = false;
        bool selfRedef = false;
        unsigned consumers = 0;
        unsigned archIndex = 0;
        InstSeqNum producer = 0;
        ReadPoint read;
    };
    CPU *cpu;
    const unsigned numIntRegs;
    std::vector<Value> values;
    uint64_t currentEpoch = 1;
    uint64_t lastStallCycle = UINT64_MAX;
    std::array<uint64_t, 2> stallPrefix{};
    std::array<uint64_t, 4> intervalStart{};
    std::array<uint64_t, 4> intervalEnd{};
    std::ostream *trace = nullptr;
    static int valueClass(PhysRegIdPtr reg);
    void flushInterval(unsigned cls);

    statistics::Scalar epoch;
    statistics::Scalar demandStallCycles;
    statistics::Vector shortageCycles;
    statistics::Vector freeAtShortage;
    statistics::Vector allocations;
    statistics::Vector completedValues;
    statistics::Vector unaliasedValues;
    statistics::Vector aliasedValues;
    statistics::Vector zeroConsumerValues;
    statistics::Vector singleConsumerValues;
    statistics::Vector multiConsumerValues;
    statistics::Vector eligibleSingleValues;
    statistics::Vector selfRedefSingleValues;
    statistics::Vector singleHoldCycles;
    statistics::Vector singleStallExposure;
    statistics::Vector eligibleStallExposure;
    statistics::Vector selfRedefStallExposure;
    statistics::Vector singleValuesOverlappingStall;
    statistics::Vector squashedValues;
    statistics::Vector liveValues;
};
} // namespace o3
} // namespace gem5
#endif

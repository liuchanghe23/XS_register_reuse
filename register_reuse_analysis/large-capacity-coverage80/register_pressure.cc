/*
 * Copyright (c) 2026
 * All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 */
#include "cpu/o3/register_pressure.hh"

#include <algorithm>

#include "base/output.hh"
#include "cpu/o3/cpu.hh"
#include "cpu/o3/dyn_inst.hh"
#include "params/BaseO3CPU.hh"

namespace gem5
{
namespace o3
{

RegisterPressure::RegisterPressure(CPU *cpu, const BaseO3CPUParams &params)
    : statistics::Group(cpu, "regPressure"),
      enabled(params.enableRegPressureStats), cpu(cpu),
      numIntRegs(params.numPhysIntRegs),
      values(params.numPhysIntRegs + params.numPhysFloatRegs),
      ADD_STAT(epoch, statistics::units::Count::get(), "Measurement epoch"),
      ADD_STAT(schemaVersion, statistics::units::Count::get(),
               "Observer schema: 2 counts capacity failures independently of attribution"),
      ADD_STAT(demandStallCycles, statistics::units::Cycle::get(),
               "Capacity-check failures with waiting instructions, including other-block overlap"),
      ADD_STAT(standaloneStallCycles, statistics::units::Cycle::get(),
               "Capacity-check failures with demand and no explicit downstream rename block"),
      ADD_STAT(otherBlockedStallCycles, statistics::units::Cycle::get(),
               "Capacity-check failures with demand and simultaneous downstream rename block"),
      ADD_STAT(standaloneShortageCycles, statistics::units::Cycle::get(),
               "Standalone capacity-check failures by deficient register class"),
      ADD_STAT(shortageCycles, statistics::units::Cycle::get(),
               "Capacity-check failures deficient by register class; classes can overlap"),
      ADD_STAT(freeAtShortage, statistics::units::Count::get(),
               "Sum of free registers on class-shortage cycles"),
      ADD_STAT(allocations, statistics::units::Count::get(), "Fresh physical value allocations"),
      ADD_STAT(completedValues, statistics::units::Count::get(),
               "Committed-producer physical values actually freed in this epoch"),
      ADD_STAT(unaliasedValues, statistics::units::Count::get(), "Completed values never aliased"),
      ADD_STAT(aliasedValues, statistics::units::Count::get(), "Completed values ever aliased; excluded from single-use classification"),
      ADD_STAT(zeroConsumerValues, statistics::units::Count::get(), "Unaliased completed values with no committed consumers"),
      ADD_STAT(singleConsumerValues, statistics::units::Count::get(), "Unaliased completed values with one distinct committed consumer"),
      ADD_STAT(multiConsumerValues, statistics::units::Count::get(), "Unaliased completed values with multiple committed consumers"),
      ADD_STAT(eligibleSingleValues, statistics::units::Count::get(), "Single-use values whose consumer freshly allocates a destination of the same class"),
      ADD_STAT(selfRedefSingleValues, statistics::units::Count::get(), "Eligible single-use values whose consumer redefines the producer architectural register"),
      ADD_STAT(singleHoldCycles, statistics::units::Cycle::get(), "Register-cycles from unique consumer last execute proxy to actual release"),
      ADD_STAT(singleStallExposure, statistics::units::Cycle::get(), "Single-use register-cycles overlapping same-class demand RegFull; NOT a cycle fraction"),
      ADD_STAT(eligibleStallExposure, statistics::units::Cycle::get(), "Eligible single-use register-cycles overlapping same-class demand RegFull"),
      ADD_STAT(selfRedefStallExposure, statistics::units::Cycle::get(), "Self-redefining single-use register-cycles overlapping same-class demand RegFull"),
      ADD_STAT(singleValuesOverlappingStall, statistics::units::Count::get(), "Single-use values held through at least one same-class shortage cycle"),
      ADD_STAT(squashedValues, statistics::units::Count::get(), "Fresh values freed without their producer committing"),
      ADD_STAT(liveValues, statistics::units::Count::get(), "Tracked values still allocated at dump; right censored")
{
    panic_if(enabled && params.numThreads != 1,
             "Register-pressure lifetime tracking currently requires one thread");
    const char *names[] = {"int", "float", "vector", "misc"};
    for (auto *v : {&shortageCycles, &freeAtShortage,
                    &standaloneShortageCycles}) {
        v->init(4);
        for (unsigned i = 0; i < 4; ++i)
            v->subname(i, names[i]);
    }
    for (auto *v : {&allocations, &completedValues, &unaliasedValues,
                   &aliasedValues, &zeroConsumerValues, &singleConsumerValues,
                   &multiConsumerValues, &eligibleSingleValues,
                   &selfRedefSingleValues, &singleHoldCycles,
                   &singleStallExposure, &eligibleStallExposure,
                   &selfRedefStallExposure, &singleValuesOverlappingStall,
                   &squashedValues, &liveValues}) {
        v->init(2);
        for (unsigned i = 0; i < 2; ++i)
            v->subname(i, names[i]);
    }
    if (enabled && !params.regPressureTrace.empty()) {
        trace = simout.create(params.regPressureTrace)->stream();
        *trace << "kind,epoch,class,start_cycle,end_cycle,eligible,self_redef\n";
    }
}

int
RegisterPressure::valueClass(PhysRegIdPtr reg)
{
    if (reg && reg->is(IntRegClass))
        return 0;
    if (reg && reg->is(FloatRegClass))
        return 1;
    return -1;
}

void
RegisterPressure::allocate(PhysRegIdPtr reg, const RegId &arch,
                           InstSeqNum producer)
{
    if (!enabled || valueClass(reg) < 0)
        return;
    auto &v = values.at(reg->flatIndex());
    v = Value{};
    v.active = true;
    v.producer = producer;
    v.archIndex = arch.index();
    ++allocations[valueClass(reg)];
}

void
RegisterPressure::alias(PhysRegIdPtr reg)
{
    if (enabled && valueClass(reg) >= 0)
        values.at(reg->flatIndex()).aliased = true;
}

void
RegisterPressure::renamed(DynInst &inst)
{
    if (!enabled)
        return;
    // Store-address/data splitting subsequently replaces one source with an
    // invalid ID. Preserve the architectural instruction's original sources.
    for (unsigned i = 0; i < inst.numSrcRegs(); ++i)
        inst.regPressureSources.push_back(inst.renamedSrcIdx(i));
}

void
RegisterPressure::execute(DynInst &inst)
{
    if (!enabled)
        return;
    // Last execution attempt is a conservative operand-use proxy for replayed
    // instructions. Elided instructions without Execute use commit instead.
    const ReadPoint point{currentEpoch, uint64_t(cpu->curCycle()), stallPrefix};
    inst.regPressureRead = point;
    if (inst.isSplitStoreData())
        inst.sqIt->instruction()->regPressureRead = point;
}

void
RegisterPressure::commit(const DynInst &inst)
{
    if (!enabled)
        return;
    for (unsigned i = 0; i < inst.regPressureSources.size(); ++i) {
        auto reg = inst.regPressureSources[i];
        const int cls = valueClass(reg);
        if (cls < 0)
            continue;
        bool duplicate = false;
        for (unsigned j = 0; j < i; ++j)
            duplicate |= reg == inst.regPressureSources[j];
        if (duplicate)
            continue;
        auto &v = values.at(reg->flatIndex());
        if (!v.active)
            continue;
        // Saturation preserves zero/one/many classification.
        v.consumers = std::min(v.consumers + 1, 2u);
        if (v.consumers != 1)
            continue;
        v.read = inst.regPressureRead;
        if (v.read.epoch != currentEpoch)
            v.read = {currentEpoch, uint64_t(cpu->curCycle()), stallPrefix};
        for (unsigned d = 0; d < inst.numDestRegs(); ++d) {
            auto dst = inst.renamedDestIdx(d);
            if (valueClass(dst) != cls)
                continue;
            const auto &dv = values.at(dst->flatIndex());
            if (!dv.active || dv.producer != inst.seqNum)
                continue;
            v.eligible = true;
            v.selfRedef |= inst.flattenedDestIdx(d).index() == v.archIndex;
        }
    }
    for (unsigned d = 0; d < inst.numDestRegs(); ++d) {
        auto reg = inst.renamedDestIdx(d);
        if (valueClass(reg) < 0)
            continue;
        auto &v = values.at(reg->flatIndex());
        if (v.active && v.producer == inst.seqNum)
            v.committed = true;
    }
}

void
RegisterPressure::release(PhysRegIdPtr reg)
{
    if (!enabled || valueClass(reg) < 0)
        return;
    const int cls = valueClass(reg);
    auto &v = values.at(reg->flatIndex());
    if (!v.active)
        return;
    v.active = false;
    if (!v.committed) {
        ++squashedValues[cls];
        return;
    }
    ++completedValues[cls];
    if (v.aliased) {
        ++aliasedValues[cls];
        return;
    }
    ++unaliasedValues[cls];
    if (v.consumers == 0) {
        ++zeroConsumerValues[cls];
        return;
    }
    if (v.consumers != 1) {
        ++multiConsumerValues[cls];
        return;
    }
    ++singleConsumerValues[cls];
    const uint64_t now = cpu->curCycle();
    const uint64_t overlap = stallPrefix[cls] - v.read.stalls[cls];
    singleHoldCycles[cls] += now - v.read.cycle;
    singleStallExposure[cls] += overlap;
    if (v.eligible) {
        ++eligibleSingleValues[cls];
        eligibleStallExposure[cls] += overlap;
    }
    if (v.selfRedef) {
        ++selfRedefSingleValues[cls];
        selfRedefStallExposure[cls] += overlap;
    }
    if (overlap) {
        ++singleValuesOverlappingStall[cls];
        if (trace) {
            *trace << "value," << currentEpoch << ',' << cls << ','
                   << v.read.cycle << ',' << now << ','
                   << v.eligible << ',' << v.selfRedef << '\n';
        }
    }
}

void
RegisterPressure::flushInterval(unsigned cls)
{
    if (trace && intervalEnd[cls] > intervalStart[cls]) {
        *trace << "stall," << currentEpoch << ',' << cls << ','
               << intervalStart[cls] << ',' << intervalEnd[cls]
               << ",0,0\n";
    }
    intervalStart[cls] = intervalEnd[cls] = 0;
}

void
RegisterPressure::stall(const std::array<unsigned, 4> &free,
                        const std::array<unsigned, 4> &demand,
                        bool other_block)
{
    if (!enabled)
        return;
    const uint64_t now = cpu->curCycle();
    if (lastStallCycle == now)
        return;
    lastStallCycle = now;
    ++demandStallCycles;
    if (other_block)
        ++otherBlockedStallCycles;
    else
        ++standaloneStallCycles;
    for (unsigned cls = 0; cls < 4; ++cls) {
        if (free[cls] >= demand[cls])
            continue;
        ++shortageCycles[cls];
        if (!other_block)
            ++standaloneShortageCycles[cls];
        freeAtShortage[cls] += free[cls];
        if (cls < 2)
            ++stallPrefix[cls];
        if (intervalEnd[cls] != now) {
            flushInterval(cls);
            intervalStart[cls] = now;
        }
        intervalEnd[cls] = now + 1;
    }
}

void
RegisterPressure::resetStats()
{
    statistics::Group::resetStats();
    ++currentEpoch;
    std::fill(values.begin(), values.end(), Value{});
    stallPrefix = {};
    intervalStart = intervalEnd = {};
    lastStallCycle = UINT64_MAX;
}

void
RegisterPressure::preDumpStats()
{
    statistics::Group::preDumpStats();
    epoch = currentEpoch;
    schemaVersion = 2;
    for (unsigned c = 0; c < 4; ++c)
        flushInterval(c);
    for (unsigned c = 0; c < 2; ++c)
        liveValues[c] = 0;
    // INT and FP occupy consecutive flat-index ranges in PhysRegFile.
    for (unsigned i = 0; i < values.size(); ++i) {
        if (values[i].active)
            ++liveValues[i < numIntRegs ? 0 : 1];
    }
    if (trace)
        trace->flush();
}

} // namespace o3
} // namespace gem5

/* SPDX-License-Identifier: BSD-3-Clause */
#include "cpu/o3/register_reuse.hh"

#include <algorithm>
#include <set>

#include "cpu/o3/cpu.hh"
#include "cpu/o3/dyn_inst.hh"
#include "cpu/o3/issue_queue.hh"
#include "cpu/o3/rename_map.hh"
#include "cpu/o3/scoreboard.hh"
#include "params/BaseO3CPU.hh"

namespace gem5::o3
{
RegisterReuse::RegisterReuse(CPU *cpu, const BaseO3CPUParams &p)
    : statistics::Group(cpu, "regReuse"), enabled(p.enableRegisterReuse),
      cpu(cpu), numInt(p.numPhysIntRegs), numFloat(p.numPhysFloatRegs),
      shadows(p.regReuseShadowCopies), repairLatency(p.regReuseRepairLatency),
      recoveryLatency(p.regReuseRecoveryLatency), prediction(p.regReusePrediction),
      slots(enabled ? numInt + numFloat : 0),
      predictor(p.regReusePredictorEntries, 1),
      ADD_STAT(allocatedSlots, statistics::units::Count::get(), "Fresh scalar physical slots allocated"),
      ADD_STAT(sharedVersions, statistics::units::Count::get(), "Destination allocations avoided by source-slot reuse"),
      ADD_STAT(deterministicReuses, statistics::units::Count::get(), "First consumer redefines the same architectural register"),
      ADD_STAT(predictedReuses, statistics::units::Count::get(), "Predicted single-consumer cross-register reuses"),
      ADD_STAT(predictionMisses, statistics::units::Count::get(), "Previously shared versions subsequently encountering another consumer"),
      ADD_STAT(repairCopies, statistics::units::Count::get(), "Shadow values copied into fresh temporary source slots"),
      ADD_STAT(repairWaitCycles, statistics::units::Cycle::get(), "Rename waits for repair latency or source readiness"),
      ADD_STAT(aliasRejects, statistics::units::Count::get(), "Reuse candidates rejected because of register aliases"),
      ADD_STAT(versionLimitRejects, statistics::units::Count::get(), "First-use candidates with no unused shadow version"),
      ADD_STAT(squashEvents, statistics::units::Count::get(), "Squashes discarding reuse metadata"),
      ADD_STAT(restoredGroups, statistics::units::Count::get(), "Shared physical groups requiring old-version recovery"),
      ADD_STAT(returnedSlots, statistics::units::Count::get(), "Slots returned only after every live version is released")
{
    if (!enabled) return;
    panic_if(p.numThreads != 1, "Register reuse currently supports single-thread CPUs only");
    panic_if(shadows < 1 || shadows > 3, "Register reuse requires 1..3 shadow copies");
    panic_if(!p.regReusePredictorEntries, "Register reuse requires a nonempty predictor");
    panic_if(!repairLatency || !recoveryLatency, "Register reuse repair/recovery latency must be positive");
    panic_if(p.enableRegPressureStats, "The passive register-pressure observer must be disabled with register reuse");
    panic_if(p.RobCompressPolicy != ROBCompressPolicy::none,
             "Register reuse currently requires an uncompressed ROB");
    panic_if(p.enableConstantFolding || p.enableMovImmElimination || p.valuePred,
             "Register reuse does not support constant folding, immediate elimination or value prediction");
}

int
RegisterReuse::slotIndex(PhysRegIdPtr reg) const
{
    if (!reg) return -1;
    reg = reg->getReuseBase();
    if (reg->is(IntRegClass)) return reg->index();
    if (reg->is(FloatRegClass)) return numInt + reg->index();
    return -1;
}
ReuseSlot &RegisterReuse::slot(PhysRegIdPtr reg)
{ return slots.at(slotIndex(reg)); }
const ReuseSlot &RegisterReuse::slot(PhysRegIdPtr reg) const
{ return slots.at(slotIndex(reg)); }

void
RegisterReuse::allocated(PhysRegIdPtr reg, const DynInstPtr &inst)
{
    if (!enabled || slotIndex(reg) < 0) return;
    assert(!reg->getReuseVersion());
    slot(reg).allocate(inst->seqNum, inst->getPC());
    ++allocatedSlots;
}

PhysRegIdPtr
RegisterReuse::candidate(const DynInstPtr &inst, UnifiedRenameMap &map,
                         bool count)
{
    if (!enabled || inst->isSquashed() || inst->numDestRegs() != 1 ||
        inst->isVector() || inst->isMicroop() || inst->isMemRef() ||
        inst->isControl() || inst->isMov() || inst->isNonSpeculative())
        return nullptr;
    const auto dest = inst->tcBase()->flattenRegId(inst->destRegIdx(0));
    if (!dest.is(IntRegClass) && !dest.is(FloatRegClass)) return nullptr;
    if (inst->destRegIdx(0).getNumPinnedWrites()) return nullptr;
    for (unsigned i = 0; i < inst->numSrcRegs(); ++i) {
        const auto src = inst->tcBase()->flattenRegId(inst->srcRegIdx(i));
        if (src.classValue() != dest.classValue()) continue;
        const VirtRegId virt = map.lookup(src);
        auto reg = virt.PhyReg();
        if (virt.IEOper() || slotIndex(reg) < 0 || reg->isPinned()) continue;
        auto &s = slot(reg);
        const unsigned version = reg->getReuseVersion();
        if (!s.versions[version].live || s.versions[version].reads ||
            s.versions[version].committedReads ||
            version != s.current()) continue;
        if (reg->getRef() != 1) {
            if (count) ++aliasRejects;
            continue;
        }
        if (s.highWater >= shadows) {
            if (count) ++versionLimitRejects;
            continue;
        }
        const bool certain = src == dest;
        const auto pc = s.versions[version].pc;
        if (!certain && (!prediction || predictor[(pc >> 2) % predictor.size()] < 2))
            continue;
        return reg;
    }
    return nullptr;
}

PhysRegIdPtr
RegisterReuse::reuse(PhysRegIdPtr source, const DynInstPtr &inst)
{
    auto &s = slot(source);
    assert(s.canReuse(source->getReuseVersion(), shadows));
    bool certain = false;
    const auto dest = inst->tcBase()->flattenRegId(inst->destRegIdx(0));
    for (unsigned i = 0; i < inst->numSrcRegs(); ++i) {
        const auto src = inst->tcBase()->flattenRegId(inst->srcRegIdx(i));
        if (src == dest && inst->renamedSrcIdx(i) == source) certain = true;
    }
    const unsigned next = s.reuse(inst->seqNum, inst->getPC());
    auto result = cpu->getRegFile()->reuseId(source, next);
    assert(!result->getRef());
    result->incRef();
    result->setNumPinnedWrites(0);
    result->setNumPinnedWritesToComplete(1);
    ++sharedVersions;
    if (certain) ++deterministicReuses;
    else ++predictedReuses;
    return result;
}

bool
RegisterReuse::prepare(const DynInstPtr &inst, UnifiedRenameMap &map,
                       UnifiedFreeList &free, Scoreboard &scoreboard)
{
    if (!enabled) return true;
    std::vector<PhysRegIdPtr> stale;
    for (unsigned i = 0; i < inst->numSrcRegs(); ++i) {
        const auto src = inst->tcBase()->flattenRegId(inst->srcRegIdx(i));
        auto reg = map.lookup(src).PhyReg();
        if (slotIndex(reg) < 0) continue;
        const auto &s = slot(reg);
        if (s.versions[reg->getReuseVersion()].live &&
            reg->getReuseVersion() < s.current() &&
            std::find(stale.begin(), stale.end(), reg) == stale.end())
            stale.push_back(reg);
    }
    if (stale.empty()) { waitingSeq = 0; return true; }
    const uint64_t now = cpu->curCycle();
    if (waitingSeq != inst->seqNum) {
        waitingSeq = inst->seqNum;
        waitingUntil = now + repairLatency * stale.size();
    }
    bool ready = now >= waitingUntil;
    unsigned intNeed = 0, floatNeed = 0;
    for (auto reg : stale) {
        ready &= scoreboard.getReg(reg);
        if (reg->is(IntRegClass)) ++intNeed;
        else ++floatNeed;
    }
    // Preserve enough capacity for the instruction's own normal destinations.
    ready &= free.numFreeRegs(IntRegClass) >= intNeed + inst->numDestRegs(IntRegClass);
    ready &= free.numFreeRegs(FloatRegClass) >= floatNeed + inst->numDestRegs(FloatRegClass);
    if (!ready) { ++repairWaitCycles; return false; }
    auto &event = events[inst->seqNum];
    for (auto old : stale) {
        const auto &v = slot(old).versions[old->getReuseVersion()];
        predictor[(v.pc >> 2) % predictor.size()] = 0;
        if (v.reads + v.committedReads <= 1) ++predictionMisses;
        auto fresh = free.getReg(old->classValue(), inst->threadNumber);
        allocated(fresh, inst);
        // A repair is not an ISA producer; do not train the producer-PC
        // predictor using the temporary's consumer count at release.
        slot(fresh).versions[0].producer = 0;
        // Data is copied only after its original producer is ready. The
        // temporary uses a normal free-list slot and is held until commit or
        // squash; subsequent consumers each repair independently. This is a
        // conservative timing model rather than an uncharged shadow read.
        cpu->setReg(fresh, cpu->peekReg(old));
        scoreboard.setReg(fresh);
        cpu->getIEW()->getScheduler()->setAllScoreBoard(fresh);
        event.repairs.emplace_back(old, fresh);
        ++repairCopies;
    }
    waitingSeq = 0;
    return true;
}

VirtRegId
RegisterReuse::source(const DynInstPtr &inst, VirtRegId original) const
{
    if (!enabled) return original;
    auto event = events.find(inst->seqNum);
    if (event == events.end()) return original;
    for (const auto &[old, fresh] : event->second.repairs) {
        if (old == original.PhyReg()) {
            original.setPhyReg(fresh);
            return original;
        }
    }
    return original;
}

void
RegisterReuse::renamed(const DynInstPtr &inst)
{
    if (!enabled) return;
    auto &event = events[inst->seqNum];
    std::set<PhysRegIdPtr> unique;
    for (unsigned i = 0; i < inst->numSrcRegs(); ++i)
        unique.insert(inst->renamedSrcIdx(i));
    for (const auto &[old, fresh] : event.repairs) unique.insert(old);
    for (auto reg : unique) {
        if (slotIndex(reg) < 0) continue;
        auto &v = slot(reg).versions[reg->getReuseVersion()];
        if (!v.live) continue;
        ++v.reads;
        if (v.reads + v.committedReads > 1) predictor[(v.pc >> 2) % predictor.size()] = 0;
        event.reads.push_back(reg);
    }
}

PhysRegIdPtr
RegisterReuse::release(PhysRegIdPtr reg)
{
    if (!enabled || slotIndex(reg) < 0) return reg;
    auto &s = slot(reg);
    if (!s.versions[reg->getReuseVersion()].live) {
        // Initial architectural registers predate tracking.
        assert(!reg->getReuseVersion());
        return reg;
    }
    s.release(reg->getReuseVersion());
    if (!s.empty()) return nullptr;
    for (const auto &version : s.versions) {
        if (!version.producer) continue;
        auto &entry = predictor[(version.pc >> 2) % predictor.size()];
        entry = version.committedReads == 1 ? std::min<unsigned>(3, entry + 1) : 0;
    }
    ++returnedSlots;
    return reg->getReuseBase();
}

void
RegisterReuse::returnTemporary(PhysRegIdPtr reg)
{
    cpu->getRename()->releaseReuseTemporary(reg);
}

void
RegisterReuse::commit(InstSeqNum seq)
{
    if (!enabled) return;
    for (auto it = events.begin(); it != events.end() && it->first <= seq;) {
        for (auto reg : it->second.reads) {
            auto &v = slot(reg).versions[reg->getReuseVersion()];
            if (v.live) {
                assert(v.reads);
                --v.reads;
                v.committedReads = std::min(2u, v.committedReads + 1);
            }
        }
        for (const auto &[old, fresh] : it->second.repairs) returnTemporary(fresh);
        it = events.erase(it);
    }
}

void
RegisterReuse::squash(InstSeqNum seq)
{
    if (!enabled) return;
    ++squashEvents;
    for (auto it = events.upper_bound(seq); it != events.end();) {
        for (auto reg : it->second.reads) {
            auto &v = slot(reg).versions[reg->getReuseVersion()];
            // Destination ownership is released later by rename history walk.
            if (v.live) { assert(v.reads); --v.reads; }
        }
        for (const auto &[old, fresh] : it->second.repairs) returnTemporary(fresh);
        it = events.erase(it);
    }
    for (unsigned i = 0; i < slots.size(); ++i) {
        const auto &s = slots[i];
        for (unsigned v = 1; v <= s.highWater; ++v) {
            if (s.versions[v].live && s.versions[v].producer > seq) {
                ++restoredGroups;
                recoveryUntil = std::max(recoveryUntil,
                    uint64_t(cpu->curCycle()) + recoveryLatency);
                break;
            }
        }
    }
    waitingSeq = 0;
}

bool RegisterReuse::recovering() const
{ return enabled && uint64_t(cpu->curCycle()) < recoveryUntil; }
} // namespace gem5::o3

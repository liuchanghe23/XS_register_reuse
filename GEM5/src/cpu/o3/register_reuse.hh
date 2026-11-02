/* SPDX-License-Identifier: BSD-3-Clause */
#ifndef __CPU_O3_REGISTER_REUSE_HH__
#define __CPU_O3_REGISTER_REUSE_HH__
#include <map>
#include <vector>
#include "base/statistics.hh"
#include "cpu/inst_seq.hh"
#include "cpu/o3/dyn_inst_ptr.hh"
#include "cpu/o3/register_reuse_state.hh"
#include "cpu/o3/regfile.hh"

namespace gem5
{
struct BaseO3CPUParams;
namespace o3
{
class CPU;
class UnifiedRenameMap;
class UnifiedFreeList;
class Scoreboard;

/** Bounded scalar INT/FP sharing with version tags and shadow values. */
class RegisterReuse : public statistics::Group
{
  public:
    RegisterReuse(CPU *cpu, const BaseO3CPUParams &params);
    const bool enabled;
    PhysRegIdPtr candidate(const DynInstPtr &inst, UnifiedRenameMap &map,
                           bool count = false);
    PhysRegIdPtr reuse(PhysRegIdPtr source, const DynInstPtr &inst);
    void allocated(PhysRegIdPtr reg, const DynInstPtr &inst);
    void renamed(const DynInstPtr &inst);
    PhysRegIdPtr release(PhysRegIdPtr reg);
    bool prepare(const DynInstPtr &inst, UnifiedRenameMap &map,
                 UnifiedFreeList &free, Scoreboard &scoreboard);
    VirtRegId source(const DynInstPtr &inst, VirtRegId original) const;
    void commit(InstSeqNum seq);
    void squash(InstSeqNum seq);
    bool recovering() const;

  private:
    struct Event {
        std::vector<PhysRegIdPtr> reads;
        std::vector<std::pair<PhysRegIdPtr, PhysRegIdPtr>> repairs;
    };
    CPU *cpu;
    unsigned numInt, numFloat, shadows, repairLatency, recoveryLatency;
    bool prediction;
    std::vector<ReuseSlot> slots;
    std::vector<uint8_t> predictor;
    std::map<InstSeqNum, Event> events;
    InstSeqNum waitingSeq = 0;
    uint64_t waitingUntil = 0, recoveryUntil = 0;
    int slotIndex(PhysRegIdPtr reg) const;
    ReuseSlot &slot(PhysRegIdPtr reg);
    const ReuseSlot &slot(PhysRegIdPtr reg) const;
    void returnTemporary(PhysRegIdPtr reg);

    statistics::Scalar allocatedSlots;
    statistics::Scalar sharedVersions;
    statistics::Scalar deterministicReuses;
    statistics::Scalar predictedReuses;
    statistics::Scalar predictionMisses;
    statistics::Scalar repairCopies;
    statistics::Scalar repairWaitCycles;
    statistics::Scalar aliasRejects;
    statistics::Scalar versionLimitRejects;
    statistics::Scalar squashEvents;
    statistics::Scalar restoredGroups;
    statistics::Scalar returnedSlots;
};
} // namespace o3
} // namespace gem5
#endif

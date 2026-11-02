/* SPDX-License-Identifier: BSD-3-Clause */
#ifndef __CPU_O3_REGISTER_REUSE_STATE_HH__
#define __CPU_O3_REGISTER_REUSE_STATE_HH__
#include <array>
#include <cassert>
#include <cstdint>

namespace gem5::o3
{
/** Monotonic version numbers: a squash cannot cause tag ABA within a slot. */
struct ReuseSlot
{
    struct Version {
        bool live = false;
        unsigned reads = 0;
        uint64_t producer = 0;
        uint64_t pc = 0;
        unsigned committedReads = 0; // Saturates at two; reads counts in-flight tokens only.
    };
    std::array<Version, 4> versions{};
    unsigned highWater = 0;

    void allocate(uint64_t producer, uint64_t pc)
    {
        assert(empty());
        *this = ReuseSlot{};
        versions[0] = {true, 0, producer, pc};
    }
    bool empty() const
    {
        for (const auto &v : versions)
            if (v.live) return false;
        return true;
    }
    unsigned current() const
    {
        for (unsigned v = highWater; v > 0; --v)
            if (versions[v].live) return v;
        return 0;
    }
    bool canReuse(unsigned version, unsigned shadows) const
    {
        return versions[version].live && !versions[version].reads &&
               !versions[version].committedReads &&
               version == current() && highWater < shadows;
    }
    unsigned reuse(uint64_t producer, uint64_t pc)
    {
        assert(highWater < 3);
        const unsigned v = ++highWater;
        assert(!versions[v].live);
        versions[v] = {true, 0, producer, pc};
        return v;
    }
    void release(unsigned version)
    {
        assert(versions[version].live);
        versions[version].live = false;
    }
};
} // namespace gem5::o3
#endif

/* SPDX-License-Identifier: BSD-3-Clause */
#include <gtest/gtest.h>
#include "cpu/o3/register_reuse_state.hh"
using gem5::o3::ReuseSlot;

TEST(RegisterReuseState, DistinctVersionsAndBoundedShadows)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    EXPECT_TRUE(s.canReuse(0, 3));
    EXPECT_EQ(s.reuse(11, 0x8004), 1);
    EXPECT_FALSE(s.canReuse(0, 3));
    EXPECT_EQ(s.reuse(12, 0x8008), 2);
    EXPECT_EQ(s.reuse(13, 0x800c), 3);
    EXPECT_FALSE(s.canReuse(3, 3));
    EXPECT_EQ(s.versions[0].producer, 10);
    EXPECT_EQ(s.versions[3].producer, 13);
}

TEST(RegisterReuseState, SquashNeverReusesDependencyTag)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    s.reuse(11, 0x8004);
    s.release(1);
    EXPECT_EQ(s.current(), 0);
    EXPECT_TRUE(s.canReuse(0, 3));
    EXPECT_EQ(s.reuse(12, 0x8008), 2);
    EXPECT_EQ(s.highWater, 2);
}

TEST(RegisterReuseState, SlotCannotBeReturnedWithAnOlderLiveVersion)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    s.reuse(11, 0x8004);
    s.release(1);
    EXPECT_FALSE(s.empty());
    s.release(0);
    EXPECT_TRUE(s.empty());
    s.allocate(12, 0x9000);
    EXPECT_EQ(s.highWater, 0);
}

TEST(RegisterReuseState, PriorConsumerDisqualifiesReuse)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    ++s.versions[0].reads;
    EXPECT_FALSE(s.canReuse(0, 3));
    --s.versions[0].reads;
    EXPECT_TRUE(s.canReuse(0, 3));
}

TEST(RegisterReuseState, OneShadowIsAHardCapacityLimit)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    s.reuse(11, 0x8004);
    EXPECT_FALSE(s.canReuse(1, 1));
    s.release(0);
    EXPECT_FALSE(s.canReuse(1, 1));
}

TEST(RegisterReuseState, CommittedReadPreventsReuseAfterSpeculativeTokenRetires)
{
    ReuseSlot s;
    s.allocate(10, 0x8000);
    s.versions[0].committedReads = 1;
    EXPECT_FALSE(s.canReuse(0, 3));
    ++s.versions[0].reads;
    --s.versions[0].reads;
    EXPECT_FALSE(s.canReuse(0, 3));
}

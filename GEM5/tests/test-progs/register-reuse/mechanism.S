/* SPDX-License-Identifier: BSD-3-Clause */
/* Deterministic reuse witness; TEST_MULTI_CONSUMER is the negative control. */
.option norvc
.option norelax
.section .text
.global _start
.global int_chain_begin, int_chain_end, fp_chain_begin, fp_chain_end
_start:
    la t0, fail
    csrw mtvec, t0
    li t0, 0x6000
    csrs mstatus, t0
    li s0, 0x80010000
    li s1, 17
    li t0, 0x3ff0000000000000
    fmv.d.x f8, t0

int_chain_begin:
    .rept 64
#ifdef TEST_MULTI_CONSUMER
    /* A distinct earlier consumer must disqualify the following self-write. */
    sd s1, 0(s0)
#endif
    addi s1, s1, 1
    .endr
int_chain_end:

fp_chain_begin:
    .rept 16
#ifdef TEST_MULTI_CONSUMER
    fsd f8, 8(s0)
#endif
    /* Two equal operands are one dynamic consumer, not two consumers. */
    fadd.d f8, f8, f8
    .endr
fp_chain_end:
    fence rw, rw
    li t0, 81
    bne s1, t0, fail
    fmv.x.d t1, f8
    li t0, 0x40f0000000000000 /* 2^16 = 65536.0 */
    bne t1, t0, fail
#ifdef TEST_MULTI_CONSUMER
    /* The prior consumers must really observe the old, not overwritten, values. */
    ld t1, 0(s0)
    li t0, 80
    bne t1, t0, fail
    ld t1, 8(s0)
    li t0, 0x40e0000000000000 /* 2^15 = 32768.0 */
    bne t1, t0, fail
#endif
    li a0, 0
    .word 0x0000006b
fail:
    j fail

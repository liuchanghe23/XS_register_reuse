/* SPDX-License-Identifier: BSD-3-Clause */
/* Prior consumer commits while enough unrelated instructions pass rename. */
.option norvc
.section .text
.global _start
_start:
    la t0, fail
    csrw mtvec, t0
loop:
    li s1, 17
    add s2, s1, s1
    .rept 128
    nop
    .endr
    addi s1, s1, 1
    li t0, 18
    bne s1, t0, fail
    li t0, 34
    bne s2, t0, fail
    j loop
fail:
    j fail

/* Scalar version, alias, replay-source, branch and precise-trap regression. */
.option norvc
.section .text
.global _start
_start:
    la t0, trap
    csrw mtvec, t0
    csrw medeleg, zero
    li t0, -1
    csrw pmpaddr0, t0
    li t0, 0xf
    csrw pmpcfg0, t0
    li t0, 0x6000
    csrs mstatus, t0
    li s10, 0
    li s9, 64
again:
    /* Reuse more than the two-bit version limit. */
    li s1, 17
    .rept 12
    addi s1, s1, 1
    .endr
    li t0, 29
    bne s1, t0, fail

    /* Train a stable single-use producer, then add an unexpected consumer. */
    li s8, 8
train_prediction:
    li s1, 17
    addi s2, s1, 3
    beqz s8, extra_consumer
    li s1, 0
    addi s8, s8, -1
    j train_prediction
extra_consumer:
    add s3, s1, s2
    li t0, 37
    bne s3, t0, fail

    /* A second consumer must recover the old source, including duplicate src. */
    li s1, 17
    addi s2, s1, 3
    add s3, s1, s2
    li t0, 37
    bne s3, t0, fail
    li t0, 17
    bne s1, t0, fail

    /* Move aliases must not permit destructive sharing. */
    li s1, 29
    mv s2, s1
    addi s1, s1, 1
    li t0, 29
    bne s2, t0, fail
    li t0, 30
    bne s1, t0, fail

    /* Store data and load-address source lifetimes survive split/replay. */
    li s0, 0x80010000
    li s1, 41
    addi s2, s1, 1
    sd s1, 0(s0)
    ld s3, 0(s0)
    li t0, 41
    bne s3, t0, fail
    addi s4, s0, 8
    ld s5, 0(s0)
    bne s5, t0, fail

    /* A delayed older store aliases a younger speculative load result. */
    li t0, 11
    sd t0, 0(s0)
    fence rw, rw
    li t2, 0x880110000
    li t1, 17
    li t4, 19
    div t3, t2, t1
    sd t4, 0(t3)
    ld s1, 0(s0)
    addi s1, s1, 1
    li t0, 20
    bne s1, t0, fail

    /* An unresolved branch lets younger instructions overwrite speculatively. */
    li s1, 57
    li t0, 1234567
    li t1, 17
    div t2, t0, t1
    li t3, 72621
    beq t2, t3, taken
    addi s1, s1, 100
    addi s1, s1, 100
    j fail
 taken:
    li t0, 57
    bne s1, t0, fail

    /* Preserve the producer's value at an older precise exception boundary. */
    li s1, 71
    li s11, 71
    li t0, 0x3ff0000000000000
    fmv.d.x f10, t0
fault_pc:
    .word 0xffffffff
    addi s1, s1, 1
    fadd.d f10, f10, f10
    li t0, 72
    bne s1, t0, fail

    /* FP versions, cross-register repair, and same-instruction source dedup. */
    li t0, 0x3ff0000000000000
    fmv.d.x f0, t0
    .rept 4
    fadd.d f0, f0, f0
    .endr
    fmv.x.d t1, f0
    li t2, 0x4030000000000000
    bne t1, t2, fail
    fmv.d.x f4, t0
    fadd.d f5, f4, f4
    fadd.d f6, f4, f5
    fmv.x.d t1, f6
    li t2, 0x4008000000000000
    bne t1, t2, fail

    addi s9, s9, -1
    bnez s9, again
    li t0, 64
    bne s10, t0, fail
    li a0, 0
    .word 0x0000006b
fail:
    j fail
.balign 4
trap:
    bne s1, s11, fail
    fmv.x.d t2, f10
    li t1, 0x3ff0000000000000
    bne t2, t1, fail
    csrr t0, mcause
    li t1, 2
    bne t0, t1, fail
    csrr t0, mepc
    la t1, fault_pc
    bne t0, t1, fail
    addi t0, t0, 4
    csrw mepc, t0
    addi s10, s10, 1
    mret

.option norvc
.section .text
.global _start
_start:
    li x9, 0x5b2238cc79c335f3
    li x10, 0x2172853571ff4776
    li x11, 0x7673735f314fd416
    li x12, 0x76dd059c87d87aca
    li x13, 0xfe37290580ca8915
    li x14, 0xfee45de4338566ae
    li x15, 0x969354327ae05aec
    li x16, 0x199309fdd4e58f34
    li x17, 0x13afae76d86da9da
    li x18, 0xaeb678c3a2442c02
    li x19, 0x049326f9f1c7966b
    li x20, 0x706b400b0424b922
    li x21, 0xa72e5a630272ffd8
    li x22, 0xf91b92f3942a36f7
    li x23, 0x2632252ca2045619
    addi x9, x9, 1111
    xor x11, x17, x10
    sll x15, x15, x17
    sub x20, x19, x12
    sub x19, x15, x14
    or x9, x9, x14
    and x15, x15, x12
    xor x22, x22, x23
    addi x14, x14, -442
    sll x17, x9, x12
    sub x19, x19, x22
    or x19, x14, x17
    li t6, 0x80010000
    sd x11, 64(t6)
    and x21, x13, x22
    li t6, 0x80010000
    ld x13, 64(t6)
    xor x17, x17, x21
    li t6, 0x80010000
    sd x15, 72(t6)
    xor x9, x21, x15
    li t6, 0x80010000
    ld x16, 64(t6)
    li t6, 0x80010000
    sd x22, 40(t6)
    srl x21, x21, x19
    sub x12, x12, x20
    add x9, x9, x9
    or x13, x9, x11
    sub x22, x22, x21
    add x15, x15, x19
    li t6, 0x80010000
    ld x11, 72(t6)
    xor x13, x14, x21
    sub x10, x10, x19
    addi x18, x15, -815
    xor x16, x16, x15
    add x20, x14, x14
    sll x23, x23, x10
    addi x11, x11, 931
    srl x12, x21, x20
    srl x20, x20, x10
    xor x17, x9, x13
    or x13, x22, x9
    xor x23, x15, x21
    and x11, x10, x13
    sub x22, x22, x16
    sub x20, x15, x21
    xor x11, x21, x21
    and x15, x15, x12
    li t6, 0x80010000
    sd x16, 64(t6)
    li t6, 0x80010000
    sd x21, 112(t6)
    li t6, 0x80010000
    ld x18, 72(t6)
    sll x13, x17, x14
    srl x17, x17, x17
    sub x9, x20, x17
    li t6, 0x80010000
    ld x16, 64(t6)
    sub x14, x12, x13
    li t6, 0x80010000
    sd x22, 88(t6)
    sll x21, x21, x19
    or x11, x17, x21
    add x18, x10, x10
    li t6, 0x80010000
    ld x11, 112(t6)
    sub x14, x14, x21
    add x19, x15, x10
    srl x23, x23, x11
    srl x20, x16, x19
    add x10, x10, x18
    sll x12, x12, x10
    srl x16, x14, x14
    srl x19, x19, x19
    srl x20, x14, x15
    srl x15, x18, x22
    xor x18, x10, x11
    li t6, 0x80010000
    ld x10, 112(t6)
    sub x22, x22, x21
    or x9, x15, x17
    sub x17, x16, x14
    or x13, x22, x10
    li t6, 0x80010000
    sd x14, 48(t6)
    li t6, 0x80010000
    sd x21, 88(t6)
    and x19, x19, x9
    li t6, 0x80010000
    sd x12, 120(t6)
    or x10, x10, x18
    or x22, x22, x14
    srl x16, x11, x10
    li t6, 0x80010000
    ld x16, 48(t6)
    li t6, 0x80010000
    sd x15, 8(t6)
    and x13, x15, x19
    or x18, x18, x23
    srl x10, x10, x23
    li t6, 0x80010000
    sd x10, 0(t6)
    sub x13, x13, x18
    sll x10, x10, x17
    and x20, x11, x14
    and x22, x14, x17
    li t6, 0x80010000
    ld x19, 40(t6)
    srl x12, x12, x19
    addi x18, x13, 764
    or x20, x20, x16
    sll x20, x22, x13
    sll x19, x19, x15
    and x12, x17, x11
    addi x13, x12, 21
    li t6, 0x80010000
    sd x13, 120(t6)
    and x14, x9, x18
    sll x16, x10, x17
    xor x22, x13, x21
    addi x17, x22, -1523
    or x19, x19, x17
    li t6, 0x80010000
    ld x12, 40(t6)
    sub x14, x18, x14
    add x10, x18, x19
    sub x14, x14, x20
    sub x11, x11, x11
    or x12, x12, x14
    xor x13, x13, x14
    addi x20, x22, -1461
    srl x16, x16, x10
    and x11, x11, x14
    addi x15, x15, 710
    sub x22, x22, x18
    and x14, x9, x10
    xor x12, x17, x10
    and x23, x23, x14
    li t6, 0x80010000
    sd x20, 88(t6)
    sll x18, x18, x12
    sub x13, x23, x10
    add x22, x14, x23
    xor x10, x19, x10
    sub x17, x17, x17
    li t6, 0x80010000
    sd x15, 88(t6)
    srl x11, x13, x12
    and x23, x23, x21
    and x16, x16, x19
    or x18, x19, x21
    add x20, x16, x20
    sll x19, x19, x12
    or x22, x22, x23
    and x15, x15, x14
    xor x20, x18, x22
    xor x9, x9, x19
    li t6, 0x80010000
    sd x16, 32(t6)
    and x13, x12, x9
    srl x12, x12, x13
    li t6, 0x80010000
    ld x18, 64(t6)
    xor x21, x21, x18
    add x14, x19, x11
    add x22, x22, x17
    li t6, 0x80010000
    sd x22, 104(t6)
    xor x13, x13, x14
    li t6, 0x80010000
    ld x17, 8(t6)
    li t6, 0x80010000
    sd x22, 80(t6)
    sub x9, x9, x18
    sll x9, x11, x19
    and x13, x13, x17
    sll x19, x19, x20
    li t6, 0x80010000
    sd x9, 0(t6)
    li t6, 0x80010000
    sd x20, 64(t6)
    srl x17, x15, x21
    add x19, x19, x9
    or x16, x11, x13
    sll x11, x11, x10
    li t6, 0x80010000
    sd x13, 8(t6)
    sub x16, x21, x22
    addi x10, x19, 1309
    sub x21, x13, x12
    or x21, x21, x23
    and x23, x12, x16
    addi x9, x9, 1485
    xor x22, x15, x12
    xor x11, x11, x18
    add x18, x18, x10
    sll x16, x16, x23
    sll x18, x21, x19
    or x12, x9, x21
    addi x17, x17, -748
    add x10, x10, x15
    srl x21, x12, x17
    li t6, 0x80010000
    ld x19, 112(t6)
    or x12, x12, x23
    sll x20, x18, x23
    li t6, 0x80010000
    ld x18, 72(t6)
    add x13, x13, x23
    or x15, x13, x18
    sub x11, x18, x13
    addi x23, x13, 287
    xor x19, x14, x11
    sub x20, x20, x18
    sll x20, x20, x11
    add x19, x22, x9
    sll x22, x10, x20
    and x10, x22, x16
    or x13, x17, x17
    or x19, x17, x23
    srl x17, x17, x18
    xor x22, x12, x12
    and x20, x10, x22
    add x21, x21, x20
    or x11, x19, x21
    sub x17, x20, x14
    add x19, x19, x21
    sub x17, x22, x14
    sub x13, x16, x17
    sll x21, x14, x9
    addi x23, x18, 756
    li t6, 0x80010000
    sd x10, 24(t6)
    or x13, x13, x11
    and x13, x13, x21
    sll x19, x19, x17
    or x11, x22, x21
    addi x17, x17, 642
    li t6, 0x80010000
    ld x18, 112(t6)
    sub x22, x11, x12
    and x21, x21, x20
    sll x11, x22, x9
    xor x10, x12, x15
    or x14, x15, x17
    li t6, 0x80010000
    ld x11, 64(t6)
    li t6, 0x80010000
    ld x12, 0(t6)
    li t6, 0x80010000
    sd x22, 48(t6)
    add x21, x21, x12
    li t6, 0x80010000
    ld x19, 40(t6)
    srl x13, x15, x21
    srl x19, x10, x12
    li t6, 0x80010000
    ld x22, 8(t6)
    addi x21, x22, 12
    or x22, x22, x20
    li t6, 0x80010000
    sd x17, 40(t6)
    li t6, 0x80010000
    sd x23, 56(t6)
    xor x23, x23, x13
    addi x12, x23, 345
    add x23, x23, x23
    sll x22, x19, x16
    xor x19, x20, x11
    addi x17, x21, 884
    sll x18, x20, x13
    xor x20, x20, x14
    sub x13, x9, x18
    add x20, x20, x16
    addi x21, x21, -2004
    sll x11, x11, x19
    and x18, x18, x9
    add x11, x15, x16
    and x16, x16, x11
    addi x23, x23, -193
    li t6, 0x80010000
    sd x21, 80(t6)
    and x18, x18, x18
    and x16, x14, x12
    xor x22, x14, x23
    or x9, x19, x22
    li t6, 0x80010000
    sd x11, 0(t6)
    sub x12, x10, x16
    or x23, x23, x9
    li t6, 0x80010000
    sd x12, 8(t6)
    add x15, x14, x22
    add x15, x12, x17
    add x17, x17, x10
    xor x9, x9, x17
    li t6, 0x80010000
    ld x12, 64(t6)
    and x12, x9, x21
    sll x11, x11, x16
    sll x22, x14, x14
    li t6, 0x80010000
    sd x18, 48(t6)
    xor x19, x19, x14
    sll x22, x22, x14
    sll x17, x22, x19
    li t6, 0x80010000
    sd x18, 64(t6)
    addi x14, x23, -573
    li t6, 0x80010000
    sd x17, 72(t6)
    xor x14, x21, x9
    xor x17, x23, x13
    li t6, 0x80010000
    ld x17, 72(t6)
    addi x12, x12, -393
    add x21, x16, x23
    sll x23, x23, x14
    add x22, x18, x19
    or x11, x12, x13
    xor x21, x21, x21
    li t6, 0x80010000
    sd x11, 32(t6)
    sub x12, x12, x13
    li t6, 0x80010000
    ld x11, 8(t6)
    sub x11, x9, x16
    sll x21, x18, x13
    and x13, x18, x22
    sll x13, x13, x15
    sll x23, x10, x9
    add x11, x15, x14
    add x18, x18, x18
    sll x21, x21, x15
    and x17, x13, x14
    add x11, x11, x20
    li t6, 0x80010000
    sd x23, 24(t6)
    or x11, x11, x14
    srl x9, x15, x11
    li t6, 0x80010000
    ld x21, 104(t6)
    addi x19, x20, 816
    sll x22, x10, x22
    and x17, x11, x19
    li t6, 0x80010000
    ld x22, 24(t6)
    add x17, x18, x12
    li t6, 0x80010000
    ld x13, 24(t6)
    xor x15, x12, x17
    xor x13, x21, x10
    li t6, 0x80010000
    ld x21, 88(t6)
    xor x11, x11, x15
    li t6, 0x80010000
    ld x20, 72(t6)
    or x20, x20, x23
    sll x21, x21, x18
    sub x10, x18, x10
    addi x20, x20, -1929
    sub x13, x9, x9
    li t6, 0x80010000
    sd x14, 88(t6)
    sll x23, x23, x21
    li t6, 0x80010000
    ld x15, 120(t6)
    srl x13, x21, x14
    srl x19, x11, x14
    add x19, x13, x22
    li t6, 0x80010000
    sd x14, 0(t6)
    and x22, x21, x13
    or x9, x9, x11
    addi x11, x11, 723
    li t6, 0x80010000
    ld x19, 72(t6)
    srl x15, x15, x14
    xor x13, x13, x16
    sub x15, x22, x18
    sub x15, x18, x15
    srl x19, x19, x21
    addi x15, x12, 1721
    or x23, x10, x18
    sll x16, x16, x9
    li t6, 0x80010000
    ld x11, 80(t6)
    xor x11, x11, x23
    or x19, x19, x20
    xor x11, x10, x14
    li t6, 0x80010000
    ld x19, 24(t6)
    and x14, x14, x10
    srl x19, x16, x15
    or x19, x21, x12
    sll x20, x13, x21
    srl x9, x16, x10
    sll x17, x22, x10
    or x15, x13, x10
    add x23, x23, x20
    add x15, x9, x10
    xor x12, x12, x17
    or x10, x10, x19
    li t6, 0x80010000
    ld x10, 104(t6)
    or x22, x13, x9
    sub x13, x13, x10
    addi x21, x21, -1105
    addi x14, x21, 156
    li t6, 0x80010000
    ld x16, 104(t6)
    sub x16, x18, x14
    add x19, x15, x22
    xor x15, x11, x22
    add x22, x9, x14
    sll x9, x11, x14
    srl x11, x11, x10
    addi x10, x10, 1645
    sub x10, x12, x19
    addi x18, x18, 1492
    sll x12, x15, x12
    srl x11, x11, x19
    xor x13, x9, x21
    srl x20, x20, x12
    or x20, x10, x11
    sll x15, x22, x17
    srl x10, x10, x10
    and x23, x9, x22
    xor x21, x21, x13
    sll x19, x10, x12
    addi x19, x13, -1842
    li t6, 0x80010000
    ld x12, 56(t6)
    add x10, x10, x18
    sub x22, x14, x9
    srl x15, x15, x17
    add x18, x19, x13
    sub x14, x11, x13
    addi x14, x11, -1413
    sub x21, x9, x16
    srl x10, x21, x13
    or x12, x12, x23
    srl x11, x11, x14
    srl x23, x14, x21
    sub x14, x15, x20
    addi x22, x11, -1228
    xor x22, x9, x18
    xor x16, x16, x23
    li t6, 0x80010000
    ld x10, 104(t6)
    or x10, x10, x19
    sll x17, x12, x17
    srl x12, x22, x17
    addi x22, x22, -1164
    add x14, x22, x10
    li t6, 0x80010000
    ld x16, 24(t6)
    sll x18, x18, x15
    sll x13, x13, x15
    xor x21, x23, x23
    xor x22, x22, x18
    xor x19, x14, x9
    srl x12, x21, x12
    sub x19, x19, x21
    sll x17, x16, x19
    and x20, x10, x16
    li t6, 0x80010000
    ld x18, 24(t6)
    and x13, x22, x18
    sll x17, x17, x17
    srl x18, x18, x23
    and x23, x23, x21
    add x16, x16, x11
    sll x11, x11, x12
    srl x23, x13, x12
    add x12, x12, x12
    and x22, x22, x13
    and x17, x17, x23
    xor x18, x14, x16
    addi x11, x22, 2028
    add x11, x13, x20
    and x17, x17, x21
    add x19, x20, x19
    li t6, 0x80010000
    ld x10, 8(t6)
    srl x22, x22, x19
    or x18, x18, x12
    xor x13, x13, x10
    or x12, x11, x16
    li t6, 0x80010000
    ld x23, 88(t6)
    li t6, 0x80010000
    sd x15, 48(t6)
    sll x13, x13, x23
    add x11, x16, x12
    xor x19, x19, x17
    sub x22, x13, x12
    srl x13, x16, x14
    add x11, x11, x9
    or x19, x19, x18
    xor x13, x10, x16
    xor x9, x15, x12
    or x22, x15, x19
    srl x18, x18, x16
    sll x12, x17, x19
    li t6, 0x80010000
    ld x13, 0(t6)
    or x12, x13, x17
    sub x13, x13, x11
    li t6, 0x80010000
    ld x18, 0(t6)
    li t6, 0x80010000
    ld x22, 64(t6)
    xor x18, x14, x11
    and x16, x16, x18
    add x21, x18, x17
    li t6, 0x80010000
    ld x16, 64(t6)
    or x17, x10, x11
    li t6, 0x80010000
    ld x17, 112(t6)
    li t6, 0x80010000
    sd x23, 64(t6)
    or x13, x12, x13
    li t6, 0x80010000
    ld x16, 48(t6)
    addi x18, x12, 865
    and x19, x9, x12
    and x11, x11, x12
    xor x19, x19, x12
    li t6, 0x80010000
    ld x10, 64(t6)
    li t6, 0x80010000
    ld x16, 32(t6)
    srl x9, x9, x10
    or x19, x9, x9
    li t6, 0x80010000
    sd x13, 40(t6)
    or x14, x14, x22
    sll x14, x20, x15
    li t6, 0x80010000
    ld x23, 104(t6)
    xor x21, x22, x9
    li t6, 0x80010000
    sd x14, 120(t6)
    li t6, 0x80010000
    ld x11, 72(t6)
    and x14, x19, x21
    li t6, 0x80010000
    ld x18, 40(t6)
    sll x12, x23, x9
    xor x9, x15, x13
    srl x12, x12, x12
    xor x15, x22, x15
    addi x14, x10, -114
    sll x15, x15, x19
    sub x13, x10, x18
    xor x23, x9, x17
    addi x17, x13, -1622
    srl x11, x19, x22
    and x11, x21, x17
    li t6, 0x80010000
    ld x9, 56(t6)
    addi x20, x20, 1136
    srl x23, x10, x10
    or x12, x19, x22
    li t6, 0x80010000
    sd x10, 88(t6)
    add x15, x19, x22
    add x17, x19, x17
    add x20, x12, x22
    addi x18, x20, 1649
    add x10, x16, x13
    li t6, 0x80010000
    ld x14, 104(t6)
    and x19, x23, x15
    li t6, 0x80010000
    ld x13, 120(t6)
    li t6, 0x80010000
    ld x18, 112(t6)
    sub x20, x20, x23
    and x12, x12, x22
    add x12, x11, x20
    sub x11, x13, x9
    addi x9, x17, 327
    and x14, x14, x16
    li t6, 0x80010000
    ld x17, 24(t6)
    srl x15, x16, x17
    addi x16, x16, -1781
    xor x11, x16, x9
    xor x19, x16, x13
    sub x23, x20, x22
    sub x14, x11, x10
    xor x17, x20, x16
    srl x10, x16, x22
    li t6, 0x80010000
    sd x20, 80(t6)
    and x21, x18, x23
    or x18, x18, x9
    sub x15, x15, x17
    and x11, x11, x22
    addi x19, x18, 21
    sll x17, x17, x12
    li t6, 0x80010000
    ld x22, 104(t6)
    xor x18, x14, x23
    sub x13, x17, x19
    srl x14, x14, x15
    li t6, 0x80010000
    sd x11, 56(t6)
    addi x11, x13, -241
    li t6, 0x80010000
    sd x14, 16(t6)
    srl x9, x19, x20
    sub x12, x16, x19
    add x22, x12, x18
    srl x23, x14, x21
    li t6, 0x80010000
    ld x20, 24(t6)
    xor x22, x23, x23
    li t6, 0x80010000
    ld x19, 0(t6)
    and x23, x23, x11
    xor x12, x17, x19
    and x17, x17, x23
    sub x17, x17, x18
    li t6, 0x80010000
    sd x11, 88(t6)
    li t6, 0x80010000
    ld x17, 40(t6)
    xor x19, x16, x18
    addi x20, x20, -1616
    li t6, 0x80010000
    ld x12, 88(t6)
    li t6, 0x80010000
    sd x23, 0(t6)
    li t6, 0x80010000
    ld x20, 80(t6)
    add x9, x16, x21
    addi x23, x13, -1187
    li t6, 0x80010000
    ld x20, 64(t6)
    li t6, 0x80010000
    sd x19, 0(t6)
    sub x15, x15, x22
    sub x18, x18, x19
    li t6, 0x80010000
    sd x16, 32(t6)
    sll x16, x16, x14
    li t6, 0x80010000
    ld x10, 0(t6)
    addi x9, x17, 520
    add x12, x12, x15
    li t6, 0x80010000
    sd x16, 16(t6)
    and x15, x15, x19
    and x9, x13, x23
    li t6, 0x80010000
    ld x21, 8(t6)
    add x14, x14, x22
    srl x22, x12, x10
    sll x20, x20, x9
    sub x16, x23, x10
    and x17, x20, x18
    and x19, x19, x22
    srl x11, x11, x16
    add x13, x13, x9
    add x10, x13, x9
    xor x10, x19, x21
    addi x14, x14, 222
    or x19, x19, x13
    sub x22, x22, x16
    xor x21, x21, x23
    srl x16, x15, x13
    sub x21, x17, x19
    srl x17, x17, x14
    or x10, x21, x14
    add x9, x9, x23
    sub x17, x22, x16
    li t6, 0x80010000
    ld x14, 48(t6)
    srl x22, x22, x12
    xor x10, x9, x23
    sub x15, x15, x9
    srl x21, x21, x19
    sub x22, x22, x18
    sub x22, x18, x13
    addi x14, x14, 1513
    li t6, 0x80010000
    ld x21, 8(t6)
    xor x14, x14, x22
    and x23, x21, x16
    xor x14, x9, x22
    li t6, 0x80010000
    sd x14, 56(t6)
    add x23, x23, x22
    or x18, x18, x20
    addi x23, x23, 1247
    li t6, 0x80010000
    sd x18, 24(t6)
    sub x14, x9, x19
    and x11, x11, x17
    addi x13, x14, -1186
    srl x12, x12, x18
    srl x17, x17, x13
    and x13, x11, x18
    xor x23, x23, x9
    and x13, x13, x11
    srl x22, x22, x15
    li t6, 0x80010000
    sd x21, 48(t6)
    sll x11, x11, x20
    sub x12, x12, x20
    xor x14, x14, x10
    xor x23, x23, x16
    srl x19, x12, x16
    or x19, x14, x19
    li t6, 0x80010000
    ld x12, 48(t6)
    li t6, 0x80010000
    ld x23, 80(t6)
    sub x14, x14, x12
    sll x17, x13, x16
    and x10, x10, x20
    li t6, 0x80010000
    ld x18, 56(t6)
    sub x16, x10, x22
    li t6, 0x80010000
    sd x14, 40(t6)
    sll x16, x18, x19
    xor x21, x19, x19
    li t6, 0x80010000
    ld x10, 40(t6)
    and x13, x13, x20
    srl x11, x18, x18
    or x20, x20, x11
    srl x23, x23, x17
    addi x17, x14, -314
    add x23, x16, x11
    and x21, x23, x11
    sll x17, x17, x16
    li t6, 0x80010000
    sd x16, 16(t6)
    and x17, x23, x15
    and x14, x11, x13
    addi x9, x22, -443
    xor x10, x10, x10
    xor x9, x15, x10
    or x17, x17, x14
    sub x21, x21, x21
    sll x16, x16, x20
    xor x16, x16, x17
    srl x10, x10, x21
    sub x14, x17, x16
    and x9, x9, x15
    li t6, 0x80010000
    sd x20, 56(t6)
    li t6, 0x80010000
    ld x10, 88(t6)
    and x20, x13, x17
    sub x23, x19, x18
    li t6, 0x80010000
    ld x23, 0(t6)
    xor x15, x15, x19
    addi x15, x15, -459
    add x17, x21, x20
    and x23, x11, x11
    or x20, x20, x10
    li t6, 0x80010000
    sd x22, 0(t6)
    li t6, 0x80010000
    sd x23, 112(t6)
    srl x21, x21, x18
    and x23, x23, x23
    li t6, 0x80010000
    ld x15, 72(t6)
    or x12, x10, x10
    and x13, x13, x23
    or x10, x20, x20
    sll x14, x14, x20
    or x21, x21, x17
    li t6, 0x80010000
    sd x13, 24(t6)
    sll x11, x11, x21
    sub x14, x17, x10
    li t6, 0x80010000
    sd x21, 80(t6)
    li t6, 0x80010000
    ld x16, 0(t6)
    and x11, x15, x22
    li t6, 0x80010000
    ld x20, 0(t6)
    xor x17, x18, x12
    or x23, x10, x19
    and x13, x9, x9
    li t6, 0x80010000
    ld x12, 64(t6)
    li t6, 0x80010000
    ld x15, 24(t6)
    li t6, 0x80010000
    ld x19, 64(t6)
    li t6, 0x80010000
    sd x10, 96(t6)
    or x17, x17, x22
    and x23, x23, x23
    addi x23, x18, 430
    add x13, x19, x10
    sll x15, x15, x16
    or x10, x10, x14
    li t6, 0x80010000
    sd x10, 8(t6)
    xor x14, x14, x19
    sub x15, x15, x10
    srl x9, x11, x19
    or x15, x14, x9
    srl x12, x12, x9
    add x18, x12, x17
    li t6, 0x80010000
    ld x16, 32(t6)
    li t6, 0x80010000
    ld x22, 64(t6)
    addi x13, x13, -881
    or x18, x18, x9
    and x19, x19, x18
    addi x12, x12, 852
    add x12, x12, x17
    and x16, x20, x21
    sll x10, x10, x18
    and x18, x18, x17
    srl x13, x15, x10
    srl x20, x10, x21
    add x21, x21, x10
    li t6, 0x80010000
    ld x21, 112(t6)
    or x9, x9, x23
    and x16, x16, x15
    li t6, 0x80010000
    sd x13, 120(t6)
    li t6, 0x80010000
    sd x23, 24(t6)
    and x22, x22, x17
    li t6, 0x80010000
    sd x22, 8(t6)
    xor x16, x12, x21
    or x16, x15, x18
    or x13, x12, x10
    add x22, x22, x17
    addi x17, x12, -1259
    sll x20, x20, x9
    li t6, 0x80010000
    sd x13, 80(t6)
    srl x13, x9, x20
    add x23, x21, x14
    addi x9, x13, -932
    xor x14, x14, x22
    sll x15, x21, x15
    li t6, 0x80010000
    sd x16, 16(t6)
    li t6, 0x80010000
    sd x23, 48(t6)
    srl x14, x20, x15
    li t6, 0x80010000
    sd x19, 24(t6)
    sll x15, x15, x20
    add x19, x19, x15
    sub x20, x10, x12
    or x18, x18, x17
    addi x12, x12, -1164
    addi x10, x10, 709
    xor x11, x9, x16
    sll x10, x20, x10
    add x22, x22, x20
    li t6, 0x80010000
    ld x17, 96(t6)
    li t6, 0x80010000
    ld x20, 72(t6)
    srl x10, x16, x15
    srl x23, x22, x19
    srl x9, x9, x12
    add x11, x11, x19
    xor x13, x13, x23
    xor x16, x16, x23
    and x9, x12, x9
    sub x17, x23, x14
    li t6, 0x80010000
    ld x19, 56(t6)
    li t6, 0x80010000
    sd x15, 16(t6)
    or x13, x15, x22
    add x23, x23, x22
    or x23, x22, x12
    li t6, 0x80010000
    ld x13, 16(t6)
    li t6, 0x80010000
    sd x19, 0(t6)
    addi x16, x17, -1023
    or x19, x20, x15
    sll x21, x21, x15
    and x20, x13, x17
    xor x23, x10, x9
    xor x19, x20, x22
    li t6, 0x80010000
    ld x16, 64(t6)
    srl x15, x16, x14
    xor x12, x12, x11
    add x14, x13, x21
    and x16, x16, x21
    addi x19, x19, -1142
    li t6, 0x80010000
    sd x17, 48(t6)
    addi x15, x23, 464
    sll x17, x17, x11
    addi x14, x23, -97
    and x17, x17, x15
    addi x13, x17, -1620
    xor x16, x11, x13
    xor x10, x9, x14
    li t6, 0x80010000
    sd x17, 0(t6)
    and x17, x16, x12
    xor x16, x16, x9
    add x23, x23, x9
    sll x17, x17, x12
    or x14, x14, x15
    sub x15, x20, x23
    sll x10, x20, x11
    sll x21, x21, x9
    xor x20, x14, x18
    srl x22, x23, x23
    and x21, x20, x20
    li t6, 0x80010000
    sd x10, 96(t6)
    and x9, x9, x10
    sll x16, x13, x22
    li t6, 0x80010000
    ld x12, 40(t6)
    or x14, x14, x18
    or x22, x19, x9
    li t6, 0x80010000
    sd x16, 0(t6)
    and x13, x22, x19
    or x22, x13, x23
    li t6, 0x80010000
    sd x12, 112(t6)
    xor x13, x21, x14
    or x13, x15, x9
    sub x18, x14, x12
    li t6, 0x80010000
    ld x12, 104(t6)
    xor x16, x16, x23
    sub x11, x11, x9
    sub x21, x19, x21
    addi x13, x11, -1714
    li t6, 0x80010000
    sd x12, 64(t6)
    li t6, 0x80010000
    ld x14, 40(t6)
    li t6, 0x80010000
    ld x18, 8(t6)
    srl x20, x13, x21
    li t6, 0x80010000
    sd x14, 8(t6)
    li t6, 0x80010000
    sd x9, 64(t6)
    srl x18, x23, x14
    or x19, x9, x15
    addi x11, x17, 1097
    sub x15, x23, x10
    li t6, 0x80010000
    ld x18, 24(t6)
    xor x16, x16, x17
    sll x10, x22, x14
    or x15, x15, x18
    xor x14, x14, x17
    sub x23, x23, x20
    add x18, x14, x9
    li t6, 0x80010000
    ld x20, 64(t6)
    li t6, 0x80010000
    sd x20, 72(t6)
    add x18, x18, x11
    add x21, x21, x20
    or x10, x10, x20
    sub x14, x15, x23
    sll x12, x18, x20
    and x11, x16, x19
    srl x15, x15, x18
    sll x10, x11, x20
    or x23, x23, x13
    sll x10, x17, x14
    xor x16, x16, x19
    li t6, 0x80010000
    sd x20, 96(t6)
    add x13, x10, x13
    or x19, x19, x12
    and x22, x22, x23
    sub x11, x11, x12
    li t6, 0x80010000
    ld x19, 112(t6)
    or x19, x17, x12
    sll x13, x13, x13
    li t6, 0x80010000
    ld x19, 104(t6)
    or x19, x19, x15
    sll x21, x21, x21
    or x21, x22, x18
    li t6, 0x80010000
    sd x12, 8(t6)
    addi x21, x21, -1640
    and x9, x9, x19
    or x16, x16, x12
    li t6, 0x80010000
    sd x20, 120(t6)
    srl x20, x9, x9
    xor x19, x19, x10
    li t6, 0x80010000
    ld x14, 48(t6)
    sll x16, x16, x14
    srl x16, x16, x9
    li t6, 0x80010000
    sd x13, 24(t6)
    li t6, 0x80010000
    sd x19, 88(t6)
    sll x20, x20, x10
    li t6, 0x80010000
    ld x11, 32(t6)
    add x12, x12, x10
    li t6, 0x80010000
    sd x21, 72(t6)
    li t6, 0x80010000
    sd x13, 72(t6)
    and x16, x16, x23
    xor x9, x15, x23
    srl x13, x13, x22
    li t6, 0x80010000
    ld x22, 40(t6)
    sub x17, x16, x19
    sub x23, x17, x10
    sll x16, x16, x16
    li t6, 0x80010000
    sd x9, 0(t6)
    add x19, x14, x9
    sll x21, x21, x13
    or x21, x17, x17
    li t6, 0x80010000
    ld x20, 112(t6)
    or x10, x23, x10
    or x16, x16, x15
    sll x17, x21, x21
    li t6, 0x80010000
    sd x20, 80(t6)
    li t6, 0x80010000
    ld x12, 0(t6)
    add x23, x23, x13
    sub x23, x21, x12
    or x10, x10, x22
    sll x17, x21, x11
    add x13, x13, x10
    srl x14, x14, x9
    sub x13, x13, x17
    xor x23, x23, x22
    li t6, 0x80010000
    ld x21, 0(t6)
    li t6, 0x80010000
    ld x9, 8(t6)
    sll x12, x12, x18
    addi x23, x11, -1009
    sll x11, x9, x17
    and x9, x9, x10
    xor x19, x19, x18
    srl x20, x22, x16
    li t6, 0x80010000
    sd x13, 32(t6)
    sll x14, x14, x17
    xor x23, x10, x12
    srl x22, x22, x23
    li t6, 0x80010000
    sd x16, 112(t6)
    and x12, x14, x21
    li t6, 0x80010000
    ld x21, 120(t6)
    and x12, x14, x15
    li t6, 0x80010000
    ld x21, 24(t6)
    addi x15, x15, 599
    or x18, x18, x18
    and x20, x20, x20
    xor x21, x21, x16
    xor x12, x22, x14
    sll x12, x18, x20
    srl x21, x20, x18
    addi x10, x10, -544
    srl x23, x23, x23
    sll x23, x12, x13
    addi x17, x11, 1235
    li t6, 0x80010000
    sd x19, 8(t6)
    li t6, 0x80010000
    ld x15, 24(t6)
    addi x11, x13, -1398
    and x15, x18, x19
    sll x19, x18, x12
    li t6, 0x80010000
    ld x12, 112(t6)
    addi x21, x14, -1901
    and x13, x13, x14
    li t6, 0x80010000
    ld x23, 40(t6)
    srl x20, x20, x15
    sub x18, x18, x14
    li t6, 0x80010000
    sd x22, 80(t6)
    li t6, 0x80010000
    ld x15, 8(t6)
    sub x23, x16, x14
    add x10, x10, x23
    sub x20, x18, x15
    li t6, 0x80010000
    sd x20, 120(t6)
    sll x22, x9, x18
    add x14, x13, x20
    sub x14, x14, x19
    li t6, 0x80010000
    sd x9, 0(t6)
    sll x23, x23, x17
    and x10, x19, x22
    add x19, x23, x20
    sll x13, x13, x22
    li t6, 0x80010000
    sd x12, 32(t6)
    sub x14, x19, x22
    sll x20, x20, x16
    sll x11, x19, x10
    li t6, 0x80010000
    ld x23, 16(t6)
    addi x14, x14, -327
    xor x12, x23, x10
    li t6, 0x80010000
    ld x18, 64(t6)
    sub x22, x22, x14
    sll x17, x13, x19
    sub x17, x17, x15
    sll x21, x10, x16
    li t6, 0x80010000
    ld x10, 32(t6)
    li t6, 0x80010000
    sd x20, 64(t6)
    add x9, x16, x11
    sll x21, x21, x19
    srl x13, x13, x21
    addi x22, x22, -743
    li t6, 0x80010000
    ld x15, 120(t6)
    addi x14, x14, -1705
    li t6, 0x80010000
    sd x12, 0(t6)
    sll x9, x18, x17
    li t6, 0x80010000
    sd x17, 0(t6)
    or x21, x16, x12
    xor x14, x14, x22
    sll x12, x12, x22
    li t6, 0x80010000
    ld x13, 0(t6)
    sll x17, x17, x23
    li t6, 0x80010000
    sd x19, 88(t6)
    xor x17, x17, x12
    li t6, 0x80010000
    sd x11, 56(t6)
    or x20, x20, x18
    and x10, x10, x14
    addi x13, x19, -433
    or x21, x21, x12
    xor x22, x20, x12
    and x12, x13, x22
    xor x17, x17, x9
    xor x12, x12, x14
    li t6, 0x80010000
    sd x12, 40(t6)
    or x15, x15, x16
    li t6, 0x80010000
    sd x10, 104(t6)
    li t6, 0x80010000
    ld x20, 80(t6)
    li t6, 0x80010000
    ld x12, 104(t6)
    sll x11, x11, x22
    sub x18, x18, x20
    li t6, 0x80010000
    ld x19, 72(t6)
    and x18, x14, x21
    and x15, x20, x17
    li t6, 0x80010000
    ld x18, 32(t6)
    xor x14, x15, x11
    li t6, 0x80010000
    ld x12, 112(t6)
    srl x22, x13, x9
    li t6, 0x80010000
    sd x16, 104(t6)
    or x20, x9, x21
    xor x12, x23, x22
    and x11, x11, x21
    and x12, x10, x21
    sub x19, x19, x23
    addi x15, x15, 290
    addi x11, x15, -1998
    or x14, x16, x23
    li t6, 0x80010000
    sd x16, 0(t6)
    add x10, x22, x9
    addi x14, x23, -1797
    xor x23, x22, x11
    addi x16, x16, 266
    and x12, x22, x17
    add x11, x21, x12
    sub x12, x12, x15
    sll x9, x9, x16
    li t6, 0x80010000
    ld x21, 16(t6)
    srl x12, x11, x19
    li t6, 0x80010000
    ld x10, 120(t6)
    li t6, 0x80010000
    ld x20, 24(t6)
    or x22, x23, x23
    add x10, x17, x22
    addi x21, x21, 652
    sub x9, x9, x17
    sub x12, x12, x19
    li t6, 0x80010000
    ld x19, 8(t6)
    and x19, x19, x16
    addi x17, x17, 1840
    srl x12, x16, x20
    or x15, x16, x23
    or x9, x9, x17
    li t6, 0x80010000
    ld x17, 112(t6)
    addi x18, x18, -1415
    li t6, 0x80010000
    ld x16, 32(t6)
    add x10, x22, x21
    srl x18, x18, x13
    srl x23, x20, x9
    sub x12, x11, x9
    and x15, x21, x14
    srl x14, x17, x14
    and x11, x9, x23
    sub x14, x14, x16
    sll x15, x23, x15
    srl x10, x10, x10
    li t6, 0x80010000
    sd x9, 8(t6)
    and x16, x16, x12
    li t6, 0x80010000
    ld x18, 104(t6)
    li t6, 0x80010000
    sd x14, 40(t6)
    and x13, x11, x19
    sub x10, x22, x15
    sub x16, x22, x17
    li t6, 0x80010000
    ld x16, 120(t6)
    li t6, 0x80010000
    sd x12, 88(t6)
    srl x18, x19, x10
    srl x11, x17, x22
    add x16, x10, x12
    and x21, x21, x10
    sub x17, x20, x20
    add x11, x11, x10
    xor x12, x13, x9
    li t6, 0x80010000
    sd x9, 120(t6)
    or x17, x21, x12
    or x13, x19, x19
    or x12, x12, x23
    and x16, x16, x19
    add x20, x20, x20
    srl x15, x17, x10
    sub x11, x15, x21
    xor x22, x10, x12
    or x22, x21, x23
    srl x12, x16, x14
    add x10, x10, x13
    sub x17, x17, x23
    and x9, x9, x9
    srl x23, x21, x18
    li t6, 0x80010000
    ld x10, 96(t6)
    li t6, 0x80010000
    sd x14, 88(t6)
    sub x21, x10, x21
    or x22, x21, x22
    srl x20, x16, x13
    li t6, 0x80010000
    ld x21, 32(t6)
    add x18, x11, x20
    li t6, 0x80010000
    sd x16, 72(t6)
    sll x16, x23, x16
    or x13, x10, x14
    li t6, 0x80010000
    sd x21, 96(t6)
    addi x16, x15, -61
    sll x20, x20, x13
    xor x11, x11, x22
    sub x17, x16, x19
    li t6, 0x80010000
    sd x17, 8(t6)
    xor x20, x20, x19
    sub x10, x23, x9
    add x16, x9, x22
    li t6, 0x80010000
    sd x17, 8(t6)
    li t6, 0x80010000
    sd x9, 24(t6)
    li t6, 0x80010000
    ld x10, 112(t6)
    srl x12, x23, x11
    srl x21, x21, x9
    or x21, x21, x20
    xor x22, x11, x23
    or x15, x22, x20
    srl x17, x15, x17
    sll x18, x18, x12
    sub x22, x22, x9
    or x15, x18, x16
    and x16, x13, x23
    li t6, 0x80010000
    ld x11, 0(t6)
    sub x10, x9, x16
    li t6, 0x80010000
    sd x14, 72(t6)
    li t6, 0x80010000
    ld x9, 72(t6)
    add x20, x20, x16
    addi x15, x15, 1360
    sub x10, x10, x20
    xor x17, x17, x16
    add x16, x16, x23
    and x11, x11, x17
    add x9, x9, x12
    sll x9, x9, x19
    and x15, x15, x16
    addi x17, x17, 596
    li t6, 0x80010000
    sd x14, 24(t6)
    sub x10, x10, x20
    sub x23, x23, x17
    sll x18, x12, x17
    xor x11, x11, x18
    or x11, x11, x13
    addi x12, x11, -578
    or x21, x16, x22
    add x19, x19, x10
    add x12, x12, x11
    srl x21, x10, x11
    li t6, 0x80010000
    sd x21, 0(t6)
    srl x18, x18, x14
    srl x10, x20, x18
    sub x15, x15, x20
    xor x14, x14, x12
    sub x12, x9, x20
    li t6, 0x80010000
    sd x18, 56(t6)
    li t6, 0x80010000
    ld x15, 32(t6)
    srl x10, x10, x19
    sll x21, x15, x13
    and x19, x19, x13
    li t6, 0x80010000
    sd x19, 120(t6)
    and x21, x21, x15
    and x22, x22, x9
    xor x11, x17, x9
    sll x18, x16, x16
    addi x13, x18, -734
    or x17, x20, x21
    li t6, 0x80010000
    sd x9, 32(t6)
    addi x22, x22, 1885
    addi x18, x18, 232
    add x23, x23, x12
    sub x18, x18, x17
    li t6, 0x80010000
    ld x9, 104(t6)
    sll x11, x12, x13
    sll x15, x15, x20
    sub x22, x22, x23
    li t6, 0x80010000
    ld x11, 40(t6)
    xor x11, x11, x17
    sll x17, x20, x14
    add x13, x13, x19
    li t6, 0x80010000
    ld x17, 56(t6)
    li t6, 0x80010000
    ld x11, 112(t6)
    xor x23, x23, x11
    xor x13, x13, x16
    xor x18, x18, x22
    addi x17, x17, -1524
    or x22, x22, x19
    addi x18, x17, 1654
    add x21, x21, x22
    or x13, x17, x18
    or x19, x12, x21
    srl x16, x16, x10
    li t6, 0x80010000
    sd x23, 16(t6)
    or x12, x12, x12
    and x19, x19, x23
    li t6, 0x80010000
    ld x11, 48(t6)
    or x23, x21, x22
    li t6, 0x80010000
    ld x12, 8(t6)
    sub x21, x21, x9
    and x17, x17, x19
    li t6, 0x80010000
    ld x15, 72(t6)
    li t6, 0x80010000
    ld x10, 32(t6)
    addi x16, x12, -1679
    or x9, x9, x15
    li t6, 0x80010000
    sd x15, 40(t6)
    and x13, x13, x18
    li t6, 0x80010000
    ld x10, 8(t6)
    and x9, x9, x18
    sub x16, x17, x11
    add x11, x11, x10
    srl x12, x12, x16
    li t6, 0x80010000
    ld x9, 16(t6)
    and x19, x11, x19
    add x16, x16, x12
    add x18, x21, x14
    li t6, 0x80010000
    sd x11, 56(t6)
    and x22, x22, x15
    sub x22, x22, x13
    addi x18, x18, -879
    li t6, 0x80010000
    sd x10, 32(t6)
    addi x20, x13, -1882
    and x17, x17, x18
    li t6, 0x80010000
    ld x13, 40(t6)
    sub x19, x19, x11
    or x21, x21, x23
    li t6, 0x80010000
    sd x20, 16(t6)
    sub x22, x13, x17
    li t6, 0x80010000
    ld x12, 8(t6)
    add x15, x15, x18
    li t6, 0x80010000
    sd x20, 104(t6)
    add x12, x12, x14
    sll x21, x21, x13
    addi x14, x14, 1331
    li t6, 0x80010000
    sd x12, 88(t6)
    addi x18, x18, 996
    or x18, x18, x13
    addi x16, x9, -355
    sub x15, x14, x12
    sll x15, x10, x13
    and x21, x21, x11
    li t6, 0x80010000
    ld x12, 120(t6)
    add x15, x15, x16
    srl x17, x17, x17
    or x22, x22, x20
    or x19, x19, x16
    li t6, 0x80010000
    ld x14, 72(t6)
    or x23, x23, x20
    srl x14, x14, x16
    srl x19, x19, x20
    add x19, x19, x11
    srl x14, x19, x17
    xor x20, x9, x16
    li t6, 0x80010000
    ld x23, 32(t6)
    sll x10, x10, x16
    li t6, 0x80010000
    sd x14, 0(t6)
    li t6, 0x80010000
    sd x18, 56(t6)
    xor x22, x22, x12
    sub x20, x16, x20
    addi x18, x18, -1147
    xor x14, x10, x17
    xor x12, x21, x13
    srl x23, x23, x21
    add x17, x20, x11
    and x16, x10, x9
    addi x9, x9, 1974
    and x18, x18, x15
    srl x11, x11, x22
    li t6, 0x80010000
    sd x22, 24(t6)
    li t6, 0x80010000
    ld x16, 40(t6)
    li t6, 0x80010000
    sd x23, 96(t6)
    li t6, 0x80010000
    sd x18, 40(t6)
    add x11, x13, x15
    add x14, x14, x20
    or x18, x18, x23
    addi x19, x19, 192
    xor x18, x19, x9
    li t6, 0x80010000
    sd x14, 80(t6)
    li t6, 0x80010000
    sd x17, 48(t6)
    add x23, x23, x20
    addi x12, x12, 1511
    or x15, x15, x10
    li t6, 0x80010000
    sd x22, 48(t6)
    li t6, 0x80010000
    ld x13, 72(t6)
    srl x20, x11, x17
    li t6, 0x80010000
    ld x9, 24(t6)
    or x15, x15, x20
    sll x10, x13, x9
    xor x19, x13, x19
    li t6, 0x80010000
    sd x17, 80(t6)
    addi x16, x16, 1801
    sub x23, x10, x14
    srl x22, x19, x9
    srl x21, x23, x9
    and x21, x21, x13
    add x16, x19, x12
    or x17, x9, x22
    sll x12, x18, x9
    sub x12, x15, x12
    and x15, x13, x19
    or x15, x15, x21
    addi x9, x11, 391
    sll x16, x16, x13
    srl x11, x11, x17
    and x19, x19, x21
    srl x9, x23, x13
    li t6, 0x80010000
    ld x17, 64(t6)
    li t6, 0x80010000
    sd x12, 0(t6)
    add x19, x22, x23
    xor x23, x14, x11
    sub x23, x15, x23
    sub x15, x21, x18
    li t6, 0x80010000
    sd x21, 48(t6)
    add x13, x14, x16
    add x16, x16, x20
    xor x18, x12, x10
    addi x16, x19, -1295
    li t6, 0x80010000
    ld x17, 40(t6)
    xor x21, x11, x13
    and x16, x23, x17
    xor x12, x18, x19
    li t6, 0x80010000
    sd x21, 72(t6)
    li t6, 0x80010000
    ld x23, 96(t6)
    or x13, x13, x10
    sub x17, x17, x16
    li t6, 0x80010000
    ld x11, 40(t6)
    li t6, 0x80010000
    sd x11, 80(t6)
    sub x19, x19, x11
    sll x21, x19, x23
    sub x16, x16, x21
    li t6, 0x80010000
    ld x22, 24(t6)
    sll x19, x19, x11
    xor x18, x18, x18
    srl x13, x23, x13
    srl x15, x15, x17
    sub x9, x9, x10
    xor x19, x19, x18
    and x23, x23, x21
    addi x14, x14, 656
    or x13, x13, x9
    add x22, x23, x21
    li t6, 0x80010000
    ld x23, 96(t6)
    sub x23, x9, x12
    sub x22, x21, x13
    srl x20, x12, x13
    addi x13, x13, -1759
    or x9, x17, x20
    li t6, 0x80010000
    sd x19, 32(t6)
    srl x11, x19, x19
    and x19, x19, x18
    sub x20, x14, x17
    or x21, x17, x11
    srl x19, x15, x16
    li t6, 0x80010000
    sd x22, 0(t6)
    or x21, x13, x21
    li t6, 0x80010000
    sd x23, 0(t6)
    xor x21, x21, x10
    sll x20, x20, x12
    xor x9, x21, x20
    sub x10, x18, x18
    srl x17, x17, x19
    xor x20, x20, x15
    sll x23, x17, x15
    li t6, 0x80010000
    ld x10, 24(t6)
    xor x11, x15, x17
    sll x17, x17, x12
    addi x14, x23, -1292
    and x10, x10, x10
    addi x10, x10, -1293
    srl x12, x12, x9
    addi x21, x21, -351
    addi x23, x23, -604
    li t6, 0x80010000
    ld x18, 96(t6)
    add x19, x19, x23
    or x20, x15, x11
    li t6, 0x80010000
    sd x15, 80(t6)
    sll x14, x21, x15
    or x17, x17, x19
    srl x10, x10, x16
    addi x9, x9, 1118
    li t6, 0x80010000
    sd x22, 56(t6)
    xor x16, x20, x23
    li t6, 0x80010000
    ld x15, 104(t6)
    or x18, x18, x19
    add x18, x11, x21
    xor x20, x20, x23
    li t6, 0x80010000
    ld x12, 64(t6)
    and x22, x22, x20
    sll x13, x13, x22
    and x12, x12, x13
    xor x14, x14, x22
    xor x23, x23, x12
    sll x12, x12, x22
    srl x17, x17, x9
    li t6, 0x80010000
    ld x17, 8(t6)
    srl x18, x12, x9
    xor x19, x10, x19
    li t6, 0x80010000
    ld x14, 80(t6)
    sll x11, x13, x9
    or x19, x19, x10
    xor x11, x11, x13
    or x21, x21, x16
    or x17, x15, x15
    xor x15, x15, x19
    srl x16, x15, x22
    xor x10, x10, x18
    xor x13, x13, x23
    sll x22, x22, x22
    li t6, 0x80010000
    ld x23, 24(t6)
    li t6, 0x80010000
    ld x15, 48(t6)
    sll x17, x17, x9
    sll x11, x14, x9
    sub x9, x12, x18
    or x17, x17, x21
    srl x23, x23, x10
    srl x17, x17, x12
    srl x15, x23, x13
    sub x13, x23, x14
    li t6, 0x80010000
    ld x22, 40(t6)
    li t6, 0x80010000
    ld x17, 112(t6)
    xor x17, x17, x18
    or x10, x10, x14
    add x22, x17, x10
    sll x13, x11, x21
    addi x19, x15, -1676
    add x11, x11, x18
    sll x12, x12, x19
    addi x16, x16, 2021
    sub x13, x17, x19
    li t6, 0x80010000
    sd x15, 0(t6)
    li t6, 0x80010000
    sd x17, 0(t6)
    or x9, x9, x16
    srl x18, x18, x19
    srl x17, x23, x19
    or x22, x9, x22
    addi x16, x19, -1034
    xor x9, x9, x20
    or x16, x12, x16
    srl x9, x18, x21
    li t6, 0x80010000
    sd x13, 64(t6)
    add x22, x22, x19
    li t6, 0x80010000
    sd x20, 0(t6)
    li t6, 0x80010000
    sd x16, 16(t6)
    sub x13, x13, x20
    li t6, 0x80010000
    ld x10, 72(t6)
    li t6, 0x80010000
    sd x21, 88(t6)
    add x21, x13, x21
    add x22, x18, x12
    or x19, x9, x16
    srl x10, x10, x16
    li t6, 0x80010000
    ld x22, 0(t6)
    sll x13, x22, x22
    li t6, 0x80010000
    ld x21, 24(t6)
    or x9, x11, x23
    xor x20, x14, x22
    or x15, x15, x22
    add x22, x22, x12
    xor x13, x14, x11
    li t6, 0x80010000
    ld x12, 64(t6)
    srl x16, x19, x13
    or x12, x12, x19
    sll x18, x12, x10
    li t6, 0x80010000
    sd x9, 96(t6)
    sub x19, x19, x18
    add x17, x17, x11
    li t6, 0x80010000
    sd x13, 96(t6)
    li t6, 0x80010000
    ld x9, 120(t6)
    or x15, x15, x10
    xor x14, x14, x15
    xor x16, x11, x15
    xor x11, x13, x19
    or x23, x23, x20
    srl x14, x14, x9
    addi x10, x9, -1426
    li t6, 0x80010000
    ld x14, 56(t6)
    sll x10, x10, x20
    xor x18, x12, x16
    or x9, x22, x19
    li t6, 0x80010000
    ld x22, 104(t6)
    and x16, x16, x19
    add x9, x9, x16
    or x18, x18, x17
    li t6, 0x80010000
    sd x20, 24(t6)
    or x18, x21, x14
    li t6, 0x80010000
    sd x14, 32(t6)
    addi x12, x16, 1484
    addi x20, x23, -1794
    or x19, x18, x14
    sll x14, x14, x19
    add x13, x13, x22
    addi x20, x20, 1749
    and x11, x11, x12
    addi x20, x11, 131
    srl x15, x22, x18
    li t6, 0x80010000
    sd x18, 96(t6)
    and x11, x11, x12
    li t6, 0x80010000
    ld x16, 120(t6)
    or x22, x22, x18
    sub x21, x21, x10
    or x17, x17, x22
    add x16, x22, x9
    li t6, 0x80010000
    ld x23, 96(t6)
    and x14, x21, x9
    sll x21, x15, x19
    add x9, x9, x18
    addi x15, x15, 515
    srl x21, x21, x19
    li t6, 0x80010000
    ld x15, 16(t6)
    or x23, x21, x10
    li t6, 0x80010000
    ld x11, 64(t6)
    li t6, 0x80010000
    sd x19, 48(t6)
    li t6, 0x80010000
    sd x22, 112(t6)
    li t6, 0x80010000
    ld x9, 0(t6)
    li t6, 0x80010000
    ld x21, 88(t6)
    addi x11, x10, 1932
    and x17, x9, x17
    srl x15, x15, x13
    li t6, 0x80010000
    sd x22, 112(t6)
    or x23, x22, x15
    sub x14, x14, x23
    xor x22, x22, x20
    xor x19, x19, x14
    add x22, x13, x13
    sub x19, x17, x13
    sll x21, x21, x21
    srl x19, x22, x13
    addi x13, x17, -467
    li t6, 0x80010000
    ld x22, 8(t6)
    li t6, 0x80010000
    sd x12, 64(t6)
    srl x9, x23, x10
    li t6, 0x80010000
    sd x18, 24(t6)
    add x22, x17, x11
    xor x13, x13, x15
    li t6, 0x80010000
    sd x11, 24(t6)
    xor x14, x14, x16
    and x11, x11, x14
    srl x16, x16, x15
    sub x15, x13, x21
    sub x20, x20, x13
    sll x14, x9, x11
    and x13, x13, x23
    addi x18, x18, 1722
    li t6, 0x80010000
    sd x14, 32(t6)
    sll x20, x17, x17
    or x16, x9, x9
    or x10, x22, x9
    srl x20, x9, x21
    addi x18, x15, -400
    addi x16, x13, -786
    or x22, x12, x19
    sub x9, x21, x12
    li t6, 0x80010000
    sd x16, 112(t6)
    addi x15, x15, 86
    sll x21, x21, x19
    or x12, x12, x22
    add x23, x23, x14
    add x10, x10, x12
    addi x18, x16, 206
    add x14, x14, x10
    srl x16, x16, x11
    and x13, x16, x11
    xor x16, x16, x22
    addi x9, x9, 1537
    or x10, x10, x15
    and x12, x12, x15
    add x18, x9, x10
    add x13, x13, x20
    or x16, x10, x13
    and x10, x18, x13
    srl x15, x15, x19
    srl x12, x12, x18
    sll x23, x23, x20
    sub x10, x22, x13
    addi x15, x10, 1684
    srl x19, x19, x15
    and x18, x18, x12
    sll x9, x12, x10
    sub x22, x22, x22
    sub x17, x14, x18
    sll x23, x23, x10
    sub x17, x17, x21
    or x17, x21, x16
    xor x22, x13, x17
    or x12, x12, x21
    add x11, x11, x21
    sll x20, x20, x14
    sll x12, x22, x15
    sll x19, x19, x9
    li t6, 0x80010000
    ld x22, 0(t6)
    and x9, x9, x22
    addi x18, x18, -1737
    add x12, x12, x9
    or x9, x15, x21
    li t6, 0x80010000
    sd x18, 72(t6)
    li t6, 0x80010000
    sd x11, 104(t6)
    li t6, 0x80010000
    sd x11, 96(t6)
    sll x14, x14, x21
    or x11, x23, x9
    and x23, x23, x16
    li t6, 0x80010000
    ld x23, 64(t6)
    xor x15, x15, x19
    xor x11, x19, x10
    li t6, 0x80010000
    sd x18, 88(t6)
    sub x23, x23, x15
    addi x17, x17, 186
    srl x14, x19, x19
    and x19, x19, x16
    li t6, 0x80010000
    ld x12, 40(t6)
    addi x15, x9, 354
    addi x15, x15, -684
    li t6, 0x80010000
    ld x9, 88(t6)
    add x17, x20, x9
    sll x10, x10, x14
    sub x16, x16, x21
    addi x19, x18, -1653
    add x17, x16, x21
    xor x18, x15, x13
    sub x13, x22, x10
    srl x12, x12, x14
    srl x23, x23, x12
    li t6, 0x80010000
    sd x9, 104(t6)
    addi x10, x13, 1700
    addi x9, x9, -1898
    and x23, x23, x22
    li t6, 0x80010000
    ld x12, 8(t6)
    li t6, 0x80010000
    sd x23, 24(t6)
    srl x22, x22, x13
    li t6, 0x80010000
    sd x12, 104(t6)
    or x17, x17, x19
    srl x15, x15, x17
    or x14, x14, x11
    and x18, x9, x11
    and x19, x14, x22
    li t6, 0x80010000
    sd x21, 48(t6)
    and x19, x19, x22
    sll x13, x13, x9
    and x11, x11, x13
    li t6, 0x80010000
    ld x12, 72(t6)
    and x15, x16, x12
    or x11, x18, x9
    xor x19, x10, x9
    or x16, x18, x20
    sll x23, x23, x22
    li t6, 0x80010000
    ld x22, 88(t6)
    li t6, 0x80010000
    ld x15, 32(t6)
    and x21, x21, x23
    or x22, x22, x20
    xor x22, x22, x22
    li t6, 0x80010000
    sd x18, 48(t6)
    xor x11, x11, x18
    sub x18, x10, x19
    addi x16, x16, 1
    sll x16, x16, x23
    and x11, x11, x13
    or x16, x11, x16
    addi x21, x17, 759
    sub x12, x16, x15
    sub x20, x20, x17
    li t6, 0x80010000
    ld x10, 104(t6)
    sub x10, x10, x23
    sll x19, x19, x16
    srl x15, x15, x11
    srl x20, x20, x13
    sub x17, x19, x11
    add x11, x13, x17
    srl x20, x23, x12
    xor x16, x20, x11
    addi x9, x23, -2039
    sll x15, x15, x9
    sll x16, x21, x20
    and x11, x11, x14
    add x20, x17, x15
    add x17, x13, x13
    addi x11, x11, 998
    sub x17, x17, x12
    srl x17, x17, x18
    add x18, x12, x17
    addi x16, x23, 124
    and x13, x18, x9
    add x20, x20, x14
    sll x17, x17, x20
    sll x14, x9, x22
    sll x13, x9, x15
    sub x15, x18, x20
    addi x11, x20, -1087
    sll x15, x15, x12
    srl x18, x18, x11
    sub x12, x20, x19
    li t6, 0x80010000
    sd x15, 48(t6)
    sub x16, x19, x23
    li t6, 0x80010000
    sd x9, 48(t6)
    xor x10, x10, x14
    sll x17, x14, x12
    sub x10, x10, x13
    li t6, 0x80010000
    sd x16, 40(t6)
    and x21, x16, x11
    li t6, 0x80010000
    sd x19, 56(t6)
    srl x18, x18, x19
    sll x16, x21, x19
    sub x20, x20, x11
    and x15, x16, x10
    or x14, x20, x18
    add x16, x16, x20
    add x16, x16, x23
    li t6, 0x80010000
    sd x10, 56(t6)
    sll x19, x23, x12
    xor x12, x12, x16
    sub x13, x13, x12
    sub x11, x23, x17
    xor x16, x14, x23
    srl x11, x11, x14
    addi x12, x23, 1401
    and x11, x18, x23
    add x12, x12, x15
    and x16, x17, x18
    add x17, x17, x11
    li t6, 0x80010000
    ld x20, 112(t6)
    xor x11, x10, x11
    xor x23, x14, x9
    li t6, 0x80010000
    ld x21, 0(t6)
    or x12, x12, x12
    srl x17, x16, x20
    sll x21, x18, x13
    srl x16, x16, x10
    sll x22, x19, x19
    sub x17, x9, x15
    sub x22, x14, x23
    srl x17, x17, x21
    sll x19, x19, x21
    srl x16, x18, x18
    li t6, 0x80010000
    sd x22, 16(t6)
    and x16, x10, x22
    and x17, x17, x13
    or x11, x11, x18
    srl x20, x10, x16
    add x15, x15, x15
    li t6, 0x80010000
    ld x12, 40(t6)
    sll x16, x9, x16
    li t6, 0x80010000
    sd x13, 24(t6)
    and x15, x15, x18
    or x18, x18, x11
    li t6, 0x80010000
    ld x14, 0(t6)
    and x21, x21, x19
    xor x15, x16, x17
    and x15, x15, x23
    srl x17, x16, x20
    sub x16, x16, x15
    add x19, x19, x13
    sub x15, x15, x12
    srl x11, x17, x11
    srl x13, x12, x19
    srl x13, x9, x19
    xor x20, x20, x19
    and x10, x10, x18
    or x23, x23, x11
    sll x21, x21, x15
    sll x16, x16, x20
    addi x20, x22, 1845
    addi x23, x17, -1800
    sub x20, x16, x17
    addi x21, x11, 1485
    sll x19, x19, x22
    li t6, 0x80010000
    sd x16, 8(t6)
    li t6, 0x80010000
    sd x13, 88(t6)
    addi x13, x17, 1341
    xor x10, x13, x15
    addi x21, x12, -1476
    li t6, 0x80010000
    sd x12, 120(t6)
    sll x13, x13, x11
    srl x17, x17, x21
    xor x18, x16, x15
    sub x18, x19, x9
    sub x23, x23, x12
    add x22, x22, x16
    xor x14, x14, x17
    or x9, x17, x12
    or x14, x14, x15
    sub x10, x18, x17
    xor x19, x9, x13
    sll x12, x12, x23
    srl x15, x10, x16
    sll x9, x9, x21
    xor x19, x19, x19
    and x17, x17, x14
    and x20, x20, x12
    xor x22, x22, x16
    sll x22, x22, x13
    srl x13, x13, x12
    li t6, 0x80010000
    ld x11, 104(t6)
    add x23, x23, x14
    or x20, x20, x12
    and x15, x20, x19
    sub x14, x22, x19
    and x16, x14, x21
    addi x19, x19, -1255
    or x12, x9, x23
    li t6, 0x80010000
    sd x15, 112(t6)
    or x22, x13, x18
    addi x21, x21, -1991
    or x15, x9, x23
    addi x12, x9, 568
    addi x23, x23, -1576
    li t6, 0x80010000
    ld x17, 64(t6)
    add x13, x13, x18
    addi x18, x11, 1690
    sub x9, x13, x14
    sll x23, x10, x13
    li t6, 0x80010000
    sd x9, 104(t6)
    li t6, 0x80010000
    ld x15, 80(t6)
    sub x14, x17, x10
    li t6, 0x80010000
    sd x21, 96(t6)
    sll x9, x9, x15
    add x17, x10, x16
    addi x11, x13, -806
    srl x12, x12, x18
    sll x16, x16, x15
    add x13, x13, x17
    addi x9, x9, -333
    addi x14, x23, -269
    li t6, 0x80010000
    ld x13, 24(t6)
    sub x11, x15, x14
    or x16, x16, x17
    xor x17, x9, x14
    and x19, x12, x16
    or x10, x15, x18
    xor x9, x9, x15
    srl x18, x18, x9
    sll x16, x9, x14
    and x11, x11, x20
    srl x22, x22, x16
    sll x22, x22, x9
    sub x12, x12, x14
    and x11, x11, x17
    and x18, x18, x10
    add x19, x18, x10
    sll x23, x23, x21
    sub x14, x14, x12
    add x22, x12, x15
    srl x16, x16, x22
    srl x10, x9, x11
    sub x10, x16, x19
    sll x23, x17, x15
    add x18, x9, x18
    sub x14, x14, x20
    or x21, x13, x16
    addi x12, x21, -1278
    or x17, x9, x18
    or x20, x20, x21
    add x23, x9, x15
    add x13, x10, x16
    or x16, x16, x23
    sub x12, x12, x9
    li t6, 0x80010000
    sd x19, 96(t6)
    or x15, x15, x10
    addi x17, x12, 1816
    srl x16, x16, x13
    addi x12, x12, 1945
    sll x22, x22, x20
    srl x15, x15, x10
    xor x10, x16, x19
    li t6, 0x80010000
    ld x18, 72(t6)
    sll x19, x12, x23
    addi x17, x17, 1116
    and x20, x18, x18
    sll x20, x20, x14
    and x13, x15, x20
    li t6, 0x80010000
    ld x20, 112(t6)
    and x13, x12, x20
    sll x19, x19, x15
    sub x15, x15, x14
    addi x18, x18, -103
    li t6, 0x80010000
    ld x13, 88(t6)
    sll x14, x13, x23
    and x10, x10, x17
    li t6, 0x80010000
    sd x16, 96(t6)
    or x9, x23, x12
    xor x16, x16, x17
    and x19, x14, x12
    sub x20, x20, x17
    sub x22, x14, x22
    add x19, x19, x22
    xor x12, x12, x23
    xor x19, x19, x19
    sll x21, x21, x11
    li t6, 0x80010000
    sd x18, 0(t6)
    sub x10, x10, x14
    addi x19, x20, -535
    xor x17, x21, x13
    sub x22, x20, x15
    srl x17, x16, x19
    addi x14, x14, 1684
    and x23, x23, x16
    sub x13, x18, x22
    and x17, x18, x11
    and x12, x20, x21
    xor x13, x13, x11
    sub x14, x13, x18
    sub x9, x9, x11
    addi x16, x14, -1407
    or x9, x18, x13
    addi x22, x12, 1610
    sub x17, x16, x12
    add x16, x16, x21
    sll x14, x10, x20
    sll x11, x11, x21
    srl x21, x21, x9
    xor x23, x16, x10
    li t6, 0x80010000
    sd x20, 56(t6)
    and x20, x19, x14
    li t6, 0x80010000
    ld x11, 0(t6)
    or x18, x18, x10
    srl x17, x14, x23
    add x23, x23, x19
    li t6, 0x80010000
    sd x19, 8(t6)
    or x20, x20, x19
    and x20, x23, x21
    sub x12, x22, x21
    add x11, x11, x12
    sub x14, x17, x12
    sub x22, x21, x18
    sub x23, x11, x21
    srl x22, x11, x19
    sub x17, x17, x20
    li t6, 0x80010000
    sd x23, 80(t6)
    srl x18, x15, x23
    xor x10, x10, x21
    and x16, x16, x17
    sll x14, x21, x15
    and x10, x15, x11
    li t6, 0x80010000
    ld x13, 0(t6)
    li t6, 0x80010000
    ld x11, 104(t6)
    sll x15, x23, x13
    addi x19, x21, 418
    and x12, x11, x12
    add x10, x11, x23
    xor x9, x19, x11
    srl x11, x11, x9
    sll x16, x16, x9
    or x11, x11, x9
    or x20, x18, x18
    addi x11, x11, 206
    li t6, 0x80010000
    ld x18, 24(t6)
    li t6, 0x80010000
    ld x19, 64(t6)
    li t6, 0x80010000
    sd x21, 88(t6)
    sll x11, x11, x12
    addi x23, x23, 1835
    li t6, 0x80010000
    ld x10, 120(t6)
    and x18, x20, x15
    addi x10, x10, 1784
    sll x14, x22, x11
    xor x23, x23, x9
    srl x17, x17, x14
    li t6, 0x80010000
    ld x14, 104(t6)
    sub x20, x11, x16
    and x14, x14, x14
    sll x10, x10, x23
    add x12, x12, x9
    sub x14, x14, x19
    addi x14, x10, -885
    or x19, x19, x10
    li t6, 0x80010000
    ld x13, 72(t6)
    add x17, x17, x20
    li t6, 0x80010000
    ld x17, 72(t6)
    sub x13, x13, x23
    or x21, x21, x21
    addi x18, x12, 435
    li t6, 0x80010000
    ld x20, 80(t6)
    addi x16, x23, -47
    xor x18, x18, x23
    sub x18, x22, x15
    or x12, x12, x21
    sll x13, x13, x21
    addi x10, x18, 673
    li t6, 0x80010000
    sd x11, 112(t6)
    sll x15, x15, x14
    sll x21, x21, x9
    li t6, 0x80010000
    ld x21, 88(t6)
    xor x16, x13, x20
    and x17, x19, x18
    addi x12, x9, -986
    and x20, x20, x21
    addi x15, x11, 971
    xor x13, x17, x19
    sub x9, x9, x12
    addi x18, x18, 313
    sll x13, x23, x18
    or x20, x22, x9
    and x16, x17, x20
    addi x13, x13, -1533
    addi x19, x19, -576
    or x16, x16, x14
    addi x19, x14, 1185
    xor x22, x22, x12
    or x14, x14, x12
    sll x15, x18, x18
    add x21, x21, x22
    sub x13, x13, x22
    sll x22, x18, x14
    li t6, 0x80010000
    sd x13, 0(t6)
    add x20, x20, x21
    addi x16, x11, -1445
    sll x14, x14, x11
    xor x22, x18, x16
    sub x21, x21, x19
    sub x14, x14, x13
    or x9, x9, x14
    sll x18, x10, x20
    or x14, x14, x13
    xor x23, x23, x12
    li t6, 0x80010000
    sd x15, 72(t6)
    srl x22, x15, x21
    srl x22, x22, x11
    sll x21, x21, x22
    and x15, x16, x18
    li t6, 0x80010000
    ld x22, 56(t6)
    sll x23, x23, x16
    or x15, x12, x18
    li t6, 0x80010000
    ld x14, 56(t6)
    xor x9, x12, x23
    li t6, 0x80010000
    ld x15, 56(t6)
    li t6, 0x80010000
    sd x21, 48(t6)
    add x11, x11, x16
    add x10, x19, x15
    li t6, 0x80010000
    sd x18, 32(t6)
    addi x21, x9, -203
    srl x15, x15, x15
    and x21, x21, x11
    sub x10, x10, x14
    and x22, x22, x17
    add x23, x23, x13
    srl x14, x9, x17
    xor x14, x20, x23
    srl x21, x14, x15
    li t6, 0x80010000
    ld x13, 48(t6)
    srl x21, x11, x17
    li t6, 0x80010000
    ld x12, 64(t6)
    srl x23, x15, x12
    li t6, 0x80010000
    sd x20, 120(t6)
    sub x22, x22, x20
    li t6, 0x80010000
    sd x15, 96(t6)
    sub x11, x11, x20
    sub x22, x19, x15
    and x22, x21, x20
    or x9, x9, x9
    and x22, x16, x22
    sll x11, x11, x10
    addi x18, x18, -1737
    sub x10, x23, x15
    or x17, x23, x9
    xor x10, x10, x17
    sll x11, x11, x10
    add x17, x17, x22
    li t6, 0x80010000
    ld x15, 56(t6)
    li t6, 0x80010000
    ld x21, 104(t6)
    or x23, x23, x20
    add x16, x19, x22
    li t6, 0x80010000
    ld x19, 64(t6)
    addi x18, x18, -1819
    addi x21, x18, -308
    sll x18, x20, x22
    and x21, x9, x22
    li t6, 0x80010000
    ld x9, 120(t6)
    srl x18, x18, x15
    or x9, x9, x19
    xor x22, x21, x14
    and x9, x9, x19
    addi x17, x17, 1315
    sll x9, x13, x22
    xor x12, x22, x22
    li t6, 0x80010000
    sd x13, 40(t6)
    xor x22, x22, x17
    add x15, x15, x17
    li t6, 0x80010000
    sd x13, 72(t6)
    sub x16, x10, x10
    li t6, 0x80010000
    ld x13, 96(t6)
    sll x16, x22, x17
    or x18, x18, x19
    and x23, x12, x17
    li t6, 0x80010000
    ld x14, 120(t6)
    xor x16, x13, x13
    xor x16, x17, x20
    li t6, 0x80010000
    sd x23, 24(t6)
    srl x17, x17, x18
    sll x14, x15, x21
    sll x15, x16, x12
    add x16, x16, x22
    or x23, x11, x9
    sub x14, x11, x13
    addi x9, x19, -767
    sll x17, x18, x14
    xor x13, x19, x17
    or x22, x23, x20
    li t6, 0x80010000
    ld x21, 72(t6)
    or x9, x9, x20
    or x16, x13, x12
    xor x17, x22, x14
    sub x12, x12, x15
    and x23, x21, x14
    and x11, x11, x19
    li t6, 0x80010000
    sd x17, 56(t6)
    sll x22, x11, x12
    and x15, x12, x20
    li t6, 0x80010000
    ld x20, 56(t6)
    addi x16, x18, 853
    li t6, 0x80010000
    sd x18, 64(t6)
    and x14, x15, x13
    and x15, x12, x23
    li t6, 0x80010000
    ld x21, 72(t6)
    srl x17, x17, x19
    srl x15, x17, x15
    sub x16, x14, x11
    sub x20, x11, x18
    add x20, x20, x9
    add x20, x19, x13
    and x20, x10, x18
    add x12, x12, x14
    and x21, x21, x13
    li t6, 0x80010000
    ld x20, 40(t6)
    srl x22, x22, x21
    add x23, x23, x17
    li t6, 0x80010000
    ld x12, 88(t6)
    xor x21, x23, x22
    srl x11, x21, x15
    or x16, x16, x15
    srl x16, x15, x13
    sub x12, x12, x16
    add x21, x21, x11
    addi x17, x17, -1812
    sub x15, x20, x17
    srl x21, x21, x12
    and x11, x11, x12
    addi x19, x18, 859
    li t6, 0x80010000
    sd x9, 112(t6)
    sub x10, x14, x17
    srl x16, x16, x23
    and x9, x18, x10
    li t6, 0x80010000
    ld x9, 40(t6)
    li t6, 0x80010000
    sd x18, 112(t6)
    srl x14, x21, x22
    li t6, 0x80010000
    sd x14, 24(t6)
    and x13, x13, x19
    and x13, x13, x16
    sub x13, x13, x17
    li t6, 0x80010000
    sd x10, 64(t6)
    addi x10, x10, -1701
    li t6, 0x80010000
    ld x17, 112(t6)
    and x13, x13, x19
    li t6, 0x80010000
    sd x22, 80(t6)
    sub x11, x11, x21
    or x9, x9, x18
    sub x14, x17, x12
    or x11, x16, x12
    li t6, 0x80010000
    ld x11, 96(t6)
    sub x13, x13, x20
    li t6, 0x80010000
    ld x9, 56(t6)
    li t6, 0x80010000
    sd x14, 40(t6)
    sll x12, x12, x19
    li t6, 0x80010000
    sd x16, 56(t6)
    add x15, x16, x21
    or x16, x19, x22
    and x20, x17, x13
    addi x20, x20, 476
    sub x20, x20, x18
    li t6, 0x80010000
    sd x20, 120(t6)
    sub x17, x23, x18
    or x10, x13, x18
    sll x21, x21, x21
    srl x15, x15, x22
    sll x12, x15, x14
    xor x13, x13, x20
    li t6, 0x80010000
    ld x16, 88(t6)
    li t6, 0x80010000
    ld x18, 64(t6)
    and x20, x20, x15
    li t6, 0x80010000
    ld x17, 16(t6)
    xor x14, x14, x19
    and x22, x22, x15
    or x21, x15, x11
    li t6, 0x80010000
    ld x17, 0(t6)
    addi x13, x13, -346
    add x20, x20, x23
    or x21, x23, x13
    sll x15, x15, x16
    li t6, 0x80010000
    sd x23, 0(t6)
    addi x16, x16, -605
    and x23, x10, x19
    sub x9, x22, x10
    addi x22, x22, 792
    add x16, x15, x21
    li t6, 0x80010000
    sd x23, 96(t6)
    and x15, x17, x23
    xor x15, x11, x11
    li t6, 0x80010000
    ld x10, 56(t6)
    and x15, x22, x18
    li t6, 0x80010000
    sd x19, 88(t6)
    add x17, x17, x14
    addi x22, x20, -2032
    li t6, 0x80010000
    ld x11, 96(t6)
    xor x21, x18, x16
    li t6, 0x80010000
    ld x12, 96(t6)
    addi x23, x23, -976
    or x22, x22, x10
    li t6, 0x80010000
    ld x14, 104(t6)
    and x15, x15, x19
    li t6, 0x80010000
    sd x13, 0(t6)
    srl x14, x14, x15
    or x12, x9, x21
    sll x21, x21, x20
    sll x15, x15, x16
    li t6, 0x80010000
    ld x16, 88(t6)
    add x12, x21, x18
    srl x14, x13, x19
    and x10, x22, x17
    addi x11, x9, 431
    and x17, x17, x9
    addi x20, x10, 1725
    sll x22, x19, x22
    addi x23, x23, -948
    and x19, x19, x14
    srl x20, x20, x17
    srl x13, x19, x19
    addi x11, x11, 1438
    li t6, 0x80010000
    sd x12, 112(t6)
    li t6, 0x80010000
    sd x20, 8(t6)
    or x23, x23, x16
    xor x18, x18, x21
    li t6, 0x80010000
    ld x21, 0(t6)
    add x23, x23, x9
    addi x15, x15, 1044
    srl x19, x13, x16
    li t6, 0x80010000
    ld x13, 0(t6)
    sub x14, x14, x10
    xor x15, x22, x9
    or x20, x20, x15
    addi x13, x13, -47
    xor x9, x18, x23
    li t6, 0x80010000
    ld x22, 56(t6)
    li t6, 0x80010000
    sd x17, 24(t6)
    xor x10, x10, x11
    sll x21, x21, x17
    srl x10, x22, x17
    addi x22, x12, 57
    sll x9, x16, x14
    srl x11, x11, x11
    sub x9, x9, x17
    or x11, x14, x12
    sll x15, x15, x15
    li t6, 0x80010000
    ld x19, 96(t6)
    and x13, x13, x19
    and x9, x17, x20
    xor x11, x11, x18
    sll x23, x23, x14
    or x10, x15, x18
    srl x16, x12, x9
    li t6, 0x80010000
    sd x17, 0(t6)
    li t6, 0x80010000
    ld x11, 64(t6)
    and x12, x14, x16
    srl x20, x21, x15
    and x23, x23, x22
    li t6, 0x80010000
    sd x18, 72(t6)
    xor x21, x15, x16
    addi x22, x15, 1775
    add x12, x18, x15
    add x22, x16, x12
    addi x23, x23, 401
    li t6, 0x80010000
    sd x22, 8(t6)
    li t6, 0x80010000
    sd x16, 112(t6)
    and x12, x12, x13
    srl x20, x22, x23
    sll x14, x14, x11
    li t6, 0x80010000
    ld x12, 112(t6)
    li t6, 0x80010000
    ld x12, 64(t6)
    srl x20, x20, x13
    sll x19, x17, x20
    srl x13, x20, x11
    sll x10, x17, x10
    xor x21, x21, x14
    sll x21, x21, x10
    xor x19, x16, x20
    srl x20, x20, x18
    addi x14, x14, 2043
    li t6, 0x80010000
    sd x16, 0(t6)
    li t6, 0x80010000
    sd x12, 112(t6)
    sub x19, x21, x23
    addi x18, x13, 1744
    li t6, 0x80010000
    sd x16, 24(t6)
    xor x19, x19, x13
    li t6, 0x80010000
    sd x17, 24(t6)
    sub x19, x19, x16
    addi x14, x14, 1912
    or x19, x23, x14
    srl x12, x12, x15
    sub x15, x12, x9
    add x15, x15, x19
    or x21, x23, x16
    xor x9, x19, x22
    add x18, x21, x18
    or x9, x17, x17
    add x12, x18, x23
    and x14, x14, x15
    addi x16, x16, 1996
    add x16, x16, x11
    li t6, 0x80010000
    ld x22, 32(t6)
    srl x12, x17, x11
    li t6, 0x80010000
    ld x13, 80(t6)
    and x22, x18, x18
    srl x13, x9, x18
    and x23, x23, x19
    sll x23, x15, x13
    li t6, 0x80010000
    sd x21, 32(t6)
    sub x9, x11, x20
    li t6, 0x80010000
    ld x21, 24(t6)
    xor x9, x9, x19
    xor x11, x23, x22
    sub x23, x23, x22
    srl x11, x20, x20
    srl x23, x23, x17
    add x12, x12, x12
    srl x19, x19, x19
    sll x16, x15, x23
    and x18, x18, x19
    sll x14, x14, x16
    and x23, x23, x11
    li t6, 0x80010000
    sd x22, 24(t6)
    li t6, 0x80010000
    ld x11, 16(t6)
    or x20, x16, x21
    addi x13, x11, -2024
    add x20, x20, x20
    srl x22, x18, x20
    addi x18, x18, 863
    li t6, 0x80010000
    ld x22, 88(t6)
    add x23, x16, x9
    li t6, 0x80010000
    sd x13, 64(t6)
    sll x11, x10, x11
    and x12, x12, x12
    li t6, 0x80010000
    ld x9, 64(t6)
    sub x10, x10, x15
    xor x22, x22, x18
    add x23, x20, x21
    srl x16, x16, x23
    li t6, 0x80010000
    sd x14, 96(t6)
    or x10, x11, x12
    li t6, 0x80010000
    ld x9, 40(t6)
    addi x15, x15, -1537
    li t6, 0x80010000
    sd x18, 0(t6)
    and x19, x10, x20
    sub x22, x12, x11
    and x16, x16, x18
    sll x21, x20, x14
    li t6, 0x80010000
    sd x12, 120(t6)
    srl x23, x18, x22
    srl x18, x15, x11
    or x20, x16, x19
    sub x19, x15, x11
    li t6, 0x80010000
    ld x12, 120(t6)
    srl x9, x16, x15
    sub x15, x23, x18
    add x9, x9, x15
    xor x14, x14, x14
    or x18, x20, x19
    xor x15, x15, x11
    xor x13, x13, x17
    or x22, x22, x19
    or x19, x17, x12
    or x21, x16, x17
    srl x19, x19, x14
    or x9, x18, x11
    srl x13, x20, x10
    add x21, x21, x21
    srl x14, x23, x14
    or x12, x12, x21
    xor x17, x17, x16
    add x10, x9, x19
    li t6, 0x80010000
    sd x22, 8(t6)
    sub x15, x15, x10
    sll x23, x23, x15
    addi x18, x21, 1067
    sll x15, x15, x9
    sll x12, x12, x12
    addi x11, x13, 797
    or x22, x12, x15
    and x18, x23, x18
    srl x12, x9, x11
    srl x21, x21, x14
    sub x15, x10, x18
    addi x14, x20, -1667
    sll x14, x14, x19
    sub x21, x21, x21
    srl x17, x17, x17
    addi x22, x22, -933
    sll x22, x22, x23
    and x23, x16, x23
    xor x13, x13, x21
    and x14, x18, x16
    sll x15, x12, x15
    li t6, 0x80010000
    ld x12, 80(t6)
    and x18, x18, x23
    sub x21, x21, x16
    li t6, 0x80010000
    ld x20, 104(t6)
    add x19, x19, x17
    addi x20, x9, -1292
    srl x16, x16, x13
    and x11, x21, x16
    or x15, x15, x13
    srl x10, x10, x16
    add x14, x14, x12
    addi x19, x16, 1174
    add x14, x14, x14
    sll x10, x15, x14
    or x12, x12, x23
    add x13, x14, x20
    sub x17, x22, x22
    add x16, x13, x10
    addi x11, x13, 824
    sll x15, x16, x14
    li t6, 0x80010000
    ld x22, 64(t6)
    or x23, x17, x15
    sll x11, x14, x13
    li t6, 0x80010000
    sd x15, 120(t6)
    add x23, x22, x12
    li t6, 0x80010000
    sd x15, 8(t6)
    addi x12, x13, -332
    addi x21, x19, 1822
    add x11, x11, x22
    xor x10, x10, x17
    or x14, x14, x19
    sll x19, x19, x15
    sub x9, x21, x11
    or x14, x14, x21
    or x21, x21, x9
    and x18, x20, x10
    and x11, x11, x16
    li t6, 0x80010000
    sd x10, 120(t6)
    or x12, x14, x10
    sub x11, x16, x14
    addi x9, x12, 842
    sll x20, x20, x21
    li t6, 0x80010000
    sd x11, 88(t6)
    sub x12, x13, x16
    li t6, 0x80010000
    sd x9, 48(t6)
    xor x10, x10, x13
    li t6, 0x80010000
    sd x9, 88(t6)
    and x11, x11, x9
    sub x15, x16, x11
    or x11, x12, x21
    or x18, x10, x23
    sll x19, x12, x21
    li t6, 0x80010000
    sd x16, 0(t6)
    li t6, 0x80010000
    ld x14, 0(t6)
    sll x15, x19, x18
    xor x20, x20, x9
    add x20, x20, x15
    li t6, 0x80010000
    sd x16, 88(t6)
    sll x20, x20, x18
    add x11, x11, x22
    and x14, x14, x14
    sll x23, x21, x16
    srl x23, x23, x9
    or x13, x17, x11
    or x20, x15, x22
    li t6, 0x80010000
    ld x21, 0(t6)
    sub x19, x19, x17
    addi x12, x12, 1520
    li t6, 0x80010000
    ld x18, 64(t6)
    srl x21, x19, x17
    and x18, x23, x14
    xor x14, x22, x12
    li t6, 0x80010000
    sd x12, 40(t6)
    sub x13, x13, x23
    li t6, 0x80010000
    sd x18, 64(t6)
    or x14, x11, x11
    li t6, 0x80010000
    sd x23, 24(t6)
    or x16, x15, x9
    li t6, 0x80010000
    ld x12, 56(t6)
    addi x18, x11, -1126
    srl x19, x12, x16
    li t6, 0x80010000
    sd x19, 64(t6)
    sub x16, x23, x21
    and x18, x12, x21
    addi x15, x15, -1342
    sll x10, x10, x20
    add x16, x23, x9
    and x22, x22, x16
    li t6, 0x80010000
    ld x18, 0(t6)
    srl x20, x20, x23
    xor x23, x14, x23
    sub x11, x11, x21
    and x18, x21, x20
    sll x11, x11, x21
    or x23, x23, x16
    li t6, 0x80010000
    ld x22, 96(t6)
    or x19, x19, x13
    add x12, x9, x13
    li t6, 0x80010000
    sd x20, 16(t6)
    srl x15, x16, x15
    addi x16, x14, 891
    srl x20, x18, x23
    xor x18, x9, x20
    and x23, x10, x17
    or x15, x15, x16
    li t6, 0x80010000
    sd x22, 96(t6)
    srl x19, x19, x13
    or x11, x12, x11
    xor x9, x23, x23
    add x11, x15, x10
    li t6, 0x80010000
    sd x18, 64(t6)
    li t6, 0x80010000
    ld x10, 0(t6)
    xor x22, x19, x22
    li t6, 0x80010000
    sd x14, 72(t6)
    li t6, 0x80010000
    ld x12, 8(t6)
    add x13, x10, x15
    li t6, 0x80010000
    ld x21, 56(t6)
    li t6, 0x80010000
    sd x22, 120(t6)
    li t6, 0x80010000
    sd x9, 40(t6)
    addi x11, x22, -841
    li t6, 0x80010000
    sd x9, 24(t6)
    add x10, x10, x21
    li t6, 0x80010000
    ld x19, 80(t6)
    add x18, x13, x11
    add x16, x23, x19
    srl x22, x22, x17
    li t6, 0x80010000
    ld x20, 56(t6)
    addi x17, x17, 1350
    or x13, x16, x10
    or x9, x12, x19
    srl x11, x11, x9
    xor x20, x20, x15
    sub x14, x14, x19
    sll x19, x20, x17
    and x10, x21, x14
    sll x21, x18, x23
    li t6, 0x80010000
    ld x19, 104(t6)
    addi x11, x18, -1394
    and x16, x17, x21
    li t6, 0x80010000
    ld x11, 96(t6)
    and x13, x12, x13
    or x10, x18, x16
    addi x15, x15, 1020
    xor x9, x12, x19
    sub x11, x17, x21
    and x15, x15, x23
    add x23, x23, x19
    sll x23, x19, x22
    srl x21, x14, x16
    or x16, x16, x15
    li t6, 0x80010000
    ld x19, 8(t6)
    sll x20, x20, x23
    xor x22, x22, x11
    and x12, x14, x15
    li t6, 0x80010000
    sd x11, 120(t6)
    sub x22, x22, x17
    and x22, x22, x22
    li t6, 0x80010000
    ld x10, 104(t6)
    addi x13, x19, -1746
    or x15, x15, x10
    and x12, x10, x12
    sll x17, x9, x13
    and x23, x13, x12
    addi x14, x20, 1000
    add x11, x11, x16
    sll x20, x17, x12
    li t6, 0x80010000
    sd x14, 104(t6)
    srl x20, x11, x21
    li t6, 0x80010000
    sd x10, 40(t6)
    and x17, x20, x12
    li t6, 0x80010000
    sd x22, 24(t6)
    or x14, x19, x18
    li t6, 0x80010000
    ld x23, 56(t6)
    sll x18, x10, x17
    srl x22, x21, x19
    srl x17, x17, x22
    or x20, x20, x21
    or x14, x20, x9
    li t6, 0x80010000
    sd x15, 104(t6)
    li t6, 0x80010000
    sd x17, 16(t6)
    xor x19, x19, x23
    add x18, x12, x21
    and x23, x23, x20
    addi x20, x20, 491
    li t6, 0x80010000
    ld x10, 64(t6)
    and x11, x20, x11
    sll x10, x10, x19
    addi x13, x18, -1143
    add x17, x17, x22
    or x13, x13, x22
    xor x19, x19, x16
    srl x17, x12, x9
    sll x20, x18, x20
    srl x16, x10, x9
    li t6, 0x80010000
    ld x17, 112(t6)
    add x22, x22, x16
    li t6, 0x80010000
    ld x20, 8(t6)
    srl x17, x23, x15
    xor x20, x17, x19
    or x10, x10, x10
    li t6, 0x80010000
    ld x11, 104(t6)
    and x15, x15, x17
    and x16, x16, x11
    addi x13, x19, -1203
    li t6, 0x80010000
    ld x15, 8(t6)
    add x10, x15, x10
    li t6, 0x80010000
    sd x10, 24(t6)
    sll x19, x19, x22
    sll x17, x10, x19
    addi x11, x11, -1545
    sub x17, x10, x10
    srl x11, x11, x18
    xor x22, x10, x21
    li t6, 0x80010000
    sd x17, 72(t6)
    and x20, x22, x20
    sub x16, x16, x22
    li t6, 0x80010000
    sd x13, 72(t6)
    add x10, x10, x16
    sll x15, x9, x10
    li t6, 0x80010000
    ld x14, 120(t6)
    sub x14, x14, x18
    add x17, x17, x13
    li t6, 0x80010000
    sd x15, 64(t6)
    xor x13, x15, x19
    and x11, x11, x23
    li t6, 0x80010000
    sd x19, 24(t6)
    sll x18, x19, x11
    li t6, 0x80010000
    ld x13, 88(t6)
    or x22, x22, x22
    or x11, x15, x14
    li t6, 0x80010000
    sd x20, 40(t6)
    addi x20, x19, 349
    or x19, x11, x18
    xor x12, x16, x22
    srl x10, x10, x18
    and x22, x22, x19
    add x23, x16, x18
    add x20, x11, x12
    add x17, x12, x11
    addi x16, x16, -19
    li t6, 0x80010000
    sd x17, 56(t6)
    and x22, x23, x15
    sll x10, x10, x15
    or x20, x9, x16
    add x15, x17, x9
    add x19, x19, x19
    li t6, 0x80010000
    sd x10, 48(t6)
    add x12, x12, x9
    or x18, x18, x21
    or x21, x21, x12
    sub x22, x18, x12
    sll x17, x17, x11
    srl x10, x9, x22
    sll x17, x17, x16
    add x22, x22, x12
    add x14, x15, x23
    addi x17, x18, 1762
    li t6, 0x80010000
    ld x22, 32(t6)
    srl x9, x20, x13
    sll x20, x17, x12
    addi x17, x17, -897
    addi x22, x15, 182
    or x15, x15, x20
    sub x22, x22, x11
    srl x12, x18, x19
    sub x15, x20, x17
    xor x15, x15, x13
    and x10, x14, x13
    li t6, 0x80010000
    ld x9, 0(t6)
    li t6, 0x80010000
    sd x15, 96(t6)
    sll x17, x17, x19
    xor x21, x21, x22
    li t6, 0x80010000
    sd x15, 40(t6)
    srl x17, x12, x10
    and x17, x17, x9
    sub x20, x10, x20
    sll x12, x11, x23
    or x22, x22, x9
    srl x9, x13, x15
    or x11, x11, x9
    sub x19, x19, x9
    and x23, x22, x11
    or x10, x10, x16
    addi x13, x13, 1008
    and x11, x16, x15
    li t6, 0x80010000
    ld x12, 8(t6)
    or x17, x17, x9
    sll x19, x19, x9
    or x17, x23, x16
    xor x12, x13, x22
    sub x16, x21, x22
    or x22, x22, x20
    li t6, 0x80010000
    sd x16, 32(t6)
    or x13, x12, x19
    xor x10, x18, x22
    li t6, 0x80010000
    sd x17, 56(t6)
    xor x22, x10, x14
    srl x9, x9, x21
    srl x10, x12, x16
    xor x21, x21, x9
    add x23, x9, x18
    or x10, x15, x23
    sub x9, x19, x16
    xor x19, x13, x20
    add x11, x14, x23
    xor x20, x20, x16
    xor x22, x23, x10
    xor x22, x22, x22
    sub x10, x20, x16
    or x17, x13, x9
    or x20, x20, x10
    li t6, 0x80010000
    ld x10, 96(t6)
    xor x15, x15, x17
    add x9, x9, x11
    and x17, x12, x10
    li t6, 0x80010000
    ld x22, 72(t6)
    addi x12, x11, -258
    sll x9, x18, x11
    and x20, x9, x12
    li t6, 0x80010000
    ld x16, 16(t6)
    sll x12, x12, x23
    sub x15, x15, x16
    addi x19, x19, -1914
    xor x21, x21, x17
    li t6, 0x80010000
    ld x21, 56(t6)
    addi x12, x12, -35
    srl x19, x19, x21
    add x21, x17, x23
    or x12, x17, x10
    xor x11, x16, x14
    li t6, 0x80010000
    ld x20, 64(t6)
    xor x21, x21, x18
    sub x16, x19, x17
    sll x22, x10, x14
    or x14, x19, x9
    srl x14, x14, x21
    srl x11, x15, x20
    and x17, x21, x11
    add x21, x10, x21
    sll x20, x22, x13
    xor x19, x19, x16
    addi x19, x19, 1638
    and x19, x9, x17
    xor x23, x23, x10
    li t6, 0x80010000
    sd x18, 104(t6)
    srl x11, x11, x20
    srl x12, x17, x20
    and x11, x13, x14
    srl x9, x17, x14
    sub x18, x18, x9
    sub x16, x16, x22
    li t6, 0x80010000
    sd x13, 16(t6)
    xor x13, x21, x14
    li t6, 0x80010000
    sd x10, 56(t6)
    srl x12, x12, x13
    li t6, 0x80010000
    ld x16, 16(t6)
    add x9, x16, x12
    addi x9, x17, 531
    sll x14, x14, x10
    srl x9, x20, x16
    srl x16, x13, x18
    or x20, x13, x22
    add x21, x13, x16
    addi x22, x9, 549
    srl x17, x21, x23
    sub x14, x16, x11
    or x9, x13, x11
    addi x20, x20, -127
    li t6, 0x80010000
    ld x20, 48(t6)
    sub x11, x11, x14
    sll x19, x15, x21
    srl x15, x15, x20
    li t6, 0x80010000
    sd x9, 72(t6)
    addi x13, x13, 722
    li t6, 0x80010000
    ld x14, 32(t6)
    li t6, 0x80010000
    ld x13, 64(t6)
    srl x15, x15, x20
    li t6, 0x80010000
    sd x21, 96(t6)
    add x14, x16, x14
    srl x11, x12, x10
    and x10, x10, x23
    li t6, 0x80010000
    ld x23, 104(t6)
    sll x17, x16, x9
    addi x11, x11, -988
    and x17, x17, x19
    sub x11, x20, x19
    sll x19, x20, x14
    srl x23, x23, x12
    li t6, 0x80010000
    sd x18, 24(t6)
    sll x20, x23, x19
    sll x18, x13, x14
    li t6, 0x80010000
    sd x16, 16(t6)
    li t6, 0x80010000
    ld x21, 120(t6)
    xor x23, x23, x11
    srl x23, x23, x16
    xor x14, x23, x14
    or x13, x12, x9
    srl x20, x17, x22
    srl x18, x18, x22
    or x21, x18, x12
    and x9, x9, x9
    srl x20, x23, x22
    sub x15, x16, x15
    sub x10, x10, x9
    sub x10, x10, x22
    or x17, x21, x13
    or x13, x13, x10
    li t6, 0x80010000
    ld x22, 16(t6)
    xor x12, x18, x16
    or x13, x13, x18
    li t6, 0x80010000
    sd x15, 8(t6)
    xor x22, x22, x11
    srl x17, x11, x10
    sll x18, x18, x17
    and x19, x15, x13
    li t6, 0x80010000
    sd x9, 0(t6)
    addi x14, x14, -1004
    sub x16, x14, x14
    and x19, x19, x14
    or x22, x22, x20
    or x17, x9, x11
    and x10, x16, x21
    add x11, x11, x12
    addi x12, x11, -1501
    srl x9, x9, x16
    and x21, x18, x13
    li t6, 0x80010000
    sd x15, 96(t6)
    sub x10, x22, x11
    add x16, x9, x9
    srl x21, x12, x22
    and x13, x21, x20
    or x10, x13, x11
    sll x16, x13, x21
    srl x14, x16, x20
    srl x13, x21, x17
    xor x21, x20, x11
    sub x14, x18, x19
    srl x22, x22, x21
    srl x20, x20, x14
    add x20, x21, x11
    xor x13, x13, x19
    or x12, x19, x17
    add x22, x10, x18
    addi x22, x22, 360
    addi x21, x21, -812
    li t6, 0x80010000
    ld x21, 104(t6)
    srl x16, x14, x19
    srl x21, x11, x13
    li t6, 0x80010000
    sd x21, 0(t6)
    li t6, 0x80010000
    sd x9, 8(t6)
    and x9, x9, x10
    add x15, x15, x12
    or x13, x13, x20
    srl x15, x10, x9
    sll x12, x23, x12
    li t6, 0x80010000
    sd x18, 72(t6)
    add x14, x14, x9
    add x14, x22, x17
    and x20, x10, x12
    and x10, x19, x18
    addi x12, x11, -1748
    add x12, x10, x15
    li t6, 0x80010000
    ld x17, 56(t6)
    and x20, x13, x18
    sll x14, x10, x19
    li t6, 0x80010000
    sd x14, 104(t6)
    addi x11, x11, 1712
    and x10, x10, x22
    li t6, 0x80010000
    ld x22, 96(t6)
    xor x15, x21, x14
    sll x16, x13, x11
    li t6, 0x80010000
    sd x9, 72(t6)
    sub x11, x11, x19
    and x13, x12, x23
    srl x11, x11, x19
    li t6, 0x80010000
    sd x12, 56(t6)
    add x23, x23, x13
    li t6, 0x80010000
    ld x9, 32(t6)
    sll x11, x11, x18
    sll x11, x11, x18
    xor x21, x15, x22
    or x16, x16, x10
    add x12, x12, x23
    add x17, x10, x13
    li t6, 0x80010000
    sd x15, 32(t6)
    xor x22, x22, x11
    and x20, x10, x22
    li t6, 0x80010000
    sd x12, 80(t6)
    or x9, x9, x18
    sll x16, x16, x11
    xor x11, x11, x21
    addi x21, x14, 1485
    li t6, 0x80010000
    sd x12, 32(t6)
    sub x10, x12, x9
    li t6, 0x80010000
    sd x19, 24(t6)
    xor x20, x22, x9
    li t6, 0x80010000
    ld x18, 0(t6)
    li t6, 0x80010000
    ld x14, 120(t6)
    or x16, x21, x21
    sub x17, x17, x19
    addi x16, x14, -1467
    and x12, x19, x20
    and x20, x17, x23
    addi x14, x18, -863
    li t6, 0x80010000
    ld x18, 64(t6)
    sub x12, x12, x22
    li t6, 0x80010000
    sd x19, 104(t6)
    li t6, 0x80010000
    sd x10, 8(t6)
    li t6, 0x80010000
    ld x17, 64(t6)
    or x22, x9, x15
    add x23, x23, x14
    xor x15, x15, x20
    srl x22, x19, x21
    sub x9, x14, x23
    or x20, x16, x22
    and x12, x12, x18
    or x16, x9, x13
    srl x16, x18, x10
    addi x19, x19, 615
    add x10, x21, x12
    sub x23, x23, x10
    srl x17, x21, x23
    li t6, 0x80010000
    sd x10, 0(t6)
    xor x20, x20, x20
    and x19, x18, x11
    li t6, 0x80010000
    ld x19, 16(t6)
    sll x21, x21, x17
    addi x21, x15, 1121
    sub x20, x20, x16
    srl x14, x15, x18
    li t6, 0x80010000
    ld x10, 80(t6)
    addi x23, x16, 1841
    sub x20, x20, x18
    sll x12, x16, x17
    li t6, 0x80010000
    ld x9, 40(t6)
    and x17, x10, x11
    xor x12, x19, x17
    or x16, x15, x13
    or x15, x15, x12
    and x19, x14, x19
    and x12, x17, x14
    sub x13, x13, x16
    li t6, 0x80010000
    ld x23, 72(t6)
    sub x12, x12, x23
    sll x18, x20, x17
    sll x12, x15, x22
    li t6, 0x80010000
    sd x23, 40(t6)
    or x13, x13, x9
    xor x23, x21, x23
    and x16, x16, x18
    sub x23, x9, x22
    and x11, x12, x13
    sll x12, x12, x20
    srl x14, x14, x20
    sll x14, x14, x20
    sub x18, x11, x12
    sll x16, x16, x9
    li t6, 0x80010000
    sd x10, 80(t6)
    sll x14, x16, x17
    xor x23, x10, x23
    addi x14, x14, -733
    addi x20, x10, -194
    li t6, 0x80010000
    ld x10, 80(t6)
    li t6, 0x80010000
    sd x18, 120(t6)
    and x19, x11, x12
    li t6, 0x80010000
    ld x10, 32(t6)
    srl x15, x18, x16
    and x22, x22, x20
    li t6, 0x80010000
    ld x12, 8(t6)
    srl x21, x18, x11
    srl x23, x14, x18
    addi x13, x14, 868
    srl x19, x18, x9
    add x23, x23, x10
    li t6, 0x80010000
    ld x10, 120(t6)
    li t6, 0x80010000
    sd x19, 40(t6)
    add x19, x19, x16
    and x20, x20, x21
    li t6, 0x80010000
    sd x17, 24(t6)
    li t6, 0x80010000
    sd x9, 88(t6)
    li t6, 0x80010000
    ld x9, 120(t6)
    srl x13, x19, x17
    or x15, x23, x22
    and x11, x11, x14
    li t6, 0x80010000
    ld x20, 56(t6)
    li t6, 0x80010000
    sd x10, 40(t6)
    li t6, 0x80010000
    ld x21, 0(t6)
    li t6, 0x80010000
    sd x18, 88(t6)
    sub x22, x22, x20
    xor x23, x23, x14
    srl x21, x12, x22
    xor x11, x11, x18
    li t6, 0x80010000
    sd x12, 80(t6)
    srl x18, x18, x12
    and x22, x10, x12
    li t6, 0x80010000
    ld x12, 8(t6)
    srl x15, x17, x21
    or x14, x19, x15
    li t6, 0x80010000
    sd x14, 88(t6)
    and x20, x20, x11
    and x12, x10, x20
    xor x22, x22, x23
    sll x21, x16, x15
    or x14, x14, x12
    li t6, 0x80010000
    sd x17, 88(t6)
    li t6, 0x80010000
    sd x9, 0(t6)
    sll x20, x15, x14
    add x22, x23, x10
    xor x17, x17, x21
    or x14, x20, x10
    sub x18, x14, x21
    sub x16, x22, x9
    li t6, 0x80010000
    sd x14, 96(t6)
    and x16, x17, x11
    addi x14, x18, -1145
    add x10, x13, x18
    or x23, x22, x15
    xor x19, x11, x21
    li t6, 0x80010000
    ld x19, 112(t6)
    sub x21, x13, x15
    srl x23, x13, x11
    sub x17, x17, x13
    xor x18, x18, x20
    or x20, x14, x13
    xor x18, x18, x16
    li t6, 0x80010000
    sd x12, 104(t6)
    and x23, x23, x12
    li t6, 0x80010000
    sd x18, 16(t6)
    srl x20, x20, x16
    srl x11, x19, x15
    sll x9, x10, x11
    li t6, 0x80010000
    sd x10, 88(t6)
    srl x10, x23, x10
    add x11, x13, x17
    li t6, 0x80010000
    ld x12, 64(t6)
    xor x18, x19, x14
    srl x21, x19, x15
    addi x10, x10, 1538
    addi x22, x22, 1054
    or x15, x22, x22
    add x22, x22, x23
    add x12, x15, x13
    or x16, x20, x10
    xor x15, x15, x9
    or x12, x12, x21
    xor x22, x16, x20
    xor x13, x13, x20
    sub x17, x20, x17
    li t6, 0x80010000
    ld x10, 72(t6)
    li t6, 0x80010000
    sd x13, 120(t6)
    add x15, x18, x19
    srl x13, x13, x19
    xor x17, x17, x14
    add x11, x11, x12
    or x14, x14, x22
    or x15, x10, x19
    sub x14, x9, x9
    addi x12, x12, -365
    addi x16, x13, 1240
    sub x16, x16, x18
    add x23, x23, x23
    add x18, x22, x12
    li t6, 0x80010000
    sd x18, 0(t6)
    sub x19, x19, x14
    srl x15, x20, x15
    sub x9, x9, x10
    sub x16, x11, x18
    xor x21, x21, x16
    addi x12, x19, 162
    or x17, x10, x23
    sub x12, x12, x19
    xor x13, x13, x9
    sub x12, x15, x12
    sub x21, x21, x16
    xor x16, x16, x15
    add x22, x22, x9
    sll x11, x11, x9
    li t6, 0x80010000
    ld x23, 56(t6)
    li t6, 0x80010000
    ld x18, 0(t6)
    li t6, 0x80010000
    sd x19, 16(t6)
    addi x13, x13, -146
    li t6, 0x80010000
    sd x16, 40(t6)
    li t6, 0x80010000
    sd x9, 104(t6)
    and x16, x11, x11
    li t6, 0x80010000
    ld x16, 72(t6)
    sll x19, x20, x15
    add x20, x11, x12
    sll x13, x13, x9
    xor x13, x13, x17
    sll x16, x16, x22
    add x20, x17, x18
    sll x18, x12, x12
    li t6, 0x80010000
    sd x13, 112(t6)
    li t6, 0x80010000
    ld x17, 16(t6)
    and x15, x17, x11
    and x11, x9, x10
    xor x20, x20, x17
    add x20, x14, x18
    li t6, 0x80010000
    ld x23, 64(t6)
    li t6, 0x80010000
    ld x18, 8(t6)
    li t6, 0x80010000
    sd x13, 72(t6)
    add x19, x12, x13
    xor x16, x13, x19
    srl x17, x18, x21
    xor x20, x20, x20
    add x10, x10, x12
    or x9, x12, x14
    and x12, x12, x12
    sll x21, x21, x22
    sub x17, x17, x13
    srl x15, x15, x9
    li t6, 0x80010000
    sd x16, 56(t6)
    li t6, 0x80010000
    sd x14, 72(t6)
    add x21, x16, x18
    or x12, x12, x17
    li t6, 0x80010000
    ld x17, 40(t6)
    or x12, x12, x15
    or x14, x14, x13
    and x15, x14, x20
    sub x15, x15, x22
    sll x19, x22, x15
    li t6, 0x80010000
    ld x19, 64(t6)
    sub x9, x19, x17
    xor x22, x13, x23
    xor x16, x16, x15
    or x9, x9, x10
    srl x23, x23, x10
    and x12, x12, x17
    and x17, x15, x12
    add x23, x22, x12
    li t6, 0x80010000
    ld x12, 0(t6)
    sub x12, x21, x17
    srl x11, x20, x12
    li t6, 0x80010000
    ld x16, 104(t6)
    sll x20, x23, x17
    addi x9, x9, 1504
    sll x13, x13, x11
    add x13, x11, x17
    and x20, x9, x17
    xor x10, x10, x13
    li t6, 0x80010000
    ld x13, 88(t6)
    li t6, 0x80010000
    sd x16, 48(t6)
    li t6, 0x80010000
    sd x9, 0(t6)
    and x13, x13, x23
    li t6, 0x80010000
    ld x21, 40(t6)
    or x10, x10, x19
    xor x22, x22, x20
    li t6, 0x80010000
    ld x22, 40(t6)
    or x21, x20, x18
    xor x20, x23, x13
    or x15, x21, x18
    sll x12, x12, x23
    sub x9, x9, x19
    sub x15, x13, x20
    xor x11, x11, x12
    and x11, x11, x16
    xor x13, x9, x14
    add x18, x21, x11
    xor x13, x13, x22
    sub x20, x9, x11
    sub x11, x13, x13
    and x15, x12, x16
    srl x9, x14, x12
    sub x17, x17, x21
    xor x12, x12, x10
    srl x23, x11, x15
    sll x22, x15, x21
    li t6, 0x80010000
    ld x15, 32(t6)
    sub x17, x19, x9
    xor x21, x21, x17
    or x13, x23, x23
    xor x19, x9, x22
    li t6, 0x80010000
    ld x14, 88(t6)
    li t6, 0x80010000
    ld x10, 16(t6)
    addi x18, x18, -652
    li t6, 0x80010000
    sd x15, 72(t6)
    srl x9, x15, x12
    addi x23, x14, 1960
    li t6, 0x80010000
    sd x16, 8(t6)
    sub x13, x19, x19
    li t6, 0x80010000
    ld x15, 112(t6)
    li t6, 0x80010000
    sd x15, 64(t6)
    and x23, x23, x23
    and x11, x20, x9
    sub x19, x15, x9
    or x17, x18, x20
    and x19, x19, x23
    sub x17, x10, x12
    li t6, 0x80010000
    sd x22, 56(t6)
    and x22, x9, x18
    xor x22, x22, x9
    li t6, 0x80010000
    sd x14, 80(t6)
    li t6, 0x80010000
    ld x21, 40(t6)
    and x11, x11, x20
    li t6, 0x80010000
    ld x12, 64(t6)
    li t6, 0x80010000
    sd x18, 56(t6)
    add x13, x13, x16
    li t6, 0x80010000
    ld x18, 48(t6)
    xor x15, x9, x19
    sub x23, x22, x22
    add x10, x9, x17
    sll x21, x21, x20
    or x20, x22, x21
    addi x18, x18, -616
    sub x19, x19, x12
    sll x13, x9, x20
    sll x19, x19, x22
    or x10, x23, x12
    sub x17, x17, x11
    li t6, 0x80010000
    ld x12, 112(t6)
    li t6, 0x80010000
    sd x20, 40(t6)
    xor x12, x12, x23
    add x17, x15, x18
    li t6, 0x80010000
    ld x19, 40(t6)
    and x20, x16, x22
    srl x15, x20, x19
    xor x19, x20, x15
    xor x15, x19, x13
    xor x13, x11, x10
    or x22, x22, x19
    addi x18, x11, -792
    addi x18, x19, 1644
    or x15, x10, x22
    sll x13, x11, x12
    li t6, 0x80010000
    ld x9, 104(t6)
    li t6, 0x80010000
    ld x15, 96(t6)
    sub x18, x15, x22
    li t6, 0x80010000
    ld x10, 56(t6)
    addi x11, x11, -794
    li t6, 0x80010000
    sd x16, 24(t6)
    addi x19, x19, -1666
    and x23, x18, x16
    li t6, 0x80010000
    ld x21, 64(t6)
    sub x10, x10, x18
    li t6, 0x80010000
    sd x22, 120(t6)
    li t6, 0x80010000
    sd x23, 72(t6)
    addi x15, x20, 1755
    xor x18, x11, x11
    sll x12, x15, x17
    li t6, 0x80010000
    sd x13, 112(t6)
    xor x23, x23, x14
    add x21, x9, x19
    or x23, x23, x16
    li t6, 0x80010000
    ld x17, 16(t6)
    and x19, x20, x23
    li t6, 0x80010000
    sd x16, 112(t6)
    li t6, 0x80010000
    sd x13, 0(t6)
    xor x20, x11, x23
    add x19, x18, x14
    li t6, 0x80010000
    ld x13, 112(t6)
    li t6, 0x80010000
    sd x9, 88(t6)
    sll x9, x9, x9
    li t6, 0x80010000
    ld x9, 120(t6)
    addi x18, x18, -1547
    li t6, 0x80010000
    sd x11, 96(t6)
    addi x22, x22, 1567
    sll x23, x23, x17
    add x9, x23, x11
    li t6, 0x80010000
    ld x12, 112(t6)
    and x17, x18, x12
    and x21, x14, x10
    srl x23, x23, x13
    addi x17, x17, -1635
    li t6, 0x80010000
    ld x13, 64(t6)
    sll x10, x10, x12
    li t6, 0x80010000
    sd x12, 32(t6)
    addi x23, x17, 358
    xor x21, x21, x18
    srl x16, x16, x21
    srl x14, x15, x18
    or x17, x15, x23
    li t6, 0x80010000
    ld x13, 96(t6)
    li t6, 0x80010000
    sd x9, 56(t6)
    sll x10, x10, x16
    sub x19, x20, x9
    xor x10, x10, x18
    sll x15, x15, x20
    sub x21, x23, x19
    or x19, x19, x23
    li t6, 0x80010000
    sd x19, 32(t6)
    li t6, 0x80010000
    ld x13, 80(t6)
    or x20, x20, x9
    and x17, x17, x12
    sub x14, x14, x15
    and x12, x10, x23
    sll x23, x16, x21
    sub x21, x21, x14
    addi x17, x23, 439
    and x10, x9, x18
    sub x11, x11, x17
    sub x18, x22, x17
    srl x15, x15, x23
    add x13, x13, x22
    srl x9, x18, x10
    or x12, x16, x18
    srl x21, x21, x16
    sub x19, x21, x10
    addi x18, x12, -1710
    li t6, 0x80010000
    ld x23, 48(t6)
    li t6, 0x80010000
    ld x11, 40(t6)
    li t6, 0x80010000
    sd x16, 120(t6)
    xor x13, x13, x15
    li t6, 0x80010000
    ld x11, 24(t6)
    addi x14, x20, -684
    or x12, x12, x17
    and x15, x15, x14
    or x17, x19, x18
    or x19, x15, x20
    li t6, 0x80010000
    ld x9, 120(t6)
    srl x23, x10, x22
    li t6, 0x80010000
    ld x13, 40(t6)
    sub x12, x9, x15
    addi x17, x11, -1963
    or x9, x23, x9
    add x18, x14, x22
    add x16, x18, x16
    add x19, x19, x19
    add x10, x10, x18
    addi x13, x15, -35
    sll x22, x22, x22
    addi x21, x20, -1975
    addi x9, x23, 438
    xor x9, x9, x21
    xor x13, x13, x11
    sub x12, x12, x22
    add x21, x21, x18
    li t6, 0x80010000
    sd x16, 16(t6)
    li t6, 0x80010000
    sd x10, 80(t6)
    addi x10, x14, -665
    sll x22, x22, x22
    or x16, x16, x17
    li t6, 0x80010000
    ld x16, 80(t6)
    sll x9, x9, x12
    and x21, x18, x18
    li t6, 0x80010000
    ld x20, 40(t6)
    and x21, x9, x16
    li t6, 0x80010000
    ld x14, 24(t6)
    sll x21, x10, x16
    li t6, 0x80010000
    sd x13, 8(t6)
    and x20, x20, x22
    li t6, 0x80010000
    sd x20, 48(t6)
    li t6, 0x80010000
    sd x11, 8(t6)
    li t6, 0x80010000
    sd x10, 16(t6)
    addi x11, x11, -365
    addi x15, x20, 1142
    addi x14, x14, 1166
    xor x22, x11, x14
    li t6, 0x80010000
    sd x11, 8(t6)
    sll x16, x19, x21
    li t6, 0x80010000
    sd x19, 48(t6)
    add x10, x10, x23
    sub x9, x9, x21
    li t6, 0x80010000
    ld x16, 16(t6)
    li t6, 0x80010000
    ld x21, 88(t6)
    addi x15, x17, 968
    and x14, x17, x9
    li t6, 0x80010000
    ld x21, 88(t6)
    xor x10, x18, x11
    sub x16, x18, x19
    or x17, x11, x16
    srl x11, x11, x14
    li t6, 0x80010000
    ld x10, 120(t6)
    add x10, x10, x11
    or x21, x21, x16
    addi x21, x21, -732
    add x9, x9, x22
    and x23, x23, x16
    and x17, x19, x9
    addi x10, x22, 991
    or x17, x17, x12
    li t6, 0x80010000
    sd x17, 80(t6)
    add x23, x9, x17
    sll x13, x13, x20
    li t6, 0x80010000
    sd x12, 96(t6)
    srl x17, x17, x14
    or x9, x19, x19
    and x16, x16, x21
    srl x13, x18, x16
    sub x13, x13, x23
    add x9, x21, x21
    srl x9, x9, x16
    addi x14, x14, -305
    xor x11, x11, x11
    and x13, x13, x19
    and x12, x12, x15
    addi x16, x12, -345
    sub x21, x9, x18
    addi x12, x12, 704
    or x19, x19, x18
    sll x13, x13, x10
    sll x23, x10, x19
    xor x12, x14, x22
    or x15, x22, x12
    srl x9, x20, x14
    and x14, x19, x12
    or x10, x11, x10
    xor x22, x21, x17
    srl x13, x23, x20
    li t6, 0x80010000
    sd x12, 16(t6)
    add x15, x13, x10
    or x16, x16, x21
    or x9, x9, x17
    srl x21, x21, x17
    sub x17, x17, x12
    addi x23, x23, 1497
    srl x17, x17, x22
    add x12, x12, x21
    and x19, x18, x12
    add x20, x20, x22
    srl x17, x17, x14
    li t6, 0x80010000
    sd x19, 64(t6)
    srl x20, x20, x21
    li t6, 0x80010000
    sd x22, 72(t6)
    li t6, 0x80010000
    sd x10, 104(t6)
    sub x10, x13, x17
    sub x10, x10, x23
    addi x21, x9, -1126
    addi x20, x10, 1680
    sub x16, x16, x12
    add x23, x20, x14
    add x16, x18, x13
    li t6, 0x80010000
    sd x19, 24(t6)
    sll x10, x18, x17
    xor x9, x21, x21
    li t6, 0x80010000
    sd x15, 104(t6)
    sll x16, x18, x22
    xor x14, x10, x17
    or x23, x19, x10
    sll x16, x12, x18
    sub x20, x14, x23
    sll x21, x21, x10
    li t6, 0x80010000
    ld x17, 120(t6)
    add x10, x14, x17
    sll x10, x18, x17
    addi x10, x18, 702
    li t6, 0x80010000
    sd x18, 72(t6)
    or x23, x23, x22
    addi x11, x13, 913
    addi x19, x19, 1405
    li t6, 0x80010000
    ld x13, 24(t6)
    and x11, x16, x16
    sub x20, x20, x16
    sll x16, x16, x16
    xor x14, x14, x12
    sub x15, x16, x12
    srl x12, x18, x23
    or x12, x12, x20
    add x18, x20, x16
    xor x10, x10, x18
    or x16, x19, x15
    addi x17, x17, 285
    or x10, x10, x21
    add x22, x21, x18
    xor x22, x17, x22
    li t6, 0x80010000
    sd x12, 24(t6)
    xor x20, x20, x15
    addi x12, x11, 1632
    or x22, x21, x12
    and x17, x19, x23
    srl x22, x22, x19
    sub x11, x11, x13
    sll x19, x16, x13
    xor x20, x20, x21
    or x19, x13, x18
    xor x21, x21, x12
    addi x11, x18, -290
    and x14, x12, x18
    li t6, 0x80010000
    ld x17, 112(t6)
    addi x16, x20, 346
    and x15, x15, x13
    xor x17, x9, x18
    add x21, x21, x23
    sll x19, x9, x9
    addi x13, x13, 965
    addi x18, x19, -985
    add x21, x21, x16
    addi x12, x21, -919
    srl x10, x10, x14
    and x10, x11, x11
    add x18, x18, x14
    add x19, x19, x20
    sll x15, x15, x17
    addi x15, x15, 1150
    add x11, x11, x23
    or x15, x15, x21
    srl x15, x21, x10
    sub x17, x17, x18
    add x15, x15, x11
    or x12, x21, x11
    addi x19, x19, 172
    li t6, 0x80010000
    sd x9, 64(t6)
    add x16, x16, x19
    li t6, 0x80010000
    ld x10, 56(t6)
    srl x18, x10, x18
    and x20, x20, x22
    add x12, x18, x11
    add x15, x15, x23
    add x13, x13, x22
    srl x21, x20, x10
    and x19, x18, x15
    srl x13, x14, x11
    and x17, x15, x14
    sll x13, x22, x23
    sub x16, x16, x20
    and x17, x17, x11
    xor x12, x12, x11
    sll x17, x21, x22
    and x15, x15, x21
    li t6, 0x80010000
    ld x14, 80(t6)
    xor x23, x23, x23
    xor x16, x16, x14
    add x15, x22, x22
    srl x20, x19, x9
    or x10, x21, x10
    sub x12, x12, x21
    srl x16, x10, x19
    and x9, x22, x23
    addi x19, x19, 1522
    and x11, x11, x14
    sub x14, x14, x21
    or x19, x19, x12
    addi x15, x12, -1292
    sub x11, x11, x14
    or x17, x17, x11
    li t6, 0x80010000
    sd x16, 64(t6)
    or x16, x9, x10
    srl x15, x15, x14
    li t6, 0x80010000
    sd x11, 0(t6)
    li t6, 0x80010000
    sd x22, 72(t6)
    li t6, 0x80010000
    sd x15, 96(t6)
    xor x12, x12, x17
    srl x13, x15, x12
    sll x19, x20, x12
    addi x16, x16, 326
    srl x13, x23, x18
    sll x12, x13, x18
    li t6, 0x80010000
    ld x19, 120(t6)
    or x19, x11, x12
    xor x19, x19, x9
    xor x23, x10, x15
    li t6, 0x80010000
    ld x23, 40(t6)
    xor x13, x19, x12
    or x18, x18, x21
    li t6, 0x80010000
    ld x11, 16(t6)
    sub x21, x18, x20
    or x23, x23, x17
    addi x13, x13, 116
    and x17, x17, x20
    and x16, x16, x14
    xor x11, x21, x14
    addi x17, x13, 1893
    srl x9, x15, x16
    srl x15, x13, x15
    and x22, x22, x10
    add x11, x11, x21
    and x15, x19, x12
    srl x12, x10, x21
    xor x13, x20, x13
    addi x22, x22, -967
    srl x22, x17, x23
    add x14, x22, x10
    or x14, x23, x14
    li t6, 0x80010000
    ld x20, 8(t6)
    xor x11, x18, x13
    srl x10, x10, x13
    add x15, x15, x17
    li t6, 0x80010000
    ld x22, 24(t6)
    li t6, 0x80010000
    ld x19, 0(t6)
    srl x22, x13, x18
    or x10, x21, x11
    and x18, x18, x10
    sll x13, x13, x11
    sll x13, x13, x13
    or x20, x20, x22
    sub x11, x11, x22
    addi x9, x18, -1057
    addi x22, x21, -311
    xor x22, x22, x10
    add x9, x9, x23
    sub x9, x9, x9
    li t6, 0x80010000
    ld x11, 32(t6)
    add x19, x11, x13
    xor x23, x21, x13
    sll x23, x21, x14
    or x19, x10, x17
    addi x12, x17, -127
    and x18, x18, x9
    li t6, 0x80010000
    ld x15, 80(t6)
    sub x19, x9, x12
    sub x20, x20, x21
    srl x12, x23, x13
    xor x9, x11, x20
    li t6, 0x80010000
    ld x18, 96(t6)
    or x17, x15, x18
    sll x18, x9, x9
    xor x16, x16, x23
    and x22, x11, x10
    sub x11, x16, x15
    xor x22, x22, x18
    li t6, 0x80010000
    sd x14, 32(t6)
    or x20, x20, x14
    xor x9, x22, x18
    sll x21, x9, x13
    sll x20, x20, x15
    li t6, 0x80010000
    sd x14, 120(t6)
    add x21, x22, x23
    li t6, 0x80010000
    ld x15, 104(t6)
    li t6, 0x80010000
    sd x16, 120(t6)
    li t6, 0x80010000
    sd x11, 56(t6)
    li t6, 0x80010000
    sd x21, 56(t6)
    sub x23, x23, x21
    srl x17, x17, x15
    or x11, x11, x17
    li t6, 0x80010000
    ld x19, 8(t6)
    or x11, x15, x11
    srl x9, x10, x23
    or x10, x11, x16
    xor x9, x9, x16
    or x10, x14, x21
    xor x12, x12, x23
    srl x17, x11, x18
    li t6, 0x80010000
    ld x12, 72(t6)
    li t6, 0x80010000
    ld x20, 0(t6)
    or x13, x10, x10
    sub x12, x12, x15
    sll x9, x14, x21
    xor x15, x20, x15
    addi x12, x18, -1398
    srl x22, x12, x17
    or x15, x15, x9
    add x22, x11, x15
    li t6, 0x80010000
    sd x18, 120(t6)
    li t6, 0x80010000
    ld x21, 120(t6)
    addi x9, x9, -1241
    xor x16, x16, x21
    add x15, x18, x20
    li t6, 0x80010000
    sd x20, 96(t6)
    sub x11, x18, x16
    sll x9, x9, x13
    srl x23, x23, x18
    add x15, x12, x14
    addi x16, x16, 417
    srl x23, x23, x9
    li t6, 0x80010000
    ld x18, 120(t6)
    sll x10, x23, x9
    sll x12, x14, x23
    sub x23, x23, x10
    add x13, x13, x15
    li t6, 0x80010000
    sd x12, 8(t6)
    srl x20, x23, x13
    addi x9, x14, 1928
    li t6, 0x80010000
    ld x11, 40(t6)
    li t6, 0x80010000
    sd x15, 0(t6)
    srl x12, x10, x21
    xor x13, x13, x13
    sll x11, x11, x15
    add x22, x10, x14
    li t6, 0x80010000
    ld x16, 16(t6)
    li t6, 0x80010000
    sd x10, 72(t6)
    li t6, 0x80010000
    ld x12, 64(t6)
    addi x22, x19, -1554
    add x16, x16, x22
    sll x16, x16, x13
    add x16, x13, x12
    or x16, x16, x12
    or x13, x13, x15
    addi x19, x19, -764
    addi x15, x13, 265
    sll x21, x11, x20
    li t6, 0x80010000
    ld x18, 96(t6)
    addi x20, x9, 143
    or x14, x14, x17
    sub x11, x11, x22
    xor x15, x15, x21
    srl x18, x17, x16
    and x20, x17, x19
    sll x18, x12, x22
    li t6, 0x80010000
    ld x10, 40(t6)
    li t6, 0x80010000
    sd x11, 48(t6)
    li t6, 0x80010000
    ld x15, 0(t6)
    sll x21, x21, x23
    xor x15, x15, x18
    sll x20, x11, x23
    sub x18, x18, x19
    add x12, x22, x20
    add x9, x17, x20
    sll x13, x13, x15
    and x11, x11, x22
    sll x15, x15, x16
    add x12, x15, x11
    sub x23, x23, x10
    xor x19, x19, x16
    xor x15, x15, x10
    sub x13, x10, x9
    add x14, x23, x18
    addi x20, x20, -2021
    sll x12, x12, x15
    xor x19, x14, x20
    addi x19, x18, -116
    add x21, x21, x14
    sll x12, x12, x10
    li t6, 0x80010000
    sd x13, 8(t6)
    and x13, x12, x13
    li t6, 0x80010000
    ld x13, 48(t6)
    and x13, x11, x18
    addi x21, x21, 1525
    addi x22, x22, -1503
    add x21, x10, x20
    sub x20, x20, x23
    srl x11, x17, x10
    srl x18, x18, x21
    li t6, 0x80010000
    ld x12, 104(t6)
    or x19, x18, x11
    addi x11, x11, -71
    and x21, x14, x22
    xor x18, x18, x9
    or x17, x15, x15
    li t6, 0x80010000
    sd x18, 120(t6)
    and x23, x23, x22
    addi x16, x16, -615
    li t6, 0x80010000
    ld x13, 16(t6)
    and x15, x9, x11
    sll x20, x20, x19
    sub x10, x14, x17
    sub x23, x23, x16
    add x18, x17, x13
    add x16, x21, x17
    xor x10, x10, x20
    li t6, 0x80010000
    sd x12, 64(t6)
    add x23, x23, x9
    li t6, 0x80010000
    ld x18, 120(t6)
    xor x15, x15, x9
    or x15, x15, x14
    li t6, 0x80010000
    sd x9, 56(t6)
    or x23, x18, x23
    or x13, x13, x17
    or x23, x23, x11
    and x16, x16, x21
    li t6, 0x80010000
    ld x13, 104(t6)
    or x15, x15, x14
    add x11, x11, x20
    and x15, x18, x9
    sub x9, x9, x23
    addi x19, x19, -1550
    and x22, x18, x13
    add x17, x14, x23
    srl x23, x23, x10
    sub x23, x19, x21
    sub x9, x13, x14
    li t6, 0x80010000
    sd x13, 112(t6)
    sub x13, x9, x14
    li t6, 0x80010000
    sd x11, 88(t6)
    li t6, 0x80010000
    sd x15, 24(t6)
    and x15, x15, x15
    li t6, 0x80010000
    sd x20, 88(t6)
    or x16, x14, x19
    li t6, 0x80010000
    sd x13, 64(t6)
    or x17, x12, x23
    li t6, 0x80010000
    ld x13, 0(t6)
    add x15, x14, x16
    sll x17, x17, x11
    and x14, x10, x10
    or x17, x14, x22
    srl x10, x16, x12
    and x23, x11, x18
    srl x13, x13, x20
    li t6, 0x80010000
    ld x23, 32(t6)
    or x9, x9, x16
    or x15, x15, x18
    srl x18, x9, x21
    li t6, 0x80010000
    ld x11, 32(t6)
    sub x11, x23, x22
    and x16, x16, x21
    sll x11, x11, x14
    li t6, 0x80010000
    ld x9, 48(t6)
    xor x14, x19, x18
    or x9, x13, x18
    or x20, x20, x16
    xor x17, x17, x14
    sll x13, x13, x14
    li t6, 0x80010000
    sd x17, 96(t6)
    sub x20, x20, x23
    addi x14, x22, 1412
    li t6, 0x80010000
    sd x16, 16(t6)
    srl x21, x21, x20
    sll x22, x13, x21
    li t6, 0x80010000
    ld x13, 56(t6)
    sll x13, x13, x13
    li t6, 0x80010000
    ld x13, 24(t6)
    xor x10, x22, x16
    xor x20, x15, x14
    li t6, 0x80010000
    sd x20, 8(t6)
    srl x20, x20, x12
    add x10, x22, x19
    li t6, 0x80010000
    ld x19, 0(t6)
    li t6, 0x80010000
    sd x14, 48(t6)
    and x12, x11, x13
    xor x17, x19, x22
    sll x13, x13, x10
    srl x23, x15, x13
    xor x10, x9, x11
    li t6, 0x80010000
    sd x10, 8(t6)
    and x19, x23, x19
    li t6, 0x80010000
    sd x20, 8(t6)
    li t6, 0x80010000
    sd x12, 16(t6)
    srl x15, x15, x9
    and x11, x11, x10
    addi x19, x11, 1417
    and x15, x15, x18
    and x10, x18, x14
    srl x12, x12, x23
    addi x14, x10, -12
    add x17, x17, x17
    li t6, 0x80010000
    ld x13, 88(t6)
    addi x22, x22, -180
    sub x19, x16, x17
    and x22, x9, x10
    add x18, x18, x13
    li t6, 0x80010000
    ld x14, 72(t6)
    xor x19, x14, x11
    and x20, x15, x18
    or x15, x15, x21
    li t6, 0x80010000
    ld x12, 64(t6)
    li t6, 0x80010000
    sd x13, 112(t6)
    srl x17, x17, x17
    srl x18, x12, x21
    xor x13, x13, x21
    add x11, x11, x19
    addi x22, x22, 367
    sll x19, x9, x16
    sll x15, x15, x23
    add x12, x23, x10
    srl x10, x16, x14
    li t6, 0x80010000
    ld x12, 16(t6)
    sub x14, x22, x20
    xor x9, x11, x22
    sll x16, x17, x23
    or x12, x12, x22
    li t6, 0x80010000
    sd x23, 88(t6)
    li t6, 0x80010000
    ld x15, 16(t6)
    or x23, x22, x13
    and x21, x9, x15
    sub x21, x21, x18
    li t6, 0x80010000
    sd x15, 48(t6)
    addi x15, x15, -127
    li t6, 0x80010000
    ld x10, 64(t6)
    and x13, x13, x21
    and x21, x9, x18
    li t6, 0x80010000
    sd x16, 16(t6)
    li t6, 0x80010000
    ld x19, 32(t6)
    li t6, 0x80010000
    sd x18, 32(t6)
    and x11, x13, x12
    addi x13, x13, 945
    srl x16, x18, x11
    addi x14, x14, 1643
    and x22, x13, x15
    add x16, x16, x17
    xor x20, x21, x18
    li t6, 0x80010000
    ld x12, 56(t6)
    li t6, 0x80010000
    ld x17, 0(t6)
    li t6, 0x80010000
    ld x22, 8(t6)
    add x12, x15, x19
    li t6, 0x80010000
    sd x19, 72(t6)
    xor x11, x15, x23
    li t6, 0x80010000
    sd x17, 48(t6)
    srl x21, x20, x21
    srl x10, x10, x14
    sll x18, x18, x17
    sub x15, x13, x14
    li t6, 0x80010000
    ld x11, 56(t6)
    addi x16, x19, -628
    li t6, 0x80010000
    sd x10, 56(t6)
    xor x15, x15, x16
    xor x16, x16, x22
    srl x9, x11, x23
    xor x22, x22, x9
    or x12, x12, x14
    xor x15, x13, x9
    and x9, x9, x14
    srl x17, x10, x14
    or x14, x14, x22
    or x18, x14, x17
    srl x18, x15, x19
    li t6, 0x80010000
    sd x16, 72(t6)
    addi x13, x21, -1695
    sub x13, x13, x15
    srl x12, x12, x14
    li t6, 0x80010000
    ld x21, 56(t6)
    and x9, x9, x14
    li t6, 0x80010000
    sd x10, 32(t6)
    sub x21, x21, x11
    li t6, 0x80010000
    sd x17, 8(t6)
    addi x10, x10, 931
    sll x14, x14, x20
    xor x21, x18, x15
    or x21, x22, x9
    xor x14, x14, x17
    li t6, 0x80010000
    ld x15, 0(t6)
    or x21, x21, x14
    srl x11, x11, x12
    li t6, 0x80010000
    ld x14, 32(t6)
    and x17, x23, x18
    or x21, x19, x18
    sll x19, x19, x20
    or x17, x17, x10
    srl x13, x13, x12
    li t6, 0x80010000
    ld x23, 8(t6)
    sll x21, x21, x17
    add x11, x11, x14
    sub x11, x18, x16
    xor x21, x12, x10
    li t6, 0x80010000
    ld x19, 32(t6)
    srl x18, x9, x18
    or x20, x20, x20
    sll x15, x15, x22
    li t6, 0x80010000
    ld x19, 96(t6)
    or x20, x20, x15
    xor x17, x9, x23
    or x17, x17, x19
    or x13, x15, x17
    sll x17, x20, x15
    li t6, 0x80010000
    sd x21, 112(t6)
    or x15, x10, x13
    addi x22, x22, 297
    srl x20, x20, x12
    xor x9, x9, x10
    li t6, 0x80010000
    sd x15, 40(t6)
    and x22, x22, x17
    li t6, 0x80010000
    sd x23, 8(t6)
    srl x18, x18, x22
    li t6, 0x80010000
    ld x11, 88(t6)
    sub x12, x12, x23
    xor x10, x15, x14
    and x22, x23, x22
    addi x18, x16, -1584
    srl x14, x20, x20
    addi x22, x14, 1836
    sll x17, x12, x23
    sll x12, x22, x16
    addi x9, x9, 819
    and x19, x10, x21
    sll x14, x23, x16
    sub x16, x15, x10
    or x15, x16, x10
    li t6, 0x80010000
    sd x13, 88(t6)
    and x17, x17, x9
    srl x10, x12, x9
    sll x14, x11, x18
    or x14, x14, x14
    sub x14, x18, x14
    xor x17, x17, x18
    addi x18, x20, 1043
    xor x14, x14, x15
    or x17, x12, x11
    and x22, x16, x23
    addi x12, x12, 1006
    and x10, x20, x16
    sub x22, x22, x16
    addi x18, x16, -1505
    li t6, 0x80010000
    ld x13, 80(t6)
    sll x15, x15, x22
    srl x16, x10, x9
    xor x19, x19, x20
    xor x16, x16, x14
    or x16, x16, x15
    li t6, 0x80010000
    ld x13, 104(t6)
    addi x10, x9, -1114
    and x20, x14, x14
    xor x19, x13, x17
    li t6, 0x80010000
    sd x18, 96(t6)
    add x21, x21, x22
    li t6, 0x80010000
    ld x10, 32(t6)
    addi x22, x22, -1294
    or x11, x11, x14
    li t6, 0x80010000
    ld x10, 80(t6)
    sll x17, x22, x20
    srl x14, x14, x18
    add x19, x19, x18
    srl x20, x16, x12
    sub x18, x9, x19
    sll x16, x16, x11
    or x23, x13, x10
    xor x12, x12, x16
    add x18, x18, x18
    sll x18, x19, x13
    or x16, x16, x14
    li t6, 0x80010000
    ld x12, 120(t6)
    addi x14, x19, 111
    xor x14, x14, x13
    xor x19, x19, x9
    addi x12, x12, 437
    srl x20, x23, x22
    sub x10, x20, x17
    or x19, x14, x20
    addi x19, x21, -128
    li t6, 0x80010000
    sd x10, 104(t6)
    li t6, 0x80010000
    ld x21, 16(t6)
    xor x12, x22, x21
    and x18, x18, x20
    srl x22, x22, x13
    and x11, x15, x9
    add x22, x22, x23
    li t6, 0x80010000
    sd x22, 88(t6)
    addi x19, x19, 1274
    sub x13, x14, x16
    add x18, x10, x16
    xor x23, x20, x12
    or x18, x18, x21
    addi x13, x18, -321
    addi x19, x16, 1910
    sub x17, x17, x18
    or x19, x18, x15
    addi x12, x11, -118
    sll x10, x10, x20
    or x13, x13, x10
    srl x21, x23, x23
    srl x14, x14, x17
    li t6, 0x80010000
    ld x9, 80(t6)
    li t6, 0x80010000
    ld x10, 120(t6)
    sll x19, x19, x13
    srl x9, x9, x19
    srl x10, x10, x18
    li t6, 0x80010000
    sd x23, 72(t6)
    srl x13, x11, x10
    li t6, 0x80010000
    sd x22, 72(t6)
    li t6, 0x80010000
    sd x15, 64(t6)
    li t6, 0x80010000
    ld x13, 0(t6)
    li t6, 0x80010000
    sd x22, 104(t6)
    li t6, 0x80010000
    ld x11, 104(t6)
    addi x17, x17, -1012
    xor x21, x21, x10
    li t6, 0x80010000
    ld x13, 0(t6)
    or x21, x14, x14
    addi x15, x16, -1637
    li t6, 0x80010000
    sd x9, 112(t6)
    sll x22, x9, x20
    li t0, 0x2fff37fdb0803f7b
    bne x9, t0, fail
    li t0, 0x0000016c35b3422e
    bne x10, t0, fail
    li t0, 0xafff37fdb080403a
    bne x11, t0, fail
    li t0, 0xffffffffffffff8a
    bne x12, t0, fail
    li t0, 0xfe403922e1037a88
    bne x13, t0, fail
    li t0, 0x00000000005fafff
    bne x14, t0, fail
    li t0, 0x700000000db4b179
    bne x15, t0, fail
    li t0, 0x700000000db4b7de
    bne x16, t0, fail
    li t0, 0x5dfffffff245c435
    bne x17, t0, fail
    li t0, 0xcf0000000dba37d7
    bne x18, t0, fail
    li t0, 0x00036e8df5c00000
    bne x19, t0, fail
    li t0, 0x0000000000057ff9
    bne x20, t0, fail
    li t0, 0x00000000005fafff
    bne x21, t0, fail
    li t0, 0xf600000000000000
    bne x22, t0, fail
    li t0, 0x73fffffffffa8bd4
    bne x23, t0, fail
    li t6, 0x80010000
    ld t1, 0(t6)
    li t0, 0xfe403922e1037a88
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 8(t6)
    li t0, 0x0000000000000000
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 16(t6)
    li t0, 0x8c00000000000000
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 24(t6)
    li t0, 0xb61ad9a116002159
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 32(t6)
    li t0, 0x00000000000006df
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 40(t6)
    li t0, 0xdc9f72b7bfc66ff2
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 48(t6)
    li t0, 0xfe403922e1037a88
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 56(t6)
    li t0, 0x00000000000006df
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 64(t6)
    li t0, 0x6800000000000000
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 72(t6)
    li t0, 0xafff37fdb080403a
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 80(t6)
    li t0, 0x2fff37fdb0803f7b
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 88(t6)
    li t0, 0xafff37fdb080403a
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 96(t6)
    li t0, 0x00000000000000e4
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 104(t6)
    li t0, 0xafff37fdb080403a
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 112(t6)
    li t0, 0x2fff37fdb0803f7b
    bne t1, t0, fail
    li t6, 0x80010000
    ld t1, 120(t6)
    li t0, 0xb61ad9a1174d21d9
    bne t1, t0, fail
    li a0, 0
    .word 0x0000006b
fail:
    j fail

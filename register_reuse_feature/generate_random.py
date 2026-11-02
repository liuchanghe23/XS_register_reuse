#!/usr/bin/env python3
"""Generate a deterministic integer/memory architectural-result regression."""
from pathlib import Path
import random
HERE=Path(__file__).resolve().parent
MASK=(1<<64)-1
rng=random.Random(0x5245555345)
regs=list(range(9,24))
values={r:rng.getrandbits(64) for r in regs}
lines=['.option norvc','.section .text','.global _start','_start:']
lines += [f'    li x{r}, 0x{values[r]:016x}' for r in regs]
memory={}
for i in range(4000):
    d,a,b=[rng.choice(regs) for _ in range(3)]
    if rng.random()<.45:d=a
    op=rng.choice(['add','sub','xor','or','and','sll','srl','addi','sd','ld'])
    if op=='sd':
        offset=8*rng.randrange(16)
        lines += ['    li t6, 0x80010000',f'    sd x{a}, {offset}(t6)']
        memory[offset]=values[a]
    elif op=='ld' and memory:
        offset=rng.choice(list(memory))
        lines += ['    li t6, 0x80010000',f'    ld x{d}, {offset}(t6)']
        values[d]=memory[offset]
    elif op=='addi' or op=='ld':
        imm=rng.randrange(-2048,2048)
        lines += [f'    addi x{d}, x{a}, {imm}']
        values[d]=(values[a]+imm)&MASK
    else:
        va,vb=values[a],values[b]
        if op=='add':v=va+vb
        elif op=='sub':v=va-vb
        elif op=='xor':v=va^vb
        elif op=='or':v=va|vb
        elif op=='and':v=va&vb
        elif op=='sll':v=va<<(vb&63)
        elif op=='srl':v=va>>(vb&63)
        else:raise ValueError(op)
        lines += [f'    {op} x{d}, x{a}, x{b}']
        values[d]=v&MASK
for r in regs:
    lines += [f'    li t0, 0x{values[r]:016x}',f'    bne x{r}, t0, fail']
for offset,value in sorted(memory.items()):
    lines += ['    li t6, 0x80010000',f'    ld t1, {offset}(t6)',
              f'    li t0, 0x{value:016x}','    bne t1, t0, fail']
lines += ['    li a0, 0','    .word 0x0000006b','fail:','    j fail']
(HERE/'random.S').write_text('\n'.join(lines)+'\n')

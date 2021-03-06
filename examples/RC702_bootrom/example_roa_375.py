#!/usr/bin/env python
#
# Copyright (c) 2012-2014 Poul-Henning Kamp <phk@phk.freebsd.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

'''Regnecentralen Piccolo - RC702 boot EPROM
'''

from pyreveng import mem, listing, discover, data
import pyreveng.cpu.z80 as z80

NAME = "RC702_bootrom_roa_375"

def example():
    '''A pretty vanilla example'''
    cpu = z80.z80()
    eprom = mem.Stackup(files=("EPROM_ROA_375.bin",), nextto=__file__)
    cpu.m.map(eprom, 0, 0x69)
    cpu.m.map(eprom, 0x7000, offset=0x69)

    data.Txt(cpu.m, 0x7071, 0x7071 + 0x6, label=False)
    data.Txt(cpu.m, 0x7077, 0x7077 + 0x6, label=False)
    data.Txt(cpu.m, 0x707d, 0x707d + 0x15, label=False)
    data.Txt(cpu.m, 0x7092, 0x7092 + 0x1e, label=False)
    data.Txt(cpu.m, 0x70b0, 0x70b0 + 0x10, label=False)
    data.Txt(cpu.m, 0x70c3, 0x70c3 + 0x5, label=False)
    data.Txt(cpu.m, 0x70c8, 0x70c8 + 0x5, label=False)
    data.Txt(cpu.m, 0x73f0, 0x73f0 + 0x12, label=False)

    cpu.disass(0x0000)

    # 0x70e5
    cpu.disass(0x0027)

    cpu.disass(0x0066)

    cpu.disass(0x70d0)

    cpu.disass(0x7322)
    cpu.disass(0x7615)

    # Interrupt vector table
    for a in range(16):
        cpu.codeptr(0x7300 + a * 2)

    discover.Discover(cpu)

    cpu.m.set_label(0x7068, "memcpy(BC, DE,  L)")
    return NAME, (cpu.m,)

if __name__ == '__main__':
    listing.Example(example)

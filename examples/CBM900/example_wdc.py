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

'''Commodore CBM900 - Hard Disk Controller

See also: https://datamuseum.dk/wiki/Commodore/CBM900
'''

from pyreveng import mem, data, listing
import pyreveng.cpu.mcs48 as mcs48

NAME = "CBM900_WDC"

FILENAME = "MCU_WDC_U10.bin"

def example():
    m = mem.Stackup((FILENAME,), nextto=__file__)
    cx = mcs48.mcs48()
    cx.m.map(m, 0)

    cx.vectors()

    for a in range(0x0a, 0x21):
        t = cx.m[a]
        data.Codeptr(cx.m, a, a + 1, t)
        cx.disass(t)
        cx.m.set_block_comment(t, "From PTR 0x%x" % a)


    for a in range(0x000, 0x800, 0x100):
        cx.disass(a + 0xfe)

    data.Txt(cx.m, 0x5ae, 0x5dc, label=False)
    data.Txt(cx.m, 0x5dc, 0x5f4, label=False)

    for a in (
            0x695,
            0x700,
            0x70d,
            0x720,
    ):
        cx.disass(a)
        cx.m.set_block_comment(a, "Manual")
    return NAME, (cx.m,)

if __name__ == '__main__':
    listing.Example(example)

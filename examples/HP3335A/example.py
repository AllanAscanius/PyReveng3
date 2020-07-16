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

'''HP3335 Synthesizer/Level Generator
'''

from pyreveng import mem, listing, data
from pyreveng.toolchest import seven_segment
import pyreveng.cpu.mc6800 as mc6800

NAME = "HP3335A"

FILENAMES = (
    "A13U2.bin",
    "A13U3.bin",
    "A13U4.bin",
)

SYMBOLS = {
    0x6800:        "KEY_PRESET_STORE",
    0x680f:        "KEY_PRESET_DISPLAY",
    0x6815:        "KEY_PRESET_RECALL",
    0x69ca:        "KEY_BACK_SPACE",
    0x69ea:        "KEY_PERIOD",
    0x6ab3:        "KEY_Hz_DEG",
    0x6aca:        "KEY_kHz_+dBm",
    0x6ae8:        "KEY_MHz_-dBm",
    0x6b9a:        "CMD_ILL",
    0x6cc3:        "KEY_INCR",
    0x70a0:        "KEY_MANUAL_TUNE_ON_OFF",
    0x71a0:        "FREQ_KNOB",
    0x732a:        "KEY_SWEEP_START_SINGLE_10_50",
    0x736f:        "KEY_SWEEP_MANUAL",
    0x738f:        "KEY_SWEEP_GOTO_START_FREQ",
    0x73b1:        "KEY_SWEEP_STOP",
    0x73f6:        "KEY_SWEEP_START_AUTO",
    0x748d:        "KEY_nc2 ?",
    0x760f:        "5c= 2*'.'",
    0x7617:        "5a= 2*'-'",
    0x761f:        "72= 2*'9'",
    0x7623:        "5e= 2*'?'",
    0x7627:        "digit",
    0x7966:        "KEY_nc",
    0x7cd1:        "KEY_FREQUENCY",
    0x7ce0:        "KEY_AMPLITUDE",
    0x7ce4:        "KEY_DISPLAY_LAST_ENTRY",
    0x7cf7:        "KEY_SWEEP_WIDTH",
    0x7cfe:        "KEY_PHASE_INCR",
    0x7d04:        "KEY_AMPTD_INCR",
    0x7d08:        "KEY_FREQ_INCR",
    0x7d0c:        "KEY_ENTRY_CLEAR",
    0x7d2f:        "DIGIT",
}
def example():
    m = mem.Stackup(FILENAMES, nextto=__file__, )

    cx = mc6800.mc6800()
    cx.m.map(m, 0x6800)
    nmi = m.bu16(m.hi - 4)
    print("NMI %x" % nmi)
    cx.m.map(m, 0x8000 | nmi, 0x10000, offset=nmi - 0x6800)

    for a, l in SYMBOLS.items():
        cx.m.set_label(a, l)

    def rom(lo, hi):
        cx.m.add_range(lo, hi, txt="ROM")
        s = 0
        for a in range(lo, hi):
            s += cx.m[a]
        s &= 0xff
        if s == 0:
            print("ROM %04x-%04x sum good (%02x)" % (lo, hi, s))
        else:
            print("ROM %04x-%04x sum BAD (%02x)" % (lo, hi, s))

    rom(0x6800, 0x7000)
    rom(0x7000, 0x7800)
    rom(0x7800, 0x8000)

    for i in (0x6fff, 0x77ff, 0x7ff7):
        c = data.Data(cx.m, i, i + 1, "csum")
        c.rendered = c.tag

    cx.vectors()

    def jmptbl(lo, hi, x=None):
        c = cx.m.add_range(lo, hi, txt="jmptbl (%04x-%04x)" % (lo, hi))
        # c.rendered = c.tag
        n = 0
        for a in range(lo, hi, 2):
            y = cx.codeptr(a)
            if x != None and len(x) > n:
                cx.m.set_label(y.dst, "CMD_" + x[n])
            n += 1

    jmptbl(0x7768, 0x77b6, '9876543210.-@ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    jmptbl(0x7860, 0x787c)
    jmptbl(0x78a0, 0x78bc)
    jmptbl(0x78c0, 0x78dc)

    #######################################################################

    def tblx(a):
        c = data.Data(cx.m, a, a + 16, "tblx")
        s = ""
        for i in range(10):
            v = cx.m[a + i]
            s += " %02x" % v
        s += "  "
        for i in range(10, 16):
            v = cx.m[a + i]
            s += " %02x" % v
        c.rendered = "TBLX " + s
        c.compact = True

    for a in range(0x7000, 0x70a0, 16):
        tblx(a)

    for a in range(0x7100, 0x71a0, 16):
        tblx(a)


    #######################################################################

    seven_segment.table(
        cx.m,
        0x7800,
        0x7810,
        drive=(128, 64, 32, 16, 8, 4, 2, 1, 0),
        inv=True,
        verbose=False
    )

    return NAME, (cx.m,)

if __name__ == '__main__':
    listing.Example(example)

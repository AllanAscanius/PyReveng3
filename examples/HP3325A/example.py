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

import os
from pyreveng import job, mem, listing, code
import pyreveng.cpu.hp_nanoproc as hp_nanoproc

def mem_setup():
	# Slightly confusing mapping of memory for this one.  Probably an
	# artifact of a chance from smaller to bigger ROMS along the way.
	m = mem.byte_mem(0x0000, 0x4000)
	fn = os.path.join(os.path.dirname(__file__), "A6U1.bin")
	d = bytearray(open(fn, "rb").read())
	m.load_data(0x0000, 1, d[:0x1000])
	m.load_data(0x2000, 1, d[0x1000:])
	fn = os.path.join(os.path.dirname(__file__), "A6U2.bin")
	d = bytearray(open(fn, "rb").read())
	m.load_data(0x1000, 1, d[:0x1000])
	m.load_data(0x3000, 1, d[0x1000:])
	return m

def setup():
	pj = job.Job(mem_setup(), "HP3325A")
	dx = hp_nanoproc.hp_nanoproc_pg()
	return pj, dx

def task(pj, dx):
	pj.todo(0, dx.disass)
	pj.todo(0xff, dx.disass)

	#######################################################################
	while pj.run():
		pass

	cuts = []

	#######################################################################
	if True:
		for a0 in range(4,0x20,4):
			pj.todo(a0, dx.disass)
		while pj.run():
			pass
		ix0 = pj.find(0x54)
		assert len(ix0) == 1
		ix0 = ix0[0]
		ix0.flow_out = list()
		for a0 in range(4,0x20,4):
			ix0.add_flow(pj, ">", to=a0)
			i = pj.find(a0)
			assert len(i) == 1
			i = i[0]
			assert len(i.flow_out) == 1
			dpf = i.flow_out[0].to
			cuts.append(( None, dpf))
			ix1 = pj.find(dpf + 6)
			assert len(ix1) == 1
			ix1 = ix1[0]
			ix1.flow_out = list()
			pg = dpf & ~0x7ff
			print("DISP_%d %x" % (a0 >> 2, dpf))
			pj.set_label(dpf, "DISP_%d" % (a0 >> 2))
			for a1 in range(pg, dpf, 2):
				ix1.add_flow(pj, ">", to=a1)
				pj.todo(a1, dx.disass)
				v = a0 << 3
				v |= (a1 - pg) >> 1
				pj.set_label(a1, "PTR_%02x" % v)

	#######################################################################

	while pj.run():
		pass


	#######################################################################
	def jmp_table(lo, hi, span, txt = "table", src = None):
		x = pj.add(lo, hi, "table")
		if src != None:
			ins = pj.find(src)
			print("JMPTABLE %x" % src, ins)
			if len(ins) != 1:
				ins = None
			else:
				ins = ins[0]
				assert len(ins.flow_out) == 1
				ins.flow_out = list()
		else:
			ins = None
		for a in range(lo, hi, span):
			if ins != None:
				ins.add_flow(pj, ">", to=a)
			pj.todo(a, dx.disass)
		return x

	if True:
		jmp_table(0x07d0, 0x0800, 8, "table", 0x007f)
		jmp_table(0x0f80, 0x0fa8, 4, "LED segment table", 0xd0e)
		jmp_table(0x0fa8, 0x0fc0, 2, "table", 0x0aae)
		jmp_table(0x0fc0, 0x0fe0, 4, "table", 0x0b2e)
		jmp_table(0x0fe0, 0x1000, 4, "table", 0x0b49)
		jmp_table(0x1840, 0x1870, 8, "table", 0x1b2e)
		jmp_table(0x1fd0, 0x2000, 8, "table", 0x1d01)
		jmp_table(0x2fb8, 0x3000, 8, "table", 0x2f86)
		jmp_table(0x3fd8, 0x4000, 4, "table", 0x3d17)

	#######################################################################

	while pj.run():
		pass

if __name__ == '__main__':
	pj, cx = setup()
	task(pj, cx)
	listing.Listing(pj)


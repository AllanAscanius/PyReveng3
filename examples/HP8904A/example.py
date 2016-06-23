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

from __future__ import print_function

import os
from pyreveng import job, mem, listing, data, code, assy
import pyreveng.cpu.mc6809 as mc6809

m = mem.byte_mem(0x0000, 0x10000)
m.load_binfile(0x4000, 1,
    "/critter/Doc/TestAndMeasurement/HP8904A/FW/08904-87008-pg0.bin")
m.load_binfile(0x8000, 1,
    "/critter/Doc/TestAndMeasurement/HP8904A/FW/08904-87007.bin")

pj = job.Job(m, "HP8904A")

pj.apct = "%04x"

cpu = mc6809.mc6809()

cpu.vectors(pj)

##############
# Checksums

if False:
	b = 0
	c = 0
	for x in range(0x4000,0x8000):
		b += pj.m.rd(x) + c
		c = b >> 8
		c = 1
		b &= 0xff
	print("CKSUM(0x4000-0x8000) = 0x%x" % b)

	b = 0
	c = 0
	for x in range(0x8000,0x10000):
		b += pj.m.rd(x) + c
		c = b >> 8
		c = 1
		b &= 0xff
	print("CKSUM(0x8000-0x10000) = 0x%x" % b)

	exit(0)


##############

class ptr(job.Leaf):
	def __init__(self, pj, adr):
		super(ptr, self).__init__(pj, adr, adr + 2, "ptr")
		pj.insert(self)

	def render(self, pj):
		v = pj.m.bu16(self.lo)
		l = pj.labels.get(v)
		if l == None:
			return ".PTR 0x%x" % v
		else:
			return ".PTR %s" % l

def str(lo):
	l = pj.m.rd(lo)
	y = data.Txt(pj, lo + 1, lo + l + 1, label=False)
	

def strtable(lo, hi):
	for a in range(lo, hi, 2):
		ptr(pj, a)
		v = pj.m.bu16(a)
		str(v)

for i,j in (
	(0x8f7c, 35),
	(0xea71, 40),
	(0xea99, 40),
	(0xeac1, 35),
	(0xeaf1, 40),
	(0xeb19, 40),
	(0xeb41, 40),
	(0xeb69, 40),
	(0xeb91, 40),
	(0xebb9, 21),
	(0xebce, 21),
	(0xebe3, 40),
	(0xec0b, 40),
	(0xec33, 40),
	(0xec5b, 14),
	(0xec69, 14),
	(0xec77, 14),
	(0xec85, 60),
	(0xecc1, 40),
	(0xece9, 40),
	(0xed11, 40),
	(0xed39, 40),
	(0xed61, 40),
	(0xedcf, 40),
	(0xedf7, 40),
	(0xee1f, 40),
	):
	continue
	y = data.Txt(pj, i, i + j, label=False)
	y.compact = True

strtable(0xee62, 0xee88)
strtable(0xeeee, 0xef0e)

for i in range(0xef94, 0xf014, 8):
	data.Data(pj, i, i + 8)

#############################

hpib = {
	"AHR":	"Amplitude Hop",
	"DPE":	"Digital Port",
	"FRH":	"Frequncy Hop Mode",
	"FHR":	"Frequncy Hop",
	"HRA":	"Hop Register",
	"PHH":	"Phase Hop Mode",
	"PHR":	"Phase Hop",
	"QRE":	"Query Port Status",
	"LO":	"Gaussian Filter",
	"SH":	"Sharp Filter",
	"AU":	"Auto Filter",
	"SI":	"Sine",
	"RA":	"Ramp",
	"TR":	"Triangle",
	"SQ":	"Square",
	"NS":	"Noise",
	"DC":	"DC",
	"KZ":	"kHz",
	"HZ":	"Hz",
	"DG":	"Degrees",
	"RD":	"Radians",
	"VL":	"Volts",
	"MV":	"Millivolts",
	"UV":	"Microvolts",
	"ET":	"Enter",
	"SC":	"Seconds",
	"MS":	"Milliseconds",
	"PC":	"Percent",
	"UP":	"Increment Up",
	"DN":	"Increment Down",
	"SEQE":	"Sequence end",
	"SEQP":	"Sequence index",
	"WSQ":	"Sequence string",
	"FRH":	"Tone Frequency",
	"RUNC":	"Run cont.",
	"RUNM": "Run man.",
	"RUNS":	"Run single",
	"STOP":	"Stop Run mode",
	"AM":	"AM mod.",
	"FM":	"FM mod.",
	"PM":	"PM mod.",
	"DS":	"DSB mod.",
	"PU":	"Pulse mod.",
	"APH":	"Tone/DTMF Amplitude",
	"DAPH":	"Dig.Seq. On Level",
	"DAPL":	"Dig.Seq. Off Level",
	"BSB":	"Dig.Seq. Binary Base",
	"BSO":	"Dig.Seq. Octal Base",
	"BSH":	"Dig.Seq. Hex Base",
	"STOF":	"Tone/DTMF Off time",
	"STON":	"Tone/DTMF On time",
	"SBP":	"Dig.Seq. Period",
	"HRA":	"Tone/DTMF Register Number",
	"APA":	"Amplitude A",
	"APB":	"Amplitude B",
	"APC":	"Amplitude C",
	"APD":	"Amplitude D",
	"BO":	"Backlight On",
	"BF":	"Backlight Off",
	"BP":	"Beep",
	"DEA":	"Destination",
	"DEB":	"Destination",
	"DEC":	"Destination",
	"DED":	"Destination",
	"EM":	"Exit",
	"FS":	"Filter",
	"FC":	"Float Control",
	"FRA":	"Frequency",
	"FRB":	"Frequency",
	"FRC":	"Frequency",
	"FRD":	"Frequency",
	"GM":	"Goto Mode",
	"HP":	"Help",
	"ID":	"Id",
	"IS":	"Increment Set",
	"OF":	"Off",
	"ON":	"On",
	"OO":	"Output Control",
	"PHA":	"Phase",
	"PHB":	"Phase",
	"PHC":	"Phase",
	"PHD":	"Phase",
	"PR":	"Phase Reset",
	"PS":	"Instrument Preset",
	"RC":	"Recall",
	"RP":	"Reverse Power",
	"SV":	"Save",
	"RM":	"Read Service Req Mask",
	"SM":	"Set Service Req Mask",
	"SF":	"Special Function",
	"RSF":	"Read Special Function",
	"EO":	"Read External Reference Status",
	"WFA":	"Waveform",
	"WFB":	"Waveform",
	"WFC":	"Waveform",
	"WFD":	"Waveform",
}

#############################

class lex(data.Data):
	def __init__(self, pj, lo, pfx):
		hi = lo + 4
		self.f = pj.m.rd(lo + 1)
		self.t = pj.m.bu16(lo + 2)
		self.pfx = pfx + "%c" % pj.m.rd(lo)
		if self.f > 0:
			hi += 1
		super(lex, self).__init__(pj, lo, hi, "lex")
		self.compact = True
		if self.f > 0:
			pj.set_label(self.t, self.pfx)
			cpu.disass(pj, self.t)

	def render(self, pj):
		if self.f:
			s = ".LEX\t\"%s\"\t," % self.pfx
		else:
			s = ".lex\t"
		s += "'%c', %d, 0x%04x" % (
			pj.m.rd(self.lo),
			pj.m.rd(self.lo + 1),
			pj.m.bu16(self.lo + 2))
		if self.f > 0:
			s += ",0x%02x" % pj.m.rd(self.lo + 4)
		if self.pfx in hpib:
			s += "\t# " + hpib[self.pfx]
		return s

def tx(a, pfx):
	t0 = a
	while pj.m.rd(a) != 0:
		y = lex(pj, a, pfx)
		a = y.hi
		if y.f == 0:
			b = pj.m.bu16(y.lo + 2)
			tx(b, pfx + "%c" % pj.m.rd(y.lo))

n = 65
for i in range(0x9780, 0x97b4, 2):
	ptr(pj,i)
	a = pj.m.bu16(i)
	tx(a, "%c" % n)
	n += 1

tx(0x9a22, "")

#############################

# Function pointer written into 0x2213
cpu.disass(pj, 0xc239)

# Function pointers written into 0x220d
for i in (0xa0d4, 0xa23f, 0xf1d9, 0xf3f0, 0xf9d4):
	cpu.disass(pj, i)

# Function pointers written into 0x220f
for i in (0x8c14, ):
	cpu.disass(pj, i)

# Function called through pointer
cpu.disass(pj, 0x9a40)

# Random
cpu.disass(pj, 0x975e)
cpu.disass(pj, 0x9b08)
cpu.disass(pj, 0xfe53)


while pj.run():
	pass

#############################

while pj.run():
	pass

#############################
# Switch statements

def do_switch():
	for i in pj:
		if i.tag != "mc6809":
			continue
		if pj.m.bu16(i.lo) != 0x6e9b:
			continue
		for j in pj.gaps():
			if j[0] == i.hi:
				break
		if j[0] != i.hi:
			continue
		print("SWITCH", i, "%04x-%04x" % (j[0], j[1]))
		for k in range(j[0], j[1], 2):
			# print("  %04x" % k)
			x = pj.t.find_lo(k)
			if len(x) > 0:
				break
			x = pj.m.bu16(k)
			i.add_flow(pj, ">JC", "EQ", x, i.lang)
			cpu.disass(pj, x)
			while pj.run():
				pass
		for l in range(j[0], k + 2, 2):
			cpu.codeptr(pj, l)

do_switch()

#############################

def spot():

	for lo,hi in pj.gaps():
		if lo < 0x4000:
			continue
		for i in range(lo, hi):
			if pj.m.rd(i) != 0xfc:
				continue
			if pj.m.rd(i + 3) != 0x17:
				continue
			x = pj.m.bu16(i + 4)
			if (i + x + 6) & 0xffff != 0xfd50:
				continue
			print("Spotting %04x" % i)
			cpu.disass(pj, i)
			while pj.run():
				pass
			do_switch()
			return (1)
	return (0)


#############################
# PG 0
if True:
	print("================ PG#0 ======================")
	for i,j in (
		(0x4002, 53),
		(0x4466, 6),
		):
		y = data.Txt(pj, i, i + j, label=False)
		y.compact = True
	for i in range(0x7349, 0x7445, 4):
		data.Data(pj, i, i + 4)
		x = pj.m.rd(i)
		y = pj.m.rd(i + 1)
		z = pj.m.bu16(i + 2)
		j = data.Txt(pj, z, z + y, label=False)
		j.compact = True
	cpu.disass(pj, 0x4b1e)
	cpu.disass(pj, 0x500e)
	cpu.disass(pj, 0x50ce)
	cpu.disass(pj, 0x5298)
	cpu.disass(pj, 0x5517)
	cpu.disass(pj, 0x7ac6)
	data.Txt(pj, 0x54cf)

	for i in range(16):
		a = 0x63da + 40 * i
		j = data.Txt(pj, a, a + 40, label=False)
		j.compact = True
	for i in range(0x624d,0x63a4, 8):
		j = data.Txt(pj, i, label=False)
		j.compact = True
	for i in range(0x4c64,0x4dcb, 9):
		j = data.Txt(pj, i, label=False)
		j.compact = True

	for i in range(0x4178, 0x41a0, 10):
		ptr(pj, i+0)
		cpu.codeptr(pj, i+2)
		cpu.codeptr(pj, i+4)
		cpu.codeptr(pj, i+6)
		cpu.codeptr(pj, i+8)
		u = pj.m.bu16(i)
		x = data.Txt(pj, u, u + 40, label=False)
		x.compact = True
		x = data.Txt(pj, u + 40, u + 80, label=False)
		x.compact = True

if True:
	while spot() > 0:
		continue

#############################

while pj.run():
	pass

#############################
# 0xd8a5 is display function
# 0xd8ea is display function
pj.set_label(0xd8e5, "SHOW1")
pj.set_label(0xd8ea, "SHOW2")
pj.set_label(0xc285, "SHOW3")

strmatch = [
   [ 0xc285, 6, 0x10, 2, 4, 0xc6, 5,
	"LDY-LDB-SEX-TFR-LDD-PSHS-LBSR" ],
   [ 0xd8ea, 9, 0xce, 1, 3, 0xc6, 4,
	"LDU-LDB-SEX-TFR-CLRB-SEX-TFR-LDD-PSHS-LBSR" ],
   [ 0xd8ea, 9, 0xce, 1, 3, 0xc6, 4,
	"LDU-LDB-SEX-TFR-LDB-SEX-TFR-LDD-PSHS-LBSR" ],
   [ 0xd8a5, 9, 0xce, 1, 3, 0xc6, 4,
	"LDU-LDB-SEX-TFR-LDB-SEX-TFR-LDD-PSHS-LBSR" ],
   [ 0xd8a5, 9, 0xce, 1, 3, 0xc6, 4,
	"LDU-LDB-SEX-TFR-CLRB-SEX-TFR-LDD-PSHS-LBSR" ],
]

for i in pj:
	if i.tag != "mc6809":
		continue
	for t in strmatch:
		if i.dstadr != t[0]:
			continue
		l = [i]
		s = i.mne
		for j in range(t[1]):
			x = pj.t.find_hi(l[0].lo)
			assert len(x) == 1
			l.insert(0, x[0])
			s = x[0].mne + "-" + s
		if t[7] != s:
			print("#0 %x %x" % (i.lo, i.dstadr))
			print("  ", s)
			print("  ", t)
			continue
		if pj.m.rd(l[0].lo) != t[2]:
			print("#1 %x %x" % (i.lo, i.dstadr))
			print("  ", s)
			print("  ", t)
			continue
		if pj.m.rd(l[0].lo + t[4]) != t[5]:
			print("#2 %x %x" % (i.lo, i.dstadr))
			print("  ", s)
			print("  ", t)
			continue
		x = pj.m.bu16(l[0].lo + t[3])
		if x < 0x4000:
			continue
		y = pj.m.rd(l[0].lo + t[6])
		z = data.Txt(pj, x, x + y, label=False)
		z.compact = True
		l[0].lcmt += '"' + z.txt + '"\n'
		print("S %04x %02x - %04x %04x - " % (x, y, l[0].lo, i.dstadr) + s)

for i in []:
	if i.tag != "mc6809":
		continue
	if i.dstadr != 0xd8ea and i.dstadr != 0xd8a5:
		continue
	l = [i]
	s = i.mne
	for j in range(9):
		x = pj.t.find_hi(l[0].lo)
		assert len(x) == 1
		l.insert(0, x[0])
		s = x[0].mne + "-" + s
	if pj.m.rd(l[0].lo) != 0xce:
		continue
	if pj.m.rd(l[0].lo + 3) != 0xc6:
		continue
	x = pj.m.bu16(l[0].lo + 1)
	y = pj.m.rd(l[0].lo + 4)
	if x < 0x4000:
		continue
	if i.dstadr == 0xd8ea and \
	    ( s == "LDU-LDB-SEX-TFR-CLRB-SEX-TFR-LDD-PSHS-LBSR" or \
	    s == "LDU-LDB-SEX-TFR-LDB-SEX-TFR-LDD-PSHS-LBSR" ):
		pass
	elif i.dstadr == 0xd8a5 and \
	    ( s == "LDU-LDB-SEX-TFR-LDB-SEX-TFR-LDD-PSHS-LBSR" or \
	    s == "LDU-LDB-SEX-TFR-CLRB-SEX-TFR-LDD-PSHS-LBSR" ):
		pass
	else:
		print("?? %04x" % l[0].lo, "%04x" % i.dstadr, s, l[-1].hi - l[0].lo)
		continue
	#print("S %04x %02x - %04x %04x - " % (x, y, l[0].lo, i.dstadr) + s)
	y = data.Txt(pj, x, x + y, label=False)
	y.compact = True
	l[0].lcmt += '"' + y.txt + '"\n'

#############################
# Edit LDD before PROLOGUE
for i in pj:
	if i.tag != "mc6809":
		continue
	if i.dstadr != 0xfd50:
		continue
	j = pj.t.find_hi(i.lo)
	if pj.m.rd(j[0].lo) == 0xfc:
		j[0].mne="ldd__"
		u = pj.m.bu16(j[0].lo + 1)
		v = pj.m.bu16(u)
		j[0].mne="ldd__%d" % v
		data.Data(pj, u, u + 1)
		data.Data(pj, u + 1, u + 2)


code.lcmt_flows(pj)

pj.set_label(0xfd50, "PROLOGUE")
pj.set_label(0xdc7b, "RAM_ROM_TEST")
pj.set_label(0xdc82, "RAM_TEST")
pj.set_label(0xdca9, "ROM_SUM")

listing.Listing(pj)

if False:
	import a2
	a = a2.analysis(pj)
	a.dot(pj, "/tmp/_1.dot")
	a.reduce(pj)
	a.dot(pj, "/tmp/_2.dot")


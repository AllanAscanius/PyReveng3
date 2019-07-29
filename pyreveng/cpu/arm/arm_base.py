#!/usr/bin/env python
#
# Copyright (c) 2019 Poul-Henning Kamp <phk@phk.freebsd.dk>
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
#

"""
Disassembler for ARM processors

Common/fundamental stuff
"""
from pyreveng import assy, data

OBJDUMP_COMPAT = False

if OBJDUMP_COMPAT:
	CC = [
		"eq", "ne", "cs", "cc", "mi", "pl", "vs", "vc",
		"hi", "ls", "ge", "lt", "gt", "le", "", "nv"
	]
	REG = [
		"r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7",
		"r8", "r9", "sl", "fp", "ip", "sp", "lr", "pc"
	]
else:
	CC = [
		"EQ", "NE", "CS", "CC", "MI", "PL", "VS", "VC",
		"HI", "LS", "GE", "LT", "GT", "LE", "", "NV"
	]
	REG = [
		"R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7",
		"R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"
	]

class Arm_Base_ins(assy.Instree_ins):

	def __init__(self, pj, lim, lang):
		super().__init__(pj, lim, lang)

	def assy_Rd(self, pj):
		if self['rd'] == 15:
			self.flow_R(pj)
		return REG[self['rd']]

	def assy_WRt(self, pj):
		if self['rt'] == 15:
			self.flow_J(pj)
		return REG[self['rt']]

	def assy_Rt(self, pj):
		return REG[self['rt']]

	def assy_Rt2(self, pj):
		return REG[self['rt2']]

	def assy_Rn(self, pj):
		return REG[self['rn']]

	def assy_Rdhi(self, pj):
		return REG[self['rdhi']]

	def assy_Rdlo(self, pj):
		return REG[self['rdlo']]

	def assy_Rnw(self, pj):
		if self['w']:
			return REG[self['rn']] + "!"
		return REG[self['rn']]

	def assy_Ra(self, pj):
		return REG[self['ra']]

	def assy_Rm(self, pj):
		return REG[self['rm']]

	def assy_reglist(self, pj):
		r = self['reglist']
		l = []
		i = 0
		while r:
			if r & 1:
				l.append(REG[i])
			r = r >> 1
			i += 1
		return "{" + ",".join(l) + "}"

	def assy_wreglist(self, pj):
		r = self['reglist']
		if r & 0x8000:
			self.flow_R(pj)
		return self.assy_reglist(pj)

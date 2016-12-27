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

"""
Data of various sorts
"""

from __future__ import print_function

from . import job

import struct

#######################################################################

class Data(job.Leaf):
	def __init__(self, pj, lo, hi, t="data"):
		super(Data, self).__init__(pj, lo, hi, t)
		pj.insert(self)
		self.fmt = None

	def render(self, pj):
		if self.fmt == None:
			return "<Data %x-%x %s>" % (self.lo, self.hi, self.tag)
		return self.fmt

class Const(Data):
	def __init__(self, pj, lo, hi, fmt = None, func = None, size=1):
		super(Const, self).__init__(pj, lo, hi, "const")
		if func == None:
			func = pj.m.rd
		if fmt == None:
			fmt = "0x%x"
		l = []
		for a in range(lo, hi, size):
			l.append(fmt % func(a))
		self.fmt = ",".join(l)
		self.typ = ".CONST"
		self.val = None
		self.compact = True

	def render(self, pj):
		return self.typ + "\t" + self.fmt

class Pstruct(Data):
	''' Uses python struct.* to untangle data '''
	def __init__(self, pj, lo, spec, fmt = None, typ = ".PSTRUCT"):
		hi = lo + struct.calcsize(spec)
		super(Pstruct, self).__init__(pj, lo, hi, "const")
		l = []
		for i in range(lo, hi):
			l.append(pj.m.rd(i))
		self.data = struct.unpack(spec, bytearray(l))
		self.spec = spec
		self.fmt = fmt
		self.typ = typ

	def render(self, pj):
		if self.fmt != None:
			return self.typ + "\t" + self.fmt % self.data
		return self.typ + "\t" + self.spec + " = " + str(self.data)

class Codeptr(Data):
	def __init__(self, pj, lo, hi, dst):
		super(Codeptr, self).__init__(pj, lo, hi, "codeptr")
		self.dst = dst

	def render(self, pj):
		return ".CODE\t" + pj.render_adr(self.dst)

	def arg_render(self, pj):
		return pj.render_adr(self.dst)

class Dataptr(Data):
	def __init__(self, pj, lo, hi, dst):
		super(Dataptr, self).__init__(pj, lo, hi, "dataptr")
		self.dst = dst

	def render(self, pj):
		return ".PTR\t" + pj.render_adr(self.dst)

def stringify(pj, lo, len=None, term=0):
	s = ""
	l = ""
	while True:
		x = pj.m.rd(lo)
		lo += 1
		if len == None and x == term:
			return lo,s,l
		if x > 32 and x < 127:
			s += "%c" % x
			l += "%c" % x
		elif x == 32:
			s += " "
		elif x == 10:
			s += "\\n"
			l += "NL"
		elif x == 13:
			s += "\\r"
			l += "CR"
		else:
			s += "\\x%02x" % x
			l += "%%%02x" % x
		if len != None:
			len -= 1
			if len == 0:
				return lo,s,l

class Txt(Data):
	def __init__(self, pj, lo, hi=None, label=True, term=0, pfx=None, align=2):
		self.pre = ""
		if pfx == 1:
			x = pj.m.rd(lo)
			self.pre = '%d,' % x
			hi,s,l = stringify(pj, lo + 1, len=x)
		elif hi == None:
			hi,s,l = stringify(pj, lo, term=term)
		else:
			hi,s,l = stringify(pj, lo, hi - lo, term=term)

		while hi % align:
			hi += 1
		super(Txt, self).__init__(pj, lo, hi, "txt")
		self.txt = s
		self.fmt = "'" + s + "'"
		if label:
			pj.set_label(lo, "t_" + l.strip())
		self.compact = True

	def render(self, pj):
		return ".TXT\t" + self.pre + "'" + self.txt + "'"

	def arg_render(self, pj):
		return "'" + self.txt + "'"


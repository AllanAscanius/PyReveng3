#!/usr/local/bin/python
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
#
# Data of various sorts
#

from __future__ import print_function

import pyreveng

#######################################################################

class data(pyreveng.leaf):
	def __init__(self, pj, lo, hi, t = "data"):
		super(data, self).__init__(pj, lo, hi, t)

	def render(self, pj):
		return "<Data %x-%x %s>" % (self.lo, self.hi, self.tag)

class const(data):
	def __init__(self, pj, lo, hi):
		super(const, self).__init__(pj, lo, hi, "const")
		self.typ = None
		self.val = None
		self.fmt = None
		self.compact = True

	def render(self, pj):
		return self.typ + "\t" + self.fmt

class codeptr(data):
	def __init__(self, pj, lo, hi, dst):
		super(codeptr, self).__init__(pj, lo, hi, "codeptr")
		self.dst = dst

	def render(self, pj):
		return ".CODE\t" + pj.render_adr(self.dst)

class dataptr(data):
	def __init__(self, pj, lo, hi, dst):
		super(dataptr, self).__init__(pj, lo, hi, "dataptr")
		self.dst = dst

	def render(self, pj):
		return ".PTR\t" + pj.render_adr(self.dst)

class txt(data):
	def __init__(self, pj, lo, hi = None):
		s = ""
		a = lo
		while True:
			if hi != None and a == hi:
				break
			x = pj.m.rd(a)
			a += 1
			if x >= 32 and x < 127:
				s += "%c" % x
			elif x == 10:
				s += "\\n"
			elif x == 13:
				s += "\\r"
			else:
				s += "\\x%02x" % x
			if hi == None and x == 0:
				break
		if hi == None:
			hi = a

		super(txt, self).__init__(pj, lo, hi, "txt")
		self.txt = s
		t = "t_"
		j = 0
		while j < len(s):
			i = s[j]
			if s[j:j+2] == "\\r":
				t += "CR"
				j += 1
			elif s[j:j+2] == "\\n":
				t += "NL"
				j += 1
			elif i.isalpha() or i.isdigit():
				t += i
			elif i.isspace() and (len(t) == 0 or t[-1] != "_"):
				t += "_"
			if len(t) > 8:
				break
			j += 1
		pj.set_label(lo, t)
			
	def render(self, pj):
		return ".TXT\t'" + self.txt + "'"

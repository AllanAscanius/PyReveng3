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

from . import mem, misc

class Render_mem():
	def __init__(self, pj, fmt="x", ascii=True, ncol=None):

		self.ascii = ascii

		i = "%" + fmt
		j = i % (pj.m.hi - 1)
		self.apct = "%" + "0%d" % len(j) + fmt

		j = i % (1 << pj.m.bits - 1)
		self.dpct = "%" + "0%d" % len(j) + fmt
		self.undef = "-" * len(j)
		self.space = " " * len(j)
		self.aspace = " " * (pj.m.bits//8)

		if ncol is not None:
			self.ncol = ncol
		elif pj.m.bits == 8:
			self.ncol = 4
		else:
			self.ncol = 1

	def render_word(self, pj, lo, hi):
		s = ""
		t = ""
		s += self.apct % lo + " "
		for i in range(min(self.ncol, hi - lo)):
			try:
				v = pj.m.rd(lo + i)
			except mem.MemError:
				v = None

			if v is None:
				s += " " + self.undef
			else:
				s += " " + self.dpct % v

			if self.ascii:
				b = pj.m.bits - 8
				while b >= 0:
					if v is None:
						t += " "
					else:
						x = (v >> b) & 0xff
						if x > 32 and x < 127:
							t += "%c" % x
						else:
							t += " "
					b -= 8
		while i + 1 < self.ncol:
			s += " " + self.space
			t += self.aspace
			i += 1
		if self.ascii:
			s += "  |" + t + "|"
		return s

	def render(self, pj, lo, hi, nlin):
		"""
		Render 'ncol' words per line
		"""
		l = list()
		while lo < hi and nlin >= 0:
			s = ""
			t = ""
			s += self.render_word(pj, lo, hi)
			l.append(s)
			lo += self.ncol
			nlin -= 1
		return l

class Listing():
	def __init__(self, pj, fn=None, ascii=True, pil=True, ncol=None, fmt="x"):
		self.pj = pj
		self.fmt = fmt
		self.ascii = ascii
		self.pil = pil

		self.render_mem = Render_mem(pj, fmt, ascii, ncol).render

		nxxx = 0
		cxxx = 0
		if fn is None:
			fn = "/tmp/_." + pj.name + ".txt"
		print("Listing into", fn)
		self.fo = open(fn, "w")
		misc.fill_gaps(pj)
		misc.fill_all_blanks(pj, all_vals=True, minsize=16)
		a0 = pj.m.lo
		for i in pj:
			if i.lo > a0:
				nxxx += 1
				cxxx += i.lo - a0
				self.render_chunk(a0, i.lo)
				a0 = i.lo

			rx = i.render(pj)
			if rx is None:
				alo = pj.afmt(i.lo)
				ahi = pj.afmt(i.hi)
				self.fo.write(
				    "%s-%s [%s]\n" % (alo, ahi, i.tag))
			elif i.lo < a0:
				continue
			else:
				self.render_chunk(
				    i.lo, i.hi, rx, i.lcmt, i.pil, i.compact)
				a0 = i.hi

		if a0 < pj.m.hi:
			self.render_chunk(a0, pj.m.hi)
			nxxx += 1
			cxxx += pj.m.hi - a0

		if fn is not None:
			self.fo.close()

		print("%d XXXs containing %d bytes" % (nxxx, cxxx))

	def render_chunk(self, lo, hi, rx=".XXX", lcmt="", pil=None, compact=False):
		rx = rx.strip().split("\n")
		lx = lcmt.split("\n")
		if self.pil and pil is not None:
			lx += pil.render().split("\n")
		lcmt = []
		for i in lx:
			j = i.rstrip()
			if j != "":
				lcmt.append(j)
		m = max(len(rx), len(lcmt))
		hex = self.render_mem(self.pj, lo, hi, m if compact else 9e9)
		if not compact:
			m = max(len(hex), m)

		cmt = self.pj.block_comments.get(lo)
		if cmt is not None:
			w = 72 - len(self.pj.comment_prefix)
			self.fo.write(self.pj.comment_prefix + "-" * w + "\n")
			self.fo.write(self.pj.comment_prefix)
			self.fo.write(cmt.replace("\n",
			    "\n" + self.pj.comment_prefix))
			self.fo.write("-" * w + "\n")

		lbl = self.pj.labels.get(lo)
		if lbl is None:
			lbl = "\t"
		else:
			s = set()
			for x in lbl:
				if x in s:
					continue
				s.add(x)
				self.fo.write("%s\t%s:\n" % (" " * len(hex[0]), x))
			lbl = "\t"

		for i in range(m):
			if i < len(hex):
				h = hex[i]
			else:
				h = " " * len(hex[0])
			if i < len(rx):
				r = rx[i]
			else:
				r = ""
			while len((r + "\t").expandtabs()) < 32:
				r += "\t"
			while len((r + " ").expandtabs()) < 32:
				r += " "
			if i < len(lcmt):
				l = self.pj.comment_prefix + lcmt[i]
			else:
				l = ""
			s = "%s\t%s%s%s" % (h, lbl, r, l)
			self.fo.write(s.rstrip() + "\n")
			lbl = "\t"

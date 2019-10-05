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
Misc generally usable functions which don't reallly belong anywhere else
"""

from pyreveng import mem, leaf

def fill_gaps(aspace):
	# First GAPs, where mem cannot be read

	def add_gap(aspace, lo, hi):
		print("... adding .GAP 0x%x-0x%x" % (lo, hi))
		x = leaf.Leaf(lo, hi, "gap")
		x.rendered = ".GAP\t0x%x" % (hi - lo)
		x.compact = True
		aspace.insert(x)

	gaps = 0
	ngaps = 0
	if True:
		for lo, hi in aspace.gaps():
			g0 = lo
			g1 = False
			for j in range(lo, hi):
				try:
					aspace[j]
					if g1:
						add_gap(aspace, g0, j)
						ngaps += 1
						gaps += j - g0
					g1 = False
				except mem.MemError:
					if not g1:
						g1 = True
						g0 = j
			if g1:
				add_gap(aspace, g0, hi)
				ngaps += 1
				gaps += hi - g0

	if ngaps:
		print("%d GAPs containing %d bytes" % (ngaps, gaps))

def fill_blanks(
    aspace,
    lo=None,
    hi=None,
    func=None,
    width=1,
    minsize=64,
    all_vals=False,
    vals=None,
):
	'''
		Find stretches `minsize` or more of `width` words
		of all zeros and turn them into a .BLANK.
		Instead of zeroes, matching values can be set in `vals` 
		and if `all_vals` stretches of any value will be converted.
	'''
	if lo is None:
		lo = aspace.lo
	if hi is None:
		hi = aspace.hi
	while lo & (width - 1):
		lo = lo + 1
	while hi & (width - 1):
		hi = hi - 1
	if func is None:
		func = aspace.__getitem__

	fmt = "0x%" + "0%dx" % ((width * aspace.bits + 3) // 4)

	a = lo
	b = a
	while a < hi:
		try:
			c = func(a)
		except mem.MemError:
			a += width
			continue
		if vals is not None:
			if c not in vals:
				a += width
				continue
		elif not all_vals and c:
			a += width
			continue
		b = a + width
		while b < hi:
			try:
				if func(b) == c:
					b += width
					continue
			except mem.MemError:
				pass
			break
		if b - a >= minsize:
			x = leaf.Leaf(a, b, "blank")
			x.rendered = ".BLANK\t" + fmt % c + "[0x%x]" % ((b-a) // width)
			x.compact = True
			x = aspace.insert(x)
		a = b

def fill_all_blanks(aspace, **kwargs):
	'''
		Fill in all .BLANKS
	'''
	for m, slo, shi in aspace.segments():
		for glo, ghi in aspace.gaps():
			if glo >= slo and ghi <= shi:
				fill_blanks(aspace, glo, ghi, **kwargs)

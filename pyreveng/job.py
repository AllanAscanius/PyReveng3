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
This is the core of a PyReveng job, the one class everything hangs from
and its various helpers.

The reason for not relying on global variables is that it can be very
useful to analyse multiple versions of a given image in parallel.
"""

from . import mem, code
from .exception import *
from .leaf import Leaf

class Job():
	"""
	A single analysis job

	"""
	def __init__(self, m, name="xxx"):
		self.name = name
		self.m = m
		self.apct = m.apct
		self.dolist = list()
		self.pending_flows = dict()	# flow.py
		self.labels = m.labels
		self.block_comments = m.block_comments
		self.comment_prefix = m.comment_prefix

		# Banks are valid but presently unavailable memory ranges
		# such as overlay areas in bank-switching.
		# use as:  pj.banks.append([0x1000, 0x2000])
		# This supresses WARNING about todo's into these banks
		self.banks = []

	def set_label(self, *args, **kwargs):
		self.m.set_label(*args, **kwargs)

	def set_block_comment(self, *args, **kwargs):
		self.m.set_block_comment(*args, **kwargs)

	def set_comment_prefix(self, prefix):
		self.m.comment_prefix = prefix
		self.comment_prefix = m.comment_prefix

	def afmt(self, a):
		return self.m.apct % a

	def render_adr(self, a):
		x = self.m.labels.get(a)
		if x is None:
			return self.afmt(a)
		return x[0]

	def __iter__(self):
		for i in self.m.t:
			yield i

	def find(self, adr, tag=None):
		x = self.m.t.find_lo(adr)
		if tag is None:
			return x
		for i in x:
			if i.tag == tag:
				return i
		return None

	def insert(self, leaf):
		self.m.t.insert(leaf)

	def add(self, lo, hi, tag):
		l = Leaf(self, lo, hi, tag)
		self.m.t.insert(l)
		return l

	def gaps(self):
		return self.m.gaps()

	def todo(self, adr, func):
		assert isinstance(adr, int)
		if adr >= self.m.lo and adr < self.m.hi:
			self.dolist.append((adr, func))
			return
		for lo, hi in self.banks:
			if adr >= lo and adr < hi:
				return
		print("WARNING: Ignoring todo at illegal address " +
		    self.afmt(adr), func)

	def run(self):
		rv = False
		while self.dolist:
			rv = True
			adr, func = self.dolist.pop()
			try:
				func(self, adr)
				err = None
			except code.Invalid as e:
				err = e
			except mem.MemError as e:
				err = e
			if err is None:
				continue
			print("Todo fail: " + self.name + " " + str(err) + "\n" +
			    "    adr= " + self.afmt(adr) + " func=", func)
		return rv

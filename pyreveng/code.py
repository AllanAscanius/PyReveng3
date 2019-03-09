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
Code leaf subclasses

The code object represents an amount of memory content which is executed
somehow.  Code objects tie together with "flow" objects, which tell
where execution will continue.

It is imortant to understand that 'code' is not just assembler code
but also semi-digested token-sequences in interpreted languages, for
instance the CHIP-8 'language' on RCA1802 CPUs or the RPN code of a
HP 48 Calculator.
"""

from __future__ import print_function

from . import job, pil

#######################################################################

class Flow(object):
	"""
	Flows connect code leaves together and captures where
	execution can go next and under what condition.
	"""
	def __init__(self, fm, typ, cond=True, to=None, lang=None):
		if lang is None:
			lang = fm.lang
		self.fm = fm
		self.lang = lang
		self.typ = typ
		self.cond = cond
		self.to = to
		self.dst = None

		if typ is True:
			self.to = fm.hi

	def propagate(self, pj):
		if self.fm.lo in pj.pending_flows:
			x = pj.pending_flows[self.fm.lo]
			del pj.pending_flows[self.fm.lo]
			x.propagate(pj)

		if not self.to is None:
			pj.todo(self.to, self.lang.disass)

	def __repr__(self):
		s = "<Flow @%x " % self.fm.lo + str(self.typ)
		if self.to is None:
			s += " -"
		else:
			s += " 0x%x" % self.to
		s += ">"
		return s

	def lcmt(self, leaf):
		if self.typ is True:
			return
		s = "Flow %s" % self.typ
		if self.cond is None:
			s += " cc=?"
		elif self.cond != True:
			s += " cc=%s" % self.cond
		if not self.to is None:
			s += " 0x%x" % self.to
		leaf.lcmt += s + "\n"


#######################################################################

def lcmt_flows(pj):
	"""
	Add line-comments for all flow records
	"""
	for i in pj:
		if isinstance(i, Code):
			for j in i.flow_out:
				j.lcmt(i)

#######################################################################

class Code(job.Leaf):
	"""
	A single undivisible "instruction" in some language
	"""
	def __init__(self, pj, lo, hi, lang):
		assert isinstance(lang, Decode)
		self.lang = lang
		super(Code, self).__init__(pj, lo, hi, lang.name)
		self.flow_in = []
		self.flow_out = []
		lang.init_code(pj, self)

	def render(self, pj):
		return "<Code %x-%x %s>" % (self.lo, self.hi, self.lang.name)

	def add_flow(self, pj, typ, cond=True, to=None, lang=None):
		"""
		Add a flow record
		"""
		f = Flow(self, typ, cond, to, lang)
		self.flow_out.append(f)

	def commit(self, pj):
		"""
		Follow the flow records to find more code
		"""
		for f in self.flow_out:
			f.propagate(pj)

#######################################################################

class Decode(object):
	"""
	Base class for decoding code.
	"""
	def __init__(self, name):
		assert isinstance(name, str)
		self.name = name
		self.pil = pil.PIL_State(self)

	def init_code(self, pj, x):
		"""
		A chance to add language specific members to the
		instruction before we start to flesh it out.
		"""
		return

	def decode(self, pj, adr):
		"""
		Attempt to decode at adr.

		This should return a code object or None

		The object shall not be pj.insert()'ed, since this function
		is used for speculative disassembly.

		Default always fails
		"""
		return None, "No Decoder"

	def disass(self, pj, adr):
		"""
		Decode at adr and run with it.
		Complain if it fails.
		"""
		y = pj.find(adr)
		if len(y) > 0:
			return y
		x,err = self.decode(pj, adr)
		if x is None:
			print(pj.afmt(adr) + ": disass(%s) failed" % self.name, err)
		else:
			assert isinstance(x, Code)
			self.commit(pj, x)
			x.commit(pj)
			pj.insert(x)
		return x

	def commit(self, pj, leaf):
		return

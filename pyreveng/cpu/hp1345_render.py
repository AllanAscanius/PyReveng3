#!/usr/bin/env python2
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.org> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
# ----------------------------------------------------------------------------
#
# HP1345A display emulation
#

import math

# Dump of 01347-80001 EPROM

CHARGEN_01347_80001 = [
	18,128,0,0,6,0,128,0,0,5,128,13,12,210,0,0,3,14,129,4,3,68,129,4,10,
	210,0,0,2,0,130,18,4,82,130,18,74,69,140,0,76,72,140,0,6,197,0,0,0,3,
	131,66,134,0,131,2,128,4,195,2,198,0,195,2,128,4,131,2,134,0,131,66,
	70,4,128,84,12,129,0,0,140,18,70,68,195,68,195,4,131,4,131,68,3,70,131,
	68,195,68,195,4,131,4,9,200,12,5,196,69,198,0,194,4,137,10,194,4,196,
	0,194,68,139,78,6,128,0,0,0,0,5,14,130,4,128,0,11,210,12,66,198,6,128,
	10,134,6,6,212,0,0,0,66,134,6,128,10,198,6,18,212,0,0,3,2,134,14,70,
	0,134,78,73,7,140,0,6,201,0,0,6,2,128,14,70,71,140,0,6,201,0,0,7,0,128,
	0,194,68,13,132,0,9,140,0,6,201,0,0,6,0,128,0,128,0,12,128,140,18,6,
	210,0,0,0,0,1,2,138,14,1,68,128,70,195,70,198,0,195,6,128,6,131,6,134,
	0,131,70,6,204,3,0,134,0,67,0,128,18,195,67,15,207,0,15,131,3,134,0,
	131,67,128,68,202,70,194,69,140,0,6,128,0,0,0,16,131,2,134,0,131,67,
	128,68,195,66,198,0,6,0,131,66,128,68,195,67,198,0,195,2,18,194,9,0,
	128,18,201,76,140,0,6,198,0,0,0,2,131,66,134,0,131,2,128,6,195,2,198,
	0,195,65,130,9,138,0,6,210,0,0,0,7,131,3,134,0,131,67,128,68,195,67,
	198,0,195,3,128,7,131,5,132,3,11,210,0,0,0,0,0,18,140,0,200,82,14,128,
	0,0,0,0,3,10,195,3,128,3,131,3,134,0,131,67,128,67,195,67,198,0,195,
	67,128,68,131,67,134,0,131,3,128,4,195,3,9,202,0,0,5,0,132,3,131,5,128,
	7,195,3,198,0,195,67,128,68,131,67,134,0,131,3,6,203,0,0,0,0,6,4,128,
	0,0,10,128,0,12,206,0,0,5,68,130,4,128,0,0,10,128,0,11,202,12,0,204,
	9,140,9,6,210,0,4,140,0,76,10,140,0,6,206,0,0,140,9,204,9,18,210,0,0,
	0,15,131,3,134,0,131,67,128,68,198,68,128,67,0,68,128,0,12,128,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,2,194,66,199,0,195,3,128,
	12,131,3,134,0,131,67,128,73,199,0,128,7,135,0,6,205,0,0,0,0,0,0,134,
	18,134,82,73,9,134,0,9,201,0,0,128,18,137,0,131,67,128,67,195,67,201,
	0,9,0,131,67,128,67,195,67,201,0,18,128,12,3,195,67,198,0,195,3,128,
	12,131,3,134,0,131,67,6,207,0,0,128,18,137,0,131,67,128,76,195,67,201,
	0,18,128,0,0,128,18,140,0,76,73,137,0,73,73,140,0,6,128,0,0,128,18,140,
	0,76,73,137,0,9,201,0,0,12,15,195,3,198,0,195,67,128,76,131,67,134,0,
	131,3,128,5,199,0,13,200,0,0,128,18,12,82,128,18,76,73,140,0,6,201,2,
	0,136,0,68,0,128,18,68,0,136,0,8,210,0,0,0,2,131,66,130,0,131,2,128,
	16,68,0,136,0,6,210,128,18,12,0,204,76,3,3,137,73,6,128,128,18,0,82,
	140,0,6,128,128,18,134,77,134,13,128,82,6,128,0,0,128,18,140,82,128,
	18,6,210,3,0,195,3,128,12,131,3,134,0,131,67,128,76,195,67,198,0,15,
	128,128,18,137,0,131,67,128,68,195,67,201,0,18,200,0,0,3,0,195,3,128,
	12,131,3,134,0,131,67,128,76,195,67,198,0,4,5,135,71,4,130,128,18,137,
	0,131,67,128,68,195,67,201,0,7,0,133,72,6,128,0,0,0,2,131,66,134,0,131,
	3,128,3,195,3,198,0,195,3,128,3,131,3,134,0,131,66,6,208,0,0,6,0,128,
	18,70,0,140,0,6,210,0,0,0,18,128,79,131,67,134,0,131,3,128,15,6,210,
	0,0,0,18,134,82,134,18,6,210,0,18,131,82,131,14,131,78,131,18,6,210,
	140,18,76,0,140,82,6,128,6,0,128,7,198,11,6,75,134,11,6,210,140,18,204,
	0,12,82,204,0,18,128,0,0,12,20,198,0,128,86,134,0,6,130,0,0,0,18,140,
	82,6,128,0,0,0,66,134,0,128,22,198,0,18,212,0,0,0,7,134,9,134,73,6,199,
	82,69,146,0,0,133,0,0,5,18,128,0,130,68,11,206,0,0,0,0,0,10,133,2,134,
	66,128,72,195,66,196,0,196,2,128,3,139,1,0,68,130,66,5,128,128,18,0,
	73,134,2,134,66,128,71,198,66,198,2,18,194,11,9,197,2,198,66,128,71,
	134,66,133,2,7,194,0,0,0,0,0,0,12,2,198,66,198,2,128,7,134,2,134,66,
	0,9,128,82,6,128,0,0,0,6,140,1,195,5,198,0,195,67,128,71,131,66,134,
	0,131,2,6,194,4,0,128,16,132,2,132,66,76,71,136,0,10,201,0,0,11,2,197,
	66,198,2,128,7,134,2,133,66,0,2,128,80,197,66,198,2,18,133,0,0,128,18,
	0,73,134,2,134,66,128,73,6,128,7,0,128,11,195,0,3,7,128,0,11,210,0,69,
	132,66,132,2,128,16,0,7,128,0,10,210,0,0,128,18,0,77,140,6,72,68,136,
	71,6,128,3,0,134,0,67,0,128,18,195,0,15,210,128,12,0,67,132,3,130,67,
	128,73,0,9,132,3,130,67,128,73,6,128,128,11,0,67,134,3,134,67,128,72,
	6,128,6,0,198,2,128,7,134,2,134,66,128,71,198,66,12,128,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,71,128,18,0,66,134,2,134,66,128,71,198,
	66,198,2,18,194,0,0,11,2,197,66,198,2,128,7,134,2,133,66,0,2,128,81,
	130,66,5,136,128,11,0,67,134,3,134,67,6,200,0,0,0,2,134,66,134,2,128,
	3,204,2,128,3,134,2,134,66,6,202,0,0,12,2,196,66,196,2,128,16,68,71,
	136,0,10,203,0,0,0,11,128,73,134,66,134,2,128,9,6,203,0,0,0,0,0,11,134,
	75,134,11,6,203,0,11,131,75,131,8,131,72,131,11,6,203,139,11,75,0,139,
	75,7,128,0,11,135,74,68,72,137,18,6,203,0,0,0,11,140,0,204,75,140,0,
	6,128,0,0,12,66,197,3,128,5,195,3,131,3,128,5,133,3,6,212,6,0,128,6,
	0,6,128,6,12,210,0,0,0,66,133,3,128,5,131,3,195,3,128,5,197,3,18,212,
	128,53,181,0,128,117,245,0,56,128,0,0,82,128,0,0,0,228,0,0,0,164,0,0,
	64,128,0,0,68,0,136,0,68,128,0,0,0,4,128,72,0,132,0,0,4,4,200,72,4,65,
	128,10,68,65,136,72,1,4,202,0,5,128,0,0,66,69,195,3,128,4,131,3,132,
	0,131,67,128,68,195,67,196,0,2,133,0,10,134,8,134,72,70,8,128,82,12,
	128,6,3,198,6,134,6,70,70,140,0,6,201,0,8,134,72,134,8,70,72,128,18,
	12,210,6,3,134,6,198,6,70,70,140,0,6,201,0,3,131,67,131,20,135,0,5,212,
	0,0,3,0,129,12,5,76,128,12,73,66,132,2,133,0,131,2,6,206,0,0,128,4,0,
	196,128,68,0,132,196,0,4,128,132,0,68,128,132,0,195,7,128,5,131,4,133,
	0,131,68,128,69,195,71,132,0,5,128,6,16,194,2,128,3,130,2,131,0,130,
	66,128,67,194,66,195,0,12,208,0,71,131,16,132,3,132,65,130,67,128,68,
	195,68,197,0,195,3,16,195,132,0,66,0,128,18,66,0,140,0,128,68,6,206,
	0,0,134,15,134,79,204,0,18,128,0,71,130,18,65,73,133,66,132,2,129,9,
	65,73,131,66,5,128,0,0,7,0,197,0,194,4,128,6,130,5,131,3,133,0,130,68,
	128,70,194,69,195,67,71,9,140,0,6,201,19,0,208,0,195,3,128,21,131,3,
	139,0,6,0,150,0,131,67,128,85,195,67,209,0,76,9,132,18,66,73,132,0,130,
	66,193,71,2,73,132,18,132,0,130,66,193,69,194,66,197,0,30,201,0,0,0,
	0,128,18,140,73,204,73,0,3,132,0,128,12,196,0,0,73,136,0,128,6,200,0,
	0,67,140,0,6,201,0,0,0,0,0,0,0,0,0,137,0,0,0,201,0,0,0,128,0,0,5,18,
	128,0,130,68,11,206,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,134,10,70,7,131,
	1,134,80,131,66,6,128,0,71,129,14,130,9,132,2,133,66,128,70,196,66,198,
	0,6,0,131,65,129,68,195,67,196,0,196,3,17,195,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,6,13,128,5,12,210,0,0,81,15,137,3,8,210,0,
	0,0,0,0,0,81,19,138,68,7,207,0,0,0,0,0,0,81,15,133,3,133,67,7,207,0,
	0,0,0,0,0,0,0,79,17,128,0,6,0,128,0,9,209,0,0,82,23,131,3,134,67,131,
	3,6,218,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,9,198,2,197,66,128,71,133,
	66,134,2,70,66,128,68,131,67,195,67,13,138,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,0,128,13,
	0,5,128,0,6,210,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	12,3,198,67,198,3,128,4,134,3,128,4,0,4,128,0,12,210,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,9,134,0,3,8,196,1,194,67,128,77,195,66,
	195,0,128,2,131,0,131,66,131,0,131,2,6,194,0,0,0,0,128,58,186,0,128,
	122,250,0,5,5,128,48,176,0,128,112,240,0,0,24,176,0,88,24,128,112,2,
	24,128,88,2,24,128,88,2,24,128,88,2,24,128,88,2,24,128,88,2,24,128,88,
	2,24,128,88,2,24,128,88,2,24,128,88,2,24,128,88,2,24,128,88,110,152,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,3,128,12,134,3,134,67,128,76,198,67,198,3,140,12,6,
	207,0,0,132,18,131,0,128,82,133,0,0,9,202,0,5,9,133,0,6,210,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,11,134,0,128,75,198,0,130,5,139,0,128,3,195,3,195,
	67,128,70,130,66,132,0,5,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,69,146,0,0,133,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,70,133,6,69,76,
	138,12,74,82,143,18,79,88,148,24,84,94,153,30,89,100,158,36,94,106,163,
	42,99,112,168,48,99,112,168,48,99,112,166,45,97,109,161,39,92,103,156,
	33,87,97,151,27,82,91,146,21,77,85,141,15,72,79,136,9,67,73,131,3,5,
	45,197,6,10,70,202,12,15,76,207,18,20,82,212,24,25,88,217,30,30,94,222,
	36,35,100,227,42,40,106,232,48,45,112,232,48,43,109,230,45,38,103,225,
	39,33,97,220,33,28,91,215,27,23,85,210,21,18,79,205,15,13,73,200,9,8,
	67,195,3,109,68,240,0,48,68,240,0,48,68,240,0,48,68,240,0,48,68,240,
	0,48,68,240,0,48,68,240,0,48,68,240,0,48,68,240,0,48,68,240,0,48,68,
	240,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,140,10,0,66,195,
	2,198,0,195,66,128,70,131,66,134,0,131,2,128,6,6,200,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,79,23,128,0,6,0,128,
	0,9,215,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,76,23,128,
	0,12,215,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,82,16,131,2,134,66,131,
	2,6,210,0,0,0,0,0,0,0,0,0,0,76,17,128,0,12,209,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,100,23,134,3,134,0,134,67,134,0,134,3,6,218,0,0,128,18,
	0,73,140,0,6,201,0,0,0,0,100,16,134,2,134,0,134,66,134,0,134,2,6,210,
	0,0,0,16,131,2,134,66,131,2,6,210,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,73,0,146,0,73,128,0,0,0,9,128,82,0,137,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,32,161,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,39,181,
	0,128,103,245,0,56,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,128,9,0,201,128,73,0,137,201,0,9,128,137,0,
	73,128,128,39,0,1,128,40,186,0,128,103,0,65,128,104,250,0,5,7,128,33,
	128,33,176,0,128,97,128,97,240,0,0,33,176,0,88,33,128,97,128,97,2,33,
	128,97,2,33,128,97,2,33,128,97,2,33,128,97,2,33,128,97,2,33,128,97,2,
	33,128,97,2,33,128,97,2,33,128,97,2,33,128,97,2,33,128,97,110,161,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,71,134,7,70,78,140,14,76,85,146,
	21,82,92,152,28,88,99,158,35,94,106,164,42,100,113,170,49,106,120,176,
	56,112,127,176,56,109,123,173,52,103,116,167,45,97,109,161,38,91,102,
	155,31,85,95,149,24,79,88,143,17,73,81,137,10,67,74,131,3,6,63,198,7,
	12,71,204,14,18,78,210,21,24,85,216,28,30,92,222,35,36,99,228,42,42,
	106,234,49,48,113,240,56,48,113,240,56,48,113,237,52,45,109,231,45,39,
	102,225,38,33,95,219,31,27,88,213,24,21,81,207,17,15,74,201,10,9,67,
	195,3,109,75,240,0,48,75,240,0,48,75,240,0,48,75,240,0,48,75,240,128,
	0,0,0,0,0,0,0,0,0,0,0,0,240,0,48,75,240,0,48,75,240,0,48,75,240,0,48,
	75,240,0,48,75,240,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

# Difference between 01347-80001 and 01347-80012 EPROMs
# See also: http://phk.freebsd.dk/hacks/Wargames/index.html

CHARGEN_01347_80012_delta = {
	0xbc: 0x04,
	0xbd: 0x44,
	0xbe: 0x82,
	0xbf: 0x05,
	0xc0: 0x80,
	0xc1: 0x00,
	0xc2: 0x0c,
	0xc3: 0xc1,
}

# Dump of 1816-1500 character index ROM

CHARIDX_1816_1500 = [
	222,197,232,222,160,161,162,163,122,221,123,124,220,125,126,128,130,
	135,140,143,146,149,152,155,183,185,169,164,174,179,190,229,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,0,1,4,7,12,20,26,
	32,34,37,40,44,47,49,51,53,55,61,64,69,76,79,85,92,95,104,111,114,117,
	119,122,124,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,135,143,146,152,157,161,165,168,174,177,181,185,188,190,193,195,
	200,204,210,215,222,225,229,231,234,236,239,242,245,247,250,252,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,223,1,7,11,16,
	21,26,30,36,39,42,46,49,52,57,60,69,74,79,82,87,91,95,97,100,102,105,
	108,112,115,119,211,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,197,232,222,160,161,162,163,122,221,123,124,220,125,
	126,128,130,135,140,143,146,149,152,155,183,185,169,164,174,179,190,
	229,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,0,1,
	4,7,12,20,26,32,34,37,40,44,47,49,51,53,55,61,64,69,76,79,85,92,95,104,
	111,114,117,119,122,124,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,135,143,146,152,157,161,165,168,174,177,181,185,188,
	190,193,195,200,204,210,215,222,225,229,231,234,236,239,242,245,247,
	250,252,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	223,1,7,11,16,21,26,30,36,39,42,46,49,52,57,60,69,74,79,82,87,91,95,
	97,100,102,105,108,112,115,119,211,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,222,
	222,222,222,222,222,222,
]


class font():
	def __init__(self, romfile = "01347-80012.bin"):
		self.v = [[]] * 256

		stroke = bytearray(CHARGEN_01347_80001)
		idx = bytearray(CHARIDX_1816_1500)
		used = [False] * len(stroke)

		def buildchar(ch):
			# Address permutation of index ROM
			ia = (ch & 0x1f) | ((ch & 0xe0) << 1)

			# Address permutation of stroke ROM
			sa = idx[ia] << 2
			sa |= ((1 ^ (ch >> 5) ^ (ch >> 6)) & 1) << 10
			sa |= ((ch >> 7) & 1) << 11

			if not stroke[sa] and not stroke[sa + 1]:
				return

			l = []
			while True:

				if used[sa]:
					return
				used[sa] = True

				dx = stroke[sa] & 0x3f
				if stroke[sa] & 0x40:
					dx = -dx

				dy = stroke[sa + 1] & 0x3f
				if stroke[sa + 1] & 0x40:
					dy = -dy

				if not stroke[sa] & 0x80:
					l.append([])

				if len(l) == 0:
					l.append([(0,0)])

				l[-1].append((dx, dy))

				if stroke[sa + 1] & 0x80:
					break

				sa += 2

			self.v[ch] = l

		for i in range(128):
			buildchar(i)
		for i in (0x9b, 0x9e, 0x91, 0x82):
			buildchar(i)
		for i in range(128, 256):
			buildchar(i)

	def vectors(self, ch):
		return self.v[ch]

	def bbox(self, ch, bbox = None, x = 0, y = 0):
		if bbox == None:
			bbox = [0,0,-999,-999]
		for i in self.v[ch]:
			for dx,dy in i:
				x += dx
				y += dy
				bbox[0] = int(min(bbox[0], x))
				bbox[1] = int(min(bbox[1], y))
				bbox[2] = int(max(bbox[2], x))
				bbox[3] = int(max(bbox[3], y))
		return bbox, x, y



def vectorlist(wl):
	f = font()
	last_x = 0
	x = y = 0
	dx = 1
	rot = [ 1, 0, 0, 1 ]
	siz = 1.0
	attr = (0,0,0)
	ii = 1.0
	vl = []

	def move(x,y):
		vl.append([ii, (x, y)])

	def line(x,y):
		ox,oy = vl[-1][-1]
		if attr[1] in (2,3):
			l = math.hypot(x - ox, y - oy)
			dx = (x - ox) / l
			dy = (y - oy) / l
			if attr[1] == 2:
				dl = (400. / 13.)
			else:
				dl = (400. / 31.)
			ddx = dx * dl
			ddy = dy * dl
			while l > dl:
				vl[-1].append((ox + ddx, oy + ddy))
				ox += ddx * 2
				oy += ddy * 2
				vl.append([ii, (ox, oy)])
				l -= dl * 2
			if l > 0:
				vl[-1].append((ox + l * dx, oy + l * dy))

		if attr[1] != 5:
			vl[-1].append((x, y))
		if attr[1] in (1,5):
			vl.append([2, (x, y)])
			vl.append([ii, (x, y)])

	for a in wl:
		c = a & 0x6000
		if c == 0x6000:
			# Set Condition
			attr = ((a >> 11) & 3, (a >> 7) & 7, (a >> 3) & 3)
			ii = attr[0] / 3.0 / (4.0 - attr[2])
			vl.append([ii, (x, y)])
		elif c == 0x4000:
			# Text
			if a & 0x0100:
				rot = [
					[  1,  0,  0,  1 ],
					[  0, -1,  1,  0 ],
					[ -1,  0,  0, -1 ],
					[  0,  1, -1,  0 ],
				][(a >> 9) & 3]
				siz = 1.0 + .5 * ((a >> 11) & 3)
				siz = int(siz * 2)
			tl = f.vectors(a & 0x0ff)
			for i in tl:
				l = [ii]
				for dx,dy in i:
					ddx = dx * rot[0] + dy * rot[1]
					ddy = dx * rot[2] + dy * rot[3]
					x += ddx * siz
					y += ddy * siz
					l.append((x, y))
				vl.append(l)
		elif c == 0x2000:
			# Graph
			b = a & 0x7ff
			if a & 0x1000:
				if a & 0x800:
					vl.append((ii, (last_x, y), (x, b)))
				last_x = x
				x += dx
				y = b
			else:
				dx = b

		elif c == 0x0000:
			b = a & 0x7ff
			if a & 0x1000:
				if a & 0x0800:
					line(last_x, b)
				else:
					move(last_x, b)
				x = last_x
				y = b
			else:
				last_x = b

	return vl

def svg_wl(fn, wl, scale=.25):
	fo = open(fn, "w")
	fo.write('<?xml version="1.0" standalone="no"?>\n')
	fo.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n')
	fo.write(' "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
	fo.write('<svg version="1.1"')
	wid = 2048
	asp = 0.74
	ht = wid * asp
	off = 5
	fo.write(' width="%d" height="%d"' % (
	    scale * wid + 2 * off, scale * ht + 2 * off)
	)
	fo.write(' xmlns="http://www.w3.org/2000/svg">\n')
	fo.write('<g stroke-linecap="round" fill="none" stroke="black"')
	fo.write(' stroke-width = "%.1f"' % (5.0 * scale))
	fo.write('>\n')
	for i in vectorlist(wl):
		if i[0] <= 1.0:
			c = 255 - int(255 * i[0])
			fo.write('  <polyline points="')
			for x,y in i[1:]:
				fo.write(" %.1f,%.1f" % (
				    off + scale * x,
				    scale * (ht - y * asp) + off
				))
			fo.write('" stroke="#%02x%02x%02x"' % (c,c,c))
			fo.write('/>\n')
		elif i[0] == 2.0:
			x,y = i[1]
			fo.write('  <circle cx="%d" cy="%d"' % (
			    off + scale * x,
			    scale * (ht - y * asp) + off
			))
			fo.write(' r="%.1f" fill="black" />\n' % (5 * scale))

	fo.write('</g>\n')
	fo.write('</svg>\n')

def svg(pj, lo, hi, fn=None, l=None):
	if l is None:
		l = []
		for a in range(lo, hi, 2):
			l.append(pj.m.bu16(a))
	if fn is None:
		fn = "/tmp/_.%s.%x.svg" % (pj.name, lo)
	pj.set_block_comment(lo, "HP1345A graphics Rendered to " + fn + " [0x%x-0x%x]" % (lo, hi))
	svg_wl(fn, l)
	print("HP1345A graphics %x-%x rendered to %s" % (lo, hi, fn))

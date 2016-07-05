# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

rcc5 = {}
rcc5["disjoint"] = 1 << 0
rcc5["is_included_in"] = 1 << 1
rcc5["equals"] = 1 << 2
rcc5["includes"] = 1 << 3
rcc5["overlaps"] = 1 << 4
rcc5['"!"'] = 1 << 0
rcc5['"<"'] = 1 << 1
rcc5['"="'] = 1 << 2
rcc5['">"'] = 1 << 3
rcc5['"><"'] = 1 << 4

logmap = {}
logmap[1<<0] = 0
logmap[1<<1] = 1
logmap[1<<2] = 2
logmap[1<<3] = 3
logmap[1<<4] = 4

relation = {}
relation["no"] = 0
relation["!"] = 1 << 0
relation["<"] = 1 << 1
relation["="] = 1 << 2
relation[">"] = 1 << 3
#relation["<>"] = 1 << 3
relation["><"] = 1 << 4
relation["o"] = 1 << 4
# Imfer bit
relation["input"] = 1 << 5
relation["infer"] = 1 << 6
relation["{=, >}"] = 1 << 2 | 1 << 3
relation["{=, <}"] = 1 << 2 | 1 << 1
relation["{=, !}"] = 1 << 2 | 1 << 0
relation["{=, ><}"] = 1 << 2 | 1 << 4
relation["{>, <}"] = 1 << 3 | 1 << 1
relation["{>, !}"] = 1 << 3 | 1 << 0
relation["{>, ><}"] = 1 << 3 | 1 << 4
relation["{<, !}"] = 1 << 1 | 1 << 0
relation["{<, ><}"] = 1 << 1 | 1 << 4
relation["{!, ><}"] = 1 << 0 | 1 << 4
relation["{=, >, <}"] = 1 << 2 | 1 << 3 | 1 << 1
relation["{=, >, !}"] = 1 << 2 | 1 << 3 | 1 << 0
relation["{=, >, ><}"] = 1 << 2 | 1 << 3 | 1 << 4
relation["{=, <, !}"] = 1 << 2 | 1 << 1 | 1 << 0
relation["{=, <, ><}"] = 1 << 2 | 1 << 1 | 1 << 4
relation["{=, !, ><}"] = 1 << 2 | 1 << 0 | 1 << 4
relation["{>, <, !}"] = 1 << 3 | 1 << 1 | 1 << 0
relation["{>, <, ><}"] = 1 << 3 | 1 << 1 | 1 << 4
relation["{>, !, ><}"] = 1 << 3 | 1 << 0 | 1 << 4
relation["{<, !, ><}"] = 1 << 1 | 1 << 0 | 1 << 4
relation["{=, >, <, !}"] = 1 << 2 | 1 << 3 | 1 << 1 | 1 << 0
relation["{=, >, <, ><}"] = 1 << 2 | 1 << 3 | 1 << 1 | 1 << 4
relation["{=, >, !, ><}"] = 1 << 2 | 1 << 3 | 1 << 0 | 1 << 4
relation["{=, <, !, ><}"] = 1 << 2 | 1 << 1 | 1 << 0 | 1 << 4
relation["{>, <, !, ><}"] = 1 << 3 | 1 << 1 | 1 << 0 | 1 << 4
relation["{=, >, <, !, ><}"] = 1 << 2 | 1 << 3 | 1 << 1 | 1 << 0 | 1 << 4
relation["+="] = 1 << 7 #lsum
relation["=+"] = (1 << 7) + 1 #rsum
relation["+3="] = 1 << 8 #l3sum
relation["=3+"] = (1 << 8) + 1 #r3sum
relation["+4="] = 1 << 9 #l4sum
relation["-="] = 1 << 10 #ldiff
relation["=-"] = (1 << 10) + 1 #rdiff

relstr={}
relstr[0] = "disjoint"
relstr[1] = "is_included_in"
relstr[2] = "equals"
relstr[3] = "includes"
relstr[4] = "overlaps"

relss={}
relss[1 << 0] = "disjoint"
relss[1 << 1] = "is_included_in"
relss[1 << 2] = "equals"
relss[1 << 3] = "includes"
relss[1 << 4] = "overlaps"

reasoner={}
reasoner["dlv"] = 1 << 0
reasoner["gringo"] = 1 << 1
reasoner["rcc2"] = 1 << 2
reasoner["rcc2eq"] = 1 << 3
reasoner["rcc2pw"] = 1 << 4
reasoner["rcc1"] = 1 << 5

encode = {}
encode[0] = 0                                  # null encoding
encode["dr"] = 1                               # direct encoding
encode["direct"] = encode["dr"]                # direct encoding
encode["vr"] = 1 << 1                          # binary encoding
encode["dl"] = 1 << 2                          # probability encoding
encode["pl"] = 1 << 3                          #
encode["mn"] = 1 << 4                          # polynomial encoding
encode["pw"] = 1 << 5                          # possible world generation
encode["ve"] = 1 << 6                          # valid euler region generation
encode["cb"] = 1 << 7                          # combined concept generation
encode["ob"] = 1 << 8                          # observation dataset generation
encode["ct"] = 1 << 9
encode["drpw"] = encode["dr"] | encode["pw"]
encode["vrpw"] = encode["vr"] | encode["pw"]
encode["dlpw"] = encode["dl"] | encode["pw"]
encode["plpw"] = encode["pl"] | encode["pw"]
encode["mnpw"] = encode["mn"] | encode["pw"]
encode["vrve"] = encode["vr"] | encode["ve"]
encode["dlve"] = encode["dl"] | encode["ve"]
encode["plve"] = encode["pl"] | encode["ve"]
encode["mnve"] = encode["mn"] | encode["ve"]
encode["mncb"] = encode["mn"] | encode["cb"]
encode["mnvr"] = encode["mn"] | encode["vr"]
encode["mnob"] = encode["mn"] | encode["ob"]
encode["mnct"] = encode["mn"] | encode["ct"]

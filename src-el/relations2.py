rcc5 = {}
rcc5["equals"] = 1 << 0
rcc5["includes"] = 1 << 1
rcc5["is_included_in"] = 1 << 2
rcc5["disjoint"] = 1 << 3
rcc5["overlaps"] = 1 << 4
rcc5['"="'] = 1 << 0
rcc5['">"'] = 1 << 1
rcc5['"<"'] = 1 << 2
rcc5['"!"'] = 1 << 3
rcc5['"><"'] = 1 << 4

logmap = {}
logmap[1<<0] = 0
logmap[1<<1] = 1
logmap[1<<2] = 2
logmap[1<<3] = 3
logmap[1<<4] = 4

relation = {}
relation["no"] = 0
relation["="] = 1 << 0
relation[">"] = 1 << 1
relation["<"] = 1 << 2
relation["!"] = 1 << 3
#relation["<>"] = 1 << 3
relation["><"] = 1 << 4
# Imfer bit
relation["infer"] = 1 << 5
relation["{=, >}"] = 1 << 0 | 1 << 1
relation["{=, <}"] = 1 << 0 | 1 << 2
relation["{=, !}"] = 1 << 0 | 1 << 3
relation["{=, ><}"] = 1 << 0 | 1 << 4
relation["{>, <}"] = 1 << 1 | 1 << 2
relation["{>, !}"] = 1 << 1 | 1 << 3
relation["{>, ><}"] = 1 << 1 | 1 << 4
relation["{<, !}"] = 1 << 2 | 1 << 3
relation["{<, ><}"] = 1 << 2 | 1 << 4
relation["{!, ><}"] = 1 << 3 | 1 << 4
relation["{=, >, <}"] = 1 << 0 | 1 << 1 | 1 << 2
relation["{=, >, !}"] = 1 << 0 | 1 << 1 | 1 << 3
relation["{=, >, ><}"] = 1 << 0 | 1 << 1 | 1 << 4
relation["{=, <, !}"] = 1 << 0 | 1 << 2 | 1 << 3
relation["{=, <, ><}"] = 1 << 0 | 1 << 2 | 1 << 4
relation["{=, !, ><}"] = 1 << 0 | 1 << 3 | 1 << 4
relation["{>, <, !}"] = 1 << 1 | 1 << 2 | 1 << 3
relation["{>, <, ><}"] = 1 << 1 | 1 << 2 | 1 << 4
relation["{>, !, ><}"] = 1 << 1 | 1 << 3 | 1 << 4
relation["{<, !, ><}"] = 1 << 2 | 1 << 3 | 1 << 4
relation["{=, >, <, !}"] = 1 << 0 | 1 << 1 | 1 << 2 | 1 << 3
relation["{=, >, <, ><}"] = 1 << 0 | 1 << 1 | 1 << 2 | 1 << 4
relation["{=, >, !, ><}"] = 1 << 0 | 1 << 1 | 1 << 3 | 1 << 4
relation["{=, <, !, ><}"] = 1 << 0 | 1 << 2 | 1 << 3 | 1 << 4
relation["{>, <, !, ><}"] = 1 << 1 | 1 << 2 | 1 << 3 | 1 << 4
relation["{=, >, <, !, ><}"] = 1 << 0 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 4
relation["+="] = 1 << 5 #lsum
relation["=+"] = (1 << 5) + 1 #rsum
relation["+3="] = 1 << 6 #l3sum
relation["=3+"] = (1 << 6) + 1 #r3sum
relation["+4="] = 1 << 7 #l4sum
relation["-="] = 1 << 8 #ldiff
relation["=-"] = (1 << 8) + 1 #rdiff

relstr={}
relstr[0] = "equals"
relstr[1] = "includes"
relstr[2] = "is_included_in"
relstr[3] = "disjoint"
relstr[4] = "overlaps"

reasoner={}
reasoner["dlv"] = 1 << 0
reasoner["gringo"] = 1 << 1

encode = {}
encode[0] = 0                                  # null encoding
encode["dr"] = 1                               # direct encoding
encode["direct"] = encode["dr"]                # direct encoding
encode["vr"] = 2                               # binary encoding
encode["binary"] = encode["vr"]                # binary encoding
encode["mn"] = 3                               # polynomial encoding
encode["poly"] = encode["mn"]                  # polynomial encoding

query = {}
query[0] = 0
query["pw"] = 1
query["AllPWs"] = query["pw"]

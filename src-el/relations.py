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

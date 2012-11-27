rcc5 = {}
rcc5["equals"] = 1 << 0
rcc5["includes"] = 1 << 1
rcc5["is_included_in"] = 1 << 2
rcc5["disjoint"] = 1 << 3
rcc5["overlaps"] = 1 << 4

relation = {}
relation["no"] = 0
relation["="] = 1 << 0
relation[">"] = 1 << 1
relation["<"] = 1 << 2
relation["!"] = 1 << 3
relation["><"] = 1 << 4
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
relation["+="] = 1 << 5
relation["=+"] = (1 << 5) + 1

encode = {}
encode["dr"] = 1
encode["direct"] = encode["dr"]
encode["vr"] = 1 << 1
encode["dl"] = 1 << 2
encode["pw"] = 1 << 4
encode["drpw"] = encode["dr"] | encode["pw"]
encode["vrpw"] = encode["vr"] | encode["pw"]
encode["dlpw"] = encode["dl"] | encode["pw"]

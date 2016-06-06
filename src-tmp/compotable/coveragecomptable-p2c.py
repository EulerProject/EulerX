from relations import srel

def findkey(mapp, value):
    return mapp.keys()[mapp.values().index(value)]

# R32 composition table
#"inconsistent" = 0
#"!" = 1 << 0 = 1
#"<" = 1 << 1 = 2
#"=" = 1 << 2 = 4
#">" = 1 << 3 = 8
#"o" = 1 << 4 = 16

l = []
l.append(["<<", ""])   # (<,<) ->  inconsistent
l.append(["<>", ""])   # (<,>) ->  inconsistent
l.append(["<=", ""])   # (<,=) ->  inconsistent
l.append(["<!", "<"])  # (<,!) ->  <
l.append(["<o", ""])   # (<,o) ->  inconsistent
l.append(["><", ""])   # (>,<) ->  inconsistent
l.append([">>", ">="]) # (>,>) ->  >=
l.append([">=", ""])   # (>,=) ->  inconsistent
l.append([">!", "o"])  # (>,!) ->  o
l.append([">o", "<o"]) # (>,o) ->  <o
l.append(["=<", ""])   # (=,<) ->  inconsistent
l.append(["=>", ""])   # (=,>) ->  inconsistent
l.append(["==", ""])   # (=,=) ->  inconsistent
l.append(["=!", "<"])  # (=,!) ->  <
l.append(["=o", ""])   # (=,o) ->  inconsistent
l.append(["!<", "<"])  # (!,<) ->  <
l.append(["!>", "o"])  # (!,>) ->  o
l.append(["!=", "<"])  # (!,=) ->  <
l.append(["!!", "!"])  # (!,!) ->  !
l.append(["!o", "o"])  # (!,o) ->  o
l.append(["o<", ""])   # (o,<) ->  inconsistent
l.append(["o>", "<o"]) # (o,>) ->  <o
l.append(["o=", ""])   # (o,=) ->  inconsistent
l.append(["o!", "o"])  # (o,!) ->  o
l.append(["oo", "<o"]) # (o,o) ->  <o


# create B5 table
base = [[None for i in range(32)] for j in range(32)]
for pair in l:
    rel1 = srel[pair[0][0]]
    rel2 = srel[pair[0][1]]
    resultStr = pair[1]
    
    num = 0
    if resultStr != "":
        for ch in resultStr:
            num = num | srel[ch]
    
    base[rel1][rel2] = num

# create R32 table
covtab = [[None for i in range(32)] for j in range(32)]
for i in range(32):
    for j in range(32):
        if base[i][j]:
            covtab[i][j] = base[i][j]
        else:
            rel1s = findkey(srel, i).replace("{","").replace("}","").split(", ")
            rel2s = findkey(srel, j).replace("{","").replace("}","").split(", ")
            R = 0
            for rel1 in rel1s:
                for rel2 in rel2s:
                    tmpR = base[srel[rel1]][srel[rel2]]
                    if tmpR:
                        R = R | tmpR
                    else:
                        R = R | 0
            if R == 0:
                covtab[i][j] = None
            else:
                covtab[i][j] = R


for i in range(32):
    for j in range(32):
        print "i=",i, "j=",j, "covtab=",covtab[i][j] 



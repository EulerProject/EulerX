#!/usr/bin/env python
import re
import sys
from operator import itemgetter

file1 = sys.argv[1] # from Shawn's reasoner
#file2 = sys.argv[2] # 

# sort mir of file1
l = []
fIn = open(file1, "r")
lines = fIn.readlines()
for line in lines:
    if (re.match("\[.*?\]", line)):
        inside = re.match("\[(.*)\]", line).group(1)
        inside = inside.replace("{","").replace("}","")
        items = inside.split(" ")
        e1 = items[0].split(".")
        e3 = items[-1].split(".")
        e2 = items[1:-1]
        
        tmp = '{'
        if "equals" in e2:
            tmp = tmp + "=, "
        if "includes" in e2:
            tmp = tmp + ">, "
        if "is_included_in" in e2:
            tmp = tmp + "<, "
        if "disjoint" in e2:
            tmp = tmp + "!, "
        if "overlaps" in e2:
            tmp = tmp + "><, "
        tmp = tmp[:-2] + "}"
        
        if "," not in tmp:
            tmp = tmp.replace("{", "").replace("}","")
        
        element = [e1[0], e1[1], tmp, e3[0], e3[1]]
        l.append(element)

l = sorted(l, key=itemgetter(1,4))
fIn.close()

fOut = open("outmir.txt", "w")
for e in l:
    fOut.write(e[0] + "." + e[1] + "," + e[2] + "," + e[3] + "." + e[4] + "\n")
    
fOut.close()

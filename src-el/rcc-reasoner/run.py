#!/usr/bin/env python
import sys
import re
from itertools import permutations
from reasoner import *

def readFile(file):
    d = {}
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        if not " " in line and len(line) != 1:
            totalConceptsCount = re.match("(\d+)\n", line).group(1)
        elif len(line) != 1:
            items = re.match("(\d+)\s+(\d+)\s+\[(.*)\]", line)
            rel = "".join(sorted(items.group(3).replace(",","").replace(" ","")))
            d[(int(items.group(1)), int(items.group(2)))] = rel
    f.close()
    completeDict(d, totalConceptsCount)
    return d

def completeDict(d, totalConceptsCount):
    indexList = []
    pairs = []
    for i in range(int(totalConceptsCount)):
        indexList.append(i)
    pairs = list(permutations(indexList,2))
    
    for pair in pairs:
        reversePair = (pair[1], pair[0])
        if pair in d:
            pass
        elif pair not in d and reversePair not in d:
            d[pair] = "!<=>o"
        elif pair not in d and reversePair in d:
            symbol = d[reversePair]
            if "<" in symbol and ">" not in symbol:
                symbol = symbol.replace("<", ">")
            elif ">" in symbol and "<" not in symbol:
                symbol = symbol.replace(">", "<")
            d[pair] = "".join(sorted(symbol))
#    for k,v in d.iteritems():
        
        
    
    return

    


def main(d):
    
    # test input 
#    d2 = {
#         (0,1) : ">",       (1,0) : "<",
#         (0,2) : ">",       (2,0) : "<",  
#         (0,3) : "=",       (3,0) : "=", 
#         (0,4) : "!<=>o",   (4,0) : "!<=>o", 
#         (0,5) : "!<=>o",   (5,0) : "!<=>o",  
#         (1,2) : "!",       (2,1) : "!", 
#         (1,3) : "!<=>o",   (3,1) : "!<=>o", 
#         (1,4) : "<=",      (4,1) : "=>", 
#         (1,5) : "!<=>o",   (5,1) : "!<=>o",
#         (2,3) : "!<=>o",   (3,2) : "!<=>o",
#         (2,4) : "!<=>o",   (4,2) : "!<=>o",
#         (2,5) : "=>",      (5,2) : "<=", 
#         (3,4) : ">",       (4,3) : "<",
#         (3,5) : ">",       (5,3) : "<",
#         (4,5) : "!",       (5,4) : "!",
#         }

    
    toDo = []
    for k,v in d.iteritems():
        if len(v) != 5:
            toDo.append(k)
    
    relativeOfPair = {}
    
    while len(toDo) > 0:
        pair = toDo[0]
        del toDo[0]    
        relativeOfPair = reasonOver(pair, d, toDo)
        d.update(relativeOfPair)
        
    print "********"
    for k,v in d.iteritems():
        if k[0] < k[1]:
            print k, v
    
    return


if __name__ == "__main__":
    d = readFile(sys.argv[1])
    main(d)

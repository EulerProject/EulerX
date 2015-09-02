#!/usr/bin/env python
import sys
import re
from itertools import permutations
from reasoner import *

def readFile(file):
    d = {}
    f = open(file, "r")
    lines = f.readlines()
    if sys.argv[2] in ['True', 'true', '1']:
        return eliminateEquals(lines, d)
    else:
        return nonEliminateEquals(lines, d) 

def completeDict(newAllConcepts, d):
    indexList = []
    pairs = []

    pairs = list(permutations(newAllConcepts,2))
    
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
    
    diagnalConcepts = []
    for k,v in d.iteritems():
        if k[0] == k[1]:
            diagnalConcepts.append(k)
    
    for diagnalConcept in diagnalConcepts:
        if diagnalConcept in d:
            del d[diagnalConcept]
    
    return d

def eliminateEquals(lines, d):
    allConcepts = []
    newAllConcepts = []
    allRels = []
    equalsPair = {}
    for line in lines:
        items = re.match("(\d+)\s+(\d+)\s+\[(.*)\]", line)
        allConcepts.append(int(items.group(1)))
        allConcepts.append(int(items.group(2)))
        rel = "".join(sorted(items.group(3).replace(",","").replace(" ","")))
        allRels.append([int(items.group(1)), int(items.group(2)), rel])
        
        if rel == "=":
            equalsPair[int(items.group(2))] = int(items.group(1))
    
    for allRel in allRels:
        for c1,c2 in equalsPair.iteritems():
            if allRel[0] == c1:
                allRel[0] = c2
            if allRel[1] == c1:
                allRel[1] = c2
        
    allRels_set = set(map(tuple,allRels))
    allRels = map(list,allRels_set)
    allConcepts = list(set(allConcepts))

    for allRel in allRels:
        d[(allRel[0], allRel[1])] = allRel[2]
        newAllConcepts.append(allRel[0])
        newAllConcepts.append(allRel[1])
    
    newAllConcepts = list(set(newAllConcepts))
    
    d = completeDict(newAllConcepts, d)
    
    return d

def nonEliminateEquals(lines, d):
    allConcepts = []
    allRels = []
    for line in lines:
        items = re.match("(\d+)\s+(\d+)\s+\[(.*)\]", line)
        allConcepts.append(int(items.group(1)))
        allConcepts.append(int(items.group(2)))
        rel = "".join(sorted(items.group(3).replace(",","").replace(" ","")))
        allRels.append([int(items.group(1)), int(items.group(2)), rel])
        
    allRels_set = set(map(tuple,allRels))
    allRels = map(list,allRels_set)
    allConcepts = list(set(allConcepts))

    for allRel in allRels:
        d[(allRel[0], allRel[1])] = allRel[2]
    
    d = completeDict(allConcepts, d)
    
    return d



def main(d):
    
    # test input 
#    d = {
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
    counter = {}
    for k,v in d.iteritems():
        if v != "!<=>o":
            toDo.append(k)
        d[k] = rcc[v]
    
    relativeOfPair = {}
    
    while len(toDo) > 0:
        pair = toDo[0]
        del toDo[0]    
        relativeOfPair = reasonOver(pair, d, toDo, counter)
        d.update(relativeOfPair)
        
    print "********"
    for k,v in d.iteritems():
        if k[0] < k[1]:
            print k, findKey(rcc, v)
    
    return


if __name__ == "__main__":
    d = readFile(sys.argv[1])
#    for k,v in d.iteritems():
#        if k[0] < k[1]:
#            print k, v
#    print "len(d)", len(d)
    main(d)

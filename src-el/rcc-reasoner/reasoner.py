import sys
import copy
from comptables import *

def findKey(d, value):
    for k,v in d.iteritems():
        if v == value:
            return k

def reasonOver(pair, d, toDo):
    relativeOfPair = {}
    for k, v in d.iteritems():
        if k[0] == pair[1]:
            newRelPost = r32compTab(rcc[d[pair]], rcc[d[k]])
            deducedPair = (pair[0], k[1])
            if deducedPair in d:
                deducedRel = rcc[d[deducedPair]] & newRelPost
                assertNew(d, rcc[d[deducedPair]], deducedPair, deducedRel, relativeOfPair, toDo)
                    
            
        if k[1] == pair[0]:
            newRelPre = r32compTab(rcc[d[k]], rcc[d[pair]])
            deducedPair = (k[0], pair[1])
            if deducedPair in d:
                deducedRel = rcc[d[deducedPair]] & newRelPre
                assertNew(d, rcc[d[deducedPair]], deducedPair, deducedRel, relativeOfPair, toDo)

    return relativeOfPair


def assertNew(d, originRel, deducedPair, deducedRel, relativeOfPair, toDo):
    if not deducedRel:
        print "inconsistent pair", deducedPair
        exit(0)
    if deducedRel == rcc["=><!o"] or originRel == deducedRel:
        return
    relativeOfPair[deducedPair] = findKey(rcc, deducedRel)
    toDo.append(deducedPair)
        
    

def areSameDict(d1,d2):
    keys = []
    for k,v in d1.iteritems():
        keys.append(k)
    for key in keys:
        if d1[key] != d2[key]:
            return False
    return True
 
# read file
#inputFile = sys.argv[1]
#f = open(inputFile, "r")
#lines = f.readlines()
#
#print lines

# test input 
d = {
     (0,1) : ">",       (1,0) : "<",
     (0,2) : ">",       (2,0) : "<",  
     (0,3) : "=",       (3,0) : "=", 
     (0,4) : "=><!o",   (4,0) : "=><!o", 
     (0,5) : "=><!o",   (5,0) : "=><!o",  
     (1,2) : "!",       (2,1) : "!", 
     (1,3) : "=><!o",   (3,1) : "=><!o", 
     (1,4) : "=<",      (4,1) : "=>", 
     (1,5) : "=><!o",   (5,1) : "=><!o",
     (2,3) : "=><!o",   (3,2) : "=><!o",
     (2,4) : "=><!o",   (4,2) : "=><!o",
     (2,5) : "=>",      (5,2) : "=<", 
     (3,4) : ">",       (4,3) : "<",
     (3,5) : ">",       (5,3) : "<",
     (4,5) : "!",       (5,4) : "!",
     }

for k,v in d.iteritems():
    print k, v
#    
#print rcc

toDo = []
for k,v in d.iteritems():
    if len(v) != 5:
        toDo.append(k)



#inputDict = copy.deepcopy(d)
relativeOfPair = {}
while len(toDo) > 0:
#    print "toDo", toDo
    pair = toDo[0]
    del toDo[0]
    
    relativeOfPair = reasonOver(pair, d, toDo)
    
    d.update(relativeOfPair)
    
print "********"
for k,v in d.iteritems():
    if k[0] < k[1]:
        print k, v
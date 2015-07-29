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
    if deducedRel == rcc["!<=>o"] or originRel == deducedRel:
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
 
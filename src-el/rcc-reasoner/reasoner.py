from tables import *

def findKey(d, value):
    for k,v in d.iteritems():
        if v == value:
            return k

def reasonOver(pair, d, toDo):
    relativeOfPair = {}
    for k, v in d.iteritems():
        if k[0] == pair[1]:
            deducedPair = (pair[0], k[1])
            newRelPost = comptab[d[pair]][d[k]]
            if deducedPair in d:
                deducedRel = d[deducedPair] & newRelPost
                assertNew(d, d[deducedPair], deducedPair, deducedRel, relativeOfPair, toDo)
                    
            
        if k[1] == pair[0]:
            deducedPair = (k[0], pair[1])
            newRelPre = comptab[d[k]][d[pair]]
            if deducedPair in d:
                deducedRel = d[deducedPair] & newRelPre
                assertNew(d, d[deducedPair], deducedPair, deducedRel, relativeOfPair, toDo)

    return relativeOfPair


def assertNew(d, originRel, deducedPair, deducedRel, relativeOfPair, toDo):
    if not deducedRel:
        print "inconsistent pair", deducedPair
        exit(0)
    if deducedRel == rcc["!<=>o"] or originRel == deducedRel:
        return
    relativeOfPair[deducedPair] = deducedRel
    toDo.append(deducedPair)

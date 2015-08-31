from tables import *

def findKey(d, value):
    for k,v in d.iteritems():
        if v == value:
            return k

# reaasonOver(pair, d, toDo)
# Take a pair (e.g. A-B) of concepts and "uber-matrix" d,
# for each B-C (and similarly, for each C-A)
#   looking at A--R1--B--R2--C we lookup R3 = R1 o_RCC32 R2 
#   and "combine" R3 with the existing R in A--R--C
#   to obtain the final A--R'--C        
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

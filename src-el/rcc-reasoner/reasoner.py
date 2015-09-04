import csv
import sys
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
def reasonOver(pair, d, toDo, counter):
    relativeOfPair = {}
    for k, v in d.iteritems():
        if k[0] == pair[1]:
            deducedPair = (pair[0], k[1])
            newRelPost = comptab[d[pair]][d[k]]
            if deducedPair in d:
                deducedRel = d[deducedPair] & newRelPost
                
                # write down the output
                if deducedPair == (int(sys.argv[3]), int(sys.argv[4])):
                    if deducedPair in counter:
                        counter[deducedPair] += 1
                    else:
                        counter[deducedPair] = 1
                    data = [str(pair)+' '+findKey(rcc,d[pair]), str(k)+' '+findKey(rcc,d[k]), deducedPair, counter[deducedPair], findKey(rcc, d[deducedPair]), findKey(rcc, newRelPost), findKey(rcc, deducedRel)]
                    with open("output.csv", "a") as csvFile:
                        writer = csv.writer(csvFile, delimiter=',')
                        writer.writerow(data)
#                print "Pair is", pair, k, "->", deducedPair
#                print "Old is", findKey(rcc, d[deducedPair])
#                print "Res is", findKey(rcc, newRelPost)
#                print "New is", findKey(rcc, deducedRel)
#                print ""

                assertNew(d, d[deducedPair], deducedPair, deducedRel, relativeOfPair, toDo)
                    
            
        if k[1] == pair[0]:
            deducedPair = (k[0], pair[1])
            newRelPre = comptab[d[k]][d[pair]]
            if deducedPair in d:
                deducedRel = d[deducedPair] & newRelPre
                
                # write down the output
                if deducedPair == (int(sys.argv[3]), int(sys.argv[4])):
                    if deducedPair in counter:
                        counter[deducedPair] += 1
                    else:
                        counter[deducedPair] = 1                
                    data = [str(k)+' '+findKey(rcc,d[k]), str(pair)+' '+findKey(rcc,d[pair]), deducedPair, counter[deducedPair], findKey(rcc, d[deducedPair]), findKey(rcc, newRelPre), findKey(rcc, deducedRel)]
                    with open("output.csv", "a") as csvFile:
                        writer = csv.writer(csvFile, delimiter=',')
                        writer.writerow(data)                
#                print "Pair is", k, pair, "->", deducedPair
#                print "Old is", findKey(rcc, d[deducedPair])
#                print "Res is", findKey(rcc, newRelPre)
#                print "New is", findKey(rcc, deducedRel)
#                print ""
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

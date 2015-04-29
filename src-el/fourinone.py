import copy
import itertools

def isPower2(num):
    return num != 0 and ((num & (num - 1)) == 0)

#def powerset(iterable):
#    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#    s = list(iterable)
#    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def isSupset(sup, s):
    for i in range(len(s)):
        if sup[i] == '0' and s[i] == '1':
            return False
    return True 

def isSubset(sub, s):
    for i in range(len(s)):
        if sub[i] == '1' and s[i] == '0':
            return False
    return True 

def findAllSupsets(s, pool):
    allSupsets = []
    for e in pool:
        if isSupset(e, s):
            allSupsets.append(e)
    return allSupsets

def findAllSubsets(s, pool):
    allSubsets = []
    for e in pool:
        if isSubset(e, s):
            allSubsets.append(e)
    return allSubsets

def genFourinone(artDictbin, mis, mus):
    # create power set lattice
    numOfNodes = 2**len(artDictbin)
    nodes = []
    edges = []
    for i in range(numOfNodes):
        nodes.append(i)
    for i in nodes:
        for j in nodes:
            if i<j and isPower2(i^j):
                s = bin(i)[2:]
                t = bin(j)[2:]
                tmp = ""
                if len(s) < len(artDictbin):
                    
                    for k in range(len(artDictbin)-len(s)):
                        tmp = '0' + tmp
                    s = tmp + s
                tmp = ""
                if len(t) < len(artDictbin):
                    
                    for k in range(len(artDictbin)-len(t)):
                        tmp = '0' + tmp
                    t = tmp + t
                edges.append([s,t])
    #print "edges=", edges

    # create binary candidates
    binCandidates = []
    s = ""
    for i in range(numOfNodes):
        s = bin(i)[2:]
        if len(s) < len(artDictbin):
            for i in range(len(artDictbin)-len(s)):
                s = '0' + s
        binCandidates.append(s)

    # create binary representation of mis and mus
    misBin = copy.deepcopy(mis)
    musBin = copy.deepcopy(mus)
    for i in range(len(mis)):
        for j in range(len(mis[i])):
            misBin[i][j] = artDictbin[mis[i][j]]
    for aMis in misBin:
        r = 0
        for aRel in aMis:
            r = r | aRel
        misBin[misBin.index(aMis)] = bin(r)[2:]
    for i in range(len(misBin)):
        s = ""
        if len(misBin[i]) < len(artDictbin):
            for i in range(len(artDictbin)-len(misBin[i])):
                s = '0' + s
            misBin[i] = s + misBin[i]
    for i in range(len(mus)):
        for j in range(len(mus[i])):
            musBin[i][j] = artDictbin[mus[i][j]]
    for aMus in musBin:
        r = 0
        for aRel in aMus:
            r = r | aRel
        musBin[musBin.index(aMus)] = bin(r)[2:]
    for i in range(len(musBin)):
        s = ""
        if len(musBin[i]) < len(artDictbin):
            for i in range(len(artDictbin)-len(musBin[i])):
                s = '0' + s
            musBin[i] = s + musBin[i] 
    #print "misBin",misBin
    #print "musBin",musBin
    
    # find all mcs and mus
    supOfmis = []
    for aMis in misBin:
        supOfmis.extend(findAllSupsets(aMis, binCandidates))
    tmpmcs = copy.deepcopy(binCandidates)
    for e in binCandidates:
        if supOfmis.count(e) > 0:
            tmpmcs.remove(e)
    mcsBin = []
    rem = []
    for e1 in tmpmcs:
        for e2 in tmpmcs:
            if e1 != e2 and isSupset(e1,e2):
                rem.append(e2)
    for e in tmpmcs:
        if e not in rem:
            mcsBin.append(e)

    supOfmus = []
    for aMus in musBin:
        supOfmus.extend(findAllSupsets(aMus, binCandidates))
    tmpmaa = copy.deepcopy(binCandidates)
    for e in binCandidates:
        if supOfmus.count(e) > 0:
            tmpmaa.remove(e)
    maaBin = []
    rem = []
    for e1 in tmpmaa:
        for e2 in tmpmaa:
            if e1 != e2 and isSupset(e1,e2):
                rem.append(e2)
    for e in tmpmaa:
        if e not in rem:
            maaBin.append(e)

    #print "mcsBin", mcsBin
    #print "maaBin", maaBin
    
    print ""
    print "MIS:",
    for e in misBin:
        print decodeToName(e, artDictbin),

    print ""
    print "MCS:",
    for e in mcsBin:
        print decodeToName(e, artDictbin),

    print ""
    print "MUS:",
    for e in musBin:
        print decodeToName(e, artDictbin),

    print ""
    print "MAA:",
    for e in maaBin:
        print decodeToName(e, artDictbin),
    

def decodeToName(bin, artDictbin):
    arts = []
    intNum = int(bin,2)
    for k,v in artDictbin.iteritems():
        if v & intNum != 0:
            arts.append(k)
    return arts

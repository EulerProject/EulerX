import copy
import os
import itertools
import yaml
from helper2 import newgetoutput

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

def genFourinone(latticedir, stylesheetdir, artDictbin, mis, mus):
    # create power set lattice
    fourinoneNodes = {}
    fourinoneEdges = {}
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
    #print "nodes=", nodes

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
    print "MIS (red box):",
    for e in misBin:
        print decodeToName(e, artDictbin),
        #print e,

    print ""
    print "MCS (green box):",
    for e in mcsBin:
        print decodeToName(e, artDictbin),
        #print e,

    print ""
    print "MUS: (green octagon)",
    for e in musBin:
        print decodeToName(e, artDictbin),
        #print e,

    print ""
    print "MAA: (cyan diamond)",
    for e in maaBin:
        print decodeToName(e, artDictbin),
        #print e,
    
    
    # prepare for yaml file
    nodesBin = []
    for node in nodes:
        nodeBin = bin(node)[2:]
        tmp = ""
        if len(nodeBin) < len(artDictbin):
            for k in range(len(artDictbin)-len(nodeBin)):
                tmp = '0' + tmp
            nodeBin = tmp + nodeBin
        nodesBin.append(nodeBin)
    #print "nodesBin", nodesBin
    
    fourinonedot = os.path.join(latticedir, "fourinone.gv")
    fDot = open(fourinonedot, 'w')
    fDot.write("digraph {\n\nrankdir = BT\n\n")
     
    for nodeBin in nodesBin:
        if nodeBin in misBin:
            #addFourinoneVizNode(nodeBin, "mis", fourinoneNodes)
            fDot.write(nodeBin + ' [shape=box style="filled" fillcolor="#FF0000"];\n')
        elif nodeBin in mcsBin and nodeBin in musBin:
            #addFourinoneVizNode(nodeBin, "mcsANDmus", fourinoneNodes)
            fDot.write(nodeBin + ' [shape=octagon style="filled" fillcolor="#00FF00"];\n')
        elif nodeBin in mcsBin and nodeBin in maaBin:
            #addFourinoneVizNode(nodeBin, "mcsANDmaa", fourinoneNodes)
            fDot.write(nodeBin + ' [shape=diamond style="filled" fillcolor="#00FFCC"];\n')
        elif nodeBin in mcsBin:
            #addFourinoneVizNode(nodeBin, "mcs", fourinoneNodes)
            fDot.write(nodeBin + ' [shape=box style="filled" fillcolor="#00FF00"];\n')
        else:
            fDot.write(nodeBin + ' [shape=box style="filled" fillcolor="#FFFFFF"];\n')
    
    for edge in edges:
        #addFourinoneVizEdge(edge[0], edge[1], "default", fourinoneEdges)
        fDot.write(edge[0] +  ' -> ' + edge[1] + ' [arrowhead=none]\n')
    
    
    # lengend
    #print "artDictbin", artDictbin
    artsLabels = ""
    for art, binN in artDictbin.iteritems():
        artsLabels += "<TR> \n <TD>" + str(bin(binN)[2:]) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
    fDot.write("node[shape=box] \n")
    fDot.write('{rank=sink Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
    fDot.write(artsLabels)
    fDot.write("</TABLE> \n >] } \n")
    
    
    fDot.write('}')
    fDot.close()
    
    # generate yaml file
    fourinoneyaml = os.path.join(latticedir, "fourinone.yaml")
    #fourinonedot = os.path.join(latticedir, "fourinone.gv")
    fourinonepdf = os.path.join(latticedir, "fourinone.pdf")
    fourinonesvg = os.path.join(latticedir, "fourinone.svg")
        
    ffourinone = open(fourinoneyaml, 'w')
    if fourinoneNodes:
        ffourinone.write(yaml.safe_dump(fourinoneNodes, default_flow_style=False))
    if fourinoneEdges:
        ffourinone.write(yaml.safe_dump(fourinoneEdges, default_flow_style=False))
    ffourinone.close()

        
#    newgetoutput("cat "+fourinoneyaml+" | y2d -s "+stylesheetdir+"fourinonestyle.yaml" + ">" + fourinonedot)
#    newgetoutput("dot -Tpdf "+cldot+" -o "+cldotpdf)
#    newgetoutput("dot -Tsvg "+cldot+" -o "+cldotsvg)
    

def decodeToName(bin, artDictbin):
    arts = []
    intNum = int(bin,2)
    for k,v in artDictbin.iteritems():
        if v & intNum != 0:
            arts.append(k)
    return arts

#def addFourinoneVizNode(concept, group, fourinoneNodes):
#    node = {}
#    node.update({"concept": concept})
#    node.update({"group": group})
#    fourinoneNodes.update({concept: node})
#
#def addFourinoneVizEdge(s, t, label, fourinoneEdges):
#    edge = {}
#    edge.update({"s" : s})
#    edge.update({"t" : t})
#    edge.update({"label" : label})
#    fourinoneEdges.update({s + "_" + t : edge})

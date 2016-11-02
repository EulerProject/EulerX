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

def decodeToName(bin, artDictbin):
    arts = []
    intNum = int(bin,2)
    for k,v in artDictbin.iteritems():
        if v & intNum != 0:
            arts.append(k)
    return arts

def genFourinone(latticedir, stylesheetdir, artDictbin, mis, mus, fourinoneinternalfile):
    # create power set lattice
    fourinoneNodes = {}
    fourinoneEdges = {}
    power = len(artDictbin)
    numOfNodes = 2**power
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
                if len(s) < power:
                    
                    for k in range(power-len(s)):
                        tmp = '0' + tmp
                    s = tmp + s
                tmp = ""
                if len(t) < power:
                    
                    for k in range(power-len(t)):
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
        if len(s) < power:
            for j in range(power-len(s)):
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
        if len(misBin[i]) < power:
            for j in range(power-len(misBin[i])):
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
        if len(musBin[i]) < power:
            for j in range(power-len(musBin[i])):
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
        if e not in rem and supOfmis.count(e) == 0:
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
    
    
    # prepare the internal files
    f = open(fourinoneinternalfile, "w")
    f.write('nodes = ' + repr(nodes) + '\n')
    f.write('edges = ' + repr(edges) + '\n')
    f.write('power = ' + repr(power) + '\n')
    f.write('misBin = ' + repr(misBin) + '\n')
    f.write('mcsBin = ' + repr(mcsBin) + '\n')
    f.write('musBin = ' + repr(musBin) + '\n')
    f.write('maaBin = ' + repr(maaBin) + '\n')
    f.write('artDictbin = ' + repr(artDictbin) + '\n')
    f.close()
    
#     # prepare for yaml file
#     nodesBin = []
#     for node in nodes:
#         nodeBin = bin(node)[2:]
#         tmp = ""
#         if len(nodeBin) < power:
#             for k in range(power-len(nodeBin)):
#                 tmp = '0' + tmp
#         nodeBin = tmp + nodeBin
#         nodesBin.append(nodeBin)
#     #print "nodesBin", nodesBin
#     
#     fourinonedot = os.path.join(latticedir, "fourinone.gv")
#     fDot = open(fourinonedot, 'w')
#     fDot.write("digraph {\n\nrankdir = BT\n\n")
#      
#     for nodeBin in nodesBin:
#         if nodeBin in misBin:
#             #addFourinoneVizNode(nodeBin, "mis", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=box style="filled" fillcolor="#FF0000"];\n')
#         elif nodeBin in mcsBin and nodeBin in musBin:
#             #addFourinoneVizNode(nodeBin, "mcsANDmus", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=octagon style="filled" fillcolor="#00FF00"];\n')
#         elif nodeBin in mcsBin and nodeBin in maaBin:
#             #addFourinoneVizNode(nodeBin, "mcsANDmaa", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=diamond style="filled" fillcolor="#00FFCC"];\n')
#         elif nodeBin in mcsBin:
#             #addFourinoneVizNode(nodeBin, "mcs", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=box style="filled" fillcolor="#00FF00"];\n')
#         elif nodeBin in musBin:
#             #addFourinoneVizNode(nodeBin, "musOnly", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=octagon style="filled" fillcolor="#00FF00"];\n')
#         elif nodeBin in maaBin:
#             #addFourinoneVizNode(nodeBin, "maaOnly", fourinoneNodes)
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=diamond style="filled" fillcolor="#00FFCC"];\n')
#         else:
#             fDot.write(convertToIndex(nodeBin, power) + ' [shape=box style="filled" fillcolor="#FFFFFF"];\n')
#     
#     for edge in edges:
#         #addFourinoneVizEdge(edge[0], edge[1], "default", fourinoneEdges)
#         fDot.write(convertToIndex(edge[0], power) +  ' -> ' + convertToIndex(edge[1], power) + ' [arrowhead=none]\n')
#     
#     
#     # lengend
#     #print "artDictbin", artDictbin
#     artsLabels = ""
#     for art, binN in artDictbin.iteritems():
#         artsLabels += "<TR> \n <TD>" + convertToIndex(str(bin(binN)[2:]),power) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
#     fDot.write("node[shape=box] \n")
#     fDot.write('{rank=top Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
#     fDot.write(artsLabels)
#     fDot.write("</TABLE> \n >] } \n")
#     fDot.write('Legend -> "None" [style=invis]\n')
#     fDot.write("node[shape=box] \n")
#     fDot.write('{rank=top Intro [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
#     intro = "<TR> \n <TD> Minimal Inconsistent Subsets (MIS) </TD> \n <TD> Red box </TD> \n </TR> \n" \
#           + "<TR> \n <TD> Maximal Consistent Subsets </TD> \n <TD> Green box </TD> \n </TR> \n" \
#           + "<TR> \n <TD> Minimal Unique Subsets </TD> \n <TD> Green octagon</TD> \n </TR> \n" \
#           + "<TR> \n <TD> Maximal Ambiguous Subsets </TD> \n <TD> Cyan diamond </TD> \n </TR> \n"
#     fDot.write(intro)
#     fDot.write("</TABLE> \n >] } \n")
#     fDot.write('}')
#     fDot.close()
    
#     # generate yaml file
#     fourinoneyaml = os.path.join(latticedir, "fourinone.yaml")
#     #fourinonedot = os.path.join(latticedir, "fourinone.gv")
#     fourinonepdf = os.path.join(latticedir, "fourinone.pdf")
#     fourinonesvg = os.path.join(latticedir, "fourinone.svg")
#         
#     ffourinone = open(fourinoneyaml, 'w')
#     if fourinoneNodes:
#         ffourinone.write(yaml.safe_dump(fourinoneNodes, default_flow_style=False))
#     if fourinoneEdges:
#         ffourinone.write(yaml.safe_dump(fourinoneEdges, default_flow_style=False))
#     ffourinone.close()

        
#    newgetoutput("cat "+fourinoneyaml+" | y2d -s "+stylesheetdir+"fourinonestyle.yaml" + ">" + fourinonedot)
#    newgetoutput("dot -Tpdf "+cldot+" -o "+cldotpdf)
#    newgetoutput("dot -Tsvg "+cldot+" -o "+cldotsvg)

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

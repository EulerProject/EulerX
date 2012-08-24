from itertools import *
from taxonomy import *
from utility import *
from re import *	

# this module  defines the classes: Node

class Node:

    def __init__(self, taxMap, p, n):
	self.taxMap = taxMap
	self.children = []
	self.taxMap = copy.deepcopy(taxMap)
	self.num = n
	if(len(p) != 0):
	    pGoal=p.pop()
	    for i in range(len(pGoal[2])):
		tmpP = copy.deepcopy(p)
		tmpTM = copy.deepcopy(self.taxMap)
		list=pGoal[0]+" "+pGoal[2][i]+" "+pGoal[1]
		tmpTM.articulationSet.addArticulationWithList(list, self.taxMap)
		consistencyCheck = tmpTM.testConsistencyWithoutGoal("/home/michen/tmp/")
		print consistencyCheck[0]
		if(consistencyCheck[0] == "true"):
		    self.children.append([list,Node(tmpTM, tmpP, n*10+i)])

    def addChild(self, desc, node):
	self.children.append([desc, node])

    def dump(self, i):
	for j in range(i):
	    print "    ",
	print i
	if(len(self.children) ==0):
	    for j in range(i):
	        print "    ",
	    print "  []"
	for child in self.children:
	    for j in range(i):
	        print "    ",
	    print " --"+child[0]+"-->"
	    child[1].dump(i+1)

    def dotHelper(self, fDot):
	fDot.write("\""+self.num.__str__()+"\" [color=blue];\n")
	for child in self.children:
	    # Node
	    child[1].dotHelper(fDot)
	    # Edge
	    fDot.write("\""+self.num.__str__()+"\" -> \""+child[1].num.__str__()+"\" [label=\""+child[0]+"\", style=filled, color=black];\n")

class Forest:

    def __init__(self, taxMap, branches):
	self.taxMap = taxMap
	self.trees=[]
	self.branches=branches
	self.buildTrees()

    def buildTrees(self):
	goals=self.taxMap.getAllTaxonPairs()
	for p in permutations(self.branches):
	    #tmpTM = copy.deepcopy(self.taxMap)
	    #tmpTM
	    self.trees.append(Node(self.taxMap, list(p), 1))

    def dump(self):
	for i in range(len(self.trees)):
	    tree=self.trees[i]
	    print "Tree "+i.__str__()+":"
	    tree.dump(1)
	    print "[]"

    def genDot(self, outputFileName):
	for i in range(len(self.trees)):
            fDot = open(outputFileName+"_dt_"+i.__str__()+".dot", 'w')
            fDot.write("digraph {\n\nrankdir = RL\n\n")
	    tree=self.trees[i]
	    tree.dotHelper(fDot)
	    fDot.write("}\n")
	    fDot.close()
	

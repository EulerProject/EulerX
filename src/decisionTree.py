from itertools import *
from taxonomy import *
from utility import *
from re import *	

# this module  defines the classes: Node

class Node:

    def __init__(self, taxMap, p):
	self.taxMap = taxMap
	self.children = []
	if(len(p) != 0):
	    pGoal=p.pop()
	    for i in range(len(pGoal[2])):
		tmpTaxMap = copy.deepcopy(taxMap)
		tmpP = copy.deepcopy(p)
		list=pGoal[0]+" "+pGoal[2][i]+" "+pGoal[1]
		tmpTaxMap.articulationSet.addArticulationWithList
		self.children.append([list,Node(tmpTaxMap, tmpP)])

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

class Forest:

    def __init__(self, taxMap, branches):
	self.taxMap = taxMap
	self.trees=[]
	self.branches=branches
	self.buildTrees()

    def buildTrees(self):
	goals=self.taxMap.getAllTaxonPairs()
	for p in permutations(self.branches):
	    self.trees.append(Node(self.taxMap, list(p)))

    def dump(self):
	for i in range(len(self.trees)):
	    tree=self.trees[i]
	    print "Tree "+i.__str__()+":"
	    tree.dump(1)
	    print "[]"

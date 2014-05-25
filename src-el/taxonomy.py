import re
import copy
import commands
from relations import *
from articulation import *

class Taxon:
   
    def __init__(self, name="", level=0):
        self.parent = ""
        self.children = []
        self.name = name
        self.abbrev = name
	self.level = level
        self.taxonomy = Taxonomy()    
 
    def addChild(self, child):
        self.children += [child]
  
    def hasChildren(self):
        return len(self.children) > 0

    def dotName(self):
        return self.taxonomy.abbrev + "." + self.abbrev

    def dlvName(self):
        return "c" + self.taxonomy.abbrev + "_" + self.abbrev

class Taxonomy:
    def __init__(self):
        self.roots = [] 
        self.taxa = {}
        self.abbrev = ""
        self.name = ""

    def nameit(self, name):
        self.name = name
        self.abbrev = name

    def nameit(self, abbrev, name):
        self.abbrev = abbrev
        self.name = name
    
    def dlvName(self):
        return "t" + self.abbrev

    def addTaxon(self, parent):
        if self.taxa.has_key(parent):
            return None
        else: 
            thisParent = Taxon(parent)
            thisParent.taxonomy = self
            self.taxa[parent] = thisParent
            self.roots.append(thisParent)

    def addDoubleTaxon(self, taxaMap, parent, child, onlyOne):
        thisParent = self.taxa[parent]
        
        if (child != ""):
            if self.taxa.has_key(child):
                thisChild = self.taxa[child]
            else:
                thisChild = Taxon(child, thisParent.level+1)
                thisChild.taxonomy = self
                self.taxa[child] = thisChild
            
            thisChild.parent = thisParent
            # the special case that parent = its only child
            if onlyOne and taxaMap.options.enableCov:
		taxaMap.addEMir(thisParent.dotName(), thisChild.dotName())
		taxaMap.addEqMap(thisParent.dotName(), thisChild.dotName())
	    else:
	    	taxaMap.addTMir(self.abbrev, parent, child)
	    	for sibling in thisParent.children:
	    	    taxaMap.addDMir(self.abbrev, child, sibling.abbrev)
            thisParent.addChild(thisChild)

    def getTaxon(self, theTaxon):
        if (not(self.taxa.has_key(theTaxon))):
            print "no taxon " + theTaxon + " in " + self.abbrev
            return None
        else:
            return (self.taxa[theTaxon]);
            
    def addTaxaWithList(self, taxaMap, theList):
        noParens = re.match("\((.*)\)", theList).group(1)
        if (noParens.find(" ") != -1):
            elements = re.split("\s", noParens)
            # no coverage
            nc = False
            if elements[len(elements)-1] != "nc":
                nchildren = len(elements)-1
            else:
                nchildren = len(elements)-2
                nc = True
                elements[len(elements)-1] += elements[0]
            self.addTaxon(elements[0])
            for index in range (1, len(elements)):
                self.addDoubleTaxon(taxaMap, elements[0], elements[index], nchildren == 1 and not nc)
        else:
            self.addTaxon(noParens)    
   


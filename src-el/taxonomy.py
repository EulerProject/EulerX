import re
import copy
import commands
from relations import *

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
        return self.abbrev + self.taxonomy.abbrev
    
class Articulation:
    
    def __init__(self, initInput="", mapping=None):
        # TODO relations
	self.string = initInput
	self.numTaxon = 2
	self.confidence = 2
        self.relations = 0
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.taxon4 = Taxon()
	    return None
	if (initInput.find("confidence=") != -1):
	    elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
	if (initInput.find("sum") != -1 or initInput.find("diff") != -1):
	    if (initInput.find("lsum") != -1):
	        self.relations = 0 #[relationDict["+="]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) lsum (.*)\.(.*)", initInput)
	    elif (initInput.find("rsum") != -1):
	        self.relations = 0 #[relationDict["=+"]]
	        elements = re.match("(.*)\.(.*) rsum (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("ldiff") != -1):
	        self.relations = 0 #[relationDict["-="]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) ldiff (.*)\.(.*)", initInput)
	    elif (initInput.find("rdiff") != -1):
	        self.relations = 0 #[relationDict["=-"]]
	        elements = re.match("(.*)\.(.*) rdiff (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("e4sum") != -1):
	        self.relations = 0 #[relationDict["+=+"]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) e4sum (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("i4sum") != -1):
	        self.relations = 0 #[relationDict["+<=+"]]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) i4sum (.*)\.(.*) (.*)\.(.*)", initInput)
            taxon1taxonomy = elements.group(1)
            taxon1taxon = elements.group(2)
            taxon2taxonomy = elements.group(3)
            taxon2taxon = elements.group(4)
            taxon3taxonomy = elements.group(5)
            taxon3taxon = elements.group(6)
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
            self.taxon3 = mapping.getTaxon(taxon3taxonomy, taxon3taxon)
	    self.numTaxon = 3
            if(initInput.find("4sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
	        self.numTaxon = 4
        else:
            ## initInput is of form b48.a equals k04.a
            self.relation = 0
            if (initInput.find("{") != -1):
                elements = re.match("(.*)\.(.*) {(.*)} (.*)\.(.*)", initInput)
            else:
                elements = re.match("(.*)\.(.*) (.*) (.*)\.(.*)", initInput)
            
            taxon1taxonomy = elements.group(1)
            taxon1taxon = elements.group(2)
            relString = elements.group(3)
            taxon2taxonomy = elements.group(4)
            taxon2taxon = elements.group(5)
          
          
            if (relString.find(" ") != -1):
                if (relation.has_key(relString)):
                    self.relations = relation[relString]
                else:
                    relElements = re.split("\s", relString)
          
                    for rel in relElements:
                        self.relations |= relation[rel]
                  
            else:
                self.relations = relation[relString]
              
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
 
    def toDlv(self):
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        if self.relations == relation["equals"]:
            result  = "ir(X) :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
            result += "ir(X) :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
        elif self.relations == relation["includes"]:
            result  = "ir(X) :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
        elif self.relations == relation["is_included_in"]:
            result  = "ir(X) :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
        elif self.relations == relation["disjoint"]:
            result  = "ir(X) :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
        elif self.relations == relation["overlaps"]:
            result  = "\n"
        elif self.relations == (relation["equals"] | relation["is_included_in"]):
            result  = "ir(X) :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
            result += "vr(X) v ir(X) :- in(" + name1 + ",X), out(" + name2 + ",X).\n" 
        elif self.relations == (relation["equals"] | relation["includes"]):
            result  = "ir(X) :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
            result += "vr(X) v ir(X) :- out(" + name1 + ",X), in(" + name2 + ",X).\n" 
        return result

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
    
    def addTaxon(self, parent):
        if self.taxa.has_key(parent):
            return None
        else: 
            thisParent = Taxon(parent)
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
	    if(onlyOne):
		taxaMap.addEMir(parent, child)
	    else:
	    	#taxaMap.addTMir(self.authority.abbrev, parent, child)
	    	for sibling in thisParent.children:
	    	    taxaMap.addDMir(self.abbrev, child, sibling.abbrev)
            thisParent.addChild(thisChild)

    def getTaxon(self, theTaxon):
        if (not(self.taxa.has_key(theTaxon))):
            print "no taxon " + theTaxon + " in " + self.authority.abbrev
            return None
        else:
            return (self.taxa[theTaxon]);
            
    def addTaxaWithList(self, taxaMap, theList):
        noParens = re.match("\((.*)\)", theList).group(1)
        if (noParens.find(" ") != -1):
            elements = re.split("\s", noParens)
            self.addTaxon(elements[0])
            for index in range (1, len(elements)):
                self.addDoubleTaxon(taxaMap, elements[0], elements[index], len(elements) == 2)
        else:
            self.addTaxon(noParens)    


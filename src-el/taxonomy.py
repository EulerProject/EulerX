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
	        elements = re.match("(.*)_(.*) (.*)_(.*) e4sum (.*)_(.*) (.*)_(.*)", initInput)
	    elif (initInput.find("i4sum") != -1):
	        self.relations = 0 #[relationDict["+<=+"]]
	        elements = re.match("(.*)_(.*) (.*)_(.*) i4sum (.*)_(.*) (.*)_(.*)", initInput)
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
 
class TaxonomyMapping:

    def __init__(self):
        self.mir = {}                          # MIR
        self.tr = []                           # transitive reduction
        self.eq = []                           # euqlities
        self.taxonomies = {}
        self.articulations = []
        self.map = {}
        self.baseDlv = ""

    def addDMir(self, tName, child, sibling):
	self.mir[tName + "." + child +"," + tName + "." + sibling] ="{disjoint}"
	self.mir[tName + "." + sibling +"," + tName + "." + child] ="{disjoint}"

    def getTaxon(self, taxonomyName="", taxonName=""):
        taxonomy = self.taxonomies[taxonomyName]
        taxon = taxonomy.getTaxon(taxonName)
        return taxon

    def run(self):
        self.genDlv()
        com = "dlv -silent -filter=vr tmp.dlv"
        print commands.getoutput(com)

    def genDlv(self):
        if self.baseDlv != "":
            return  None
        self.genDlvConcept()
        self.genDlvPC()
        self.genDlvAr()
        fdlv = open("tmp.dlv", 'w')
        fdlv.write(self.baseDlv)
        fdlv.close()

    def genDlvConcept(self):
        con = "%%% Concepts\n"

        # numbering concepts
        num = 0
        for key in self.taxonomies.keys():
            for taxon in self.taxonomies[key].taxa.keys():
                t = self.taxonomies[key].taxa[taxon]
                self.map[t.dlvName()] = num
                con += "concept(" + t.dlvName() + "," + num.__str__()+").\n"
                num += 1

        self.baseDlv = "#maxint=" + int(2**num).__str__() + ".\n\n"
        self.baseDlv += con
        self.baseDlv += "\n%%% power\n"
        self.baseDlv += "p(0,1).\n"
        self.baseDlv += "p(N,M) :- #int(N),N>0,#succ(N1,N),p(N1,M1),M=M1*2.\n\n"

        self.baseDlv += "%%% regions\n"
        self.baseDlv += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

        self.baseDlv += "%%% count of concepts\n"
        self.baseDlv += "count(N):- #int(N),N>=0,N<#count{Y:concept(Y,_)}.\n\n"

        self.baseDlv += "%%% bit\n"
        self.baseDlv += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
        self.baseDlv += "bit(M, N, 1):-r(M),count(N),not bit(M,N,0).\n\n"

        self.baseDlv += "%%% Meaning of regions\n"
        self.baseDlv += "in(X, M) v out(X, M) :- r(M),concept(X,N),count(N).\n"
        self.baseDlv += "in(X, M) :- r(M),concept(X,N),bit(M,N,1).\n"
        self.baseDlv += "out(X, M) :- r(M),concept(X,N),bit(M,N,0).\n\n"

        self.baseDlv += "%%% Constraints of regions.\n"
        self.baseDlv += "vr(X) :- r(X), not ir(X).\n"
        self.baseDlv += ":- vr(X), ir(X).\n\n"

    def genDlvPC(self):
        self.baseDlv += "%%% PC relations\n"
        for key in self.taxonomies.keys():
            queue = copy.deepcopy(self.taxonomies[key].roots)
            while len(queue) != 0:
                t = queue.pop(0)
                if t.hasChildren:
                    # ISA
                    self.baseDlv += "%% ISA\n"
                    coverage = "ir(X) :- in(" + t.dlvName() + ", X)"
                    for t1 in t.children:
                        self.baseDlv += "% " + t1.dlvName() + " isa " + t.dlvName() + "\n"
                        self.baseDlv += "ir(X) :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n\n"
                        coverage += ",out(" + t1.dlvName() + ", X)"
                    # C
                    self.baseDlv += "%% coverage\n"
                    self.baseDlv += coverage + ".\n\n"
                    # D
                    self.baseDlv += "%% sibling disjointness\n"
                    for i in range(len(t.children) - 1):
                        for j in range(i+1, len(t.children)):
                            name1 = t.children[i].dlvName()
                            name2 = t.children[j].dlvName()
                            self.baseDlv += "% " + name1 + " ! " + name2+ "\n"
                            self.baseDlv += "ir(X) :- in(" + name1 + ", X), in(" + name2+ ", X).\n\n"


    def genDlvAr(self):
        self.baseDlv += "%%% Articulations\n"
        for i in range(len(self.articulations)):
            self.baseDlv += "% " + self.articulations[i].string + "\n"
            self.baseDlv += self.articulations[i].toDlv()+ "\n"

        #print self.baseDlv

    def readFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        for line in lines:

            if (re.match("taxonomy", line)):
                taxName = re.match("taxonomy (.*)", line).group(1) 
                taxonomy = Taxonomy()
                if (taxName.find(" ") == -1):
                    taxonomy.nameit(taxName)
                else:
                    taxName = re.match("(.*?)\s(.*)", taxName)
                    taxonomy.nameit(taxName.group(1), taxName.group(2))
                  
                self.taxonomies[taxonomy.abbrev] = taxonomy
              
            # reads in lines of the form (a b c) where a is the parent
            # and b c are the children
            elif (re.match("\(.*\)", line)):
                taxonomy.addTaxaWithList(self, line)

            elif (re.match("articulation", line)):
                None
              
            elif (re.match("\[.*?\]", line)):
                inside = re.match("\[(.*)\]", line).group(1)
                # TODO add articulation
                self.articulations += [Articulation(inside, self)]
		if inside.find("{") != -1:
		    r = re.match("(.*) \{(.*)\} (.*)", inside)
		    #self.addPMir(r.group(1), r.group(3), r.group(2).replace(" ",","), 0)
		else:
                    None
		    #self.addAMir(inside, 0)
              
           # elif (re.match("\<.*\>", line)):
            #    inside = re.match("\<(.*)\>", line).group(1)
             #   hypElements = re.split("\s*\?\s*", inside)
              #  self.hypothesisType = hypElements[0]
               # hyp = hypElements[1]
               # hypArticulation = Articulation(hyp, self)
               # self.hypothesis = hypArticulation
                   
        return True              
 

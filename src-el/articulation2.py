import re
import copy
import commands
from relations import *
from taxonomy import *

class Articulation:
    
    def __init__(self, initInput="", mapping=None):
	self.string = initInput
	self.numTaxon = 2
	self.confidence = 2
        self.relations = 0
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.taxon4 = Taxon()
            self.taxon5 = Taxon()
	    return None

        # Parsing begins here
	if (initInput.find("confidence=") != -1):
	    elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
	if (initInput.find("sum") != -1 or initInput.find("diff") != -1):
	    if (initInput.find("lsum") != -1):
	        self.relations = relation["+="]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) lsum (.*)\.(.*)", initInput)
            elif (initInput.find("l3sum") != -1):
	        self.relations = relation["+3="]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l3sum (.*)\.(.*)", initInput)
	    elif (initInput.find("l4sum") != -1):
	        self.relations = relation["+4="]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l4sum (.*)\.(.*)", initInput)
	    elif (initInput.find("rsum") != -1):
	        self.relations = relation["=+"]
	        elements = re.match("(.*)\.(.*) rsum (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("r3sum") != -1):
	        self.relations = relation["=3+"]
	        elements = re.match("(.*)\.(.*) r3sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("r4sum") != -1):
		self.relations = relation["=4+"]
		elements = re.match("(.*)\.(.*) r4sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
	    elif (initInput.find("ldiff") != -1):
	        self.relations = relation["-="]
	        elements = re.match("(.*)\.(.*) (.*)\.(.*) ldiff (.*)\.(.*)", initInput)
	    elif (initInput.find("rdiff") != -1):
	        self.relations = relation["=-"]
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
            if(initInput.find("e4sum") != -1 or initInput.find("i4sum") != -1 or initInput.find("l3sum") != -1 or initInput.find("r3sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
	        self.numTaxon = 4
            if(initInput.find("l4sum") != -1 or initInput.find("r4sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
                taxon5taxonomy = elements.group(9)
                taxon5taxon = elements.group(10)
                self.taxon5 = mapping.getTaxon(taxon5taxonomy, taxon5taxon)
	        self.numTaxon = 5
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
                    self.relations = rcc5[relString]
                else:
                    relElements = re.split("\s", relString)
          
                    for rel in relElements:
                        self.relations |= rcc5[rel]
                  
            else:
                self.relations = rcc5[relString]
              
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
 
    def toASP(self, enc, rnr, align):
        result = ""
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        if encode[enc] & encode["vr"] or encode[enc] & encode["dl"] or encode[enc] & encode["mn"]:


rule   = {}   # common encoding for both dlv and potassco
ruleEx = {}   # for dlv only
rule["equals"]     = "ir(X, $r) :- out($x ,X), in($y ,X).\n"\
	           + "ir(X, $r) :- in($x,X), out($y,X).\n"\
                   + "ir(X, prod($r,R)) :- out3($x, X, R), in($y,X), ix.\n"\
                   + "ir(X, prod($r,R)) :- in($x,X), out3($y, X, R), ix.\n"\
	           + "pie($r, A, 1) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
	           + "c($r, A, 1) :- vr(X, A), in($x, X), in($y, X), ix.\n"
ruleEx["equals"]   = ":- #count{X: vrs(X) $d in($x,X), in($y,X)} = 0, pw.\n" 
rule["includes"]   = "ir(X, $r) :- out($x,X), in($y,X), pw.\n"\
		   + "ir(X, prod($r,R)) :- out3($x, X, R), in($y,X), ix.\n"\
                   + "pie($r, A, 1) :- ir(X, A), in($x, X), out($y, X), ix.\n"\
                   + "c($r, A, 1) :- vr(X, A), in($x, X), out($y, X), ix.\n"\
                   + "pie($r, A, 2) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
                   + "c($r, A, 2) :- vr(X, A), in($x, X), in($y, X), ix.\n"\
                   + "ir(X, $r) :- in($x,X), out($y,X), pw.\n"\
                   + "pie($r, A, 1) :- ir(X, A), out($x, X), in($y, X), ix.\n"\
                   + "c($r, A, 1) :- vr(X, A), out($x, X), in($y, X), ix.\n"\
                   + "pie($r, A, 2) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
                   + "c($r, A, 2) :- vr(X, A), in($x, X), in($y, X), ix.\n"
ruleEx["includes"] = ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n"\
                   + ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n" 
rule["is_included_in"] = "ir(X, $r) :- out($x,X), in($y,X), pw.\n"\
                       + "pie($r, A, 1) :- ir(X, A), in($x, X), out($y, X), ix.\n"\
                       + "c($r, A, 1) :- vr(X, A), in($x, X), out($y, X), ix.\n"\
                       + "pie($r, A, 2) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
                       + "c($r, A, 2) :- vr(X, A), in($x, X), in($y, X), ix.\n"
ruleEx["is_included_in"] = ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n"\
                         + ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0, pw.\n"
rule["disjoint"] = "pie($r, A, 1) :- ir(X, A), out($x, X), in($y, X), ix.\n"\
                 + "c($r, A, 1) :- vr(X, A), out($x, X), in($y, X), ix.\n"\
                 + "pie($r, A, 2) :- ir(X, A), in($x, X), out($y, X), ix.\n"\
                 + "c($r, A, 2) :- vr(X, A), in($x, X), out($y, X), ix.\n"\
                 + "ir(X, $r) :- in($x,X), in($y,X).\n" 
ruleEx["disjoint"] = ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n"\
		   + ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0, pw.\n" 
rule["overlaps"]   = "pie($r, A, 1) :- ir(X, A), in($x, X), out($y, X), ix.\n"\
                   + "c($r, A, 1) :- vr(X, A), in($x, X), out($y, X), ix.\n"\
                   + "pie($r, A, 2) :- ir(X, A), out($x, X), in($y, X), ix.\n"\
                   + "c($r, A, 2) :- vr(X, A), out($x, X), in($y, X), ix.\n"\
                   + "pie($r, A, 3) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
                   + "c($r, A, 3) :- vr(X, A), in($x, X), in($y, X), ix.\n"
ruleEx["overlaps"] = ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n"\
		   + ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0, pw.\n"\
		   + ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n" 
rule[rcc5["equals"] | rcc5["disjoint"]] =\
                   ":- #count{X : vrs(X), in($x, X), out($y, X)} > 0, #count{Y : vrs(Y), out($x, Y), in($y, Y)} > 0.\n"\
                   + ":- #count{X : vrs(X), in($x, X), out($y, X)} = 0, #count{Y : vrs(Y), out($x, Y), in($y, Y)} = 0.\n"\
                   + ":- #count{X : vrs(X), in($x, X), in($y, X)} > 0, #count{Y : vrs(Y), out($x, Y), in($y, Y)} = 0.\n"\
                   + ":- #count{X : vrs(X), in($x, X), in($y, X)} = 0, #count{Y : vrs(Y), out($x, Y), in($y, Y)} > 0.\n"
rule[rcc5["equals"] | rcc5["is_included_in"]] =\
		   "ir(X, $r) :- in($x,X), out($y,X).\n"\
		   "ir(X, prod($r,R)) :- in($x,X), out3($y, X, R), ix.\n"\
	           "pie($r, A, 1) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
	           "c($r, A, 1) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
ruleEx[rcc5["equals"] | rcc5["is_included_in"]] =\
		   "vr(X, $r) v ir(X, $r) :- out($x,X), in($y,X).\n"\
		   ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n"
rule[rcc5["equals"] | rcc5["includes"]] =\
		   "ir(X, $r) :- out($x,X), in($y,X).\n"\
		   "ir(X, prod($r,R)) :- out3($x, X, R), in($y,X), ix.\n"\
	           "pie($r, A, 1) :- ir(X, A), in($x, X), in($y, X), ix.\n"\
	           "c($r, A, 1) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
ruleEx[rcc5["equals"] | rcc5["includes"]] =\
		   "vr(X, $r) v ir(X, $r) :- in($x,X), out($y,X).\n"\
		   ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n" 
rule[rcc5["is_included_in"] | rcc5["includes"]] =\
		   "ir(X, $r) :- in($x,X), out($y,X), vr(Y, _), in($y,Y), out($x,Y).\n"\
		   "ir(Y, $r) :- #count{X: vrs(X), in($x,X), out($y,X)} > 0, in($y,Y), out($x,Y).\n"
rule[rcc5["disjoint"] | rcc5["overlaps"] =\
		   "ir(X, $r) v vr(X, $r) :- in($x,X), in($y,X).\n"
ruleEx[rcc5["disjoint"] | rcc5["overlaps"] =\
		   ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n" 
		   ":- #count{X: vrs(X), in($y,X), out($x,X)} = 0, pw.\n" 
	    elif self.relations == (rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), in($x,X), out($y,X)} > 0, #count{Y: vrs(Y), in($y,Y), out($x,Y)} = 0, pw.\n"
	            result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in($y, X), out($x, X), #count{Y: vr(Y, _), in($x,Y), out($y,Y)} > 0, ix.\n"
	            result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in($x, X), out($y, X), #count{Y: vr(Y, _), in($y,Y), out($x,Y)} > 0, ix.\n\n"
		    result += ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, #count{Y: vrs(Y), in($y,Y), out($x,Y)} > 0, pw.\n"
	            result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in($x, X), out($y, X), #count{Y: vr(Y, _), in($y,Y), out($x,Y)} > 0, ix.\n"
	            result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in($x, X), out($y, X), #count{Y: vr(Y, _), in($y,Y), out($x,Y)} > 0, ix.\n\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n"
	            result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in($x, X), in($y, X), ix.\n"
	            result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- 1[vrs(X): in($x,X): out($y,X)], [vr(Y, _): in($y,Y): out($x,Y)]0.\n"
		    result += ":- [vrs(X): in($x,X): out($y,X)]0, 1[vr(Y, _): in($y,Y): out($x,Y)].\n"
		    result += ":- [vrs(X): in($x,X): in($y,X)]0.\n"
		#result += "in($y,X) v out($y,X) :- in($x,X).\n" 
		#result += "in($x,X) v out($x,X) :- out($y,X).\n" 
		#result += "in($y,X) v out($y,X) :- out($x,X).\n" 
		#result += "in($x,X) v out($x,X) :- in($y,X).\n" 
	    elif self.relations == (rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out($y,X).\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0, pw.\n" 
	            result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in($x, X), in($y, X), ix.\n"
	            result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
	            result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), out($x, X), in($y, X), ix.\n"
	            result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), out($x, X), in($y, X), ix.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out($y,X).\n"
		    align.basePw += ":- [vrs(X): in($x,X): in($y,X)]0.\n" 
		    align.basePw += ":- [vrs(X): out($x,X): in($y,X)]0.\n" 
		#result += "in($y,X) v out($y,X) :- in($x,X).\n" 
		#result += "in($x,X) v out($x,X) :- out($y,X).\n" 
		#result += "in($y,X) v out($y,X) :- out($x,X).\n" 
		#result += "in($x,X) v out($x,X) :- in($y,X).\n" 
	    elif self.relations == (rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result += ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0, pw.\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} > 0, #count{Y: vrs(Y), out($y,Y), in($x,Y)} > 0, pw.\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, #count{Y: vrs(Y), out($y,Y), in($x,Y)} = 0, pw.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    align.basePw += ":- [vrs(X): out($x,X): in($y,X)]0.\n" 
		    align.basePw += ":- rel($x, $y, \"><\").\n" 
		    align.basePw += "rel($x, $y, \"<\") | rel($x, $y, \"!\").\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out($x, X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out($x, X), in($y, X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", prod(A, B), 2) :- vr(X, A), in($x, X), in($y, X), vr(Y, B), out("+ name2 + ",Y), in($x,Y), ix.\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in($x, X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in($x, X), out($y, X), ix.\n\n"
	    elif self.relations == (rcc5["includes"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result += "vrs(X) v irs(X) :- out($x,X), in($y,X), pw.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    align.basePw += "vrs(X) | irs(X) :- out($x,X): in($y,X).\n" 
		    align.basePw += ":- [vrs(X): in($x,X): in($y,X)]0.\n" 
		    align.basePw += ":- [vrs(X): in($x,X): out($y,X)]0.\n" 
	    elif self.relations == (rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
		    result += ":- #count{X: vrs(X), in($x,X), out($y,X)} = 0, pw.\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} > 0, #count{Y: vrs(Y), in($y,Y), out($x,Y)} > 0, pw.\n"
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0, #count{Y: vrs(Y), in($y,Y), out($x,Y)} = 0, pw.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    #align.basePw += ":- [vrs(X): in($x,X): out($y,X)]0.\n" 
		    align.basePw += "rel($x, $y, \"!\") | rel($x, $y, \">\").\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in($x, X), out($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in($x, X), out($y, X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", prod(A, B), 2) :- vr(X, A), in($x, X), in($y, X), vr(Y, B), in("+ name2 + ",Y), out($x,Y), ix.\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in($x, X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out($x, X), in($y, X), ix.\n\n"
	    elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
		  result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- out($x,X), in($y,X).\n" 
		  result += "vr(X, r" + self.ruleNum.__str__() + ") v ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out($y,X).\n" 
                  result += ":- #count{X: vrs(X), in($x,X), out($y, X)} > 0, #count{Y: vrs(Y), out($x,Y), in($y, Y)} > 0.\n"
                  result += ":- #count{X: vrs(X), in($x,X), in($y, X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		  result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- out($x,X), in($y,X).\n" 
		  result += "vr(X, r" + self.ruleNum.__str__() + ") | ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out($y,X).\n" 
                  result += ":- 1[vrs(X): in($x,X): out($y, X)], 1[vrs(X): out($x,X): in($y, X)].\n"
                  result += ":- [vrs(X): in($x,X): in($y, X)]0.\n\n"
	    elif self.relations == (rcc5["is_included_in"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                  result += ":- #count{X: vrs(X), in($x,X), out($y, X)} > 0, #count{Y: vrs(Y), out($x,Y), in($y, Y)} = 0.\n"
                  result += ":- #count{X: vrs(X), in($x,X), in($y, X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                  result += ":- 1[vrs(X): in($x,X): out($y, X)], [vrs(X): out($x,X): in($y, X)]0.\n"
                  result += ":- [vrs(X): in($x,X): in($y, X)]0.\n\n"
	    elif self.relations == (rcc5["includes"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                  result += ":- #count{X: vrs(X), in($x,X), out($y, X)} = 0, #count{Y: vrs(Y), out($x,Y), in($y, Y)} > 0.\n"
                  result += ":- #count{X: vrs(X), in($x,X), in($y, X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                  result += ":- [vrs(X): in($x,X): out($y, X)]0, 1[vrs(X): out($x,X): in($y, X)].\n"
                  result += ":- [vrs(X): in($x,X): in($y, X)]0.\n\n"
	    elif self.relations == (rcc5["equals"] | rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                  result += ":- #count{X: vrs(X), out($x, X), in($y, X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in($y, Y)} = 0.\n"
                  result += ":- #count{X: vrs(X), out($x, X), in($y, X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in($y, Y)} > 0.\n"
                  result += ":- #count{X: vrs(X), out($x, X), in($y, X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in($y, Y)} = 0, #count{Z: vrs(Z), in($x, Z), out($y, Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                  # TODO
                  result = ""
	    elif self.relations == (rcc5["equals"] | rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                  result += ":- #count{X: vrs(X), in($x, X), out($y, X)} = 0, #count{Y:vrs(Y), in($x, Y), in($y, Y)} = 0.\n"
                  result += ":- #count{X: vrs(X), in($x, X), out($y, X)} > 0, #count{Y:vrs(Y), in($x, Y), in($y, Y)} > 0.\n"
                  result += ":- #count{X: vrs(X), in($x, X), out($y, X)} > 0, #count{Y:vrs(Y), in($x, Y), in($y, Y)} = 0, #count{Z: vrs(Z), out($x, Z), in($y, Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                  # TODO
                  result = ""
	    elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                  result += ":- #count{X: vrs(X), in($x,X), out($y, X)} = 0, #count{Y: vrs(Y), out($x,Y), in($y, Y)} = 0, #count{Z: vrs(Z), in($x,Z), in($y, Z)} > 0.\n"
                  result += ":- #count{X: vrs(X), in($x,X), in($y, X)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["gringo"]:
                  result += ":- [vrs(X): in($x,X): out($y, X)]0, [vrs(X): out($x,X): in($y, X)]0, 1[vrs(X): in($x,X): in($y, X)].\n"
                  result += ":- [vrs(X): in($x,X): in($y, X)]0.\n\n"
            elif self.relations == relation["+="]: # lsum
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result += ":- #count{X: vrs(X), out($x,X), in(" + name3 + ",X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), in(" + name3 + ",X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), out($y,X), in(" + name3 + ",X)} = 0, pw.\n" 
		    result += ":- #count{X: vrs(X), in($y,X), in(" + name3 + ",X)} = 0, pw.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    align.basePw += ":- [vrs(X): out($x,X): in(" + name3 + ",X)]0.\n" 
		    align.basePw += ":- [vrs(X): in($x,X): in(" + name3 + ",X)]0.\n" 
		    align.basePw += ":- [vrs(X): out($y,X): in(" + name3 + ",X)]0.\n" 
		    align.basePw += ":- [vrs(X): in($y,X): in(" + name3 + ",X)]0.\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out($x, X), in(" + name3 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out($x, X), in(" + name3 + ", X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in($x, X), in(" + name3 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in($x, X), in(" + name3 + ", X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out($y, X), in(" + name3 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out($y, X), in(" + name3 + ", X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in($y, X), in(" + name3 + ", X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in($y, X), in(" + name3 + ", X), ix.\n\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out(" + name3 + ",X), pw.\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out(" + name3 + ",X), pw.\n" 
		#result += "in(" + name3 + ",X) :- in($x,X).\n" 
		#result += "in(" + name3 + ",X) :- in($y,X).\n" 
		#result += "out($x,X) :- out(" + name3 + ",X).\n" 
		#result += "out($y,X) :- out(" + name3 + ",X).\n" 
		#result += "in($x,X) v in($y,X) :- in(" + name3 + ",X).\n" 
		#result += "out(" +name3 + ",X) :- out($x,X), out($y,X).\n"
            elif self.relations == relation["=-"]: # rdiff
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out($x,X), in($y,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), in($y,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in($y,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in($y,X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- [vrs(X): out($x,X): in($y,X)]0.\n" 
		    result += ":- [vrs(X): in($x,X): in($y,X)]0.\n" 
		    result += ":- [vrs(X): out(" + name3 + ",X): in($y,X)]0.\n" 
		    result += ":- [vrs(X): in(" + name3 + ",X): in($y,X)]0.\n" 
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out($x, X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out($x, X), in($y, X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in($x, X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in($x, X), in($y, X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out(" + name3 + ", X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name3 + ", X), in($y, X), ix.\n\n"
	        result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in(" + name3 + ", X), in($y, X), ix.\n"
	        result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in(" + name3 + ", X), in($y, X), ix.\n\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out($y,X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out($y,X).\n" 
            elif self.relations == relation["+3="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out($x,X), in(" + name4 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), in(" + name4 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out($y,X), in(" + name4 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($y,X), in(" + name4 + ",X)} = 0.\n"
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name4 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name4 + ",X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- [vrs(X): out($x,X): in(" + name4 + ",X)]0.\n" 
		    result += ":- [vrs(X): in($x,X): in(" + name4 + ",X)]0.\n" 
		    result += ":- [vrs(X): out($y,X): in(" + name4 + ",X)]0.\n" 
		    result += ":- [vrs(X): in($y,X): in(" + name4 + ",X)]0.\n"
		    result += ":- [vrs(X): out(" + name3 + ",X): in(" + name4 + ",X)]0.\n" 
		    result += ":- [vrs(X): in(" + name3 + ",X): in(" + name4 + ",X)]0.\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out(" + name4 + ",X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out(" + name4 + ",X).\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name4 + ",X).\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- out(" +name1 + ",X), out($y,X),\
                           out(" + name3 + ",X), in(" + name4 + ",X).\n"
            elif self.relations == relation["+4="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out($x,X), in(" + name5 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($x,X), in(" + name5 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out($y,X), in(" + name5 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($y,X), in(" + name5 + ",X)} = 0.\n"
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in(" + name5 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in(" + name5 + ",X)} = 0.\n"
		    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in(" + name5 + ",X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in(" + name5 + ",X)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
		    result  = ":- [vrs(X): out($x,X): in(" + name5 + ",X)]0.\n" 
		    result += ":- [vrs(X): in($x,X): in(" + name5 + ",X)]0.\n" 
		    result += ":- [vrs(X): out($y,X): in(" + name5 + ",X)]0.\n" 
		    result += ":- [vrs(X): in($y,X): in(" + name5 + ",X)]0.\n"
		    result += ":- [vrs(X): out(" + name3 + ",X): in(" + name5 + ",X)]0.\n" 
		    result += ":- [vrs(X): in(" + name3 + ",X): in(" + name5 + ",X)]0.\n"
		    result += ":- [vrs(X): out(" + name4 + ",X): in(" + name5 + ",X)]0.\n" 
		    result += ":- [vrs(X): in(" + name4 + ",X): in(" + name5 + ",X)]0.\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($x,X), out(" + name5 + ",X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out(" + name5 + ",X).\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name5 + ",X).\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name5 + ",X).\n" 
            elif self.relations == relation["=+"] or self.relations == relation["-="]: # rsum and ldiff
                name3 = self.taxon3.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out($y,X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($y,X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in($x,X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result  = ":- [vrs(X): out($y,X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): in($y,X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): out(" + name3 + ",X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): in(" + name3 + ",X): in($x,X)]0.\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out($x,X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out($x,X).\n"
            elif self.relations == relation["=3+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
		    result  = ":- #count{X: vrs(X), out($y,X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in($y,X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in($x,X)} = 0.\n"
		    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in($x,X)} = 0.\n" 
		    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in($x,X)} = 0.\n" 
                elif reasoner[rnr] == reasoner["gringo"]:
                    result  = ":- [vrs(X): out($y,X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): in($y,X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): out(" + name3 + ",X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): in(" + name3 + ",X): in($x,X)]0.\n"
                    result += ":- [vrs(X): out(" + name4 + ",X): in($x,X)]0.\n"            
                    result += ":- [vrs(X): in(" + name4 + ",X): in($x,X)]0.\n"
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out($x,X).\n" 
		result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out($x,X).\n"
	    	result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out($x,X).\n"
	    elif self.relations == relation["=4+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                if reasoner[rnr] == reasoner["dlv"]:
            	    result  = ":- #count{X: vrs(X), out($y,X), in($x,X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in($y,X), in($x,X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), out(" + name3 + ",X), in($x,X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name3 + ",X), in($x,X)} = 0.\n"
            	    result += ":- #count{X: vrs(X), out(" + name4 + ",X), in($x,X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name4 + ",X), in($x,X)} = 0.\n"
            	    result += ":- #count{X: vrs(X), out(" + name5 + ",X), in($x,X)} = 0.\n" 
            	    result += ":- #count{X: vrs(X), in(" + name5 + ",X), in($x,X)} = 0.\n"
                elif reasoner[rnr] == reasoner["gringo"]:
            	    result  = ":- [vrs(X): out($y,X): in($x,X)]0.\n" 
            	    result += ":- [vrs(X): in($y,X): in($x,X)]0.\n" 
            	    result += ":- [vrs(X): out(" + name3 + ",X): in($x,X)]0.\n" 
            	    result += ":- [vrs(X): in(" + name3 + ",X): in($x,X)]0.\n"
            	    result += ":- [vrs(X): out(" + name4 + ",X): in($x,X)]0.\n" 
            	    result += ":- [vrs(X): in(" + name4 + ",X): in($x,X)]0.\n"
            	    result += ":- [vrs(X): out(" + name5 + ",X): in($x,X)]0.\n" 
            	    result += ":- [vrs(X): in(" + name5 + ",X): in($x,X)]0.\n"
        	result += "ir(X, r" + self.ruleNum.__str__() + ") :- in($y,X), out($x,X).\n" 
        	result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out($x,X).\n"
        	result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out($x,X).\n"
        	result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name5 + ",X), out($x,X).\n" 
		#result += "in($x,X) :- in($y,X).\n" 
		#result += "in($x,X) :- in(" + name3 + ",X).\n" 
		#result += "out($y,X) :- out($x,X).\n" 
		#result += "out(" + name3 + ",X) :- out($x,X).\n" 
		#result += "in($y,X) v in(" + name3 + ",X) :- in($x,X).\n" 
		#result += "out(" +name1 + ",X) :- out($y,X), out(" + name3 + ",X).\n" 
	    else:
		print "Relation ",self.relations," is not yet supported!!!!"
		result = "\n"
        elif encode[enc] & encode["direct"]:
            prefix = "label($x, " + name2 +", "
            result = ""
            firstrel = True
            if self.relations < relation["+="]:
		if self.relations & rcc5["includes"] == rcc5["includes"]:
		    result  = prefix + "in) "
		    firstrel = False
		if self.relations & rcc5["is_included_in"] == rcc5["is_included_in"]:
		    if firstrel:
			result  = prefix + "ls) "
			firstrel = False
		    else:
			result += " v " + prefix + "ls) "
		if self.relations & rcc5["overlaps"] == rcc5["overlaps"]:
		    if firstrel:
			result  = prefix + "ol) "
			firstrel = False
		    else:
			result += " v " + prefix + "ol) "
		if self.relations & rcc5["disjoint"] == rcc5["disjoint"]:
		    if firstrel:
			result  = prefix + "ds) "
			firstrel = False
		    else:
			result += " v " + prefix + "ds) "
		if self.relations & rcc5["equals"] == rcc5["equals"]:
		    if firstrel:
			result  = prefix + "eq) "
			firstrel = False
		    else:
			result += " v " + prefix + "eq) "
                if not firstrel:
                    result += "."
            elif self.relations == relation["+="]:
                result = "sum(" + self.taxon3.dlvName() + ",$x,$y).\n"
            elif self.relations == relation["=+"]:
                result = "sum($x,$y," + self.taxon3.dlvName() + ").\n"
        else:
            raise Exception("Encoding:", enc, " is not supported !!")
	return result


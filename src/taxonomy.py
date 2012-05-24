import re
import copy
from relations import *
from latent_tax_assumption import *
from reasoner import *
from utility import *
import pdb

# this module  defines the classes: Authority, Taxon, Taxonomy

# 
class Authority:
    
    def __init__(self, fullName="", abbrev=""):
        self.fullName = fullName
        self.abbrev = abbrev
    
    def __repr__(self):
        return "Authority: " + self.abbrev + "\n"


class Taxon:
   
    def __init__(self):
        self.parent = ""
        self.children = []
        self.fullName = ""
        self.abbrev = ""
        self.taxonomy = Taxonomy()    
            
    def addChild(self, child):
        self.children += [child]
  
    def hasChildren(self):
        result = False
        if (len(self.children) > 0):
            result = True
        return result


    def stringOf(self):
        return self.taxonomy.authority.abbrev + "_" + self.abbrev
    
    def depthFirstPrint(self):
        
        result = self.abbrev + " "
        
        for child in self.children:
            result += child.depthFirstPrint()
            
        return result
 
    def depthFirstLTax(self):
        #pdb.set_trace()
        result = ""
        for child in self.children:
            result += child.stringOf() + "(x) -> " + self.stringOf() + "(x).\n"
            result += child.depthFirstLTax()
        return result
 
class Taxonomy:

    def __init__(self, initString=""):
        self.authority = Authority()
        if (initString != ""):
            authInfo = re.match("(.*?)\s(.*)", initString)
            self.authority.abbrev = authInfo.group(1)
            if (len(authInfo.groups() > 1)):
                self.authority.fullName = authInfo.group(2)
   
        self.roots = [] 
        self.taxa = {}
        
            
    def isEmpty(self):
        if len(self.taxa.keys) == 0:
            return True
        else:
            return False
        
        
    def hasTaxon(self, theTaxon):
        return (self.taxa.has_key(theTaxon))
    
    def getTaxon(self, theTaxon):
        if (not(self.taxa.has_key(theTaxon))):
            print "no taxon " + theTaxon + " in " + self.authority.abbrev
            return None
        else:
            return (self.taxa[theTaxon]);
            

    def addTaxon(self, parent):
        if self.taxa.has_key(parent):
            return None
        else: 
            thisParent = Taxon()
            thisParent.abbrev = parent
            thisParent.taxonomy = self
            self.taxa[parent] = thisParent
            self.roots.append(thisParent)

    def addDoubleTaxon(self, taxaMap, parent, child):
        thisParent = self.taxa[parent]
        
        if (child != ""):
            if self.taxa.has_key(child):
                thisChild = self.taxa[child]
            else:
                thisChild = Taxon()
                thisChild.abbrev = child
                thisChild.taxonomy = self
                self.taxa[child] = thisChild
            
            thisChild.parent = thisParent
	    taxaMap.addTMir(self.authority.abbrev, parent, child)
	    for sibling in thisParent.children:
	    	taxaMap.addDMir(self.authority.abbrev, child, sibling.stringOf())
            thisParent.addChild(thisChild)

    def addTaxaWithList(self, taxaMap, theList):
        noParens = re.match("\((.*)\)", theList).group(1)
        if (noParens.find(" ") != -1):
            elements = re.split("\s", noParens)
            self.addTaxon(elements[0])
            for index in range (1, len(elements)):
                self.addDoubleTaxon(taxaMap, elements[0], elements[index])
        else:
            self.addTaxon(noParens)    
            
    def toLTax(self):
        result = ""
        for root in self.roots: 
          result += root.depthFirstLTax()
        return result
        
            
    def __repr__(self):
        result = "Taxonomy: " + self.authority.abbrev + "\n"
        for root in self.roots:
          result += root.depthFirstPrint()
        return result + "\n"
      

        
class Articulation:
    
    def __init__(self, initInput="", mapping=None):
        
	self.string = initInput
	self.numTaxon = 2
	self.confidence = 1
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.relations = []
	    return None
	if (initInput.find("confidence=") != -1):
	    elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
	if (initInput.find("sum") != -1 or initInput.find("diff") != -1):
	    if (initInput.find("lsum") != -1):
	        self.relations = [relationDict["+="]]
	        elements = re.match("(.*)_(.*) (.*)_(.*) lsum (.*)_(.*)", initInput)
	    elif (initInput.find("rsum") != -1):
	        self.relations = [relationDict["=+"]]
	        elements = re.match("(.*)_(.*) rsum (.*)_(.*) (.*)_(.*)", initInput)
	    elif (initInput.find("ldiff") != -1):
	        self.relations = [relationDict["-="]]
	        elements = re.match("(.*)_(.*) (.*)_(.*) ldiff (.*)_(.*)", initInput)
	    elif (initInput.find("rdiff") != -1):
	        self.relations = [relationDict["=-"]]
	        elements = re.match("(.*)_(.*) rdiff (.*)_(.*) (.*)_(.*)", initInput)
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
        else:
            ## initInput is of form b48_a equals k04_a
            self.relations = []
            if (initInput.find("{") != -1):
                elements = re.match("(.*)_(.*) {(.*)} (.*)_(.*)", initInput)
            else:
                elements = re.match("(.*)_(.*) (.*) (.*)_(.*)", initInput)
            
            taxon1taxonomy = elements.group(1)
            taxon1taxon = elements.group(2)
            relString = elements.group(3)
            taxon2taxonomy = elements.group(4)
            taxon2taxon = elements.group(5)
          
          
            if (relString.find(" ") != -1):
                if (relationDict.has_key(relString)):
                    self.relations = [relationDict[relString]]
                else:
                    relElements = re.split("\s", relString)
          
                    for rel in relElements:
                        self.relations += [relationDict[rel]]
                  
            else:
                self.relations = [relationDict[relString]]
              
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
            
    def toString(self):
        return self.string

    def toLTax(self):
        result = ""
	if self.relations == [relationDict["+="]] or self.relations == [relationDict["=+"]]:
            result = self.sArticulationSubtitution(self.taxon1, self.taxon2, self.taxon3, self.relations[0])
        elif len(self.relations) == 1:
            result = self.articulationSubtitution(self.taxon1, self.taxon2, self.relations[0])
        else:
            for relation in self.relations:
                result += "(" + self.articulationSubtitution(self.taxon1, self.taxon2, relation)+ ")"
                if (relation != self.relations[-1:][0]):
                    result += " | "
                    
            
        return result
    
    def articulationSubtitution(self, taxon1, taxon2, relation):
        relString = relation.logicSymbol
        relString = relString.replace("$x", taxon1.stringOf())
        relString = relString.replace("$y", taxon2.stringOf())
        return relString
    
    def sArticulationSubtitution(self, taxon1, taxon2, taxon3, relation):
        relString = relation.logicSymbol
        relString = relString.replace("$x", taxon1.stringOf())
        relString = relString.replace("$y", taxon2.stringOf())
        relString = relString.replace("$z", taxon3.stringOf())
        return relString
    
    def __str__(self):
        result = ""
        if len(self.relations) == 1:
            result += self.relations[0].name
        else:
            result += "{"
            for relation in self.relations:
                if relation != self.relations[0]:
                    result += " "
                result += relation.name
            result += "}"
        result += " " + self.taxon1.stringOf()
        result += " " + self.taxon2.stringOf()
	if self.numTaxon == 3:
            result += " " + self.taxon3.stringOf()
        return result
                
    
    def __repr__(self):
        result = "Articulation: " + self.taxon1.stringOf() + " "
        for relation in self.relations:
            result += relation.name + " " 
    
        result += self.taxon2.stringOf() + " \n"
        return result
  
class ArticulationSet:
    
    def __init__(self):
        self.authority = Authority()
        self.articulations = []   
    
    def addArticulationWithList(self, theList, taxonMapping):
        articulation = Articulation(theList, taxonMapping)
        self.articulations += [articulation]
        
    def toLTax(self):
        result = ""
        for articulation in self.articulations:
            result += articulation.toLTax() + ".\n"
            
        return result
        
            
    def __repr__(self):
        result = "Articulation Set: " + self.authority.abbrev + "\n"
        for articulation in self.articulations:
            result += `articulation`
    
        return result
    
class TaxonomyMapping:
    
    #prover = Prover9()
    #mace = Mace4()
    
    
    def __init__(self):
      self.articulationSet = ArticulationSet()
      self.mir = {}
      self.ltas = []
      self.hypothesisType = ""
      self.hypothesis = Articulation()
      self.taxonomies = {}
    
    def __repr__(self):
        result = ""
        for key in self.taxonomies.keys():
            result += `self.taxonomies[key]`
            
        result += `self.articulationSet`    
        return result
    
    def addTMir(self, tName, parent, child):
	self.mir[tName + "_" + parent +"," + tName + "_" + child] = "{includes}"
	self.addIMir(tName + "_" + parent, tName + "_" + child)

    def addDMir(self, tName, child, sibling):
	self.mir[tName + "_" + child +"," + tName + "_" + sibling] ="{disjoint}"
	self.mir[tName + "_" + sibling +"," + tName + "_" + child] ="{disjoint}"

    def addPMir(self, t1, t2, r):
    	if(self.mir.has_key(t1 + "," + t2)):
	    return None
	else:
	    r=r.rstrip()
	    tmpStr=r.replace("{", "")
	    tmpStr=tmpStr.replace("}", "")
	    tmpStr=tmpStr.replace(" ", ",")
	    self.addAMir(t1+" "+tmpStr+" "+t2)

    # articulation
    def addAMir(self, astring):
    	r = astring.split(" ")
	if (r[1] == "includes"):
	    self.addIMir(r[0], r[2])
	elif (r[1] == "is_included_in"):
	    self.addIMir(r[2], r[0])
	elif (r[1] == "equals"):
	    self.addEMir(r[0], r[2])
	elif (r[2] == "lsum"):
	    self.addIMir(r[3], r[0])
	    self.addIMir(r[3], r[1])
	    self.mir[r[0] + "," + r[3]] = "{is_included_in}"
	    self.mir[r[1] + "," + r[3]] = "{is_included_in}"
	    return None
	elif (r[1] == "rsum"):
	    self.addIMir(r[0], r[2])
	    self.addIMir(r[0], r[3])
	    self.mir[r[0] + "," + r[2]] = "{includes}"
	    self.mir[r[0] + "," + r[3]] = "{includes}"
	    return None
	elif (r[2] == "ldiff"):
	    self.addIMir(r[0], r[3])
	    self.mir[r[0] + "," + r[3]] = "{includes}"
	    return None
	elif (r[1] == "rdiff"):
	    self.addIMir(r[3], r[0])
	    self.mir[r[3] + "," + r[0]] = "{is_included_in}"
	    return None
	self.mir[r[0] + "," + r[2]] = "{"+r[1]+"}"
	self.mir[r[0] + "," + r[2]] = "{"+r[1]+"}"

    def removeMir(self, string):
        r = string.split(" ")
	self.mir[r[1] + "," + r[len(r)-1]] = ""
	if len(r) > 3:
	    if r[0] == "+=":
	        self.mir[r[2] + "," + r[3]] = ""
	    elif r[0] == "=+":
	        self.mir[r[1] + "," + r[2]] = ""

    # isa
    def addIMir(self, parent, child):
	for pair in self.mir.keys():
	    if (self.mir[pair] == "{includes}"):
	        if (pair.find("," + parent) != -1):
		    newPair = pair.replace(parent, child)
		    self.mir[newPair] = "{includes}"
	        elif (pair.find(child + ",") != -1):
		    newPair = pair.replace(child, parent)
	    	    self.mir[newPair] = "{includes}"
    # Equality mir
    def addEMir(self, parent, child):
	for pair in self.mir.keys():
	    if (pair.find(parent) != -1):
		newPair = pair.replace(parent, child)
		self.mir[newPair] = self.mir[pair]
	    elif (pair.find(child) != -1):
		newPair = pair.replace(child, parent)
	    	self.mir[newPair] = self.mir[pair]

    def setReasonerTimeout(self, timeout):
        self.prover.setTimeout(timeout)
        self.mace.setTimeout(timeout)
    ## this and the next
    ## method make it obvious
    ## that we need an ltaSet class
    ## which can print itself in various ways
    ##
    def ltaString(self):
        result = ""
        if (len(self.ltas) == 0) :
            result = "No LTAs"
        else:
            for lta in self.ltas:
                result += lta.name + " "
        return result
    
    def ltaAbbrevString(self):
        result = ""
        for lta in self.ltas:
            result += lta.abbrev + "_"
        return result
    
    def getTaxon(self, taxonomyName="", taxonName=""):
        taxonomy = self.taxonomies[taxonomyName]
        taxon = taxonomy.getTaxon(taxonName)
        return taxon
    
    def getAllArticulationPairs(self):
        taxa = []
        theseTaxonomies = self.taxonomies.keys()
        for outerloop in range(len(theseTaxonomies)):
            for innerloop in range(outerloop+1, len(theseTaxonomies)):
                outerTaxa = self.taxonomies[theseTaxonomies[outerloop]].taxa.keys()
                innerTaxa = self.taxonomies[theseTaxonomies[innerloop]].taxa.keys()
                for outerTaxonLoop in range (len(outerTaxa)):
                    for innerTaxonLoop in range (len(innerTaxa)):
                        newTuple = (theseTaxonomies[outerloop] + "_" + outerTaxa[outerTaxonLoop], theseTaxonomies[innerloop] + "_" + innerTaxa[innerTaxonLoop])
                        taxa.append(newTuple)
        return taxa
                        
    def getAllTaxonPairs(self):
        taxa = self.getAllArticulationPairs()
        theseTaxonomies = self.taxonomies.keys()
        for taxonLoop in range(len(theseTaxonomies)):
            thisTaxonomy = self.taxonomies[theseTaxonomies[taxonLoop]];
            theseTaxa = thisTaxonomy.taxa.keys()
            for outerloop in range(len(theseTaxa)):
                for innerloop in range(outerloop+1, len(theseTaxa)):
                    newTuple = (theseTaxonomies[taxonLoop] + "_" + theseTaxa[outerloop], theseTaxonomies[taxonLoop] + "_" + theseTaxa[innerloop])
                    taxa.append(newTuple)
        return taxa
        
    def testConsistencyWithGoal(self,outputDir,compression, memory):    
 
        ltaxRules = ""
        # write out taxonomies
        for taxonomyName in self.taxonomies.keys():
            ltaxRules += self.taxonomies[taxonomyName].toLTax()
            
        
        # write out articulations
        ltaxRules += self.articulationSet.toLTax()

        #write out LTAs
        for lta in self.ltas:
            ltaxRules += lta.toLTax(self)
        
        thisLTaxGoal = self.hypothesis.toLTax()
        
        goalRel = str(self.hypothesis)
        goalRel = goalRel.replace(" ","_")
        goalRel = goalRel.replace("{","")
        goalRel = goalRel.replace("}","")
        thisGoal = goalRel + "_" + self.hypothesisType + "_"
        #thisGoal = str(self.hypothesis).replace(" ", "_") + "_" + self.hypothesisType + "_"
        # write out files for prover9 and mace4
        
        
        # eventually this should be an option - it decides whether
        # or not to test rules which have been given
        #if (ltaxRules.find(thisLTaxGoal) == -1):
        
        if (1 == 1):
            if (memory == False):
                proverOutputFile = outputDir  + self.name + self.ltaAbbrevString() + thisGoal + "Prover.txt"
                self.writeGoalFile(proverOutputFile, ltaxRules, self.prover, True)

                maceOutputFile = outputDir + self.name + self.ltaAbbrevString() + thisGoal + "Mace.txt"
                self.writeGoalFile(maceOutputFile, ltaxRules, self.mace, False)
            else:
                proverOutputFile = self.makeGoalFile(ltaxRules, self.prover, True)
                maceOutputFile = self.makeGoalFile(ltaxRules, self.mace, False)
        
            if (self.hypothesisType == "implied"):
                result = self.testConsistencyWithImpliedGoalNoMace(proverOutputFile, maceOutputFile, memory)
            else:
                result = self.testConsistencyWithPossibleGoal(proverOutputFile, maceOutputFile, memory)

        
            if (ltaxRules.find(thisLTaxGoal) != -1):
                result.append("given");
            else:
                result.append("inferred");

            outputs = result[3] 
            if (compression):
                compressFile(proverOutputFile)
                compressFile(maceOutputFile)
                       
                for outputFile in outputs:
                    compressFile(outputFile)

        else:
            result = ["stated"]
            #print "STATED!" + thisLTaxGoal
            
        return result
    
    def testConsistencyWithImpliedGoalNoMace(self, proverInput, maceInput, memory):

        ## this version does not do mace
        
        reasoners = []
        inputs = []
        outputs = []
        
        timeoutString = ""
        proverOutput = self.prover.run(proverInput, memory)
        reasoners.append(self.prover.name)
        if (memory == False):
            inputs.append(proverInput)
        else:
            inputs.append("memory");
        outputs.append(proverOutput[1])
        
        if (proverOutput[0] == "proved"):
            result = "true"
        else:
            if (proverOutput[0].find("max_sec_no") != -1):
                timeoutString += " prover9 timeout "
            result = "false" + timeoutString
                                                           
        return [result, reasoners, inputs, outputs]
        
    def testConsistencyWithImpliedGoal(self, proverInput, maceInput, memory):
        
        reasoners = []
        inputs = []
        outputs = []
        
        timeoutString = ""
        proverOutput = self.prover.run(proverInput,memory)
        reasoners.append(self.prover.name)
        if (memory == False):
            inputs.append(proverInput)
        else:
            inputs.append("memory");
        outputs.append(proverOutput[1])
        
        if (proverOutput[0] == "proved"):
            result = "true"
            self.prover.makeDot(proverOutput[1])
        else:
            if (proverOutput[0].find("max_sec_no") != -1):
                timeoutString += " prover9 timeout "
                                                           
            maceOutput = self.mace.run(proverInput,memory)
            reasoners.append(self.mace.name)
            if (memory == False):
                inputs.append(proverInput)
            else:
                inputs.append("memory");
            outputs.append(maceOutput[1])
            if (maceOutput[0] == "model found"):
                result = "false" + timeoutString
            else:
                if (maceOutput[0].find("max_sec_no") != -1):
                    timeoutString += " mace4 timeout "
                result = "unclear" + timeoutString
                
        return [result, reasoners, inputs, outputs]
        
    def testConsistencyWithPossibleGoal(self, proverInput, maceInput, memory):
        
        reasoners = []
        inputs = []
        outputs = []
        
        timeoutString = ""
        reasoners.append(self.mace.name)
        if (memory == False):
            inputs.append(maceInput)
        else:
            inputs.append("memory");
        
        maceOutput = self.mace.run(maceInput, False)
        outputs.append(maceOutput[1])
        if (maceOutput[0] == "model found"):
            result = "true"
        else:
            if (maceOutput[0].find("max_sec_no") != -1):
                timeoutString += " mace4 timeout "
            reasoners.append(self.prover.name)
            if (memory == False):
                inputs.append(proverInput)
            else:
                inputs.append("memory");
            proverOutput = self.prover.run(proverInput, False)
            outputs.append(proverOutput[1])
            if (proverOutput[0] == "proved"):
                result = "false" + timeoutString
            else:
                if (proverOutput[0].find("max_sec_no") != -1):
                    timeoutString += " prover9 timeout "
                    result = "unclear" + timeoutString
                else:
                    result = "true" + timeoutString
              
        return [result, reasoners, inputs, outputs]
    
    #results are lists [result, [provers], [inputs], [outputs]]
    def simpleRemedy(self, outputDir):
        s = len(self.articulationSet.articulations)
        for c in range(2):
            for i in range(s):
	        a = self.articulationSet.articulations.pop(i)    
                if(a.confidence != 3-c):
	            self.articulationSet.articulations.insert(i, a)
                    continue
	        self.removeMir(a.__str__())
	        if(self.testConsistency(outputDir)):
		    #print "Remedial measure: remove [" + a.toString() + "]"
		    return True
            return False

    def BCSremedy(self, outputDir):
	testTaxMap = TaxonomyMapping()
	testTaxMap = copy.deepcopy(self)
	testTaxMap.articulationSet.articulations = []
	consArti = self.BCS1(self.articulationSet.articulations, testTaxMap, outputDir)
	print "BCS choose [" + ','.join(map(str,consArti)) + "] as the consistent articulation subset"
	for a in self.articulationSet.articulations:
	    if not (a in consArti):
		print a
		self.removeMir(a.__str__())
	return True

    def divideByTwo(self, articulations):
	s = len(articulations)
	arti1 = []
	arti2 = []
	for i in range(s/2):
	    arti1.append(articulations[i])
	for i in range(s/2, s):
	    arti2.append(articulations[i])
	return [arti1, arti2]

    def BCS(self, articulations, inTaxMap, outputDir):
	testTaxMap = copy.deepcopy(inTaxMap)
	testTaxMap.articulationSet.articulations = testTaxMap.articulationSet.articulations + articulations
	if(testTaxMap.testConsistency(outputDir)):
	    print ','.join(map(str,testTaxMap.articulationSet.articulations)) + " is consistent" 
	    outArti = articulations
	    return outArti
	if(len(articulations) <= 1):
	    return []
	testTaxMap1 = copy.deepcopy(inTaxMap)
	testTaxMap2 = copy.deepcopy(inTaxMap)
	arti = self.divideByTwo(articulations)
	testTaxMap1.articulationSet.articulations += arti[0]
	testTaxMap2.articulationSet.articulations += arti[1]
	flag1 = testTaxMap1.testConsistency(outputDir)
	flag2 = testTaxMap2.testConsistency(outputDir)
	if(flag1 and not flag2):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is consistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is inconsistent" 
	    return arti[0]+self.BCS(arti[1],testTaxMap1, outputDir)
	elif(flag2 and not flag1):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is inconsistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is consistent" 
	    return arti[1]+self.BCS(arti[0],testTaxMap2, outputDir)
	elif(flag1 and flag2):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is consistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is consistent" 
	    arti1 = self.divideByTwo(arti[0])
	    testTaxMap11 = copy.deepcopy(testTaxMap2)
	    testTaxMap12 = copy.deepcopy(testTaxMap2)
	    testTaxMap11.articulationSet.articulations += arti1[0]
	    testTaxMap12.articulationSet.articulations += arti1[1]
	    flag11 = testTaxMap11.testConsistency(outputDir)
	    flag12 = testTaxMap12.testConsistency(outputDir)
            if(not flag11 and not flag12):
		return arti[0]+self.BCS(arti[1], testTaxMap1, outputDir)
            elif(flag11 and not flag12):
		return arti[1]+arti1[0]+self.BCS(arti1[1], testTaxMap11, outputDir)
	    return arti[1]+arti1[1]+self.BCS(arti1[0], testTaxMap12, outputDir)
	else:
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is inconsistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is inconsistent" 
	    return self.BCS(self.BCS(arti[0], inTaxMap, outputDir)+self.BCS(arti[1], inTaxMap, outputDir), inTaxMap, outputDir)
	

    def BCS1(self, articulations, inTaxMap, outputDir):
	testTaxMap = copy.deepcopy(inTaxMap)
	testTaxMap.articulationSet.articulations = testTaxMap.articulationSet.articulations + articulations
	if(testTaxMap.testConsistency(outputDir)):
	    print ','.join(map(str,testTaxMap.articulationSet.articulations)) + " is consistent" 
	    outArti = articulations
	    return outArti
	if(len(articulations) <= 1):
	    return []
	testTaxMap1 = copy.deepcopy(inTaxMap)
	testTaxMap2 = copy.deepcopy(inTaxMap)
	arti = self.divideByTwo(articulations)
	testTaxMap1.articulationSet.articulations += arti[0]
	testTaxMap2.articulationSet.articulations += arti[1]
	flag1 = testTaxMap1.testConsistency(outputDir)
	flag2 = testTaxMap2.testConsistency(outputDir)
	if(flag1 and not flag2):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is consistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is inconsistent" 
	    return self.BCS1(arti[0]+self.BCS1(arti[1],inTaxMap, outputDir), inTaxMap, outputDir)
	elif(flag2 and not flag1):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is inconsistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is consistent" 
	    return self.BCS1(self.BCS1(arti[0],inTaxMap, outputDir)+arti[1], inTaxMap, outputDir)
	elif(flag1 and flag2):
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is consistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is consistent" 
	    return self.BCS1_int(arti[0], arti[1], inTaxMap, outputDir)
	else:
	    print ','.join(map(str,testTaxMap1.articulationSet.articulations)) + " is inconsistent" 
	    print ','.join(map(str,testTaxMap2.articulationSet.articulations)) + " is inconsistent" 
	    return self.BCS1(self.BCS(arti[0], inTaxMap, outputDir)+self.BCS1(arti[1], inTaxMap, outputDir), inTaxMap, outputDir)
	
    def BCS1_int(self, arti1, arti2, inTaxMap, outputDir):
	if(len(arti2) <= 1):
	    return arti1
	arti = self.divideByTwo(arti2)
	testTaxMap1 = copy.deepcopy(inTaxMap)
	testTaxMap2 = copy.deepcopy(inTaxMap)
	testTaxMap1.articulationSet.articulations += arti1+arti[0]
	testTaxMap2.articulationSet.articulations += arti1+arti[1]
	flag1 = testTaxMap1.testConsistency(outputDir)
	flag2 = testTaxMap2.testConsistency(outputDir)
        if(flag1 and flag2):
	    return self.BCS1_int(arti1+arti[0], arti[1], inTaxMap, outputDir)
        elif(flag1 and not flag2):
	    return self.BCS1(arti[0]+self.BCS1(arti1+arti[1], inTaxMap, outputDir), inTaxMap, outputDir)
	return self.BCS1(arti[1]+self.BCS1(arti1+arti[0], inTaxMap, outputDir), inTaxMap, outputDir)

    def testConsistency(self, outputDir):
        
        ltaxRules = ""
	outputFileName = outputDir + self.name + self.ltaAbbrevString() + "tmp.txt"

        # write out taxonomies
        for taxonomyName in self.taxonomies.keys():
            ltaxRules += self.taxonomies[taxonomyName].toLTax()
        
        # write out articulations
        ltaxRules += self.articulationSet.toLTax()

        #write out LTAs
        for lta in self.ltas:
            ltaxRules += lta.toLTax(self)
        
        #print ltaxRules    
        
        output = open(outputFileName, "w")
        output.write(self.prover.formatInputFile(ltaxRules))
        output.close()
        maceOutput = self.mace.run(outputFileName, False)
        
        # if theroem is proved without a goal, then things are 
        # incconsistent
        if (maceOutput[0] == "model found"):
            return True
        else:
            return False
        
    
    def testConsistencyWithoutGoal(self, outputDir):
        
        ltaxRules = ""
        outputFileName = outputDir + self.name + self.ltaAbbrevString() + "noGoal.txt"
        reasoners = []
        inputs = []
        outputs = []

        # write out taxonomies
        for taxonomyName in self.taxonomies.keys():
            ltaxRules += self.taxonomies[taxonomyName].toLTax()
        
        # write out articulations
        ltaxRules += self.articulationSet.toLTax()

        #write out LTAs
        for lta in self.ltas:
            ltaxRules += lta.toLTax(self)
        
        #print ltaxRules    
        
        output = open(outputFileName, "w")
        output.write(self.prover.formatInputFile(ltaxRules))
        output.close()
        maceOutput = self.mace.run(outputFileName, False)
        
        reasoners.append(self.mace.name)
        inputs.append(outputFileName)
        outputs.append(maceOutput[1])
        
        timeoutString = ""
        # if theroem is proved without a goal, then things are 
        # incconsistent
        if (maceOutput[0] == "model found"):
            result = "true"
        else:
            if (maceOutput[0]) == "timeout":
                timeoutString += " mace4 timeout "

            # if theorem is not proved, but there's a model
            # then these axioms are consistent
            reasoners.append(self.prover.name)
            inputs.append(outputFileName)
            proverOutput = self.prover.run(outputFileName, False)
            outputs.append(proverOutput[1])
            if (proverOutput[0] == "proved"):
              result = "false" + timeoutString
            # if the theoem is not proved, but no model is
            # found, then we're not sure what's going on
            else:   
              if (proverOutput[0] == "timeout"):
                  timeoutString += "prover9 timeout "
              result = "unclear" + timeoutString
              
        
        return [result, reasoners, inputs, outputs]
    

    def makeGoalFile(self, ltaxRules, program, flag):
        result = program.formatInputFile(ltaxRules)
        outString = "("
        if(flag):
            outString = "-("
        outString += self.hypothesis.toLTax()
        outString += ").\n"
        result += program.formatGoalFile(outString)
        
        return result   

    def writeGoalFile(self, outputFileName, ltaxRules, program, flag):
        result = self.makeGoalFile(ltaxRules, program, flag)
        outputFileName = cleanOutputFileName(outputFileName)
        output = open(outputFileName, "w")
        output.write(result)
        output.close()
        
    def writeGoalFileOld(self, outputFileName, ltaxRules, program):
        outputFileName = cleanOutputFileName(outputFileName)
        output = open(outputFileName, "w")
        output.write(program.formatInputFile(ltaxRules))
        outString = ""
        outString += self.hypothesis.toLTax()
        outString += ".\n"
            
        output.write(program.formatGoalFile(outString))                          
        output.close()
        
        
    def readFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        for line in lines:

            if (re.match("taxonomy", line)):
                taxName = re.match("taxonomy (.*)", line).group(1) 
                taxonomy = Taxonomy()
                if (taxName.find(" ") == -1):
                    taxonomy.authority.abbrev = taxName
                else:
                    taxParse = re.match("(.*?)\s(.*)", taxName)
                    taxonomy.authority.abbrev = taxParse.group(1)
                    taxonomy.authority.fullName = taxParse.group(2)
                  
                self.taxonomies[taxonomy.authority.abbrev] = taxonomy
              
            # reads in lines of the form (a b c) where a is the parent
            # and b c are the children
            elif (re.match("\(.*\)", line)):
                taxonomy.addTaxaWithList(self, line)

            elif (re.match("articulation", line)):
                
                artName = re.match("articulation (.*)", line).group(1)
                if (artName.find(" ") == -1):
                    self.articulationSet.authority.abbrev = artName
                else:
                    artParse = re.match("(.*?)\s(.*)", artName)
                    self.articulationSet.authority.abbrev = artParse.group(1)
                    self.articulationSet.authority.fullName = artParse.group(2)
              
            elif (re.match("\[.*?\]", line)):
                inside = re.match("\[(.*)\]", line).group(1)
                self.articulationSet.addArticulationWithList(inside, self)
		self.addAMir(inside)
              
            elif (re.match("\<.*\>", line)):
                inside = re.match("\<(.*)\>", line).group(1)
                hypElements = re.split("\s*\?\s*", inside)
                self.hypothesisType = hypElements[0]
                hyp = hypElements[1]
                hypArticulation = Articulation(hyp, self)
                self.hypothesis = hypArticulation
                   
        return True              
              
                   
              
              
        

    

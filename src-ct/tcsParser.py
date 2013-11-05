import sys
import re
import os
from utility import *

DELIM = ":"
nameIdToString = {}
nameStringToId = {}
conceptIdToString = {}
children = {}
parents = {}
conceptStringToId = {}
allNodes = {}
childNodes = {}
articulations = {}
taxonConceptsToDo = {}
taxonConceptsDone = {}
taxonomy = {}



# notes
# this currently only works on two taxonomies
# so neither taxonomy can have an articulation pointing to anything
# other than the other taxonomy

def getTaxon(taxonNameString, authorString):
    result = ""
    nameId = nameStringToId[taxonNameString]
    if (conceptStringToId.has_key(nameId + DELIM + authorString)):
        result = conceptStringToId[nameId + DELIM + authorString]
    return result

def getChildTaxa(taxon):
    result = []
    if(children.has_key(taxon)):
        result = children[taxon].split(":")
    
    return result
    
def notChildInTaxonomy(taxon, taxonomy):
    result = True
    lines = taxonomy.split("\n")
    for line in lines:
        if (line.find(" ") != -1):
            inner = re.match("\((.*?)\)", line).group(1)
            nodes = inner.split(" ")
            if (len(nodes) > 1):
                del(nodes[0])
                if taxon in nodes:
                    result = False
    return result

def removeLeaves(taxonomy):
    result = ""
    lines = taxonomy.split("\n")
    for line in lines:
        if (re.match("\(.*?\)",line)):
            if (line.find(" ") != -1):
                result += line + "\n"
            else:
                # if this has no parent then leave it
                potential = re.match("\((.*?)\)", line).group(1)
                if (notChildInTaxonomy(potential, taxonomy)):
                    result += line + "\n"
        else:
            result += line + "\n"
            
    return result

def printArticulations(articulationString, abbrev, articulator, outputFile):
    articulations = articulationString.split("\n")
    articulations = uniqueList(articulations)
    outputFile.write("articulation ")
    outputFile.write(abbrev + " " + articulator + "\n")
    for art in articulations:
        if (len(art) > 0):
            outputFile.write(art + "\n")
    
def addParents(taxonomy,abbrev):
    result = taxonomy
    theseParents = {}
    for node in allNodes[abbrev]:
        parent = parents[node]
        if (not(parent in allNodes[abbrev])):
            if (parent in theseParents.keys()):
                theseParents[parent] += DELIM + node
            else:
                theseParents[parent] = node
                
    for parent in theseParents.keys():
        parentString = "(" + parent
        children = theseParents[parent].split(DELIM)
        for child in children:
            parentString += " " + child
        parentString += ")"
        result += parentString + "\n"
        
    return result

def printTaxonomy(taxonomy, abbrev, author, outputFile):

    outputFile.write("taxonomy ")
    outputFile.write(abbrev + " " + author)
    #outputFile.write("\n")
    
    #taxonomy = addSuperParent(taxonomy, abbrev)
    #taxonomy = addParents(taxonomy, abbrev)
    taxonomy = removeLeaves(taxonomy)
    taxonomy = fixNodeString(taxonomy)
    outputFile.write(taxonomy)
    outputFile.write("\n")
        
def getTaxonomy(taxon,abbrev):
    
    
    if (taxon in taxonConceptsToDo[abbrev]):
        taxonConceptsToDo[abbrev].remove(taxon)
    
    taxonConceptsDone[abbrev].append(taxon)
    
    #myList = taxonConceptsToDo[abbrev]
    #for taxon in myList:
    #    print taxon
 
    if (not(taxon in allNodes[abbrev])):
        allNodes[abbrev].append(taxon)
        
    result = "\n("
    result += taxon
    children = getChildTaxa(taxon)
    for child in children:
        result += " " + child
        if (not(child in childNodes[abbrev])):
            childNodes[abbrev].append(child)
        if (not(child in allNodes[abbrev])):
            allNodes[abbrev].append(child)
    result += ")"
    for child in children:
        result += getTaxonomy(child, abbrev)
        
    return result

# this finds all nodes which don't have a parent
# and make the abbrev node the parent
def addSuperParent(taxonomy, abbrev):

    orphans = []
    for node in allNodes[abbrev]:
        if ((node in childNodes[abbrev]) == False):
            orphans.append(node)
    
    result = "(" + abbrev
    for orphan in orphans:
        result += " " + orphan
    result += ")\n"
    taxonomy += result   
    
    return taxonomy

def fixNodeString(inputString):
    return inputString.replace('_','')
        


def getPrintType(reltype):
    result = ""
    
    
    if (reltype == "is congruent to"):
        result = "equals"
    elif (reltype == "includes"):
        result="includes"
    elif (reltype == "is included in"):
        result = "is_included_in"
    elif (reltype == "overlaps"):
        result = "overlaps"
    elif (reltype == "is not congruent to"):
        result = "{overlaps includes is_included_in disjoint}"
    elif (reltype == ""):
        result = ""
    else:
        result = "UNKNOWN: " + reltype  
        print "UNKNOWN RELATION!!!!   " + reltype  

    return result

def uniqueList(theList):
    myHash = {}
    for item in theList:
        myHash[item] = 1

    return myHash.keys()
 

def getAllNodes():
    allLists = allNodes.values()
    result = []
    for list in allLists:
        result += list
    
    return uniqueList(result)

def getAuthority(concept):
    conceptString = conceptIdToString[concept]
    info = conceptString.split(DELIM)
    return info[1]

# print articulations between any node in a taxonomy
# and any other node which appears in a taxonomy by
# the other author
# right now it only gets articluations where both nodes are already 
# present in the taxonmies.  Next step is to fix that.
#
def getArticulations(abbrev, author1, abbrev1, author2, abbrev2):   
    result = ""
    artList = articulations.values()

    relevantList = []
    for articulation in artList:
        artInfo = articulation.split(DELIM)
        sourceConcept = artInfo[0]
        relType = artInfo[1]
        targetConcept = artInfo[2]
        
        #if ((sourceConcept in totalNodes) and (targetConcept in totalNodes)):
        if ((sourceConcept in allNodes[abbrev1]) and (getAuthority(targetConcept) == author2) or
             (sourceConcept in allNodes[abbrev2]) and (getAuthority(targetConcept) == author1) or
             (targetConcept in allNodes[abbrev1]) and (getAuthority(sourceConcept) == author2) or
             (targetConcept in allNodes[abbrev2]) and (getAuthority(sourceConcept) == author1)):
            
            if (getAuthority(targetConcept) == author2):
                sourceAbbrev = abbrev1
                targetAbbrev = abbrev2
            else:
                sourceAbbrev = abbrev2
                targetAbbrev = abbrev1
            
            
            if ((not(sourceConcept in taxonConceptsDone[sourceAbbrev])) and
                (not(sourceConcept in taxonConceptsToDo[sourceAbbrev]))):
                taxonConceptsToDo[sourceAbbrev].append(sourceConcept)
                
                        
            if ((not(targetConcept in taxonConceptsDone[targetAbbrev])) and
                (not(targetConcept in taxonConceptsToDo[targetAbbrev]))):
                taxonConceptsToDo[targetAbbrev].append(targetConcept)
                    
            sourceAbbrev="??"
            sourceAuth = getAuthority(sourceConcept)
            if (sourceAuth == author1):
                sourceAbbrev = abbrev1
            elif (sourceAuth == author2):
                sourceAbbrev = abbrev2
            
            targetAbbrev = "??"
            targetAuth = getAuthority(targetConcept)
            if (targetAuth == author1):
                targetAbbrev = abbrev1
            elif (targetAuth == author2):
                targetAbbrev = abbrev2
            
            relevantList.append("[" + sourceAbbrev+ "_" + fixNodeString(sourceConcept) + " " + relType + " " + targetAbbrev + "_" + fixNodeString(targetConcept) + "]")
            
        
    for articulation in relevantList:
        result += articulation + "\n"
        
    return result
        

def singleRun(author1, abbrev1, author2, abbrev2, articulator, artAbbrev, taxonNameString, outputDir):
    print "looking at " + taxonNameString
    outputFileName = abbrev1 + "_" + abbrev2 + "_" + taxonNameString.replace(' ', '_') + ".txt"
    outputFileName = cleanOutputFileName(outputFileName)
    
    taxonId1 = getTaxon(taxonNameString, author1)
    taxonId2 = getTaxon(taxonNameString, author2)
    allNodes[abbrev1] = []
    childNodes[abbrev1] = []
    allNodes[abbrev2] = []
    childNodes[abbrev2] = []
    taxonConceptsDone[abbrev1] = []
    taxonConceptsDone[abbrev2] = []
    taxonConceptsToDo[abbrev1] = []
    taxonConceptsToDo[abbrev2] = []
    
    if taxonId1 != "":
        taxonConceptsToDo[abbrev1] = [taxonId1]
    if taxonId2 != "":    
        taxonConceptsToDo[abbrev2] = [taxonId2]
    taxonomy[abbrev1] = ""
    taxonomy[abbrev2] = ""
    articulationString = ""
    
    while ((len(taxonConceptsToDo[abbrev1]) > 0) or (len(taxonConceptsToDo[abbrev2]) > 0)):
                
        for taxon in taxonConceptsToDo[abbrev1]:
            taxonomy[abbrev1] += getTaxonomy(taxon, abbrev1)
            
        for taxon in taxonConceptsToDo[abbrev2]:
            taxonomy[abbrev2] += getTaxonomy(taxon, abbrev2)
            
        articulationString += getArticulations(artAbbrev, author1, abbrev1, author2, abbrev2)

    if (taxonomy[abbrev1]!= "" and taxonomy[abbrev2] != ""):
        outputFile = open(outputDir + outputFileName, "w")
        printTaxonomy(taxonomy[abbrev1], abbrev1, author1, outputFile)
    
        printTaxonomy(taxonomy[abbrev2], abbrev2, author2, outputFile)
        if articulationString != "":
            printArticulations(articulationString,artAbbrev, articulator, outputFile)    
    
        outputFile.close()
    
def getDictionaries(inputFile): 
    input = open(inputFile, "r")
    lines = input.readlines()
    switch = ""
    child_switch = ""
    
    for line in lines:
        
        if (line.find("<TaxonName id=") != -1):
            switch = "tn"
            name_id = re.match(".*id=\"(.*?)\"", line).group(1)
            
        elif (line.find("</TaxonName>") != -1):
            switch = ""
            nameIdToString[name_id] = this_name
            nameStringToId[this_name] = name_id
            name_id = ""
            this_name = ""
                
        elif ((switch == "tn") and (line.find("<Simple") != -1)):
            this_name = re.match(".*<Simple>(.*)</Simple", line).group(1)
                    
        elif (line.find("<TaxonConcept id=") != -1):
            switch = "tc"
            concept_id = re.match(".*id=\"(.*?)\"", line).group(1)
            
        elif (line.find("</TaxonConcept") != -1):
            switch = ""
            conceptIdToString[concept_id] = name_id + DELIM + according_to
            conceptStringToId[name_id + DELIM + according_to] = concept_id
            parents[concept_id] = parent
            if (children.has_key(parent)):
                children[parent] += ":" + concept_id
            else:
                children[parent] = concept_id
            concept_id = ""
            name_id = ""
            according_to = ""
            parent = ""
            
        elif ((switch == "tc") and (line.find("<Name") != -1)):
            name_id = re.match(".*ref=\"(.*?)\"", line).group(1)
       
        elif ((switch == "tc") and (line.find("<Simple>") != -1)):
            according_to = re.match(".*<Simple>(.*)</Simple>", line).group(1)
        
        elif ((switch == "tc") and (line.find("is child taxon of") != -1)):
            child_switch = "tc"
            
        elif ((switch == "tc") and (child_switch == "tc") and
            (line.find("<ToTaxonConcept") != -1)):
            child_switch = ""
            parent = re.match(".*ref=\"(.*?)\"", line).group(1)
           
        elif (line.find("<TaxonRelationshipAssertion id=") != -1):
            switch = "tra"
            tra_id = re.match(".*id=\"(.*?)\"", line).group(1)
            relType = re.match(".*type=\"(.*?)\"", line).group(1)
            
        elif (line.find("</TaxonRelationshipAssertion") != -1):
            switch = ""
            articulations[tra_id] = sourceId + DELIM + getPrintType(relType) + DELIM + targetId
            sourceId = ""
            targetId = ""
            relType = ""
            authority = ""
            
        elif ((switch == "tra") and (line.find("<FromTaxonConcept") != -1)):
            sourceId = re.match(".*ref=\"(.*?)\"", line).group(1)
            
        elif ((switch == "tra") and (line.find("<ToTaxonConcept") != -1)):
            targetId = re.match(".*ref=\"(.*?)\"", line).group(1)

        elif ((switch == "tra") and (line.find("<Simple>") != -1)):
            authority = re.match(".*<Simple>(.*?)</Simple>", line).group(1)

def parseTCS(inputFile, taxonomies, species, outputDir):
    
    articulator = "R.K. Peet"
    artAbbrev = "p05"

    tliDir = outputDir + "tli/"
    if (not(os.path.exists(tliDir))):
        os.mkdir(tliDir)
        
    getDictionaries(inputFile)
   
    # if no species are given, add all names which have a space (are not a genus or higher taxon)
    # and don't have the word var. in them (and are therefore varieties)
    if len(species) == 0:
        names = nameStringToId.keys()
        for name in names:
            if ((name.find(" ") != -1) and (name.find("var.") == -1)):
                species.append(name)

    for outerloop in range(0, len(taxonomies)):
        nextOne = outerloop+1
        for innerloop in range(nextOne, len(taxonomies)):
            author1, abbrev1 = taxonomies[outerloop]
            author2, abbrev2 = taxonomies[innerloop]
            print author1 + " " + abbrev1 + " " + author2 + " " + abbrev2
            for taxonName in species:
                nameList = taxonName.split(" ")
                #if ((len(nameList) == 2) and (nameList[0] == "Ranunculus")):
                if (len(nameList) == 2):
                    #if (authorKnowsTaxon(author1, taxonName) or authorKnowsTaxon(author2, taxonName)):
                    if (authorKnowsTaxon(author1, taxonName)):
                        singleRun(author1, abbrev1, author2, abbrev2, articulator, artAbbrev, taxonName, tliDir)
   
    return tliDir

def authorKnowsTaxon(author, taxonName):
        taxon = getTaxon(taxonName, author)
        if (taxon != ""):
            return True
        else:
            return False
        
#def parseXML(inputFile, taxonomies, species, outputDir):
#    tliDir = outputDir + "tli/"
#    if (not(os.path.exists(tliDir))):
#        os.mkdir(tliDir)
#    run(inputFile, taxonomies, species, tliDir)
#    return tliDir


from taxonomy import *
from windows import *
from subprocess import Popen
from latent_tax_assumption import *
from tcsParser import *
from utility import *
from graphViz import *
from config import *
from reasoner import *
import threading
import time
import getopt
import sys
import os



# todo
# make the taxmap name a function of the file name
# nicer ltastring (put in ands)

#some nice arguments:
#-x Ranunculus.xml -s "Ranunculus flammula"  -t "[('Kartesz 2004','k04'),('Benson 1948','b48')]"  -w "implied" -n "('k04_buttercup10259','b48_buttercup10261')" -o happy.txt

def newTLIFile(goalType, inputFile, articulations, ltaString, inText, outputDir):
    
    # write new implied values
    artText = inText
    #fileName = inputFile[:-4] + "_" + ltaString + "_" + goalType + ".tli"
    fileName = outputDir + "tli/" + getNameFromFile(inputFile) + "_" + ltaString + "_" + goalType + ".tli"
    
    for articulation in articulations:
        thisArt = str(articulation)
        thisArt = thisArt.replace("[", "*")
        thisArt = thisArt.replace("]", "*")
#        if (thisArt.find("{") == -1):
#            artText += thisArt + "\n"
        artText += thisArt + "\n"
         
    outFile = open(fileName, "w")
    outFile.write(artText)
    outFile.close()
    #makeGraph(fileName)

def runSingleReasoner(outputDir, inputFile, reasonerDir, reasonerTimeout):
    # basically, take a file, run prover9, run mace, return results
    
    reasonerOutputDir = outputDir + "reasonerFiles/"
    if (not(os.path.exists(reasonerOutputDir))):
        os.mkdir(reasonerOutputDir)
    
    prover = Prover9(reasonerDir, reasonerTimeout)    
    mace = Mace4(reasonerDir, reasonerTimeout)
    
    proverOutput = prover.run(inputFile)
    maceOutput = mace.run(inputFile)
    
    fileName = getNameFromFile(inputFile)
    elements = fileName.split("-")
    
    return [fileName, elements[0], elements[1], proverOutput[0], maceOutput[0]]
      
        
def runDirReasoner(outputDir, inputDir):
    
    result = []
    files = os.listdir(inputDir)
    
    for inputFile in files:
        result.append(runSingleReasoner(outputDir, inputDir + "/" + inputFile))
        
    return result   
          

def runSingle(inputFile, ltaSets, goals, goalRelations, goalTypes, outputDir, outputType, outputFile, numberOutputCols, reasonerDir, reasonerTimeout, compression, htmlDir, memory, uncertaintyRed = True, pw = False):

    #ltaClass = LatentTaxAssumption()

    taxMap = TaxonomyMapping()
    taxMap.prover = Prover9(reasonerDir, reasonerTimeout)
    taxMap.mace = Mace4(reasonerDir, reasonerTimeout)
    #taxMap.prover = GQR(reasonerDir, reasonerTimeout)
    
    taxMap.name = getNameFromFile(inputFile)
    taxMap.readFile(inputFile)
      
    result = []

    if (goals == "all_articulations"):
        goals = taxMap.getAllArticulationPairs()
    elif (goals == "all_nodes"):
        goals = taxMap.getAllTaxonPairs()
        
    reasonerOutputDir = outputDir + "reasonerFiles/"
    if (memory == False) and (not(os.path.exists(reasonerOutputDir))):
        os.mkdir(reasonerOutputDir)
    fMir = open(outputDir + taxMap.name + "_mir.csv", 'w')
        
    # for each LTA se
    #ltaSets = ltaClass.powerSet(["NonEmptiness()", "DisjointChildren()", "Coverage()"])

    for ltaSet in ltaSets:
        newImplied = []
        newPossible = []
        ltaString = ""
        for lta in ltaSet:
            if (lta != ltaSet[0]):
                ltaString += "_"    
            ltaString += str(lta)
        if ltaString == "":
            ltaString = "noLTA"
        
        # test the taxonomies, articulations and LTAs for consistency   
        taxMap.ltas = ltaSet
        # first see if the taxonomies and articulations are consistent unde
        # this LTA
        output = taxMap.name + "\t"
        for taxonomy in taxMap.taxonomies.keys():
            output += taxMap.taxonomies[taxonomy].authority.abbrev + "\t"
        output += taxMap.ltaString() 

        if (memory == False):
            impliedFileName = outputDir + "tli/" + taxMap.name + "_" + ltaString + "_implied.tli"
            possibleFileName = outputDir + "tli/" + taxMap.name + "_" + ltaString + "_possible.tli"
        else:
            impliedFileName = ""
            possibleFileName = ""
        
        #results are lists [result, [provers], [inputs], [outputs]]
        consistencyCheck = taxMap.testConsistencyWithoutGoal(reasonerOutputDir)
        consistentWithoutGoal = consistencyCheck[0]
        if ("consistent" in goalTypes):     
  
          provenance = provenanceString(consistencyCheck[1], consistencyCheck[2], consistencyCheck[3])
        
          output += "\tconsistency\t" + "\t" + impliedFileName + "\t" + possibleFileName + "\t" + "\t" + \
            consistentWithoutGoal + "\t" + provenance
          result.append(output)
         
        #if ((isConsistent == True) and (len(goalTypes) != 0))): 
        if ((consistentWithoutGoal != "true") and 
		(taxMap.simpleRemedy(reasonerOutputDir) != True)):
	    print "The input is inconsistent and don't know how to remedy"
	    fMir.close()
	    return None
        elif ("implied" in goalTypes) or ("possible" in goalTypes):
           
            for thisGoal in goals:
		if (taxMap.mir.has_key(thisGoal[0] + "," + thisGoal[1]) and
			taxMap.mir[thisGoal[0] + "," + thisGoal[1]] != ""):
                    taxMap.hypothesis = Articulation(thisGoal[0] + " equals " + thisGoal[1],taxMap)
                    output = taxMap.name 
                    output += "\t" + taxMap.hypothesis.taxon1.taxonomy.authority.abbrev
                    output += "\t" + taxMap.hypothesis.taxon2.taxonomy.authority.abbrev
                    output += "\t" + taxMap.ltaString()         
                    output += "\timplied\tmir"
                    output += "\t" + taxMap.hypothesis.taxon1.abbrev 
                    output += "\t" + taxMap.hypothesis.taxon2.abbrev
		    tmpGoal = taxMap.mir[thisGoal[0] + "," + thisGoal[1]]
                    output += "\t" + tmpGoal
                    output += "\tTRUE\tno input file\tno output file\tno input dir\tno output dir\td\td\td\td"
		    result.append(output)
		    fMir.write(thisGoal[0] + "," + thisGoal[1] + ",mir," + tmpGoal + "\n")
		    continue
                for goalType in goalTypes:
		    tmpGoal = ""
		    threads = []
                    for goalRelation in goalRelations:                 
                        if goalType != "consistent":
                             #print goalType + " " + goalRelation + " " + str(thisGoal)
                             #goal = eval(thisGoal) goal should be an array of tuples
			     t = ThreadProve(taxMap, reasonerOutputDir, thisGoal, goalRelation, goalType, compression, memory)
			     t.start()
			     threads.append(t)
		    sleepT = 0
                    for t in threads:

		        while sleepT < 600:
			    t.join(1)
			    if not t.isAlive():
				break
			    sleepT += 10
			    time.sleep(9)
		        if t.isAlive():
			    t.stop()
			    t.join()
			if t.result == None:
			    consistencyCheck = ["unclear", "", "", "", ""]
		        else:
		    	    consistencyCheck = t.result

		        goalRelation = t.goalRelation
		    
                        goalIsTrue = consistencyCheck[0]
                        source = consistencyCheck[4]
                        
                        output = taxMap.name 
                        output += "\t" + t.taxMap.hypothesis.taxon1.taxonomy.authority.abbrev
                        output += "\t" + t.taxMap.hypothesis.taxon2.taxonomy.authority.abbrev
                        output += "\t" + t.taxMap.ltaString()         
                        output += "\t" + t.goalType + "\t" +  source
                        output += "\t" + t.taxMap.hypothesis.taxon1.abbrev 
                        output += "\t" + t.taxMap.hypothesis.taxon2.abbrev
                        output += "\t" + goalRelation
                          
                        provenance = provenanceString(consistencyCheck[1], consistencyCheck[2], consistencyCheck[3])
                        
			#print goalIsTrue,
                        if (goalIsTrue == "true"):
                            output += "\ttrue\t" + provenance
			    tmpGoal = tmpGoal + goalRelation + " "
                            if (goalType == "implied"):
                                newImplied.append(t.taxMap.hypothesis)
			        taxMap.addPMir(thisGoal[0], thisGoal[1], goalRelation, 1)
                            else:
                                newPossible.append(t.taxMap.hypothesis)
                                
                        elif (goalIsTrue.find("false") != -1):
                            output += "\t" + goalIsTrue + "\t" + provenance
                        elif (goalIsTrue.find("unclear") != -1):
                            output += "\t" + goalIsTrue + "\t" + provenance
                            tmpGoal = "unclear"
                        else:
                            print "erronious goal is true is " + goalIsTrue
                            output += "ERROR!"    
                                
                        result.append(output)

		    if(goalType == "possible"):
                        if(tmpGoal.find("unclear") != -1):
		            fMir.write(thisGoal[0] + "," + thisGoal[1] + ",inferred,unclear\n")
                        else:
			    # Uncertainty Reduction
			    toBeReduced = tmpGoal.rstrip().split(' ')
			    if(uncertaintyRed and len(toBeReduced) != 1):
                                userQuestion = Window(thisGoal, toBeReduced)
			        tmpGoal = userQuestion.main()
			    ###################################
			    taxMap.addPMir(thisGoal[0], thisGoal[1], tmpGoal, 1)
		            fMir.write(thisGoal[0] + "," + thisGoal[1] + ",inferred,{" + tmpGoal.rstrip() + "}\n")
			    
        if (memory == False):
            outputNewTLI(inputFile, ltaSet, newImplied, newPossible, goalTypes, outputDir)

    fMir.close()
    
    # Generating RCG
    # testing purpose
    #taxMap.generateDot(outputDir, taxMap.name, taxMap)

    # Generating all possible worlds
    if pw:
        taxMap.generatePW(outputDir, taxMap.name)

    outputResult(result, outputType, outputFile, numberOutputCols, goalTypes, outputDir, htmlDir)
    
class ThreadProve(threading.Thread):
    def __init__(self, taxMap, outputDir, thisGoal, goalRelation, goalType, compression, memory):
	#threading.Thread.__init__(self)
        super(ThreadProve, self).__init__()
        self._stop = threading.Event()
	self.taxMap = copy.deepcopy(taxMap)
	self.outputDir = outputDir
	self.thisGoal = thisGoal
	self.goalType = goalType
	self.goalRelation = goalRelation
	self.compression = compression
	self.memory = memory
        self.taxMap.hypothesisType = goalType
        self.taxMap.hypothesis = Articulation(thisGoal[0] + " " + goalRelation + " " + thisGoal[1],self.taxMap)
	self.result = None
                        

    def run(self):
	self.result = self.taxMap.testConsistencyWithGoal(self.outputDir,self.compression, self.memory)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


def outputNewTLI(inputFile, ltaSet, implied, possible, goalTypes, outputDir):
    
    ltaString = ""
    for lta in ltaSet:
        if (lta != ltaSet[0]):
            ltaString += "_"    
        ltaString += lta.abbrev
    if ltaString == "":
        ltaString = "noLTA"
        
    inText = ""
    inFile = open(inputFile, "r")
    inTextList = inFile.readlines() 
    for line in inTextList:
        inText += line
    
    for goalType in goalTypes:      
        newTLIFile(goalType, inputFile, implied, ltaString, inText,outputDir)
    
    
    
def provenanceString(provers, inputs, outputs):
    
    result = ""
    for index in range(len(provers)):
        if (index != 0):
            result += "\t"
        result += provers[index] + "\t" + inputs[index] + "\t" + outputs[index]
    return result
    
def runDir(inputLocation, ltaSets, goals, goalRelations, goalTypes, outputDir, outputType, outputFile, numberOutputCols, reasonerDir, reasonerTimeout, compression, htmlDir, memory):
    
    result = []
    print "input location is " + inputLocation
    files = os.listdir(inputLocation)
    
    for inputFile in files:
        if (inputFile[0] != '.'):
        	runSingle(inputLocation + "/" + inputFile, ltaSets, goals, goalRelations, goalTypes, outputDir, outputType, outputFile, numberOutputCols, reasonerDir, reasonerTimeout, compression, htmlDir, memory)
              
  

def usage():
    print """May be called at the command line with the following arguments,
             or, if loaded in the python shell may be called with main() and the
             options as a list of strings (e.g. main(["-i","input.txt"])
             
             Options preceded by an asterisk are not yet implemented
             
             GENERAL OPTIONS
             -r : root directory
             -o : output file - if left out, goes to stdout
             -p : program directory - where the reasoners live
             -m : directory to store intermediate files
             -T : reasoner timeout in seconds
             -z : gzip everything as you go along
             -H : if you'll be looking a the output in a website, put the
                  start of the URL here (e.g. http://localhost/taxalogic/small_test/)
             -M : if provided, do everything in memory, don't write out input and output files  
             
             TLI FILE INPUT OPTIONS
             -i : input single TLI file
             -d : input directory of TLI files
             
             REASONER INPUT OPTIONS
             -D : input directory of reasoner input files
             -I : input single reasoner file
             
             PROGRAM OUTPUT OPTIONS
             -h : html table output
             * -? : latex table output
             -u : uncertainty reduction
             -P : output possible worlds
             
             XML PARSING OPTIONS
             -x : xml file to parse into TLI files
             -s : species in the xml file, either a single species or a csv string
             -t : a list of authority/abbreviation tuples 
                 (e.g. "[('Kartesz 2004','k04'),('Benson 1948','b48')]")
             * -? : directory for the resulting TLI files, if not provided
                 they go into the intermediate files/filename directory
           
             NOTE: One of -i, -d or -x must be specified.  
             
             LTA OPTIONS
             Unless otherwise specified, no LTAs will be applied.
             
             -l : a csv string of ltas to apply, for example: "n,nc,ncd,cd,none" 
                    will run LTA sets [non-empty], [non-empty and coverage], 
                    [non-empty, coverage, and disjoint children], 
                    [coverage and disjoint children], and no LTAs
                    
             -v : a csv list of single lta and run the powerset.  For example
                     "n,c,d" will run the power set 
                     "n,c,d,nc,nd,cd,ncd and none"        
             
             
             GOAL OPTIONS
              -n : nodes to test, 
                  either "all_articulations": compare all pairwise nodes between taxonomies
                  "all_nodes": compare all pairwise nodes including those within each taxonomy
                  otherwise a set of tuples to test "(a,d) (b,e) (c,f)"
              *   or two csv lists, one for T1 and one for T2 "a,b,c d,e,f", 
                  
              -c : relations to test.  This is a csv list, such as:
                  "equals,{overlaps equals},overlaps,is_included_in"
                  
              -a : a powerset of relations given in a csv list     
                
              -w : test types, either "all", or comma delimited string composed of
                     consistent, implied and/or possible 
                     eg "consistent,implied" 
                     if excluded, no goals are tested (only consistency of axioms).
             """



def outputResult(resultSet, outputType, outputFileName, outputCols, goalTypes, outputDir, htmlDir):

    outputFileName = cleanOutputFileName(outputFileName)
    
    if (outputFileName != "console"):
        outFile = open(outputFileName, "a")
        
    outputString = ""
        
    if (outputType == "text"):    
        for result in resultSet:
            #if (outputFileName == "console"):
            #    outputString += result
            #else: 
            outputString += result + "\n"
                
    elif (outputType == "html"):
        webPageTitle = "CleanTAX run " + (resultSet[0].split("\t"))[0]
        outputString = getHTMLHeader(webPageTitle)
        outputString += "<table border=\"1\">\n"
        for result in resultSet:
            outputString += "<tr>"
            elements = result.split("\t")
            consistencyFlag = False
            if (elements[4] == "consistency"):
                consistencyFlag = True
                
            for index in range(outputCols):
                thisElement = elements[index]
                if (consistencyFlag):
                    if (index == 6):
                        if ("implied" in goalTypes):
                            fileName = (elements[index].split(outputDir))[1]
                            impliedGraph = fileName[:-3] + "gif"
                            impliedGraph = impliedGraph.replace("tli","figures")
                            #thisElement = "<a href=\"file:" + fileName + "\">Implied</a> <a href=\"file:" + impliedGraph + "\">figure</a>" 
                            thisElement = "<a href=\""+ htmlDir + "/" + fileName + "\">Implied</a> <a href=\"file:" + impliedGraph + "\">figure</a>" 

                        else:
                            thisElement = ""
                    elif (index == 7):
                        if ("possible" in goalTypes):
                            fileName = (elements[index].split(outputDir))[1]
                            possibleGraph = fileName[:-3] + "gif"
                            possibleGraph = possibleGraph.replace("tli","figures")
                            thisElement = "<a href=\"" + htmlDir + "/" + fileName + "\">Possible</a> <a href=\"file:" + possibleGraph + "\">figure</a>" 
                        else:
                            thisElement = ""
                if (index == 9): 
                    if (thisElement == "true"):
                        if (elements[12].find(outputDir) != -1):
                            fileName = (elements[12].split(outputDir))[1]
                            thisElement = "<a href=\"#\" onClick=\"callDot('" + htmlDir + "/output/" + fileName + ".dot'); return false;\">true</a>" 
                    
                                    
                outputString += "<td>" + thisElement + "</td>"
 
	    if (elements[9] == "TRUE"):
		continue

            for reasonerIndex in range(outputCols, len(elements), 3):
                reasonerName = elements[reasonerIndex]
		reasonerInput = ""
		reasonerOutput = ""
                if ((len(elements) >= reasonerIndex+2) and (elements[reasonerIndex+1].find(outputDir) != -1)): 
                	reasonerInput = (elements[reasonerIndex+1].split(outputDir))[1]
                if ((len(elements) >= reasonerIndex+3) and (elements[reasonerIndex+2].find(outputDir) != -1)): 
                	reasonerOutput = (elements[reasonerIndex+2].split(outputDir))[1]
                outputString += "<td>"
                outputString += "<a href=\"" + htmlDir + "/output/" + reasonerInput + "\">" + reasonerName + " input file</a>"
                outputString += "</td>"
                outputString += "<td>"
                outputString += "<a href=\"" + htmlDir + "/output/"  + reasonerOutput + "\">" + reasonerName + " output file</a>"
                outputString += "</td>"

            outputString += "</tr>\n"
        outputString += "</table></body></html>"
            
                    
    if (outputFileName == "console"):
        print outputString;
    else: 
        outFile.write(outputString)
        outFile.close()
        
def getHTMLHeader(webPageTitle):
    htmlHeader = "<html><head><title>" + webPageTitle + "</title>"
    htmlHeader += """
    <script type="text/javascript">

    function callDot(url) {                     
      document.theForm.theURL = url;
      http_request = false;
      if (window.XMLHttpRequest) { // Mozilla, Safari,...
        http_request = new XMLHttpRequest();
        if (http_request.overrideMimeType) {    
            http_request.overrideMimeType('text/xml');
        }
      } else if (window.ActiveXObject) { // IE
         try {
            http_request = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
           try {
              http_request = new ActiveXObject("Microsoft.XMLHTTP");
           } catch (e) {}
         }
      }
      if (!http_request) {
         alert('Cannot create XMLHTTP instance');
         return false;
      }
      http_request.onreadystatechange = alertContents;
      http_request.open('GET', url, true);
      http_request.send(null);
    }

    function alertContents() {
          if (http_request.readyState == 4) {
             if (http_request.status == 200) {

                var doc = http_request.responseText;
                document.theForm.content.value = doc;
                document.theForm.submit();
                

             } else {
                alert('There was a problem with the request.');
             }
          }
       }
    </script>
    </head>
    <body>
    <form name="theForm" method="POST" action="/cgi-bin/runDot.pl">
    <input type="hidden" name="format" value="pdf">
    <input type="hidden" name="content">
    <input type="hidden" name="theURL">
    </form>
    """

    return htmlHeader
        
def fixDirectories(directory):
    if (directory[:-1] != "/"):
                directory = directory + "/"
    return directory
    
    
def getConfig(opts, config):
    ltas = LatentTaxAssumption()
    
    # set directories first
    for o, a in opts:
        if o == "-r":
            config["inputDir"] = fixDirectories(a)
        elif o == "-m":
            config["outputDir"]= fixDirectories(a)
        elif o == "-H":
            config["htmlDir"] = fixDirectories(a)
        elif o == "-p":
            config["reasonerDir"] = fixDirectories(a)
            
    if (not config.has_key("outputDir") or (config["outputDir"] == "")):
       config["outputDir"] = config["inputDir"] + "output/"
       
    # now the rest
    for o, a in opts:
        if o == "-o":
            config["outputFile"] = a
        elif o == "-i":
            config["inputType"] = "single"
            config["inputLocation"] = config["inputDir"] + a
        elif o == "-d":
            config["inputType"] = "directory"
            config["inputLocation"] = config["inputDir"] + a
        elif o == "-I":
            config["inputType"] = "single_reasoner"
            config["inputLocation"] = config["inputDir"] + a
        elif o == "-D":
            config["inputType"] = "directory_reasoner"
            config["inputLocation"] = config["inputDir"] + a     
        elif o == "-h":
            config["outputType"] = "html"
        elif o == "-M":
            config["memory"] = True
        elif o == "-z":
            config["compression"] = True
        elif o == "-x":
            config["inputType"] = "xml"
            config["inputLocation"] = config["inputDir"] + a
        elif o == "-t":
            config["taxonomies"] = eval(a)
        elif o == "-T":
            config["reasonerTimeout"] = a
        elif o == "-s":
            config["species"] = a.split(",")
        elif o == "-l":
            config["ltaList"] = config["ltas"].getLTAsFromString(a)
        elif o == "-c":
            config["goalRelations"] = a.split(",")
        elif o == "-a":
            config["goalRelations"] = []
            subRelations = a.split(",")
            allRelations = powerSet(subRelations)
            for powerRelation in allRelations:
                if len(powerRelation) > 1:
                    thisRel = "{" + " ".join(powerRelation) + "}"
                    config["goalRelations"].append(thisRel)
                elif len(powerRelation) == 1: 
                    thisRel = powerRelation[0]
                    config["goalRelations"].append(thisRel)
                  
        elif o == "-w":
            if (a == "all"):
                config["goalTypes"] = ["consistent","possible","implied"]
            else:
                config["goalTypes"] = a.split(",")
        elif o == "-n":
            if (a == "all_articulations"):
                config["goals"] = "all_articulations"
            elif (a == "all_nodes"):
                config["goals"] = "all_nodes"
            else:
            # goals now should either be a string like "(a,b) (c,d)" or nothing
            # the result should be a list of tuples
                stringGoals = a.split(" ")
                config["goals"] = []
                for goal in stringGoals:
                    config["goals"].append(eval(goal))   
        elif o == "-v":
            if (a.find(',') == -1):
                config["ltaList"] = config["ltas"].getLTAsFromString(a)
            else:
                myList = []
                theseLTAs = a.split(",")
                for thisLTA in theseLTAs:
                    myList.append(ltas.getLTAFromAbbrev(thisLTA))
                    config["ltaList"] = powerSet(myList)
        elif o == "-u":
	    config["uncertaintyRed"] = True
        elif o == "-P":
	    config["pw"] = True


    if (not(config.has_key("ltaList")) or ((len(config["ltaList"]) == 0))):
        config["ltaList"] = [[]]
            
    if (config["outputFile"] != "console"):
        config["outputFile"] = config["outputDir"] + config["outputFile"]
        
    return config

# main entry
def main(optInfo):

    # set default values
    numberOutputCols = 10  # this is the number of output columns in common to all runs
    ltas = LatentTaxAssumption()


    try:
        opts, args = getopt.getopt(optInfo, "a:c:d:D:H:i:I:l:m:n:o:p:Pr:s:t:T:x:v:w:x:huzM")
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(1)
    
    global config
    config = getConfig(opts, config)  # config is imported from config.py, command line opts override config.py
	        
    if (not(os.path.exists(config["outputDir"]))):
        os.mkdir(config["outputDir"])

    tliDir = config["outputDir"] + "tli/"

    if (not(os.path.exists(tliDir))):
        os.mkdir(tliDir)
                 
    if (config["inputType"] == ""):
        usage()
        #sys.exit(2)
    elif (config["inputType"] == "xml"):               
        parsedTLIs = parseTCS(config["inputLocation"], config["taxonomies"], config["species"], config["outputDir"])
        runDir(parsedTLIs, config["ltaList"], config["goals"], config["goalRelations"], config["goalTypes"], config["outputDir"], config["outputType"], config["outputFile"], numberOutputCols,config["reasonerDir"],config["reasonerTimeout"],config["compression"],config["htmlDir"], config["memory"])
    elif (config["inputType"] == "single"):
        runSingle(config["inputLocation"], config["ltaList"], config["goals"], config["goalRelations"], config["goalTypes"], config["outputDir"], config["outputType"], config["outputFile"], numberOutputCols, config["reasonerDir"], config["reasonerTimeout"], config["compression"], config["htmlDir"], config["memory"], config["uncertaintyRed"], config["pw"])
    elif (config["inputType"] == "directory"):
        runDir(config["inputLocation"], config["ltaList"], config["goals"], config["goalRelations"], config["goalTypes"], config["outputDir"], config["outputType"], config["outputFile"], numberOutputCols,config["reasonerDir"],config["reasonerTimeout"],config["compression"],config["htmlDir"], config["memory"])
    elif (config["inputType"] == "single_reasoner"):
        print runSingleReasoner(config["outputDir"],config["inputLocation"])
    elif (config["inputType"] == "directory_reasoner"):
        result = runDirReasoner(config["outputDir"],config["inputLocation"])
        for item in result:
            print ",".join(item) 
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        optInfo = sys.argv[1:]
        main(optInfo)
    else:
        usage()

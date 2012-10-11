import os
import signal, time
import pdb
from utility import *
#from config import *

class TimedOut(Exception):
    def __init__(self, value = "timed out"):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Reasoner:

    name = ""
    path = ""
    dotter = ""
    xmltrans = ""
    timeout = 0
    
    def __init__(self, reasonerPath, timeout):
        self.timeout = timeout
        if (os.environ.has_key("OS") and ((os.environ["OS"]).index("Windows") != -1)):
          reasonerPath = quoteSpacesInPath(reasonerPath)
        #pdb.set_trace()  
        path = reasonerPath + self.name + " -t " + str(timeout)
        if (self.name == "prover9"):
          path = path + " -f"
        if (self.name == "mace4"):
          path = path + " -N 200 -b 2000 -f"
        self.memoryPath = path
          
       # if (self.name != "gqr"):
       #     self.filePath = path + " -f "
            
        self.xmltrans = reasonerPath + "prooftrans xml -f "
        self.dotter = "python " + reasonerPath + "gvizify.py "
        
        
    def run(self, input, memory):
        if (memory == False):
            result = self.runFile(input)
        else:
            result = self.runMemory(input)
    
        return result
        
    def runMemory(self, inputString):
        
        def handler(signum, frame):
            raise TimedOut()
        # top version linux, bottom version windoze.
        #program = os.popen(self.path + " " + input, "r")
        #program = os.popen(self.path.replace("Documents and Settings", "\"Documents and Settings\"") + " " + input.replace("Documents and Settings", "\"Documents and Settings\""), "r")
        runPath = self.memoryPath
        origInput = inputString
        

   
        #old = signal.signal(signal.SIGALRM, handler)
        #signal.alarm(900)
        result = ""
        outputFileName = ""
        #try:
	if(1 == 1):
            inPipe, outPipe, errDummy = os.popen3(runPath)
            inPipe.write(inputString)
            inPipe.close()
                    
            output = outPipe.read()
            
            result = self.parseOutput(output)
        #except TimedOut:
            #result = self.name + " forced timeout";


        #signal.alarm(0)
        return [result, ""]
            
    def runFile (self,inputFileName):
        
        # top version linux, bottom version windoze.
        #program = os.popen(self.path + " " + input, "r")
        #program = os.popen(self.path.replace("Documents and Settings", "\"Documents and Settings\"") + " " + input.replace("Documents and Settings", "\"Documents and Settings\""), "r")
	#pdb.set_trace()
        runPath = self.memoryPath
        origInput = inputFileName
        
        if (os.environ.has_key("OS") and ((os.environ["OS"]).index("Windows") != -1)):
            inputFileName = quoteSpacesInPath(inputFileName)
   
        #old = signal.signal(signal.SIGALRM, handler)
        #signal.alarm(300)
        result = ""
        outputFileName = ""
        #try:
	if(1 == 1):
            outFile, inFile, errFile = os.popen3(runPath + " " + inputFileName)
        
            output = inFile.read()
            outputFileName = self.saveOutput(origInput, output)
            result = self.parseOutput(output)
        #except TimedOut:
        #    print "timed out homey! " + inputFileName + "\n"
        #    result = self.name + " forced timeout"
            
        #finally:
        #signal.signal(signal.SIGALRM, old)

        #signal.alarm(0)
        return [result, outputFileName]
                

    
    def setTimeout(self, timeout):
        self.timeout = timeout

    def saveOutput(self, inputFileName, output):
        printName = self.name.replace(" ","_")
        outputFileName = inputFileName.replace(".txt", "_" + printName + "_output.txt")
        outputFileName = cleanOutputFileName(outputFileName)
        outputFile = open(outputFileName, "w")
        outputFile.write(output)
        outputFile.close()
        return outputFileName

    
    def makeDot(self, inputFile):
        
        xmlFile = self.makeXML(inputFile)
        outFile, inFile, errFile = os.popen3(self.dotter + " " + xmlFile)
        output = inFile.read()
        dotOutName = inputFile + ".dot"
        dotOutFile = open(dotOutName,"w")
        dotOutFile.write(output)
        dotOutFile.close()
        return dotOutName
    
    def makeXML(self, inputFile):
        
        outFile, inFile, errFile = os.popen3(self.xmltrans + " " + inputFile)
        output = inFile.read()
        xmlOutName = inputFile + ".xml"
        xmlOutFile = open(xmlOutName,"w")
        xmlOutFile.write(output)
        xmlOutFile.close()
        return xmlOutName    

    
class Mace4(Reasoner):
    name = "mace4"
    
    def parseOutput(self, output):
      #print "mace output " + output
      if (output.find("MODEL") != -1):
          return "model found"
      elif (output.find("max_sec_no") != -1):
          return "timeout"
      else:
          return "false"
      
    def formatGoalFile(self, input):
        result = "formulas(assumptions).\n"
        result += input 
        result += "end_of_list.\n"    
        return result
    
    def formatInputFile(self, input):
        result = "formulas(assumptions).\n"
        result += input
        result += "end_of_list.\n\n"    
        return result
      
class Prover9(Reasoner):
    name = "prover9"
    
    
        
    def parseOutput(self, output):
      #print "prover output " + output
      #if (output.find("THEOREM PROVED") == -1):
      if (output.find("PROOF") == -1):
          return "not proved"
      elif (output.find("max_sec_no") != -1):
          return "timeout"
      else:
          return "proved"
      
    def formatGoalFile(self, input):
        result = "formulas(goals).\n"
        result += input 
        result += "end_of_list.\n"    
        return result

    def formatInputFile(self, input):
        result = "formulas(assumptions).\n"
        result += input
        result += "end_of_list.\n\n"    
        return result

class GQR(Reasoner):
    name = "gqr"
    
    def parseOutput(self, output):
      #print "mace output " + output
      if (output.find(": 1") != -1):
          return "model found"
      else:
          return "false"
      
    def formatGoalFile(self, input):
        result = input + "\n"
        result += ".\n"    
        return result
    
    def formatInputFile(self, input):
        result = input + "\n"
        return result

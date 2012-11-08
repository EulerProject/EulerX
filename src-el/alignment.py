import os
import time
import threading
from taxonomy import * 

class TaxonomyMapping:

    def __init__(self, options):
        self.mir = {}                          # MIR
        self.tr = []                           # transitive reduction
        self.eq = []                           # euqlities
        self.taxonomies = {}
        self.articulations = []
        self.map = {}
        self.baseDlv = ""
        self.options = options
        self.name = os.path.splitext(os.path.basename(options.inputfile))[0]
        if options.outputdir is None:
            options.outputdir = options.inputdir
        if not os.path.exists(options.outputdir):
            os.mkdir(options.outputdir)
        self.dlvdir = os.path.join(options.outputdir, "dlv")
        if not os.path.exists(self.dlvdir):
            os.mkdir(self.dlvdir)
        self.pwfile = os.path.join(self.dlvdir, self.name+"_pw.dlv")
        self.mirfile = os.path.join(options.outputdir, self.name+"_mir.txt")

    def addDMir(self, tName, child, sibling):
	self.mir[tName + "." + child +"," + tName + "." + sibling] = rcc5["disjoint"]
	self.mir[tName + "." + sibling +"," + tName + "." + child] = rcc5["disjoint"]

    def getTaxon(self, taxonomyName="", taxonName=""):
        taxonomy = self.taxonomies[taxonomyName]
        taxon = taxonomy.getTaxon(taxonName)
        return taxon

    def getAllArticulationPairs(self):
        taxa = []
        values = self.taxonomies.values()
        for outerloop in range(len(self.taxonomies) - 1):
            for innerloop in range(outerloop+1, len(self.taxonomies)):
                outerTaxa = values[outerloop].taxa.values()
                innerTaxa = values[innerloop].taxa.values()
                for outerTaxonLoop in range (len(outerTaxa)):
                    for innerTaxonLoop in range (len(innerTaxa)):
                        newTuple = (outerTaxa[outerTaxonLoop].dlvName(), innerTaxa[innerTaxonLoop].dlvName())
                        taxa.append(newTuple)
        return taxa

    def getAllTaxonPairs(self):
        taxa = self.getAllArticulationPairs()
        for taxonLoop in range(len(self.taxonomies)):
            thisTaxonomy = self.taxonomies[self.taxonomies[taxonLoop]];
            theseTaxa = thisTaxonomy.taxa
            for outerloop in range(len(theseTaxa)):
                for innerloop in range(outerloop+1, len(theseTaxa)):
                    newTuple = (theseTaxa[outerloop].dlvName(), theseTaxa[innerloop].dlvName())
                    taxa.append(newTuple)
        return taxa

    def run(self):
        self.genDlv()
        if not self.testConsistency():
            print "Input is inconsistent!!"
            return
        self.genPW()
        self.genMir()

    def genMir(self):       
        fmir = open(self.mirfile, 'w')
        for pair in self.getAllArticulationPairs():
            pairkey = pair[0] + "," + pair[1]
            if self.mir.has_key(pairkey) and self.mir[pairkey] != "":
                fmir.write(pairkey + ",opt," + self.mir[pairkey].__str__()+"\n")
            else:
                self.mir[pairkey] = self.getPairMir(pair)
                print self.mir[pairkey]
                rl = [k for k, v in relation.iteritems() if v == self.mir[pairkey]][0]
                fmir.write(pairkey + ",dlv," + rl +"\n")
        fmir.close()
                
    class ThreadProve(threading.Thread):
        def __init__(self, taxMap, pair, rel):
	    threading.Thread.__init__(self)
            self._stop = threading.Event()
	    self.taxMap = taxMap
            self.pair = pair
            self.rel = rel
	    self.result = -1 

        def run(self):
            self.result = self.taxMap.testConsistencyGoal(self.pair, self.rel)

        def stop(self):
            self._stop.set()

        def stopped(self):
            return self._stop.isSet()

    def getPairMir(self, pair):
        result = 0
        threads = []
        for r in rcc5.keys():
            t = self.ThreadProve(self, pair, r)   
            t.start()
            threads.append(t)
        for t in threads:
            sleept = 0
            while sleept < 60:
                t.join(1)
                if not t.isAlive():
                    break
                sleept += 5
                time.sleep(4)
            if t.isAlive():
                t.stop()
                t.join()
            if t.result == -1:
                return 0
            result = result | t.result
        return result
        
    def testConsistencyGoal(self, pair, rel):
        rsnrfile = os.path.join(self.dlvdir, pair[0]+"_"+pair[1]+"_"+rel+".dlv")
        frsnr = open(rsnrfile, "w")
        frsnr.write(self.baseDlv)
        frsnr.write("\n%%% Assumption"+pair[0]+"_"+pair[1]+"_"+rel+"\n")
        if rel == "equals":
            frsnr.write("ir(X) :- out(" + pair[0] + ",X), in(" + pair[1] + ",X).\n")
            frsnr.write("ir(X) :- in(" + pair[0] + ",X), out(" + pair[1] + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
        elif rel == "includes":
            frsnr.write("ir(X) :- out(" + pair[0] + ",X), in(" + pair[1] + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), out(" + pair[1] + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
        elif rel == "is_included_in":
            frsnr.write(":- #count{X: vr(X), out(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
            frsnr.write("ir(X) :- in(" + pair[0] + ",X), out(" + pair[1] + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
        elif rel == "disjoint":
            frsnr.write(":- #count{X: vr(X), out(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), out(" + pair[1] + ",X)} = 0.\n")
            frsnr.write("ir(X) :- in(" + pair[0] + ",X), in(" + pair[1] + ",X).\n")
        elif rel == "overlaps":
            frsnr.write(":- #count{X: vr(X), out(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), out(" + pair[1] + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + pair[0] + ",X), in(" + pair[1] + ",X)} = 0.\n")
        frsnr.close()
        com = "dlv -silent -filter=vr -n=1 "+rsnrfile
        if commands.getoutput(com) == "":
            return 0
        return rcc5[rel]

    def testConsistency(self):
        com = "dlv -silent -filter=vr -n=1 "+self.pwfile
        if commands.getoutput(com) == "{vr(0)}":
            return False
        return True

    def genPW(self):
        com = "dlv -silent -filter=vr "+self.pwfile
        print commands.getoutput(com)

    def genDlv(self):
        if self.baseDlv != "":
            return  None
        self.genDlvConcept()
        self.genDlvPC()
        self.genDlvAr()
        fdlv = open(self.pwfile, 'w')
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
        self.baseDlv += "ir(0).\n"
        self.baseDlv += "vr(X) v ir(X):- r(X).\n"
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
                        self.baseDlv += "ir(X) :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n"
                        self.baseDlv += ":- #count{X: vr(X), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X)} = 0.\n\n"
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
                            self.baseDlv += "ir(X) :- in(" + name1 + ", X), in(" + name2+ ", X).\n"
                            self.baseDlv += ":- #count{X: vr(X), in(" + name1 + ", X), out(" + name2+ ", X)} = 0.\n"
                            self.baseDlv += ":- #count{X: vr(X), out(" + name1 + ", X), in(" + name2+ ", X)} = 0.\n\n"


    def genDlvAr(self):
        self.baseDlv += "%%% Articulations\n"
        for i in range(len(self.articulations)):
            self.baseDlv += "% " + self.articulations[i].string + "\n"
            self.baseDlv += self.articulations[i].toDlv()+ "\n"

        #print self.baseDlv

    def readFile(self):
        file = open(os.path.join(self.options.inputdir, self.options.inputfile), 'r')
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
 

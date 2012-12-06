import os
import time
import threading
import StringIO
from taxonomy import * 
from helper import *

class TaxonomyMapping:

    def __init__(self, options):
        self.mir = {}                          # MIR
        self.tr = []                           # transitive reduction
        self.eq = []                           # euqlities
        self.taxonomies = {}
        self.articulations = []
        self.map = {}
        self.baseDlv = ""
        self.pw = ""
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
        self.mirfile = os.path.join(options.outputdir, self.name+"_mir.csv")

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
                        newTuple = (outerTaxa[outerTaxonLoop], innerTaxa[innerTaxonLoop])
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
        if encode[self.options.encode] & encode["pw"]:
            self.genPW()
        else:
            self.genMir()

    def decodeDlv(self):
        lines = StringIO.StringIO(self.pw).readlines()
        for line in lines:
            vrs = re.split(", " , (re.match("\{(.*)\}", line)).group(1))
            for i in range(len(vrs)):
                num = int(vrs[i].replace("vr(", "").replace(")", ""))
                print num

    class ThreadProve(threading.Thread):
        def __init__(self, taxMap, pair, rel):
            super(TaxonomyMapping.ThreadProve, self).__init__()
	    #threading.Thread.__init__(self)
	    self.taxMap = taxMap
            self.pair = pair
            self.rel = rel
	    self.result = -1 

        def run(self):
            self.result = self.taxMap.testConsistencyGoal(self.pair, self.rel)

## NF starts 
    def testConsistencyGoal(self, pair, rel):
        dn1 = pair[0].dotName()
        dn2 = pair[1].dotName()
        vn1 = pair[0].dlvName()
        vn2 = pair[1].dlvName()
        rsnrfile = os.path.join(self.dlvdir, dn1 +"_"+ dn2 + "_" + rel + ".dlv")
        frsnr = open(rsnrfile, "w")
        frsnr.write("\n%%% Assumption" + vn1 + "_" + vn2 + "_" + rel + "\n")
        if rel == "equals":
            frsnr.write("ir(X) :- out(" + vn1 + ",X), in(" + vn2 + ",X).\n")
            frsnr.write("ir(X) :- in(" + vn1 + ",X), out(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n")
        elif rel == "includes":
            frsnr.write("ir(X) :- out(" + vn1 + ",X), in(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) :- in(" + vn2 + ",X).\n") 
	    frsnr.write("out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n") 
        elif rel == "is_included_in":
            frsnr.write(":- #count{X: vr(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write("ir(X) :- in(" + vn1 + ",X), out(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
        elif rel == "disjoint":
            frsnr.write(":- #count{X: vr(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write("ir(X) :- in(" + vn1 + ",X), in(" + vn2 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n")
        elif rel == "overlaps":
            frsnr.write(":- #count{X: vr(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vr(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
        frsnr.close()
        com = "dlv -silent -filter=rel -n=1 "+rsnrfile+" "+self.pwfile
        if commands.getoutput(com) == "":
            return 0
        return rcc5[rel]
## NF ends

    def testConsistency(self):
        com = "dlv -silent -filter=rel -n=1 "+self.pwfile
        if commands.getoutput(com) == "":
            return False
        return True

    def genPW(self):
        com = "dlv -silent -filter=rel "+self.pwfile+" | muniq -u"
        self.pw = commands.getoutput(com)
        print self.pw

    def genDlv(self):
        if self.baseDlv != "":
            return  None
        self.genDlvConcept()
        self.genDlvPC()
        self.genDlvAr()
        if encode[self.options.encode] & encode["vr"] or encode[self.options.encode] & encode["dl"]:
            self.genDlvDc()
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
                if encode[self.options.encode] & encode["dl"] and t.hasChildren():
                    con += "concept(" + t.dlvName() + "," + self.taxonomies[key].dlvName() + ",i).\n"
                else:
                    self.map[t.dlvName()] = num
                    con += "concept(" + t.dlvName() + "," + self.taxonomies[key].dlvName() + "," + num.__str__()+").\n"
                    num += 1

        if encode[self.options.encode] & encode["dl"]:
            maxint = int(self.options.dl)*num
	    self.baseDlv = "#maxint=" + maxint.__str__() + ".\n\n"
	    self.baseDlv += con
	    self.baseDlv += "%%% regions\n"
	    self.baseDlv += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseDlv += "%%% bit\n"
	    self.baseDlv += "bit(M, V):-r(M),#mod(M," + int(num).__str__() + ",V).\n\n"

	    self.baseDlv += "%%% Meaning of regions\n"
	    self.baseDlv += "in(X, M) :- r(M),concept(X,_,N),bit(M,N).\n"
	    self.baseDlv += "in(X, M) :- r(M),concept(X,_,N),bit(M,N).\n"
	    self.baseDlv += "in(X, M) v out(X, M) :- r(M),concept(X,_,N),bit(M,N1), N<>N1.\n"
	    #self.baseDlv += "gin(X, M) v gout(X, M) :- r(M),concept(X,_,N),not cin(X, M), not cout(X, M).\n"
	    #self.baseDlv += ":- gin(X, M), gout(X, M), r(M), concept(X,_,_).\n\n"
            #self.baseDlv += "in(X, M) :- cin(X, M).\n"
            #self.baseDlv += "in(X, M) :- gin(X, M).\n"
            #self.baseDlv += "out(X, M) :- cout(X, M).\n"
            #self.baseDlv += "out(X, M) :- gout(X, M).\n"
	    self.baseDlv += "ir(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n\n"

	    self.baseDlv += "%%% Constraints of regions.\n"
	    self.baseDlv += "vr(X) :- r(X), not ir(X).\n"
	    self.baseDlv += ":- vr(X), ir(X).\n\n"

        elif encode[self.options.encode] & encode["vr"]:
	    self.baseDlv = "#maxint=" + int(2**num).__str__() + ".\n\n"
	    self.baseDlv += con
	    self.baseDlv += "\n%%% power\n"
	    self.baseDlv += "p(0,1).\n"
	    self.baseDlv += "p(N,M) :- #int(N),N>0,#succ(N1,N),p(N1,M1),M=M1*2.\n\n"

	    self.baseDlv += "%%% regions\n"
	    self.baseDlv += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseDlv += "%%% count of concepts\n"
	    self.baseDlv += "count(N):- #int(N),N>=0,N<#count{Y:concept(Y,_,_)}.\n\n"

	    self.baseDlv += "%%% bit\n"
	    self.baseDlv += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
	    self.baseDlv += "bit(M, N, 1):-r(M),count(N),not bit(M,N,0).\n\n"

	    self.baseDlv += "%%% Meaning of regions\n"
	    self.baseDlv += "in(X, M) v out(X, M) :- r(M),concept(X,_,N),count(N).\n"
	    self.baseDlv += "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"
	    self.baseDlv += "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"
	    self.baseDlv += "ir(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"

	    self.baseDlv += "%%% Constraints of regions.\n"
	    self.baseDlv += "ir(0).\n"
	    self.baseDlv += "vr(X) v ir(X):- r(X).\n"
	    self.baseDlv += ":- vr(X), ir(X).\n\n"

        elif encode[self.options.encode] & encode["direct"]:
            self.baseDlv += con
            self.baseDlv += "\n% GENERATE possible labels\n"
	    self.baseDlv += "node(X) :- concept(X, _, _).\n"
            self.baseDlv += "rel(X, Y, R) :- label(X, Y, R), X < Y.\n"
	    self.baseDlv += "label(X, X, eq) :- node(X).\n"

	    self.baseDlv += "label(X,Y,eq) v label(X,Y,ds) v label(X,Y,in) v label(X,Y,ls) v label(X,Y,ol) :-\n"
	    self.baseDlv += "	    node(X),node(Y), X <> Y.\n\n"

            self.baseDlv += "% Make sure they are pairwise disjoint\n"
            self.baseDlv += ":- label(X,Y,eq), label(X,Y,ds).\n"
            self.baseDlv += ":- label(X,Y,eq), label(X,Y,in).\n"
            self.baseDlv += ":- label(X,Y,eq), label(X,Y,ls).\n"
            self.baseDlv += ":- label(X,Y,eq), label(X,Y,ol).\n"

            self.baseDlv += ":- label(X,Y,ds), label(X,Y,in).\n"
            self.baseDlv += ":- label(X,Y,ds), label(X,Y,ls).\n"
            self.baseDlv += ":- label(X,Y,ds), label(X,Y,ol).\n"

	    self.baseDlv += ":- label(X,Y,in), label(X,Y,ls).\n"
	    self.baseDlv += ":- label(X,Y,in), label(X,Y,ol).\n"
	    self.baseDlv += ":- label(X,Y,ls), label(X,Y,ol).\n"

            self.baseDlv += "% integrity constraint for weak composition\n"
            self.baseDlv += "label(X, Y, in) :- label(Y, X, ls).\n"
            self.baseDlv += "label(X, Y, ls) :- label(Y, X, in).\n"
            self.baseDlv += "label(X, Y, ol) :- label(Y, X, ol).\n"
            self.baseDlv += "label(X, Y, ds) :- label(Y, X, ds).\n"
            self.baseDlv += "sum(X, Y, Z) :- sum(X, Z, Y).\n"
            self.baseDlv += "label(X, Y, in) :- sum(X, Y, _).\n"

	    self.baseDlv += "label(X,Z,eq) :- label(X,Y,eq), label(Y,Z,eq).\n"
	    self.baseDlv += "label(X,Z,in) :- label(X,Y,eq), label(Y,Z,in).\n"
	    self.baseDlv += "label(X,Z,ls) :- label(X,Y,eq), label(Y,Z,ls).\n"
	    self.baseDlv += "label(X,Z,ol) :- label(X,Y,eq), label(Y,Z,ol).\n"
	    self.baseDlv += "label(X,Z,ds) :- label(X,Y,eq), label(Y,Z,ds).\n"

	    self.baseDlv += "label(X,Z,in) :- label(X,Y,in), label(Y,Z,eq).\n"
	    self.baseDlv += "label(X,Z,in) :- label(X,Y,in), label(Y,Z,in).\n"
	    self.baseDlv += "label(X,Z,eq) v label(X,Z,in) v label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,in), label(Y,Z,ls).\n"
	    self.baseDlv += "label(X,Z,in) v label(X,Z,ol) :- label(X,Y,in), label(Y,Z,ol).\n"
	    self.baseDlv += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,in), label(Y,Z,ds).\n"

	    self.baseDlv += "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,eq).\n"
	    self.baseDlv += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseDlv += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,ol) :- label(X,Y,ls), label(Y,Z,in).\n"
	    self.baseDlv += "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,ls).\n"
	    self.baseDlv += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ol).\n"
	    self.baseDlv += "label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ds).\n"

	    self.baseDlv += "label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,eq).\n"
	    self.baseDlv += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,in).\n"
	    self.baseDlv += "label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,ol), label(Y,Z,ls).\n"
	    self.baseDlv += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseDlv += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,ol).\n"
	    self.baseDlv += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,ds).\n"

	    self.baseDlv += "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,eq).\n"
	    self.baseDlv += "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,in).\n"
	    self.baseDlv += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ls).\n"
	    self.baseDlv += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ol).\n"
	    self.baseDlv += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseDlv += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ds), label(Y,Z,ds).\n\n"

            self.baseDlv += "label(X, Y, ds) :- sum(X, X1, X2), label(X1, Y, ds), label(X2, Y, ds).\n"
            self.baseDlv += "sum(X, Y, X2) :- sum(X, X1, X2), label(X1, Y, eq).\n"
            self.baseDlv += "sum(Y, X1, X2) :- sum(X, X1, X2), label(X, Y, eq).\n"
            # A + (B + C) = (A + B) + C
            self.baseDlv += "label(X, Y, eq) :- sum(X, A, X1), sum(X1, B, C), sum(Y, B, Y1), sum(Y1, A, C).\n"
            self.baseDlv += "label(X, Y, ol) v label(X, Y, in) :- sum(X, X1, X2), label(X1, Y, ol), label(X2, Y, ol).\n"
            self.baseDlv += "label(X, Y, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X2, Y2, R).\n"
            self.baseDlv += "label(X2, Y2, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X, Y, R).\n"
            self.baseDlv += "label(X, Y, in) v label(X, Y, eq) :- sum(Y, Y1, Y2), label(X, Y1, in), label(X, Y2, in).\n"

        else:
            print "EXCEPTION: encode ",self.options.encode," not defined!!"

    def genDlvPC(self):
        self.baseDlv += "%%% PC relations\n"
        for key in self.taxonomies.keys():
            queue = copy.deepcopy(self.taxonomies[key].roots)
            while len(queue) != 0:
                t = queue.pop(0)
                if t.hasChildren():
                    if encode[self.options.encode] & encode["vr"] or encode[self.options.encode] & encode["dl"]:
			# ISA
			self.baseDlv += "%% ISA\n"
			coverage = "ir(X) :- in(" + t.dlvName() + ", X)"
			coverin = ""
			coverout = "out(" + t.dlvName() + ", X) :- "
			for t1 in t.children:
			    self.baseDlv += "% " + t1.dlvName() + " isa " + t.dlvName() + "\n"
			    self.baseDlv += "in(" + t.dlvName() + ", X) :- in(" + t1.dlvName() + ", X).\n"
			    self.baseDlv += "out(" + t1.dlvName() + ", X) :- out(" + t.dlvName() + ", X).\n"
			    self.baseDlv += "in(" + t1.dlvName() + ", X) v out(" + t1.dlvName() + ", X) :- in(" + t.dlvName() + ", X).\n"
			    self.baseDlv += "in(" + t.dlvName() + ", X) v out(" + t.dlvName() + ", X) :- out(" + t1.dlvName() + ", X).\n"
			    self.baseDlv += "ir(X) :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n"
			    self.baseDlv += ":- #count{X: vr(X), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X)} = 0.\n\n"
			    coverage += ",out(" + t1.dlvName() + ", X)"
                            if coverin != "":
                                coverin += " v "
                                coverout += ", "
                            coverin += "in(" + t1.dlvName() + ", X)"
                            coverout += "out(" + t1.dlvName() + ", X)"
			# C
			self.baseDlv += "%% coverage\n"
			self.baseDlv += coverin + " :- in(" + t.dlvName() + ", X).\n"
			self.baseDlv += coverout + ".\n"
			self.baseDlv += coverage + ".\n\n"
			# D
			self.baseDlv += "%% sibling disjointness\n"
			for i in range(len(t.children) - 1):
			    for j in range(i+1, len(t.children)):
				name1 = t.children[i].dlvName()
				name2 = t.children[j].dlvName()
				self.baseDlv += "% " + name1 + " ! " + name2+ "\n"
				self.baseDlv += "out(" + name1 + ", X) :- in(" + name2+ ", X).\n"
				self.baseDlv += "out(" + name2 + ", X) :- in(" + name1+ ", X).\n"
			        self.baseDlv += "in(" + name1 + ", X) v out(" + name1 + ", X) :- out(" + name2 + ", X).\n"
			        self.baseDlv += "in(" + name2 + ", X) v out(" + name2 + ", X) :- out(" + name1 + ", X).\n"
				self.baseDlv += "ir(X) :- in(" + name1 + ", X), in(" + name2+ ", X).\n"
				self.baseDlv += ":- #count{X: vr(X), in(" + name1 + ", X), out(" + name2+ ", X)} = 0.\n"
				self.baseDlv += ":- #count{X: vr(X), out(" + name1 + ", X), in(" + name2+ ", X)} = 0.\n\n"
                    elif encode[self.options.encode] & encode["direct"]:
			# ISA
			# C
			self.baseDlv += "\n%% ISA\n"
                        
			coverage = "ir(X) :- in(" + t.dlvName() + ", X)"
                        numkids = len(t.children)
                        if numkids == 1:
                            self.baseDlv += "label(" + t.dlvName() + "," + t.children[0] + ", eq).\n"
                        elif numkids > 1:
                            prefix ="label(" + t.dlvName() + ", "
                            pre = t.dlvName()
                            coverage = ""
			    for t1 in range(numkids - 2):
                                t1name = t.children[t1].dlvName()
				self.baseDlv += "% " + t1name + " isa " + t.dlvName() + "\n"
                                self.baseDlv += prefix + t1name + ", eq) v "
                                self.baseDlv += prefix + t1name + ", in).\n"
                                nex = t.dlvName() + t1.__str__()
				coverage += "sum(" + pre + "," + t1name + "," + nex + ").\n"
                                pre = nex
		            self.baseDlv += "% " + t.children[numkids - 2].dlvName() + " isa " + t.dlvName() + "\n"
                            self.baseDlv += prefix + t.children[numkids - 2].dlvName() + ", eq) v "
                            self.baseDlv += prefix + t.children[numkids - 2].dlvName() + ", in).\n\n"
		            self.baseDlv += "% " + t.children[numkids - 1].dlvName() + " isa " + t.dlvName() + "\n"
                            self.baseDlv += prefix + t.children[numkids - 1].dlvName() + ", eq) v "
                            self.baseDlv += prefix + t.children[numkids - 1].dlvName() + ", in).\n\n"
		            coverage += "sum(" + pre + "," + t.children[numkids - 2].dlvName() + "," + t.children[numkids - 1].dlvName() + ").\n"
                            
			    self.baseDlv += "\n%% coverage\n"
			    self.baseDlv += coverage + "\n\n"
			# D
			self.baseDlv += "%% sibling disjointness\n"
			for i in range(len(t.children) - 1):
			    for j in range(i+1, len(t.children)):
				name1 = t.children[i].dlvName()
				name2 = t.children[j].dlvName()
				self.baseDlv += "% " + name1 + " ! " + name2+ "\n"
				self.baseDlv += "label(" + name1 + ", " + name2+ ", ds).\n"


    def genDlvAr(self):
        self.baseDlv += "\n%%% Articulations\n"
        for i in range(len(self.articulations)):
            self.baseDlv += "% " + self.articulations[i].string + "\n"
            self.baseDlv += self.articulations[i].toDlv(self.options.encode)+ "\n"

    def genDlvDc(self):
        self.baseDlv += "%%% Decoding now\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"<\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \">\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"><\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"!\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \">\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \"><\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \"!\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \">\"), rel(X, Y, \"><\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \">\"), rel(X, Y, \"!\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- rel(X, Y, \"><\"), rel(X, Y, \"!\"), concept(X, N1, _), concept(Y, N2, _).\n"
        self.baseDlv += ":- not rel(X, Y, \"=\"), not rel(X, Y, \"<\"), not rel(X, Y, \">\"), not rel(X, Y, \"><\"), not rel(X, Y, \"!\"), concept(X, N1, _), concept(Y, N2, _), N1 < N2.\n\n"

        self.baseDlv += "hint(X, Y, 0) :- concept(X, N1, _), concept(Y, N2, _), N1 < N2, vr(R), in(X, R), out(Y, R).\n"
        self.baseDlv += "hint(X, Y, 1) :- concept(X, N1, _), concept(Y, N2, _), N1 < N2, vr(R), in(X, R), in(Y, R).\n"
        self.baseDlv += "hint(X, Y, 2) :- concept(X, N1, _), concept(Y, N2, _), N1 < N2, vr(R), out(X, R), in(Y, R).\n\n"

        self.baseDlv += "rel(X, Y, \"=\") :- not hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2).\n"
        self.baseDlv += "rel(X, Y, \"<\") :- not hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2).\n"
        self.baseDlv += "rel(X, Y, \">\") :- hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2).\n"
        self.baseDlv += "rel(X, Y, \"><\") :- hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2).\n"
        self.baseDlv += "rel(X, Y, \"!\") :- hint(X, Y, 0), not hint(X, Y, 1), hint(X, Y, 2).\n"

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
                self.articulations += [Articulation(inside, self)]
		if inside.find("{") != -1:
		    r = re.match("(.*) \{(.*)\} (.*)", inside)
		    self.addPMir(r.group(1), r.group(3), r.group(2).replace(" ",","), 0)
		else:
		    self.addAMir(inside, 0)
              
           # elif (re.match("\<.*\>", line)):
            #    inside = re.match("\<(.*)\>", line).group(1)
             #   hypElements = re.split("\s*\?\s*", inside)
              #  self.hypothesisType = hypElements[0]
               # hyp = hypElements[1]
               # hypArticulation = Articulation(hyp, self)
               # self.hypothesis = hypArticulation
                   
        return True              
 
    def addTMir(self, tName, parent, child):
	self.mir[tName + "." +parent +"," + tName + "." + child] = rcc5["includes"]
	self.tr.append([tName + "." + child, tName + "." + parent, 0])
	self.addIMir(tName + "." + parent, tName + "." + child, 0)

    def addAMir(self, astring, provenance):
    	r = astring.split(" ")
        if(self.options.verbose):
            print "Articulations: ",astring
	if (r[1] == "includes"):
	    self.addIMir(r[0], r[2], provenance)
	    self.tr.append([r[2], r[0], provenance])
	elif (r[1] == "is_included_in"):
	    self.addIMir(r[2], r[0], provenance)
	    self.tr.append([r[0], r[2], provenance])
	elif (r[1] == "equals"):
	    self.addEMir(r[0], r[2])
            self.eq.append([r[0], r[2]])
	elif (r[2] == "lsum"):
	    self.addIMir(r[3], r[0], provenance)
	    self.addIMir(r[3], r[1], provenance)
	    self.mir[r[0] + "," + r[3]] = rcc5["is_included_in"]
	    self.mir[r[1] + "," + r[3]] = rcc5["is_included_in"]
	    self.tr.append([r[0],r[3], provenance])
	    self.tr.append([r[1],r[3], provenance])
	    return None
	elif (r[1] == "rsum"):
	    self.addIMir(r[0], r[2], provenance)
	    self.addIMir(r[0], r[3], provenance)
	    self.mir[r[0] + "," + r[2]] = rcc5["includes"]
	    self.mir[r[0] + "," + r[3]] = rcc5["includes"]
	    self.tr.append([r[2], r[0], provenance])
	    self.tr.append([r[3], r[0], provenance])
	    return None
	elif (r[2] == "ldiff"):
	    self.addIMir(r[0], r[3], provenance)
	    self.mir[r[0] + "," + r[3]] = rcc5["includes"]
	    self.tr.append([r[3], r[0], provenance])
	    return None
	elif (r[1] == "rdiff"):
	    self.addIMir(r[3], r[0], provenance)
	    self.mir[r[3] + "," + r[0]] = rcc5["is_included_in"]
	    self.tr.append([r[3], r[0], provenance])
	    return None
        if rcc5.has_key(r[1]):
	    self.mir[r[0] + "," + r[2]] = rcc5[r[1]]
 
    def addDMir(self, tName, child, sibling):
	self.mir[tName + "." + child + "," + tName + "." + sibling] = rcc5["disjoint"]
	self.mir[tName + "." + sibling + "," + tName + "." + child] = rcc5["disjoint"]

    def addPMir(self, t1, t2, r, provenance):
    	if(self.mir.has_key(t1 + "," + t2)):
	    return None
	else:
	    r=r.rstrip()
	    #print t1+" "+r+" "+t2
	    #self.articulationSet.addArticulationWithList(t1+" "+r+" "+t2, self)
	    tmpStr=r.replace("{", "")
	    tmpStr=tmpStr.replace("}", "")
	    tmpStr=tmpStr.replace(" ", ",")
	    self.addAMir(t1+" "+tmpStr+" "+t2, provenance)


    # Equality mir
    def addEMir(self, parent, child):
	for pair in self.mir.keys():
	    if (pair.find(parent+",") == 0):
		newPair = pair.replace(parent+",", child+",")
		self.mir[newPair] = self.mir[pair]
	    elif (pair.find(child+",") == 0):
		newPair = pair.replace(child+",", parent+",")
	    	self.mir[newPair] = self.mir[pair]
	    elif (pair.find(","+parent) == len(pair)-len(parent)-1):
		newPair = pair.replace(","+parent, ","+child)
		self.mir[newPair] = self.mir[pair]
	    elif (pair.find(","+child) == len(pair)-len(child)-1):
		newPair = pair.replace(","+child, ","+parent)
	    	self.mir[newPair] = self.mir[pair]

 
    # isa
    def addIMir(self, parent, child, provenance):
	for pair in self.mir.keys():
	    if (self.mir[pair] == rcc5["includes"]):
	        if (pair.find("," + parent) == len(pair) - len(parent) - 1):
		    newPair = pair.replace("," + parent, "," + child)
		    self.mir[newPair] = rcc5["includes"]
		elif (pair.find(child + ",") == 0):
		    newPair = pair.replace(child + ",", parent + ",")
	    	    self.mir[newPair] = rcc5["includes"]
    def genMir(self):       
        fmir = open(self.mirfile, 'w')
        for pair in self.getAllArticulationPairs():
            pairkey = pair[0].dotName() + "," + pair[1].dotName()
            if self.options.verbose:
		print pairkey
            if self.mir.has_key(pairkey) and self.mir[pairkey] != 0:
                fmir.write(pairkey+",opt," + findkey(relation, self.mir[pairkey])+"\n")
                if self.options.verbose:
                    print pairkey+",opt," + findkey(relation, self.mir[pairkey])+"\n"
            else:
                self.mir[pairkey] = self.getPairMir(pair)
                rl = findkey(relation, self.mir[pairkey])
                fmir.write(pairkey + ",dlv," + rl +"\n")
                if self.options.verbose:
                    print pairkey + ",dlv," + rl +"\n"
        fmir.close()
 
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
                if self.options.verbose:
                    print "Sleept ",sleept," seconds!"
            if t.isAlive():
                t.join(1)
                continue
            if t.result == -1:
                return 0
            result = result | t.result
        return result
                
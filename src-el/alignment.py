import os
import time
import sets
import inspect
import threading
import StringIO
from taxonomy import * 
from alignment import * 
from redWind import *
from template import *
from helper import *

class TaxonomyMapping:

    # Constructor
    def __init__(self, options):
        self.mir = {}                          # MIR
        self.mirc = {}                         # MIRC
        self.mirp = {}                         # MIR Provenance
        self.obs = []                          # OBS
        self.obslen = 0                        # OBS time / location?
        self.location = []                     # location set
        self.temporal = []                     # temporal set
        self.exploc = False                    # exploring location info
        self.exptmp = False                    # exploring temporal info
        self.tr = []                           # transitive reduction, ie, < relation
        self.eq = []                           # euqlities
        self.rules = {}
        self.taxonomies = {}                   # set of taxonomies
        self.articulations = []                # set of articulations
        self.map = {}                          # mapping between the concept name and its numbering
        self.baseAsp = ""                      # tmp string for the ASP input file
        self.baseCb = ""                       # tmp string for the combined concept ASP input file
        self.pw = ""
        self.npw = 0                           # # of pws
        self.options = options
        self.enc = encode[options.encode]      # encoding
        self.name = os.path.splitext(os.path.basename(options.inputfile))[0]
        if options.outputdir is None:
            options.outputdir = options.inputdir
        if not os.path.exists(options.outputdir):
            os.mkdir(options.outputdir)
        self.aspdir = os.path.join(options.outputdir, "asp")
        if not os.path.exists(self.aspdir):
            os.mkdir(self.aspdir)
        self.pwfile = os.path.join(self.aspdir, self.name+"_pw.asp")
        self.cbfile = os.path.join(self.aspdir, self.name+"_cb.asp")
        self.pwswitch = os.path.join(self.aspdir, "pw.asp")
        self.ixswitch = os.path.join(self.aspdir, "ix.asp")
        self.pwout = os.path.join(options.outputdir, self.name+"_pw.txt")
        self.cbout = os.path.join(options.outputdir, self.name+"_cb.txt")
        self.obout = os.path.join(options.outputdir, self.name+"_ob.txt")
        self.mirfile = os.path.join(options.outputdir, self.name+"_mir.csv")
        self.clfile = os.path.join(options.outputdir, self.name+"_cl.csv")
        self.cldot = os.path.join(options.outputdir, self.name+"_cl.dot")
        self.cldotpdf = os.path.join(options.outputdir, self.name+"_cl_dot.pdf")
        self.clneatopdf = os.path.join(options.outputdir, self.name+"_cl_neato.pdf")
        self.iefile = os.path.join(options.outputdir, self.name+"_ie.dot")
        self.iepdf = os.path.join(options.outputdir, self.name+"_ie.pdf")

    def getTaxon(self, taxonomyName="", taxonName=""):
        if(self.options.verbose):
            print self.taxonomies, taxonomyName, taxonName
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
        self.genASP()
        if self.options.consCheck:
            if not self.testConsistency():
                print "Input is inconsistent o_O"
            else:
                print "Input is consistent ^_^"
            return
        if self.options.ie:
            if not self.testConsistency():
                print "Input is inconsistent!!"
                self.inconsistencyExplanation()
                return
        if self.enc & encode["pw"]:
            self.genPW(True)
        elif self.enc & encode["ve"]:
            self.genVE()
        elif self.enc & encode["cb"]:
            self.genPW(False)
            self.genCbConcept()
            fcb = open(self.cbfile, 'w')
            fcb.write(self.baseCb)
            fcb.close()
            self.genCB()
        elif self.enc & encode["ob"]:
            self.genOB()
        elif self.enc & encode["ct"]:
            self.genMir()
        else:
            self.genPW(False)

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
        rsnrfile = os.path.join(self.aspdir, dn1 +"_"+ dn2 + "_" + rel + ".dlv")
        frsnr = open(rsnrfile, "w")
        frsnr.write("\n%%% Assumption" + vn1 + "_" + vn2 + "_" + rel + "\n")
        if rel == "equals":
            frsnr.write("irs(X) :- out(" + vn1 + ",X), in(" + vn2 + ",X).\n")
            frsnr.write("irs(X) :- in(" + vn1 + ",X), out(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n")
        elif rel == "includes":
            frsnr.write("irs(X) :- out(" + vn1 + ",X), in(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) :- in(" + vn2 + ",X).\n") 
	    frsnr.write("out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n") 
        elif rel == "is_included_in":
            frsnr.write(":- #count{X: vrs(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write("irs(X) :- in(" + vn1 + ",X), out(" + vn2 + ",X).\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
        elif rel == "disjoint":
            frsnr.write(":- #count{X: vrs(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write("irs(X) :- in(" + vn1 + ",X), in(" + vn2 + ",X).\n")
	    frsnr.write("out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n")
        elif rel == "overlaps":
            frsnr.write(":- #count{X: vrs(X), out(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), out(" + vn2 + ",X)} = 0.\n")
            frsnr.write(":- #count{X: vrs(X), in(" + vn1 + ",X), in(" + vn2 + ",X)} = 0.\n")
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- in(" + vn2 + ",X).\n")
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- out(" + vn1 + ",X).\n") 
	    frsnr.write("in(" + vn1 + ",X) v out(" + vn1 + ",X) :- out(" + vn2 + ",X).\n") 
	    frsnr.write("in(" + vn2 + ",X) v out(" + vn2 + ",X) :- in(" + vn1 + ",X).\n")
        frsnr.close()
        com = "dlv -silent -filter=rel -n=1 "+rsnrfile+" "+self.pwfile+" "+self.pwswitch
        if commands.getoutput(com) == "":
            return 0
        return rcc5[rel]
## NF ends

    def testConsistency(self):
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD 1"
            if commands.getoutput(com).count("\n") < 5:
                return False
        else:
            com = "dlv -silent -filter=rel -n=1 "+self.pwfile+" "+self.pwswitch
            if commands.getoutput(com) == "":
                return False
        return True

    def inconsistencyExplanation(self):
        com = "dlv -silent -filter=ie -n=1 "+self.pwfile+" "+self.ixswitch
        ie = commands.getoutput(com)
        self.postProcessIE(ie);

    def postProcessIE(self, ie):
        print "Please see "+self.name+"_ie.pdf for the inconsistency relations between all the rules."
        print ie
        if ie.find("{}") == -1 and ie != "":
            ies = (re.match("\{(.*)\}", ie)).group(1).split(", ")
            tmpmap = {}
            for i in range(len(ies)):
              if ies[i].find("ie\(prod(") != -1:
                item = re.match("ie\(prod\((.*),(.*)\)\)", ies[i])
                key = item.group(1)
                tmpmap[key] = [item.group(2)]
              else:
                if ies[i].find("prod(") != -1:
                  item = re.match("ie\(s\((.*),prod(.*),(.*)\)\)", ies[i])
                else:
                  item = re.match("ie\(s\((.*),(.*),(.*)\)\)", ies[i])
                key = item.group(1)+","+item.group(3)
                if key in tmpmap.keys():
                  value = tmpmap[key]
                  value.append(item.group(2))
                  tmpmap[key] = value
                else:
                  tmpmap[key] = [item.group(2)]
            fie = open(self.iefile, 'w')
            fie.write("strict digraph "+self.name+"_ie {\n\nrankdir = LR\n\n")
            #fie.write("subgraph rules {\n")
            #for key in self.rules.keys():
            #    fie.write(key+"\n")
            #fie.write("}\n")
            #fie.write("subgraph inconsistencies {\n")
            #for key in tmpmap.keys():
            #    fie.write("\""+key+"\"\n")
            #fie.write("}\n")
            for key in tmpmap.keys():
                for value in tmpmap[key]:
                    fie.write("\""+value+"\" -> \"inconsistency="+key.__str__()+":"+tmpmap[key].__str__()+"\" \n")
            label=""
            for key in self.rules.keys():
                label += key+" : "+self.rules[key]+"\n"
            fie.write("graph [label=\""+label+"\"]\n")
            fie.write("}")
            fie.close()
            commands.getoutput("dot -Tpdf "+self.iefile+" -o "+self.iepdf)

    def outGringoPW(self):
        raw = self.pw.split("\n")
        pws = []
        ## Filter out those trash in the gringo output
        for i in range(2, len(raw) - 2, 2):
            pws.append(raw[i])
        self.npw = len(pws)
        outputstr = ""
        # mirs for each pw
        if self.options.cluster: pwmirs = []
        for i in range(len(pws)):
            if self.options.cluster: pwmirs.append({})

            # pwTm is the possible world taxonomy mapping, used for RCG
            pwTm = copy.deepcopy(self)
            pwTm.mir = {}
            pwTm.tr = []

            outputstr += "\nPossible world "+i.__str__()+":\n{"
            items = pws[i].split(" ")
            outputstr += pws[i]
            outputstr += "}\n"
        print outputstr

    def genPW(self, pwflag):
        pws = []
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD 0 --eq=0"
            self.pw = commands.getoutput(com)
            if self.pw.find("ERROR") != -1:
                print self.pw
                raise Exception(template.getEncErrMsg())
            if pwflag:
                raw = self.pw.split("\n")
                ## Filter out those trash in the gringo output
                for i in range(2, len(raw) - 2, 2):
                    pws.append(raw[i].strip().replace(") ",");"))
        # DLV, from here on
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.com = "dlv -silent -filter=rel "+self.pwfile+" "+ self.pwswitch+ " | "+path+"/muniq -u"
            self.pw = commands.getoutput(self.com)
            if self.pw == "":
                self.simpleRemedy()
            if self.pw.find("error") != -1:
                print self.pw
                raise Exception(template.getEncErrMsg())
                return None
            raw = self.pw.replace("{","").replace("}","").replace(" ","").replace("),",");")
            pws = raw.split("\n")
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")
        self.npw = len(pws)
        self.outPW(pws, pwflag, "rel")

    def outPW(self, pws, pwflag, ss):
        outputstr = ""
        # mirs for each pw
        if self.options.cluster: pwmirs = []
        for i in range(len(pws)):
            if self.options.cluster: pwmirs.append({})

            # pwTm is the possible world taxonomy mapping, used for RCG
            pwTm = copy.deepcopy(self)
            if self.enc & encode["cb"]:
                pwTm.mir = {}
                pwTm.tr = []

            outputstr += "\nPossible world "+i.__str__()+":\n{"
            if self.options.verbose: print pws[i]+"#"
            items = pws[i].split(";")
            if self.options.verbose: print len(items),items
            for j in range(len(items)):
                rel = items[j].replace(ss+"(","").replace(")","").split(",")
                if self.options.verbose: print items[j],rel
                dotc1 = self.dlvName2dot(rel[0])
                dotc2 = self.dlvName2dot(rel[1])
                if self.options.verbose: print dotc1,rel[2],dotc2
                if j != 0: outputstr += ", "
                outputstr += dotc1+rel[2]+dotc2
                pair = dotc1+","+dotc2
                if self.options.cluster: pwmirs[i][pair] = rcc5[rel[2]]
                # RCG
                pwTm.mir[pair] = rcc5[rel[2]]
                if rcc5[rel[2]] == rcc5["is_included_in"]:
                    pwTm.tr.append([dotc1, dotc2, 1])
                elif rcc5[rel[2]] == rcc5["includes"]:
                    pwTm.tr.append([dotc2, dotc1, 1])
                elif rcc5[rel[2]] == rcc5["equals"]:
                    pwTm.eq.append([dotc1, dotc2])
                if i == 0:
                    if not self.mir.has_key(pair) or not self.mir[pair] & rcc5[rel[2]]:
                        self.mir[pair] = rcc5[rel[2]] | relation["infer"]
                else:
                    if not self.mir.has_key(pair):
                        self.mir[pair] = rcc5[rel[2]] | relation["infer"]
                    elif not self.mir[pair] & rcc5[rel[2]]:
                        self.mir[pair] |= relation["infer"]
                    self.mir[pair] |= rcc5[rel[2]]
                pairrel = pair+","+rcc5[rel[2]].__str__()
                if pairrel in self.mirp.keys():
                    self.mirp[pairrel].append(i)
                else:
                    self.mirp[pairrel] = [i]
            self.adjustMirc(pair)
            outputstr += "}\n"
            # RCG
            # Only generate the RCG when necessary
            # for example, if mncb, genPW() is called for intermediate usage
            if self.enc & encode["pw"] and ss == "rel" or\
               self.enc & encode["cb"] and ss == "relout":
                pwTm.genPwRcg(self.name + "_" + i.__str__())
        if self.options.reduction:
            outputstr = self.uncReduction(pws)
        if pwflag:
            if self.options.output: print outputstr
            fpw = open(self.pwout, 'w')
            fpw.write(outputstr)
            fpw.close()
        self.genMir()
        if self.options.cluster: self.genPwCluster(pwmirs, False)

    def genPwRcg(self, fileName):
        fDot = open(self.options.outputdir+fileName+".dot", 'w')
	fDot.write("digraph {\n\nrankdir = RL\n\n")
        tmpCom = ""    # cache of combined taxa
        taxa1 = ""     # cache of taxa in the first taxonomy
        taxa2 = ""     # cache of taxa in the second taxonomy

        tmpTax = ""   # First taxonomy name, actually it really doesn't
                      # matter which one is the first one
	# Equalities
        for [T1, T2] in self.eq:
            T1s = T1.split(".")
            # First taxonomy name
            if tmpTax == "": tmpTax = T1s[0]
            T2s = T2.split(".")
	    if(T1s[1] == T2s[1]):
		tmpStr = T1s[1]
		fDot.write("\"" + tmpStr +"\" [color=blue];\n")
	    else:
		tmpStr = T1+","+T2
            # This assumes that eq is with arity two, eg, we don't have A=B=C
            tmpCom += "  \""+tmpStr+"\"\n"
            tmpTr = list(self.tr)
            for [T3, T4, P] in tmpTr:
		if(T1 == T3 or T2 == T3):
		    self.tr.remove([T3, T4, P])
		    self.tr.append([tmpStr, T4, 0])
		elif(T1 == T4 or T2 == T4):
		    self.tr.remove([T3, T4, P])
		    self.tr.append([T3, tmpStr, 0])

	# Duplicates
	tmpTr = list(self.tr)
        for [T1, T2, P] in tmpTr:
	    if(self.tr.count([T1, T2, P]) > 1):
		self.tr.remove([T1, T2, P])
	tmpTr = list(self.tr)
        for [T1, T2, P] in tmpTr:
	    if(P == 0):
	        if(self.tr.count([T1, T2, 1]) > 0):
		    self.tr.remove([T1, T2, 1])

	# Reductions
	tmpTr = list(self.tr)
        for [T1, T2, P1] in tmpTr:
            for [T3, T4, P2] in tmpTr:
		if (T2 == T3):
		    if(self.tr.count([T1, T4, 0])>0):
		        self.tr.remove([T1, T4, 0])
		        self.tr.append([T1, T4, 2])
		    if(self.tr.count([T1, T4, 1])>0):
		        self.tr.remove([T1, T4, 1])
		        #self.tr.append([T1, T4, 3])

        if self.options.verbose:
            print "Transitive reduction:"
            print self.tr
        # Node Coloring
	for [T1, T2, P] in self.tr:
            if(T1.find("*") == -1 and T1.find(",") == -1 and T1.find(".") != -1):
                T1s = T1.split(".")
                if tmpTax == T1s[0]: taxa1 += "  \""+T1+"\"\n"
                else: taxa2 += "  \""+T1+"\"\n"
            else:
                tmpCom += "  \""+T1+"\"\n"
            if(T2.find("*") == -1 and T2.find(",") == -1 and T2.find(".") != -1):
                T2s = T2.split(".")
                if tmpTax == T2s[0]: taxa1 += "  \""+T2+"\"\n"
                else: taxa2 += "  \""+T2+"\"\n"
            else:
                tmpCom += "  \""+T2+"\"\n"
        fDot.write("  node [shape=box style=\"filled, rounded\" fillcolor=\"#CCFFCC\"]\n")
        fDot.write(taxa1)
        fDot.write("  node [shape=box style=\"filled, rounded\" fillcolor=\"#FFFFCC\"]\n")
        fDot.write(taxa2)
        fDot.write("  node [shape=box style=\"filled, rounded\" fillcolor=\"#EEEEEE\"]\n")
        fDot.write(tmpCom)

	for [T1, T2, P] in self.tr:
	    if(P == 0):
	    	fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled, color=black];\n")
	    elif(P == 1):
	    	fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled, color=red];\n")
	    elif(P == 2):
              if False:
	    	fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=dashed, color=grey];\n")
        if self.options.rcgo:
	    fDot.write("  subgraph ig {\nedge [dir=none, style=dashed, color=blue, constraint=false]\n\n")
            for key in self.mir.keys():
                if self.mir[key] == rcc5["overlaps"]:
                    item = re.match("(.*),(.*)", key)
	    	    fDot.write("     \"" + item.group(1) + "\" -> \"" + item.group(2) + "\"\n")
	    fDot.write("  }\n")
        fDot.write("  subgraph cluster_lg {\n")
        fDot.write("    rankdir = LR\n")
        fDot.write("    label = \"Legend\";\n")
        fDot.write("    A1 -> B1 [label=\"is included in (given)\" style=filled, color=black]\n")
        fDot.write("    A2 -> B2 [label=\"is included in (inferred)\" style=filled, color=red]\n")
        fDot.write("    A3 -> B3 [label=\"overlaps\" dir=none, style=dashed, color=blue]\n")
        fDot.write("  }\n")
	fDot.write("}\n")
            
        fDot.close()
        commands.getoutput("dot -Tpng "+self.options.outputdir+fileName+".dot -o "+self.options.outputdir+fileName+".png")



    def simpleRemedy(self):
        print "************************************"
        print "Input is inconsistent"
        if self.options.ie:
            self.inconsistencyExplanation()
        s = len(self.articulations)
        for i in range(s):
            a = self.articulations.pop(i)    
            # Now refresh the input file
            self.rules = {}
            self.genASP()
    	    # Run the reasoner again
            self.pw = commands.getoutput(self.com)
            if self.pw != "":
                # Remove mir is not needed because it will be reset anyways
                self.removeMir(a.string)
                print "Repairing: remove [" + a.string + "]"
                print "************************************"
                return True
            self.articulations.insert(i, a)
        print "Don't know how to repair"
        print "************************************"
        return False

    def uncReduction(self, pws):
        ppw = sets.Set()
        for pair in self.mir.keys():
            if self.mir[pair] & ~relation["infer"] not in rcc5.values():
                userAns = RedWindow(pair, self.mir[pair])
                self.mir[pair] = userAns.main()
                self.adjustMirc(pair)
                # Reduce pws
                tmpppw = sets.Set()
                for i in range(5):
                  rel = 1 << i
                  if self.mir[pair] & rel and pair+","+rel.__str__() in self.mirp.keys():
                    for pw in self.mirp[pair+","+rel.__str__()]:
                        tmpppw.add(pw)
                # Adjust mir
                for tmppair in self.mir.keys():
                  for j in range(5):
                    relj = 1 << j
                    if tmppair+","+relj.__str__() in self.mirp.keys() and\
                       pw in self.mirp[tmppair+","+relj.__str__()]:
                      if len(tmpppw) ==1:
                        self.mir[tmppair] = relj
                      else:
                        self.mir[tmppair] |= relj
                if len(tmpppw) != 0:
                  if len(ppw) == 0:
                    ppw = tmpppw
                  else:
                    ppw = ppw.intersection(tmpppw)
                else:
                  print "Inconsistent again !!"
                  ppw = tmpppw
        outputstr = ""
        for i in ppw:
            if self.options.cluster: pwmirs.append({})
            outputstr += "Possible world "+i.__str__()+": {"
            items = pws[i].split(";")
            for j in range(len(items)):
                rel = items[j].replace("rel(","").replace(")","").split(",")
                dotc1 = self.dlvName2dot(rel[0])
                dotc2 = self.dlvName2dot(rel[1])
                if j != 0: outputstr += ", "
                outputstr += dotc1+rel[2]+dotc2
            outputstr += "}\n"
        return outputstr

    def adjustMirc(self, pair):
        self.mirc[pair] = []
        for k in range(5):
            self.mirc[pair].append(0)
        for k in range(5):
            if self.mir[pair] & (1 << k):
                self.mirc[pair][k] += 1


    def genPwCluster(self, pws, obs):
        fcl = open(self.clfile, 'w')
        fcldot = open(self.cldot, 'w')
        fcldot.write("graph "+self.name+"_cluster {\n"+\
                     "overlap=false\nsplines=true\n")
        dmatrix = []
        for i in range(self.npw):
            dmatrix.append([])
            for j in range(i+1):
                if i == j :
                    dmatrix[i].append(0)
                    fcl.write("0 "); continue
                d = 0
                if obs:
                    for ob in pws[i]:
                        if ob not in pws[j]: d += 1
                    for ob in pws[j]:
                        if ob not in pws[i]: d += 1
                else:
                    for key in pws[i].keys():
                        if pws[i][key] != pws[j][key]: d += 1
                fcl.write(d.__str__()+" ")
                dmatrix[i].append(d)
                if i != j and not self.options.simpCluster:
                    fcldot.write("\"pw"+i.__str__()+"\" -- \"pw"+j.__str__()+\
                            "\" [label="+d.__str__()+",len="+d.__str__()+"]\n")
            fcl.write("\n")
        if self.options.simpCluster:
            for i in range(self.npw):
                for j in range(i):
                    reduced = False
                    for k in range(self.npw):
                        if i == k or j == k: continue
                        if j < k and k < i:
                            if dmatrix[i][j] == dmatrix[i][k] + dmatrix[k][j]:
                                reduced = True
                                break
                        elif i < k:
                            if dmatrix[i][j] == dmatrix[k][i] + dmatrix[k][j]:
                                reduced = True
                                break
                        elif k < j:
                            if dmatrix[i][j] == dmatrix[i][k] + dmatrix[j][k]:
                                reduced = True
                                break
                    if not reduced:
                        fcldot.write("\"pw"+i.__str__()+"\" -- \"pw"+j.__str__()+\
                            "\" [label="+dmatrix[i][j].__str__()+",len="+dmatrix[i][j].__str__()+"]\n")
        fcldot.write("}")
        fcl.close()
        fcldot.close()
        commands.getoutput("dot -Tpdf "+self.cldot+" -o "+self.cldotpdf)
        commands.getoutput("neato -Tpdf "+self.cldot+" -o "+self.clneatopdf)

    def genOB(self):
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        if reasoner[self.options.reasoner] == reasoner["dlv"]:
            com = "dlv -silent -filter=pp "+self.pwfile+" "+ self.pwswitch+ " | "+path+"/muniq -u"
            raw = commands.getoutput(com).replace("{","").replace("}","").replace(" ","").replace("),",");")
        elif reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD 0 --eq=no"
            raw = commands.getoutput(com)
        pws = raw.split("\n")
        self.npw = 0
        outputstr = ""
        lastpw = ""
        if self.options.cluster: pwobs = []
        for i in range(len(pws)):
            if pws[i].find("pp(") == -1: continue
	    result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n"
	    result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n\n"
            if reasoner[self.options.reasoner] == reasoner["dlv"]:
                items = pws[i].split(";")
            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
                items = pws[i].split(" ")
            pw = ""
            for j in range(len(items)):
                if items[j] == "": continue
                if j != 0: pw += ", "
                inout = items[j].replace("pp(","").replace(")","").split(",")
                dotConcept1 = self.dlvName2dot(inout[0])
                dotConcept2 = self.dlvName2dot(inout[1])
                loct = ""
                for k in range(2,self.obslen):
                    loct += "@" + inout[k]
                pw += dotConcept1+"*"+dotConcept2+loct
            # Filter those duplicate pws
            if pw != lastpw:
                lastpw = pw
                outputstr += "Possible world "+self.npw.__str__()+": {"
                outputstr += pw + "}\n"
                self.npw += 1
        if self.options.output:
            print outputstr
        fob = open(self.obout, 'w')
        fob.write(outputstr)
        fob.close()
        if self.options.cluster: self.genPwCluster(pwobs, True)
            

    def genVE(self):
        com = "dlv -silent -filter=vr "+self.pwfile+" "+self.pwswitch
        self.ve = commands.getoutput(com)
        if self.options.output:
            print self.ve

    def genCB(self):
        pws = []
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.cbfile+" "+ self.pwswitch+ " | claspD 0 --eq=0"
            self.pw = commands.getoutput(com)
            if self.pw.find("ERROR") != -1:
                print self.pw
                raise Exception(template.getEncErrMsg())
            raw = self.pw.split("\n")
            if self.options.verbose: print raw
            ## Filter out those trash in the gringo output
            for i in range(2, len(raw) - 2, 2):
                pws.append(raw[i].strip().replace(") ",");"))
                if self.options.verbose: print pws
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.com = "dlv -silent -filter=relout "+self.cbfile+" "+ self.pwswitch+ " | "+path+"/muniq -u"
            self.cb = commands.getoutput(self.com)
            if self.cb == "":
                self.simpleRemedy()
            if self.cb.find("error") != -1:
                print self.cb
                raise Exception(template.getEncErrMsg())
                return None
            raw = self.cb.replace("{","").replace("}","").replace(" ","").replace("),",");")
            pws = raw.split("\n")
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")
        self.npw = len(pws)
        self.outPW(pws, self.options.output, "relout")
 
    def genASP(self):
        self.baseAsp == ""
        self.genAspConcept()
        self.genAspPC()
        self.genAspAr()
        if self.enc & encode["vr"] or self.enc & encode["dl"] or self.enc & encode["pl"] or self.enc & encode["mn"]:
            self.genAspDc()
        if self.obs != [] and self.enc & encode["ob"]:
            self.genAspObs()
        fdlv = open(self.pwfile, 'w')
        fdlv.write(self.baseAsp)
        fdlv.close()
        pdlv = open(self.pwswitch, 'w')
        idlv = open(self.ixswitch, 'w')
        pdlv.write("pw.")
        idlv.write("ix.")
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            if self.enc & encode["ob"]:
                pdlv.write("\n#hide.\n#show pp/" + self.obslen.__str__() + ".")
            elif self.enc & encode["pw"]:
                pdlv.write("\n#hide.\n#show rel/3.")
            elif self.enc & encode["cb"]:
                pdlv.write("\n#hide.\n#show relout/3.")
            idlv.write("\n#hide.\n#show ie/3.")
        pdlv.close()
        idlv.close()

    def genCbConcept(self):
        self.baseCb += "\n%%% combined concept\n"
        for key1 in self.taxonomies.keys():
            for key2 in self.taxonomies.keys():
                if key1 >= key2: continue
                for taxon1 in self.taxonomies[key1].taxa.keys():
                    t1 = self.taxonomies[key1].taxa[taxon1]
                    for taxon2 in self.taxonomies[key2].taxa.keys():
                        t2 = self.taxonomies[key2].taxa[taxon2]
                        if self.mirp.has_key(t1.dotName()+","+t2.dotName()+","+rcc5["overlaps"].__str__()) or\
                           self.mirp.has_key(t2.dotName()+","+t1.dotName()+","+rcc5["overlaps"].__str__()):
	                    self.baseCb += "newcon(" + t1.dlvName() + "_not_" + t2.dlvName() + ", "\
	           	                + t1.dlvName() + ", " + t2.dlvName()  + ", 0).\n"
	                    self.baseCb += "newcon(" + t1.dlvName() + "__" + t2.dlvName() + ", "\
	           	                + t1.dlvName() + ", " + t2.dlvName()  + ", 1).\n"
	                    self.baseCb += "newcon(not_" + t1.dlvName() + "__" + t2.dlvName() + ", "\
	           	                + t1.dlvName() + ", " + t2.dlvName()  + ", 2).\n"
	           		        #+ "concept2(" + t1.dlvName() + ", _), "\
	           		        #+ "concept2(" + t2.dlvName() + ", _).\n"
        # add more template rules to the input file
        self.baseCb += template.getAspCbCon()

    def genAspConcept(self):
        con = "%%% Concepts\n"

        # numbering concepts
        num = 0    # number of taxa
        prod = 0   # product
        n = 0      # number of taxonomies
        pro = 1    # product of num
        couArray = []
        proArray = []
        taxaArray = []
        for key in self.taxonomies.keys():
            cou = 0
            con += "tax(" + self.taxonomies[key].dlvName() + "," + n.__str__() + ").\n"
            con += "concept2(A, B) :- concept(A,B,_).\n"
            for taxon in self.taxonomies[key].taxa.keys():
                t = self.taxonomies[key].taxa[taxon]
                if (self.enc & encode["dl"] or self.enc & encode["mn"]) and\
                    t.hasChildren(): #and self.options.enableCov:
                    con += "concept2(" + t.dlvName() + "," + n.__str__() + ").\n"
                else:
                    fl = num + cou
                    if self.enc & encode["mn"]:
                        fl = cou
                    self.map[t.dlvName()] = num
                    con += "concept(" + t.dlvName() + "," + n.__str__() + "," + fl.__str__()+").\n"
                    cou += 1
            n += 1
            num += cou
            couArray.append(cou+1)
            proArray.append(pro)
            pro *= (cou+1)
            prod = prod*cou + prod + cou
            if self.options.verbose:
                print "count: ",cou,", product: ",prod

        if self.enc & encode["dl"]:
            maxint = int(self.options.dl)*num
	    self.baseAsp = "#maxint=" + maxint.__str__() + ".\n\n"
	    self.baseAsp += con
	    self.baseAsp += "%%% regions\n"
	    self.baseAsp += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseAsp += "%%% bit\n"
	    self.baseAsp += "bit(M, V):-r(M),#mod(M," + int(num).__str__() + ",V).\n\n"

	    self.baseAsp += "%%% Meaning of regions\n"
	    self.baseAsp += "in(X, M) :- r(M),concept(X,_,N),bit(M,N).\n"
	    self.baseAsp += "in(X, M) v out(X, M) :- r(M),concept(X,_,N),bit(M,N1), N<>N1.\n"
	    #self.baseAsp += "gin(X, M) v gout(X, M) :- r(M),concept(X,_,N),not cin(X, M), not cout(X, M).\n"
	    #self.baseAsp += ":- gin(X, M), gout(X, M), r(M), concept(X,_,_).\n\n"
            #self.baseAsp += "in(X, M) :- cin(X, M).\n"
            #self.baseAsp += "in(X, M) :- gin(X, M).\n"
            #self.baseAsp += "out(X, M) :- cout(X, M).\n"
            #self.baseAsp += "out(X, M) :- gout(X, M).\n"
	    self.baseAsp += "ir(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n\n"

	    self.baseAsp += "%%% Constraints of regions.\n"
	    self.baseAsp += "vrs(X) :- r(X), not irs(X).\n"
	    self.baseAsp += ":- vrs(X), irs(X).\n\n"

        elif self.enc & encode["mn"]:
            maxint = prod
            if reasoner[self.options.reasoner] == reasoner["dlv"]:
	        self.baseAsp = "#maxint=" + maxint.__str__() + ".\n\n"
	        self.baseAsp += "%%% regions\n"
	        self.baseAsp += "r(M):- #int(M),M>=1,M<=#maxint.\n\n"

	        self.baseAsp += con

	        self.baseAsp += "%%% bit\n"
                for i in range(len(couArray)):
	            self.baseAsp += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", #mod(M1," + couArray[i].__str__() + ",V).\n"
            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
	        self.baseAsp = con
	        self.baseAsp += "%%% regions\n"
	        self.baseAsp += "r(1.."+maxint.__str__()+").\n\n"

	        self.baseAsp += "%%% bit\n"
                for i in range(len(couArray)):
	            self.baseAsp += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", V = M1 #mod " + couArray[i].__str__() + ".\n"
            self.baseAsp += template.getAspMnCon()

        elif self.enc & encode["vr"]:
	    self.baseAsp = "#maxint=" + int(2**num).__str__() + ".\n\n"
	    self.baseAsp += con
	    self.baseAsp += "\n%%% power\n"
	    self.baseAsp += "p(0,1).\n"
	    self.baseAsp += "p(N,M) :- #int(N),N>0,#succ(N1,N),p(N1,M1),M=M1*2.\n\n"

	    self.baseAsp += "%%% regions\n"
	    self.baseAsp += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseAsp += "%%% count of concepts\n"
	    self.baseAsp += "count(N):- #int(N),N>=0,N<#count{Y:concept(Y,_,_)}.\n\n"

	    self.baseAsp += "%%% bit\n"
	    self.baseAsp += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
	    self.baseAsp += "bit(M, N, 1):-r(M),count(N),not bit(M,N,0).\n\n"

	    self.baseAsp += "%%% Meaning of regions\n"
            self.baseAsp += "in(X, M) :- not out(X, M), r(M),concept(X,_,N),count(N).\n"
            self.baseAsp += "out(X, M) :- not in(X, M), r(M),concept(X,_,N),count(N).\n"
	    self.baseAsp += "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"
	    self.baseAsp += "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"
	    self.baseAsp += "ir(M, fi) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"

	    self.baseAsp += "%%% Constraints of regions.\n"
	    self.baseAsp += "irs(X) :- ir(X, _).\n"
	    self.baseAsp += "vrs(X) :- vr(X, _).\n"
	    self.baseAsp += "vr(X, X) :- not irs(X), r(X).\n"
	    self.baseAsp += "ir(X, X) :- not vrs(X), r(X).\n"
	    self.baseAsp += "ie(prod(A,B)) :- vr(X, A), ir(X, B), ix.\n"
	    self.baseAsp += ":- vrs(X), irs(X), pw.\n\n"

	    self.baseAsp += "%%% Inconsistency Explanation.\n"
	    self.baseAsp += "ie(s(R, A, Y)) :- pie(R, A, Y), not cc(R, Y), ix.\n"
	    self.baseAsp += "cc(R, Y) :- c(R, _, Y), ix.\n"
#	    self.baseAsp += "in(X, M) v out(X, M) :- r(M),concept(X,_,N),count(N).\n"
#	    self.baseAsp += "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"
#	    self.baseAsp += "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"
#	    self.baseAsp += "ir(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"
#
#	    self.baseAsp += "%%% Constraints of regions.\n"
#	    self.baseAsp += "ir(0).\n"
#	    self.baseAsp += "vrs(X) v irs(X):- r(X).\n"
#	    self.baseAsp += ":- vrs(X), irs(X).\n\n"

        elif self.enc & encode["direct"]:
            self.baseAsp += con
            self.baseAsp += "\n% GENERATE possible labels\n"
	    self.baseAsp += "node(X) :- concept(X, _, _).\n"
            self.baseAsp += "rel(X, Y, R) :- label(X, Y, R), X < Y.\n"
	    self.baseAsp += "label(X, X, eq) :- node(X).\n"

	    self.baseAsp += "label(X,Y,eq) v label(X,Y,ds) v label(X,Y,in) v label(X,Y,ls) v label(X,Y,ol) :-\n"
	    self.baseAsp += "	    node(X),node(Y), X <> Y.\n\n"

            self.baseAsp += "% Make sure they are pairwise disjoint\n"
            self.baseAsp += ":- label(X,Y,eq), label(X,Y,ds).\n"
            self.baseAsp += ":- label(X,Y,eq), label(X,Y,in).\n"
            self.baseAsp += ":- label(X,Y,eq), label(X,Y,ls).\n"
            self.baseAsp += ":- label(X,Y,eq), label(X,Y,ol).\n"

            self.baseAsp += ":- label(X,Y,ds), label(X,Y,in).\n"
            self.baseAsp += ":- label(X,Y,ds), label(X,Y,ls).\n"
            self.baseAsp += ":- label(X,Y,ds), label(X,Y,ol).\n"

	    self.baseAsp += ":- label(X,Y,in), label(X,Y,ls).\n"
	    self.baseAsp += ":- label(X,Y,in), label(X,Y,ol).\n"
	    self.baseAsp += ":- label(X,Y,ls), label(X,Y,ol).\n"

            self.baseAsp += "% integrity constraint for weak composition\n"
            self.baseAsp += "label(X, Y, in) :- label(Y, X, ls).\n"
            self.baseAsp += "label(X, Y, ls) :- label(Y, X, in).\n"
            self.baseAsp += "label(X, Y, ol) :- label(Y, X, ol).\n"
            self.baseAsp += "label(X, Y, ds) :- label(Y, X, ds).\n"
            self.baseAsp += "sum(X, Y, Z) :- sum(X, Z, Y).\n"
            self.baseAsp += "label(X, Y, in) :- sum(X, Y, _).\n"

	    self.baseAsp += "label(X,Z,eq) :- label(X,Y,eq), label(Y,Z,eq).\n"
	    self.baseAsp += "label(X,Z,in) :- label(X,Y,eq), label(Y,Z,in).\n"
	    self.baseAsp += "label(X,Z,ls) :- label(X,Y,eq), label(Y,Z,ls).\n"
	    self.baseAsp += "label(X,Z,ol) :- label(X,Y,eq), label(Y,Z,ol).\n"
	    self.baseAsp += "label(X,Z,ds) :- label(X,Y,eq), label(Y,Z,ds).\n"

	    self.baseAsp += "label(X,Z,in) :- label(X,Y,in), label(Y,Z,eq).\n"
	    self.baseAsp += "label(X,Z,in) :- label(X,Y,in), label(Y,Z,in).\n"
	    self.baseAsp += "label(X,Z,eq) v label(X,Z,in) v label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,in), label(Y,Z,ls).\n"
	    self.baseAsp += "label(X,Z,in) v label(X,Z,ol) :- label(X,Y,in), label(Y,Z,ol).\n"
	    self.baseAsp += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,in), label(Y,Z,ds).\n"

	    self.baseAsp += "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,eq).\n"
	    self.baseAsp += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseAsp += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,ol) :- label(X,Y,ls), label(Y,Z,in).\n"
	    self.baseAsp += "label(X,Z,ls) :- label(X,Y,ls), label(Y,Z,ls).\n"
	    self.baseAsp += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ol).\n"
	    self.baseAsp += "label(X,Z,ds) :- label(X,Y,ls), label(Y,Z,ds).\n"

	    self.baseAsp += "label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,eq).\n"
	    self.baseAsp += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,in).\n"
	    self.baseAsp += "label(X,Z,ol) v label(X,Z,ls) :- label(X,Y,ol), label(Y,Z,ls).\n"
	    self.baseAsp += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseAsp += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ol), label(Y,Z,ol).\n"
	    self.baseAsp += "label(X,Z,in) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ol), label(Y,Z,ds).\n"

	    self.baseAsp += "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,eq).\n"
	    self.baseAsp += "label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,in).\n"
	    self.baseAsp += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ls).\n"
	    self.baseAsp += "label(X,Z,ls) v label(X,Z,ol) v label(X,Z,ds) :- label(X,Y,ds), label(Y,Z,ol).\n"
	    self.baseAsp += "%% Any of RCC5 is possible for X vs Z\n"
	    self.baseAsp += "%label(X,Z,eq) v label(X,Z,ds) v label(X,Z,in) v label(X,Z,ls) v label(X,Z,ol) :- label(X,Y,ds), label(Y,Z,ds).\n\n"

            self.baseAsp += "label(X, Y, ds) :- sum(X, X1, X2), label(X1, Y, ds), label(X2, Y, ds).\n"
            self.baseAsp += "sum(X, Y, X2) :- sum(X, X1, X2), label(X1, Y, eq).\n"
            self.baseAsp += "sum(Y, X1, X2) :- sum(X, X1, X2), label(X, Y, eq).\n"
            # A + (B + C) = (A + B) + C
            self.baseAsp += "label(X, Y, eq) :- sum(X, A, X1), sum(X1, B, C), sum(Y, B, Y1), sum(Y1, A, C).\n"
            self.baseAsp += "label(X, Y, ol) v label(X, Y, in) :- sum(X, X1, X2), label(X1, Y, ol), label(X2, Y, ol).\n"
            self.baseAsp += "label(X, Y, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X2, Y2, R).\n"
            self.baseAsp += "label(X2, Y2, R) :- sum(X, X1, X2), sum(Y, Y1, Y2), label(X1, Y1, eq), label(X, Y, R).\n"
            self.baseAsp += "label(X, Y, in) v label(X, Y, eq) :- sum(Y, Y1, Y2), label(X, Y1, in), label(X, Y2, in).\n"

        else:
            print "EXCEPTION: encode ",self.options.encode," not defined!!"

    def genAspPC(self):
        self.baseAsp += "%%% PC relations\n"
        for key in self.taxonomies.keys():
            queue = copy.deepcopy(self.taxonomies[key].roots)
            while len(queue) != 0:
                if self.options.verbose:
                    print "PC: ",queue
                t = queue.pop(0)
                if t.hasChildren():
                    if self.options.verbose:
                        print "PC: ",t.dlvName()
                    if self.enc & encode["vr"] or self.enc & encode["dl"] or self.enc & encode["mn"]:
			# ISA
			self.baseAsp += "%% ISA\n"
			coverage = ":- in(" + t.dlvName() + ", X)"
			coverin = ""
                        coverout = ""
			for t1 in t.children:
                            queue.append(t1)
			    self.baseAsp += "% " + t1.dlvName() + " isa " + t.dlvName() + "\n"
                            ruleNum = len(self.rules)
			    self.rules["r" + ruleNum.__str__()] = t1.dotName() + " isa " + t.dotName()
			    #self.baseAsp += "in(" + t.dlvName() + ", X) :- in(" + t1.dlvName() + ", X).\n"
			    #self.baseAsp += "out(" + t1.dlvName() + ", X) :- out(" + t.dlvName() + ", X).\n"
			    #self.baseAsp += "in(" + t1.dlvName() + ", X) v out(" + t1.dlvName() + ", X) :- in(" + t.dlvName() + ", X).\n"
			    #self.baseAsp += "in(" + t.dlvName() + ", X) v out(" + t.dlvName() + ", X) :- out(" + t1.dlvName() + ", X).\n"
			    self.baseAsp += "ir(X, r" + ruleNum.__str__() +") :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n"
		            self.baseAsp += "ir(X, prod(r" + ruleNum.__str__() + ",R)) :- in(" + t1.dlvName() + ",X), out3(" + t.dlvName() + ", X, R), ix.\n" 
                            if reasoner[self.options.reasoner] == reasoner["dlv"]:
			        self.baseAsp += ":- #count{X: vrs(X), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X)} = 0, pw.\n"
                            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
			        self.baseAsp += ":- [vrs(X): in(" + t1.dlvName() + ", X): in(" + t.dlvName() + ", X)]0, pw.\n"
			    self.baseAsp += "pie(r" + ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X), ix.\n"
			    self.baseAsp += "c(r" + ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X), ix.\n\n"
			    coverage += ",out(" + t1.dlvName() + ", X)"
                            if coverin != "":
                                coverin += " v "
                                coverout += ", "
                            coverin += "in(" + t1.dlvName() + ", X)"
                            coverout += "out(" + t1.dlvName() + ", X)"
			# C
			self.baseAsp += "%% coverage\n"
                        ruleNum = len(self.rules)
		        self.rules["r" + ruleNum.__str__()] = t.dotName() + " coverage"
			#self.baseAsp += coverin + " :- in(" + t.dlvName() + ", X).\n"
                        if self.options.enableCov:
			    coverout3 = "out3(" + t.dlvName() + ", X, r" + ruleNum.__str__() + ") :- " + coverout
			    coverout = "out(" + t.dlvName() + ", X) :- " + coverout
			    self.baseAsp += coverout3 + ", ix.\n"
                        else:
			    coverout = "in(" + t.dlvName() + ",X) v out(" + t.dlvName() + ", X) :- " + coverout
			self.baseAsp += coverout + ", pw.\n"
			#self.baseAsp += "ir(X, r" + ruleNum.__str__() + ") " +coverage + ".\n\n"

			# D
			self.baseAsp += "%% sibling disjointness\n"
			for i in range(len(t.children) - 1):
			    for j in range(i+1, len(t.children)):
				name1 = t.children[i].dlvName()
				name2 = t.children[j].dlvName()
                                ruleNum = len(self.rules)
		                self.rules["r" + ruleNum.__str__()] = t.children[i].dotName() + " disjoint " + t.children[j].dotName()
				self.baseAsp += "% " + name1 + " ! " + name2+ "\n"
				#self.baseAsp += "out(" + name1 + ", X) :- in(" + name2+ ", X).\n"
				#self.baseAsp += "out(" + name2 + ", X) :- in(" + name1+ ", X).\n"
			        #self.baseAsp += "in(" + name1 + ", X) v out(" + name1 + ", X) :- out(" + name2 + ", X).\n"
			        #self.baseAsp += "in(" + name2 + ", X) v out(" + name2 + ", X) :- out(" + name1 + ", X).\n"
				self.baseAsp += "ir(X, r" + ruleNum.__str__() + ") :- in(" + name1 + ", X), in(" + name2+ ", X).\n"
                                if reasoner[self.options.reasoner] == reasoner["dlv"]:
				    self.baseAsp += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2+ ", X)} = 0, pw.\n"
				    self.baseAsp += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2+ ", X)} = 0, pw.\n"
                                elif reasoner[self.options.reasoner] == reasoner["gringo"]:
				    self.baseAsp += ":- [vrs(X): in(" + name1 + ", X): out(" + name2+ ", X)]0, pw.\n"
				    self.baseAsp += ":- [vrs(X): out(" + name1 + ", X): in(" + name2+ ", X)]0, pw.\n"
			        self.baseAsp += "pie(r" + ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
			        self.baseAsp += "c(r" + ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
			        self.baseAsp += "pie(r" + ruleNum.__str__() + ", A, 2) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
			        self.baseAsp += "c(r" + ruleNum.__str__() + ", A, 2) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                    elif self.enc & encode["direct"]:
			# ISA
			# C
			self.baseAsp += "\n%% ISA\n"
                        
			coverage = "irs(X) :- in(" + t.dlvName() + ", X)"
                        numkids = len(t.children)
                        if numkids == 1:
                            self.baseAsp += "label(" + t.dlvName() + "," + t.children[0] + ", eq).\n"
                        elif numkids > 1:
                            prefix ="label(" + t.dlvName() + ", "
                            pre = t.dlvName()
                            coverage = ""
			    for t1 in range(numkids - 2):
                                t1name = t.children[t1].dlvName()
				self.baseAsp += "% " + t1name + " isa " + t.dlvName() + "\n"
                                self.baseAsp += prefix + t1name + ", eq) v "
                                self.baseAsp += prefix + t1name + ", in).\n"
                                nex = t.dlvName() + t1.__str__()
				coverage += "sum(" + pre + "," + t1name + "," + nex + ").\n"
                                pre = nex
		            self.baseAsp += "% " + t.children[numkids - 2].dlvName() + " isa " + t.dlvName() + "\n"
                            self.baseAsp += prefix + t.children[numkids - 2].dlvName() + ", eq) v "
                            self.baseAsp += prefix + t.children[numkids - 2].dlvName() + ", in).\n\n"
		            self.baseAsp += "% " + t.children[numkids - 1].dlvName() + " isa " + t.dlvName() + "\n"
                            self.baseAsp += prefix + t.children[numkids - 1].dlvName() + ", eq) v "
                            self.baseAsp += prefix + t.children[numkids - 1].dlvName() + ", in).\n\n"
		            coverage += "sum(" + pre + "," + t.children[numkids - 2].dlvName() + "," + t.children[numkids - 1].dlvName() + ").\n"
                            
			    self.baseAsp += "\n%% coverage\n"
			    self.baseAsp += coverage + "\n\n"
			# D
			self.baseAsp += "%% sibling disjointness\n"
			for i in range(len(t.children) - 1):
			    for j in range(i+1, len(t.children)):
				name1 = t.children[i].dlvName()
				name2 = t.children[j].dlvName()
				self.baseAsp += "% " + name1 + " ! " + name2+ "\n"
				self.baseAsp += "label(" + name1 + ", " + name2+ ", ds).\n"


    def genAspAr(self):
        self.baseAsp += "\n%%% Articulations\n"
        for i in range(len(self.articulations)):
            self.baseAsp += "% " + self.articulations[i].string + "\n"
            ruleNum = len(self.rules)
            self.articulations[i].ruleNum = ruleNum
            self.rules["r" + ruleNum.__str__()] = self.articulations[i].string
            self.baseAsp += self.articulations[i].toASP(self.options.encode, self.options.reasoner)+ "\n"

    def genAspDc(self):
        self.baseCb  += self.baseAsp
        self.baseAsp += template.getAspPwDc()
        self.baseCb  += template.getAspCbDc()

    def genAspObs(self):
        self.baseAsp += "%% Observation Information\n\n"
        if reasoner[self.options.reasoner] == reasoner["dlv"]:
            self.seperator = "v"
            self.connector = ", "
        elif reasoner[self.options.reasoner] == reasoner["gringo"]:
            self.seperator = "|"
            self.connector = ": "
        if self.location == []:
            self.baseAsp += "present(X) " + self.seperator + " absent(X) :- r(X).\n"
            self.baseAsp += ":- present(X), absent(X).\n"
            self.baseAsp += "absent(X) :- irs(X).\n"
        else:
            if self.exploc:
                self.baseAsp += "subl(X, Z) :- subl(X, Y), subl(Y, Z).\n" 
                for i in range(len(self.location)):
                    self.baseAsp += "l(" + self.location[i][0] + ").\n"
                    for j in range(1, len(self.location[i])):
                        self.baseAsp += "l(" + self.location[i][j] + ").\n"
                        self.baseAsp += "subl(" + self.location[i][j] + ", " + self.location[i][0] +").\n"
            else:
                for i in range(len(self.location)):
                    self.baseAsp += "l(" + self.location[i] + ").\n"
            if self.temporal == []:
                self.baseAsp += "present(X, L) " + self.seperator + " absent(X, L) :- r(X), l(L).\n"
                self.baseAsp += ":- present(X, L), absent(X, L).\n"
                self.baseAsp += "absent(X, L) :- irs(X), l(L).\n"
                self.baseAsp += "present(X, L) :- present(X, L1), subl(L1, L).\n"
                self.baseAsp += "absent(X, L) :- absent(X, L1), subl(L, L1).\n"
            else:
                if self.exptmp:
                    self.baseAsp += "subt(X, Z) :- subt(X, Y), subt(Y, Z).\n" 
                    for i in range(len(self.temporal)):
                        self.baseAsp += "l(" + self.temporal[i][0] + ").\n"
                        for j in range(1, len(sef.temporal[i])):
                            self.baseAsp += "t(" + self.temporal[i][j] + ").\n"
                            self.baseAsp += "subt(" + self.temporal[i][j] + ", " + self.temporal[i][0] +").\n"
                else:
                    for i in range(len(self.temporal)):
                        self.baseAsp += "t(" + self.temporal[i] + ").\n"
                self.baseAsp += "present(X, L, T) " + self.seperator + " absent(X, L, T) :- r(X), l(L), t(T).\n"
                self.baseAsp += ":- present(X, L, T), absent(X, L, T).\n"
                self.baseAsp += "absent(X, L, T) :- irs(X), l(L), t(T).\n"
                self.baseAsp += "present(X, L, T) :- present(X, L1, T), subl(L1, L), t(T).\n"
                self.baseAsp += "absent(X, L, T) :- absent(X, L1, T), subl(L, L1), t(T).\n"
                self.baseAsp += "present(X, L, T) :- present(X, L, T1), subt(T1, T), l(L).\n"
                self.baseAsp += "absent(X, L, T) :- absent(X, L, T1), subt(T, T1), l(L).\n"
                
        if self.obslen == 2:
            appendd = ""
	    self.baseAsp += "pp(X, Y) :- pinout(X, in, R), pinout(Y, in, R), X < Y.\n"
        elif self.obslen == 3:
            appendd = ", Y"
	    self.baseAsp += "pp(X, Y, Z) :- pinout(X, in, R, Z), pinout(Y, in, R, Z), X < Y.\n"
        elif self.obslen == 4:
            appendd = ", Y, Z"
	    self.baseAsp += "pp(X, Y, Z, T) :- pinout(X, in, R, Z, T), pinout(Y, in, R, Z, T), X < Y.\n"
        else:
            print "Syntax error in observation portion of input file!!"
        for i in range(len(self.obs)):
            tmp = ""
            for j in range(len(self.obs[i][0])):
                if self.obs[i][0][j][1] == "Y":
                  pre = "in"
                else:
                  pre = "out"
                if tmp != "": tmp += self.connector
                cpt = self.obs[i][0][j][0]
                tmp += pre + "(" + cpt + ", X)"
            pair = ""
	    if self.obslen > 2:
                pair += ", " + self.obs[i][2]
	        if self.obslen > 3:
                    pair += ", " + self.obs[i][3]
            if self.obs[i][1] == "N":
                self.baseAsp += ":- present(X" + pair + ")," + tmp + ".\n" 
            else:
                if reasoner[self.options.reasoner] == reasoner["dlv"]:
                    self.baseAsp += ":- #count{X: present(X" + pair + "), " + tmp + "} = 0.\n"
                elif reasoner[self.options.reasoner] == reasoner["gringo"]:
                    self.baseAsp += ":- [present(X" + pair + "): " + tmp + "]0.\n"
	self.baseAsp += "pinout(C, in, X" + appendd + ") :- present(X" + appendd + "), concept(C, _, N), in(C, X).\n"
	self.baseAsp += "pinout(C, out, X" + appendd + ") :- present(X" + appendd + "), concept(C, _, N), out(C, X).\n"
            

    def readFile(self):
        file = open(os.path.join(self.options.inputdir, self.options.inputfile), 'r')
        lines = file.readlines()
        flag = ""
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
                flag = "taxonomy"

            elif (re.match("location", line)):
                flag = "location"
              
            elif (re.match("temporal", line)):
                flag = "temporal"
              
            # reads in lines of the form (a b c) where a is the parent
            # and b c are the children
            elif (re.match("\(.*\)", line)):
                if flag == "taxonomy":
                    taxonomy.addTaxaWithList(self, line)
                elif flag == "location":
                    self.addLocation(line)
                elif flag == "temporal":
                    self.addTemporal(line)
                else:
                    None

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
              
            elif (re.match("\<.*\>", line)):
                inside = re.match("\<(.*)\>", line).group(1)
                obs = re.split(" ", inside)
                if self.obslen == 0:
                    self.obslen = len(obs)
                elif self.obslen != len(obs):
                    print "Syntax error location / time information missing in observation protion"
                    return False
                if len(obs) < 2 or ( obs[1] !="P" and obs[1] != "N" ):
                    print "Syntax error in observation portion"
                    return False
                self.addObs(obs)
                
           # elif (re.match("\<.*\>", line)):
            #    inside = re.match("\<(.*)\>", line).group(1)
             #   hypElements = re.split("\s*\?\s*", inside)
              #  self.hypothesisType = hypElements[0]
               # hyp = hypElements[1]
               # hypArticulation = Articulation(hyp, self)
               # self.hypothesis = hypArticulation
                   
        return True              

    def addLocation(self, line):
        self.exploc = True
        noParens = re.match("\((.*)\)", line).group(1)
        if (noParens.find(" ") != -1):
            elements = re.split("\s", noParens)
            llist = [elements[0]]
            for index in range (1, len(elements)):
                llist.append(elements[index])
            self.location.append(llist)
        else:
            self.location.append([noParens]) 
        
    def addTemporal(self, line):
        self.exptmp = True
        noParens = re.match("\((.*)\)", line).group(1)
        if (noParens.find(" ") != -1):
            elements = re.split("\s", noParens)
            tlist = [elements[0]]
            for index in range (1, len(elements)):
                tlist.append(elements[index])
            self.temporal.append(tlist)
        else:
            self.temporal.append([noParens]) 
        
    def addObs(self, obsin):
        items = obsin[0].split("*")
        obs = []
        obsconcept = []
        for i in range(len(items)):
            if items[i].find("-") == -1:
                obsconcept.append([self.dotName2dlv(items[i]), "Y"])
            else:
                obsconcept.append([self.dotName2dlv(items[i]), "N"])
        obs.append(obsconcept)
        for i in range(1,self.obslen):
            obs.append(obsin[i])
        if self.obslen > 2:
            if not self.exploc:
                self.location.append(obsin[2])
            if self.obslen > 3 and not self.exptmp:
                self.temporal.append(obsin[3])
        self.obs.append(obs)

    #class Observation:
     #   def __init__(self, , flag):


    def dotName2dlv(self, dotName):
        elems = re.match("(.*)\.(.*)", dotName)
        return "c" + elems.group(1) + "_" + elems.group(2)
                     
    def dlvName2dot(self, dlvName):
        if(dlvName.find("_not_") != -1):
            elems = re.match("(.*)_not_(.*)", dlvName)
            conc1 = re.match("c(.*)_(.*)", elems.group(1))
            conc2 = re.match("c(.*)_(.*)", elems.group(2))
            return conc1.group(1) + "." + conc1.group(2) + "*~"\
                  +conc2.group(1) + "." + conc2.group(2)
        elif(dlvName.find("not_") != -1):
            elems = re.match("not_(.*)__(.*)", dlvName)
            conc1 = re.match("c(.*)_(.*)", elems.group(1))
            conc2 = re.match("c(.*)_(.*)", elems.group(2))
            return "~" + conc1.group(1) + "." + conc1.group(2) + "*"\
                  +conc2.group(1) + "." + conc2.group(2)
        elif(dlvName.find("__") != -1):
            elems = re.match("(.*)__(.*)", dlvName)
            conc1 = re.match("c(.*)_(.*)", elems.group(1))
            conc2 = re.match("c(.*)_(.*)", elems.group(2))
            return conc1.group(1) + "." + conc1.group(2) + "*"\
                  +conc2.group(1) + "." + conc2.group(2)
        else:
            elems = re.match("c(.*)_(.*)", dlvName)
            return elems.group(1) + "." + elems.group(2)
                     
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
	elif (len(r) == 4):
            if (r[2] == "lsum"):
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
        elif (len(r) == 5):
            if (r[3] == "l3sum"):
                self.addIMir(r[4], r[0], provenance)
                self.addIMir(r[4], r[1], provenance)
                self.addIMir(r[4], r[2], provenance)
                self.mir[r[0] + "," + r[4]] = rcc5["is_included_in"]
                self.mir[r[1] + "," + r[4]] = rcc5["is_included_in"]
                self.mir[r[2] + "," + r[4]] = rcc5["is_included_in"]
                self.tr.append([r[0],r[4], provenance])
                self.tr.append([r[1],r[4], provenance])
                self.tr.append([r[2],r[4], provenance])
                return None
            elif (r[1] == "r3sum"):
                self.addIMir(r[0], r[2], provenance)
                self.addIMir(r[0], r[3], provenance)
                self.addIMir(r[0], r[4], provenance)
                self.mir[r[0] + "," + r[2]] = rcc5["includes"]
                self.mir[r[0] + "," + r[3]] = rcc5["includes"]
                self.mir[r[0] + "," + r[4]] = rcc5["includes"]
                self.tr.append([r[2], r[0], provenance])
                self.tr.append([r[3], r[0], provenance])
                self.tr.append([r[4], r[0], provenance])
                return None
        elif (len(r) == 6):   
            if (r[4] == "l4sum"):
                self.addIMir(r[5], r[0], provenance)
                self.addIMir(r[5], r[1], provenance)
                self.addIMir(r[5], r[2], provenance)
                self.addIMir(r[5], r[3], provenance)
                self.mir[r[0] + "," + r[5]] = rcc5["is_included_in"]
                self.mir[r[1] + "," + r[5]] = rcc5["is_included_in"]
                self.mir[r[2] + "," + r[5]] = rcc5["is_included_in"]
                self.mir[r[3] + "," + r[5]] = rcc5["is_included_in"]
                self.tr.append([r[0],r[5], provenance])
                self.tr.append([r[1],r[5], provenance])
                self.tr.append([r[2],r[5], provenance])
                self.tr.append([r[3],r[5], provenance])
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
              if self.mir[pairkey] & relation["infer"]:
                hint = ",inferred,"
              else:
                hint = ",input,"
              if self.options.countOn:
                for i in range(5):
                  if self.mirc[pairkey][i] != 0:
                    fmir.write(pairkey+hint + findkey(relation, 1 << i)+","\
                               +self.mirc[pairkey][i].__str__()+","+self.npw.__str__()+"\n")
              else:
                fmir.write(pairkey+hint + findkey(relation, self.mir[pairkey] & ~relation["infer"])+"\n")
                if self.options.verbose:
                    print pairkey+hint + findkey(relation, self.mir[pairkey] & ~relation["infer"])+"\n"
            else:
                self.mir[pairkey] = self.getPairMir(pair)
                rl = findkey(relation, self.mir[pairkey])
                fmir.write(pairkey + ",inferred," + rl +"\n")
                if self.options.verbose:
                    print pairkey + ",inferred," + rl +"\n"
        fmir.close()

    def removeMir(self, string):
        r = string.split(" ")
	self.mir[r[0] + "," + r[len(r)-1]] = 0
	if(self.tr.count([r[0], r[len(r)-1], 0]) > 0):
	    self.tr.remove([r[0], r[len(r)-1], 0])
	elif(self.tr.count([r[len(r)-1], r[0], 0]) > 0):
	    self.tr.remove([r[len(r)-1], r[0], 0])
	if len(r) > 3:
	    if r[len(r)-2] == "+=":
	        self.mir[r[1] + "," + r[3]] = 0
		if(self.tr.count([r[1], r[3], 0]) > 0):
	    	    self.tr.remove([r[1], r[3], 0])
	    elif r[1] == "=+":
	        self.mir[r[0] + "," + r[2]] = 0
		if(self.tr.count([r[2], r[0], 0]) > 0):
	    	    self.tr.remove([r[2], r[0], 0])

 
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
                

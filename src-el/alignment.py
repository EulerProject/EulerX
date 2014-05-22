#
#       alignment.py
#
#  Alignment Module:
#    We define the alignment class here for taxonomy alignment
#    and dataset integration
#


import os
import time
import sets
import inspect
import itertools
import threading
import StringIO
import yaml
import string
import getpass
import socket
from taxonomy import * 
from alignment import * 
#from redWind import *
from template import *
from helper import *
from inputViz import *
from random import randint
from time import localtime, strftime

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
        self.basemir = {}                      # base MIR
        self.basetr = []                       # transitive reduction, only input taxonomies
        self.tr = []                           # transitive reduction, ie, < relation
        self.eq = {}                           # euqlities
        self.rules = {}
        self.taxonomies = {}                   # set of taxonomies
        self.articulations = []                # set of articulations
        self.map = {}                          # mapping between the concept name and its numbering
        self.baseAsp = ""                      # tmp string for the ASP input file
        self.baseCb = ""                       # tmp string for the combined concept ASP input file
        self.basePw = ""                       # tmp string for the ASP pw input file
        self.baseIx = ""                       # tmp string for the ASP ix input file
        self.pw = ""
        self.npw = 0                           # # of pws
        self.pwflag = True                     # Whether to output pw
        self.fixedCnt = 0                      # # of fixes /repairs
        self.inputVizNodes = {}                # nodes for input visualization in stylesheet 
        self.inputVizEdges = {}                # edges for input visualization in stylesheet
        self.rcgVizNodes = {}                  # nodes for rcg visualization in stylesheet
        self.rcgVizEdges = {}                  # edges for rcg visualization in stylesheet
        self.options = options
        if self.options.ieo:
            self.options.ie = True
        # If not input visualization, change the default valude of encode to "mnpw"
        if not self.options.inputViz and not self.options.encode:
            self.options.encode = "mnpw"
        self.enc = encode[options.encode]      # encoding
        self.name = os.path.splitext(os.path.basename(options.inputfile))[0]
        self.firstTName = ""                   # The abbrev name of the first taxonomy
        self.firstRcg = False
        self.trlist = []
        self.eqConLi = []                      # list of concepts that are equal
        self.runningUser = getpass.getuser()   # get the current username
        self.runningHost = socket.gethostname()# get the current host
        self.runningDate = strftime("%Y-%m-%d-%H:%M:%S", localtime())
        if options.outputdir is None:
            options.outputdir = os.path.join(options.inputdir, self.runningUser+"-"+self.runningHost+"-"+self.runningDate)
        if not os.path.exists(options.outputdir):
            os.mkdir(options.outputdir)
        self.aspdir = os.path.join(options.outputdir, "asp")
        if not os.path.exists(self.aspdir):
            os.mkdir(self.aspdir)
        self.pwfile = os.path.join(self.aspdir, self.name+"_pw."+self.options.reasoner)
        self.cbfile = os.path.join(self.aspdir, self.name+"_cb."+self.options.reasoner)
        self.pwswitch = os.path.join(self.aspdir, self.name+"_pwswitch."+self.options.reasoner)
        self.ixswitch = os.path.join(self.aspdir, self.name+"_ixswitch."+self.options.reasoner)
        self.ivout = os.path.join(options.outputdir, self.name+"_iv.dot")
        self.cbout = os.path.join(options.outputdir, self.name+"_cb.txt")
        self.obout = os.path.join(options.outputdir, self.name+"_ob.txt")
        self.mirfile = os.path.join(options.outputdir, self.name+"_mir.csv")
        self.pwoutputfile = os.path.join(options.outputdir, self.name+".pw")
        self.clfile = os.path.join(options.outputdir, self.name+"_cl.csv")
        self.cldot = os.path.join(options.outputdir, self.name+"_cl.dot")
        self.cldotpdf = os.path.join(options.outputdir, self.name+"_cl_dot.pdf")
        self.clneatopdf = os.path.join(options.outputdir, self.name+"_cl_neato.pdf")
        self.iefile = os.path.join(options.outputdir, self.name+"_ie.dot")
        self.iepdf = os.path.join(options.outputdir, self.name+"_ie.pdf")
        self.ivpdf = os.path.join(options.outputdir, self.name+"_iv.pdf")
        self.iv2dot = os.path.join(options.outputdir, self.name+".dot")
        self.iv2pdf = os.path.join(options.outputdir, self.name+".pdf")
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.stylesheetdir = self.path + "/../example_stylesheet/"
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            # possible world command
            self.com = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD 0 --eq=0 | "+self.path+"/muniq -u"
            # consistency command
            self.con = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD --eq=1"
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            # possible world command
            self.com = "dlv -silent -filter=rel "+self.pwfile+" "+ self.pwswitch+ " | "+self.path+"/muniq -u"
            # consistency command
            self.con = "dlv -silent -filter=rel -n=1 "+self.pwfile+" "+ self.pwswitch
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")


    def getTaxon(self, taxonomyName="", taxonName=""):
        if(self.options.verbose):
            print self.taxonomies, taxonomyName, taxonName
        taxonomy = self.taxonomies[taxonomyName]
        taxon = taxonomy.getTaxon(taxonName)
        return taxon

    def allPairsNeeded(self):
        return self.options.allRelations or len(self.taxonomies) == 1

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
        values = self.taxonomies.values()
        for taxonLoop in range(len(self.taxonomies)):
            thisTaxonomy = values[taxonLoop];
            theseTaxa = thisTaxonomy.taxa.values()
            for outerloop in range(len(theseTaxa)):
                for innerloop in range(outerloop+1, len(theseTaxa)):
                    newTuple = (theseTaxa[outerloop], theseTaxa[innerloop])
                    taxa.append(newTuple)
        return taxa

    def run(self):
        if self.options.inputViz:
            inputVisualizer = InputVisual.instance()
            inputVisualizer.run(self.options.inputdir, self.options.inputfile, self.ivout)
            commands.getoutput("dot -Tpdf "+self.ivout+" -o "+self.ivpdf)
	    if not self.enc:
		return
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
            self.genPW()
        elif self.enc & encode["ve"]:
            self.genVE()
        elif self.enc & encode["cb"]:
            self.pwflag = False
            self.genPW()
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
            self.pwflag = False
            self.genPW()

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
            if commands.getoutput(com).find("Models     : 0") != -1:
                return False
        else:
            com = "dlv -silent -filter=rel -n=1 "+self.pwfile+" "+self.pwswitch
            if commands.getoutput(com) == "":
                return False
        return True

    def inconsistencyExplanation(self):
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.pwfile+" "+ self.ixswitch+ " | claspD 1"
            ie = commands.getoutput(com)
            ie.replace(" ", ", ")
        else:
            com = "dlv -silent -filter=ie -n=1 "+self.pwfile+" "+self.ixswitch
            ie = commands.getoutput(com)
            ie.replace("{", "").replace("}", "")
        self.postProcessIE(ie);

    def postProcessIE(self, ie):
        print "Please see "+self.name+"_ie.pdf for the inconsistency relations between all the rules."
        if ie.find("{}") == -1 and ie != "":
            ies = ie.split(", ")
            # print ies
            ielist = []
            tmpmap = {}
            diagraw = sets.Set()
            for i in range(len(ies)):
              if ies[i].find("ie(prod") != -1:
                keylist = re.findall('[\d]+', ies[i])
                tmpmap[keylist.__str__()] = sets.Set(keylist)
              else:
                item = re.findall('[\d]+', ies[i])
                key = item[0]+","+item[len(item)-1]
                item = item[0:len(item)-1]
                value = sets.Set()
                if key in tmpmap.keys():
                  value = sets.Set(tmpmap[key])
                tmpmap[key] = value.union(sets.Set(item))
                #print key,tmpmap[key]

            # If white box approach, not need to invoke HST algorithm
            if not self.options.ieo:
               for key in tmpmap.keys():
                 #tmpset = sets.Set()
                 tmpset = tmpmap[key]
                 
                 addor  = True
                 for i in range(len(diagraw)):
                   if tmpset.issubset(list(diagraw)[i]):
                     a = []
                     a = list(diagraw)
                     a.pop(i)
                     a.insert(i,tmpset)
                     diagraw = sets.Set(a)
                   elif tmpset.issuperset(list(diagraw)[i]):
                     addor = False
                 if addor:
                     diagraw.add(tmpset)
               self.getDiag(diagraw)
               #print "Min inconsistent subsets: "
               #print diag
                
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
                label += key+" : "+self.rules[key]+"\t"
            fie.write("graph [label=\""+label+"\"]\n")
            fie.write("}")
            fie.close()
            commands.getoutput("dot -Tpdf "+self.iefile+" -o "+self.iepdf)

    def getDiag(self, raw):
        rawl = len(raw)
        rs = sets.Set()
        print raw
        for i in range(rawl):
           rs = rs.union(raw.pop())
        print rs
        artSet = self.getArtSetFromN(rs)
        self.allJustifications(artSet)

    def getArtSetFromN(self, rs):
        artSet = sets.Set()
        for i in range(len(self.articulations)):
            if self.articulations[i].ruleNum.__str__() in rs:
                artSet.add(self.articulations[i])
        return artSet

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
            pwTm.mir = [] #pwTm.basemir
            pwTm.tr = [] #pwTm.basetr

            outputstr += "\nPossible world "+i.__str__()+":\n{"
            items = pws[i].split(" ")
            outputstr += pws[i]
            outputstr += "}\n"
        print outputstr

    def isPwNone(self):
        return self.isNone(self.pw)

    def isCbNone(self):
        return self.isNone(self.cb)

    def isNone(self, output):
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            return output.find("Models     : 0 ") != -1
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            return output.strip() == ""
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")

    def genPW(self):
        self.pw = commands.getoutput(self.com)
        if self.isPwNone():
            print "************************************"
            print "Input is inconsistent"
            if self.options.ie:
                self.inconsistencyExplanation()
            self.remedy()
            return
        if self.pw.lower().find("error") != -1:
            raise Exception(template.getEncErrMsg())
        #if not self.pwflag: return None
        self.intOutPw(self.name, self.pwflag)
        self.genMir()

    #
    # Internal routine with several callers
    #
    def intOutPw(self, name, pwflag):
        pws = []
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            raw = self.pw.split("\n")
            ## Filter out those trash in the gringo output
            for i in range(2, len(raw) - 2):
                if raw[i].find("rel") == -1: continue
                pws.append(raw[i].strip().replace(") ",");"))
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            raw = self.pw.replace("{","").replace("}","").replace(" ","").replace("),",");")
            if raw != "":
              pws = raw.split("\n")
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")
        self.npw = len(pws)
        self.outPW(name, pws, pwflag, "rel")

    def outPW(self, name, pws, pwflag, ss):
        outputstr = ""
        # mirs for each pw
        if self.options.cluster: pwmirs = []
        rcgAllDotFile = os.path.join(self.options.outputdir, self.name+"_all.dot")
        rcgAllPdfFile = os.path.join(self.options.outputdir, self.name+"_all.pdf")
        fAllDot = open(rcgAllDotFile, 'w')
        for i in range(len(pws)):
            if self.options.cluster: pwmirs.append({})

            # pwTm is the possible world taxonomy mapping, used for RCG
            pwTm = copy.deepcopy(self)
            if i == 0:
                pwTm.firstRcg = True
            else:
                pwTm.firstRcg = False
            if self.enc & encode["cb"]:
                if self.options.hideOverlaps:
                  pwTm.tr = []
                  pwTm.mir = {}
                # if not hiding orignal concepts, basetr is useful
                else:
                  pwTm.tr = pwTm.basetr
                  pwTm.mir = pwTm.basemir

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
                    pwTm.addEqMap(dotc1, dotc2)
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
                pwTm.genPwRcg(name + "_" + i.__str__() + "_" + self.options.encode)
                #pwTm.genPwCb(name + "_" + i.__str__())
                for e in pwTm.tr:
                    self.trlist.append(e)
        self.genAllPwRcg(len(pws))
        fAllDot.close()
        commands.getoutput("dot -Tpdf "+rcgAllDotFile+" -o "+rcgAllPdfFile)
        if self.options.reduction:
            outputstr = self.uncReduction(pws)
        if pwflag:
            if self.options.output: print outputstr
#        fpw = open(self.options.outputdir+name+".pw", 'w')
        fpw = open(self.pwoutputfile, 'w')
        fpw.write(outputstr)
        fpw.close()
        if self.options.cluster: self.genPwCluster(pwmirs, False)

    def genPwCb(self, fileName):
        self.name = fileName
        self.cbfile = os.path.join(self.aspdir, self.name+"_cb.asp")
        self.genCbConcept()
        fcb = open(self.cbfile, 'w')
        fcb.write(self.baseCb)
        fcb.close()
        self.genCB()

    def genPwRcg(self, fileName):
#        fDot = open(self.options.outputdir+fileName+".dot", 'w')
#        fAllDot = open(self.options.outputdir+self.name+"_all.dot", 'a')
        rcgAllFile = os.path.join(self.options.outputdir, self.name+"_all.dot")
        fAllDot = open(rcgAllFile, 'a')
#        fDot.write("digraph {\n\nrankdir = RL\n\n")
        if self.firstRcg:
            fAllDot.write("digraph {\n\nrankdir = RL\n\n")
        tmpCom = ""    # cache of combined taxa
        taxa1 = ""     # cache of taxa in the first taxonomy
        taxa2 = ""     # cache of taxa in the second taxonomy
        tmpComLi = [] # cache of list of combined taxa for --rcgo option in RCG
        replace1 = "" # used for replace combined concept in --rcgo option in RCG
        replace2 = "" # used for replace combined concept in --rcgo option in RCG
        rcgVizNodes = {} # used for rcg nodes visualization in stylesheet
        rcgVizEdges = {} # used for rcg edges visualization in stylesheet

        alias = {}
        
        # Equalities
        for T1 in self.eq.keys():
            # self.eq is dynamically changed, so we need this check
            if not self.eq.has_key(T1):
                continue
            tmpStr = ""
#            blueNode = False
            T1s = T1.split(".")
            for T2 in self.eq[T1]:
                T2s = T2.split(".")
#                if(T1s[1] == T2s[1]):
#                    blueNode = True
#                else:
                if tmpStr != "":
                    tmpStr = "\\n" + tmpStr
                tmpStr = T2 + tmpStr
            if tmpStr != "":
                tmpStr = "\\n" + tmpStr + "\\n"
#                if tmpStr.split(".")[0]  == self.firstTName:
#                    tmpStr = tmpStr + "\\n"
#                else:
#                    tmpStr = "\\n" + tmpStr
#            if blueNode:
#                tmpStr = T1s[1] + tmpStr
#                # fDot.write("\"" + tmpStr +"\" [color=blue];\n")
#                # fAllDot.write("\"" + tmpStr +"\" [color=blue];\n")
#            else:
            if T1s[0] == self.firstTName:
                tmpStr = T1 + tmpStr
            else:
                tmpStr = tmpStr + T1
            if tmpStr[0:2] == "\\n": tmpStr = tmpStr[2:]
            if tmpStr[-2:] == "\\n": tmpStr = tmpStr[:-2]
            self.eqConLi.append(tmpStr)

            tmpeqConLi2 = []
            for T in self.eqConLi:
                tmpeqConLi2.append(T)

            for T10 in tmpeqConLi2:
                for T11 in tmpeqConLi2:
                    if T10 != T11:
                        tmpC = []
                        ss = ""
                        T10s = T10.split("\\n")
                        T11s = T11.split("\\n")
                        for c1 in T10s:
                            if c1 in T11s:
                                tmpC = T10s + T11s
                                tmpC.sort()
                                self.remove_duplicate_string(tmpC)
                                for e in tmpC:
                                    ss = ss + e + "\\n"
                                ss = ss[:-2]
                                if T10 in self.eqConLi:
                                    self.eqConLi.remove(T10)
                                if T11 in self.eqConLi:
                                    self.eqConLi.remove(T11)
                                if ss not in self.eqConLi:
                                    self.eqConLi.append(ss)
                                break 

            for T2 in self.eq[T1]:
#                if self.eq.has_key(T2):
#                    del self.eq[T2]
                tmpTr = list(self.tr)
                for [T3, T4, P] in tmpTr:
                    if(T1 == T3 or T2 == T3):
                      if self.tr.count([T3, T4, P]) > 0:
                        self.tr.remove([T3, T4, P])
                        self.tr.append([tmpStr, T4, 0])
                    elif(T1 == T4 or T2 == T4):
                      if self.tr.count([T3, T4, P]) > 0:
                        self.tr.remove([T3, T4, P])
                        self.tr.append([T3, tmpStr, 0])
                    for T5 in self.eqConLi:
#                        if(T5 == T3 and T5 != tmpStr and set(T5.split("\\n")).issubset(set(tmpStr.split("\\n")))):
                        if(T3 != T5 and set(T3.split("\\n")).issubset(set(T5.split("\\n")))):
                          if self.tr.count([T3, T4, P]) > 0:
                            self.tr.remove([T3, T4, P])
                            self.tr.append([T5,T4,0])
                        elif(T4 != T5 and set(T4.split("\\n")).issubset(set(T5.split("\\n")))):
#                        elif(T5 == T4 and T5 != tmpStr and set(T5.split("\\n")).issubset(set(tmpStr.split("\\n")))):
                          if self.tr.count([T3, T4, P]) > 0:
                            self.tr.remove([T3, T4, P])
                            self.tr.append([T3,T5,0])
        tmpeqConLi = []
#        print "self.eqConLi=", self.eqConLi
        for T in self.eqConLi:
            tmpeqConLi.append(T)
        for T6 in tmpeqConLi:
            for T7 in tmpeqConLi:
                if (set(T6.split("\\n")).issubset(set(T7.split("\\n"))) and T6 != T7 and T6 in self.eqConLi):
                    self.eqConLi.remove(T6)
        
        tmpTr = list(self.tr)
        for T in self.eqConLi:
            #for [T1, T2, P] in tmpTr:
            #    if T == T1 or T == T2:
            tmpComLi.append(T)
            tmpCom += "  \""+T+"\"\n"      
            
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
            
        # Node Coloring (Creating dot file, will be replaced by stylesheet processor)
        for [T1, T2, P] in self.tr:
            if(T1.find("*") == -1 and T1.find("\\") == -1 and T1.find("\\n") == -1 and T1.find(".") != -1):
                T1s = T1.split(".")
                if self.firstTName == T1s[0]:
                    taxa1 += "  \""+T1+"\"\n"               # used in old viz
                else:
                    taxa2 += "  \""+T1+"\"\n"
                self.addRcgVizNode(T1s[1], T1s[0])          # used in stylesheet
            else:
                tmpComLi.append(T1)
                tmpCom += "  \""+T1+"\"\n"
                self.addRcgVizNode(T1, "comb")
            if(T2.find("*") == -1 and T2.find("\\") == -1 and T2.find("\\n") == -1 and T2.find(".") != -1):
                T2s = T2.split(".")
                if self.firstTName == T2s[0]:
                    taxa1 += "  \""+T2+"\"\n"
                else:
                    taxa2 += "  \""+T2+"\"\n"
                self.addRcgVizNode(T2s[1], T2s[0])
            else:
                tmpComLi.append(T2)
                tmpCom += "  \""+T2+"\"\n"
                self.addRcgVizNode(T2, "comb")
                
        # Dot drawing used for old viz
#        fDot.write("  node [shape=box style=\"filled\" fillcolor=\"#CCFFCC\"]\n")
#        fDot.write(taxa1)
#        fDot.write("  node [shape=octagon style=\"filled\" fillcolor=\"#FFFFCC\"]\n")
#        fDot.write(taxa2)
#        fDot.write("  node [shape=Msquare style=\"filled\" fillcolor=\"#EEEEEE\"]\n")
#        fDot.write(tmpCom)
        fAllDot.write("  node [shape=box style=\"filled\" fillcolor=\"#CCFFCC\"]\n")
        fAllDot.write(taxa1)
        fAllDot.write("  node [shape=octagon style=\"filled\" fillcolor=\"#FFFFCC\"]\n")
        fAllDot.write(taxa2)
        fAllDot.write("  node [shape=Msquare style=\"filled\" fillcolor=\"#EEEEEE\"]\n")
        fAllDot.write(tmpCom)
        fAllDot.close()
        
        for [T1, T2, P] in self.tr:
    	    if(P == 0):
#    	    	fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled, color=black];\n")       # used in old viz
                self.addRcgVizEdge(T1, T2, "input")
    	    elif(P == 1):
#    	    	fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled, color=red];\n")
                self.addRcgVizEdge(T1, T2, "inferred")
    	    elif(P == 2):
                if False:
#                    fDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=dashed, color=grey];\n")
                    self.addRcgVizEdge(T1, T2, "redundant")
        if self.options.rcgo:
#            fDot.write("  subgraph ig {\nedge [dir=none, style=dashed, color=blue, constraint=false]\n\n")
            oskiplist = []
            for key in self.mir.keys():
                if self.mir[key] == rcc5["overlaps"] and key not in oskiplist: # and key not in oskiplist
                    item = re.match("(.*),(.*)", key)
                    replace1 = item.group(1)
                    replace2 = item.group(2)
                    for comb in tmpComLi:
                        if item.group(1) in comb.split("\\n"):
                            replace1 = comb
                            break
                    for comb in tmpComLi:
                        if item.group(2) in comb.split("\\n"):
                            replace2 = comb
                            break                            
#                    fDot.write("     \"" + item.group(1) + "\" -> \"" + item.group(2) + "\"\n")
#                    fDot.write("     \"" + replace1 + "\" -> \"" + replace2 + "\"\n")
                    self.addRcgVizEdge(replace1, replace2, "overlaps")
                    # Skip the reverse pair for redundant edges
                    oskiplist.append(item.group(2)+","+item.group(1))
#            fDot.write("  }\n")
        #fDot.write("  subgraph cluster_lg {\n")
        #fDot.write("    rankdir = LR\n")
        #fDot.write("    label = \"Legend\";\n")
        #fDot.write("    A1 -> B1 [label=\"is included in (given)\" style=filled, color=black]\n")
        #fDot.write("    A2 -> B2 [label=\"is included in (inferred)\" style=filled, color=red]\n")
        #fDot.write("    A3 -> B3 [label=\"overlaps\" dir=none, style=dashed, color=blue]\n")
        #fDot.write("  }\n")
#        fDot.write("}\n")
#        fDot.close()
#        commands.getoutput("dot -Tpdf "+self.options.outputdir+fileName+".dot -o "+self.options.outputdir+fileName+".pdf")
        
        # create the yaml file
        rcgYamlFile = os.path.join(self.options.outputdir, fileName+".yaml")
        rcgDotFile = os.path.join(self.options.outputdir, fileName+".dot")
        rcgPdfFile = os.path.join(self.options.outputdir, fileName+".pdf")
        fRcgVizYaml = open(rcgYamlFile, 'w')
        fRcgVizYaml.write(yaml.safe_dump(self.rcgVizNodes, default_flow_style=False))
        fRcgVizYaml.write(yaml.safe_dump(self.rcgVizEdges, default_flow_style=False))
        fRcgVizYaml.close()
        
        # apply the rcgviz stylesheet
#        commands.getoutput("cat "+self.options.outputdir+fileName+".yaml"+" | y2d -s "+self.stylesheetdir+"rcgstyle.yaml" + ">" + self.options.outputdir+fileName+".dot")
        commands.getoutput("cat "+rcgYamlFile+" | y2d -s "+self.stylesheetdir+"rcgstyle.yaml" + ">" + rcgDotFile)
        commands.getoutput("dot -Tpdf "+rcgDotFile+" -o "+rcgPdfFile)


    def bottomupRemedy(self):
        first = True
        fixedOpt = []
        fixedCnt = 0
        # local copy of articulations
        tmpart = copy.deepcopy(self.articulations)
        s = len(self.articulations)
        for i in range(s-1, 0, -1):
            fixed = False
            first = True
            tmpl = list(itertools.combinations(range(s), i))
            for k in range(len(tmpl)):
                a = []
                for j in range(i):
                    a.append(self.articulations.pop(tmpl[k][j] - j))
                # Now refresh the input file
                self.genASP()
    	        # Run the reasoner again
                self.pw = commands.getoutput(self.con)
                if not self.isPwNone():
                    fixed = True
                    if first:
                        first = False
                        fixedCnt = 1
                        fixedOpt = []
                        fixedOpt.append(a)
                    else:
                        fixedCnt += 1
                        fixedOpt.append(a)
                else:
                    if k == len(tmpl)-1 and not fixed:
                        for l in range(fixedCnt):                   
                            print "**", self.pw, "**"
                            print "************************************"
                            print "Repair option ",l,": remove problematic articulation [",
                            a = fixedOpt[l]
                            for j in range(i):
                                # Remove mir is not needed because it will be reset anyways
                                # if l == 0: self.removeMir(a[j].string)
                                if j != 0: print ",",
                                print a[j].string,
                            print "]"
                            print "************************************"
                            fixed = True
                self.articulations = copy.deepcopy(tmpart)
        if not fixed: return True
        for l in range(fixedCnt):                   
            print "************************************"
            print "Repair option ",l,": remove problematic articulation [",
            a = fixedOpt[l]
            for j in range(i):
                # Remove mir is not needed because it will be reset anyways
                # if l == 0: self.removeMir(a[j].string)
                if j != 0: print ",",
                print a[j].string,
            print "]"
            print "************************************"
        return True

    def allJustifications(self, artSet):
        s = sets.Set()
        curpath = sets.Set()
        allpaths = sets.Set()
        self.computeAllJust(artSet, s, curpath, allpaths)
        
    def computeAllJust(self, artSet, justSet, curpath, allpaths):
        for path in allpaths:
            if path.issubset(curpath):
                return
        if self.isConsistent(artSet):
            allpaths.add(curpath)
            return
        j = sets.Set()
        for s in justSet:
            if len(s.intersection(curpath)) == 0:
                j = s
        if len(j) == 0:
            j = self.computeOneJust(artSet)
            if len(j) != 0:
                lj = list(j)
                print "************************************"
                print "Min inconsistent subset ",self.fixedCnt,": [",
                for i in range(len(lj)):
                    if i != 0: print ",",
                    print lj[i].ruleNum,":",lj[i].string,
                print "]"
                print "************************************"
                self.fixedCnt += 1
        if len(j) != 0:
            justSet.add(j)
        for a in j:
            tmpcur = copy.copy(curpath)
            tmpcur.add(a)
            tmpart = copy.copy(artSet)
            tmpart.remove(a)
            self.computeAllJust(tmpart, justSet, tmpcur, allpaths)
            
    def isConsistent(self, artSet):
        tmpart1 = copy.copy(self.articulations)
        tmpmir = copy.deepcopy(self.mir)
        tmptr = copy.deepcopy(self.tr)
        tmpeq = copy.deepcopy(self.eq)
	if len(artSet) == 0:
            return True
        self.articulations = []
        self.mir = copy.deepcopy(self.basemir)
        self.tr = copy.deepcopy(self.basetr)
        self.eq = {}
        tmpart = copy.copy(artSet)
        for i in range(len(artSet)):
            self.addArticulation(tmpart.pop().string)
        # Now refresh the input file
        self.genASP()
    	# Run the reasoner again
        self.pw = commands.getoutput(self.con)

        self.articulations = tmpart1
        self.mir = tmpmir
        self.tr = tmptr
        self.eq = tmpeq

        if not self.isPwNone():
            return True
        return False

    def computeOneJust(self, artSet):
        if self.isConsistent(artSet):
            return sets.Set()
        return self.computeJust(sets.Set(), artSet)

    # TODO move to generic header
    def printArtRuleN(self, artSet, prefix):
        print prefix+"= ",
        for i in range(len(artSet)):
          print list(artSet)[i].ruleNum,
        print ""

    # s is consistent, f is inconsistent
    def computeJust(self, s, f):
        if len(f) <= 1:
            return f
        f1 = copy.copy(f)
        f2 = sets.Set()
        for i in range(len(f) /2):
            f2.add(f1.pop())
        if not self.isConsistent(s.union(f1)):
            return self.computeJust(s, f1)
        if not self.isConsistent(s.union(f2)):
            return self.computeJust(s, f2)
        sl = self.computeJust(s.union(f1), f2)
        sr = self.computeJust(s.union(sl), f1)
        return sl.union(sr)

    def minInconsRemedy(self):
        fixed = False      # Whether we find a way to fix it or not
        fixedCnt = 0       # How many ways to fix the inconsistency
        # local copy of articulations
        tmpart = copy.deepcopy(self.articulations)
        tmpmir = copy.deepcopy(self.mir)
        tmptr = copy.deepcopy(self.tr)
        tmpeq = copy.deepcopy(self.eq)

        s = len(self.articulations)
        for i in range(2, s):
            tmpl = list(itertools.combinations(range(s), i))
            for k in range(len(tmpl)):
                self.articulations = []
                self.mir = self.basemir
                self.tr = self.basetr
                self.eq = {}
                for j in range(i):
                    self.addArticulation(tmpart[tmpl[k][j]].string)
                # Now refresh the input file
                self.genASP()
    	        # Run the reasoner again
                self.pw = commands.getoutput(self.con)
                if self.isPwNone():
                    print "************************************"
                    print "Min inconsistent subset ",fixedCnt,": [",
                    for j in range(i):
                        if j != 0: print ",",
                        print self.articulations[j].string,
                    print "]"
                    print "************************************"
                    fixed = True
                    # self.intOutPw(self.name+"_fix_"+fixedCnt.__str__(), False)
                    fixedCnt += 1
                # self.articulations = copy.deepcopy(tmpart)
                # self.mir = copy.deepcopy(tmpmir)
                # self.tr = copy.deepcopy(tmptr)
                # self.eq = copy.deepcopy(tmpeq)
            if fixed : return True

    def topdownRemedy(self):
        fixed = False      # Whether we find a way to fix it or not
        fixedCnt = 0       # How many ways to fix the inconsistency
        # local copy of articulations
        tmpart = copy.deepcopy(self.articulations)
        tmpmir = copy.deepcopy(self.mir)
        tmptr = copy.deepcopy(self.tr)
        tmpeq = copy.deepcopy(self.eq)

        s = len(self.articulations)
        for i in range(1, s):
            tmpl = list(itertools.combinations(range(s), i))
            for k in range(len(tmpl)):
                a = []
                for j in range(i):
                    a.append(self.articulations.pop(tmpl[k][j] - j))
                # Now refresh the input file
                self.genASP()
    	        # Run the reasoner again
                self.pw = commands.getoutput(self.con)
                if not self.isPwNone():
                    print "************************************"
                    print "Repair option ",fixedCnt,": remove problematic articulation [",
                    for j in range(i):
                        # Remove mir is not needed because it will be reset anyways
                        self.removeMir(a[j].string)
                        if j != 0: print ",",
                        print a[j].string,
                    print "]"
                    print "************************************"
                    fixed = True
                    self.intOutPw(self.name+"_fix_"+fixedCnt.__str__(), False)
                    fixedCnt += 1
                self.articulations = copy.deepcopy(tmpart)
                self.mir = copy.deepcopy(tmpmir)
                self.tr = copy.deepcopy(tmptr)
                self.eq = copy.deepcopy(tmpeq)
            if fixed : return True
        print "Don't know how to repair"
        print "************************************"
        return False


    def remedy(self):
        # Begin repairing
        if self.options.repair == "simple":
            self.simpleRemedy()
        elif self.options.repair == "bottomup":
            self.bottomupRemedy()
        elif self.options.repair == "minIncSubset":
            self.minInconsRemedy()
        elif self.options.repair == "HST":
            self.allJustifications(sets.Set(self.articulations))
        # By default, we use top down remedy to repair
        else:
            self.topdownRemedy()

    def simpleRemedy(self):
        s = len(self.articulations)
        for i in range(s):
            a = self.articulations.pop(i)    
            # Now refresh the input file
            self.genASP()
    	    # Run the reasoner again
            self.pw = commands.getoutput(self.con)
            if not self.isPwNone():
                # Remove mir is not needed because it will be reset anyways
                self.removeMir(a.string)
                print "************************************"
                print "Repairing: remove problematic articulation [" + a.string + "]"
                print "************************************"
                return True
            self.articulations.insert(i, a)
        print "Don't know how to repair"
        print "************************************"
        return False

    def uncReduction(self, pws):
        #ppw = sets.Set()
        #for pair in self.mir.keys():
        #    if self.mir[pair] & ~relation["infer"] not in rcc5.values():
        #        userAns = RedWindow(pair, self.mir[pair])
        #        self.mir[pair] = userAns.main()
        #        self.adjustMirc(pair)
        #        # Reduce pws
        #        tmpppw = sets.Set()
        #        for i in range(5):
        #          rel = 1 << i
        #          if self.mir[pair] & rel and pair+","+rel.__str__() in self.mirp.keys():
        #            for pw in self.mirp[pair+","+rel.__str__()]:
        #                tmpppw.add(pw)
        #        # Adjust mir
        #        for tmppair in self.mir.keys():
        #          for j in range(5):
        #            relj = 1 << j
        #            if tmppair+","+relj.__str__() in self.mirp.keys() and\
        #               pw in self.mirp[tmppair+","+relj.__str__()]:
        #              if len(tmpppw) ==1:
        #                self.mir[tmppair] = relj
        #              else:
        #                self.mir[tmppair] |= relj
        #        if len(tmpppw) != 0:
        #          if len(ppw) == 0:
        #            ppw = tmpppw
        #          else:
        #            ppw = ppw.intersection(tmpppw)
        #        else:
        #          print "Inconsistent again !!"
        #          ppw = tmpppw
        outputstr = ""
        #for i in ppw:
        #    if self.options.cluster: pwmirs.append({})
        #    outputstr += "Possible world "+i.__str__()+": {"
        #    items = pws[i].split(";")
        #    for j in range(len(items)):
        #        rel = items[j].replace("rel(","").replace(")","").split(",")
        #        dotc1 = self.dlvName2dot(rel[0])
        #        dotc2 = self.dlvName2dot(rel[1])
        #        if j != 0: outputstr += ", "
        #        outputstr += dotc1+rel[2]+dotc2
        #    outputstr += "}\n"
        #return outputstr

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
        fcldot.write("  node [shape=box style=\"filled, rounded\" fillcolor=\"#FFFFCC\"]\n")
        dmatrix = []
        for i in range(self.npw):
            dmatrix.append([])
            for j in range(i+1):
                if i == j :
                    dmatrix[i].append(0)
                    fcl.write("0 "); continue
                d = 0
                s = ""
                if obs:
                    for ob in pws[i]:
                        if ob not in pws[j]: d += 1
                    for ob in pws[j]:
                        if ob not in pws[i]: d += 1
                else:
                    for key in pws[i].keys():
                        if pws[i][key] != pws[j][key]: 
                            s = s + key\
                                  + " " + findkey(relation, pws[i][key]).__str__()\
                                  + " " + findkey(relation, pws[j][key]).__str__() + ";"
                            d += 1
                fcl.write(d.__str__()+" ")
                dmatrix[i].append(d)
                if i != j and not self.options.simpCluster:
                    fcldot.write("\"pw"+i.__str__()+"\" -- \"pw"+j.__str__()+\
                            "\" [label=\""+d.__str__()+"; "+s+"\",len="+d.__str__()+"]\n")
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
        print pws
        if self.options.cluster: pwobs = []
        for i in range(len(pws)):
            if pws[i].find("pp(") == -1: continue
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
            self.com = "gringo "+self.cbfile+" "+ self.pwswitch+ " | claspD 0 --eq=0"
            self.cb = commands.getoutput(self.com)
            if self.isCbNone():
                self.remedy()
            if self.cb.find("ERROR") != -1:
                print self.cb
                raise Exception(template.getEncErrMsg())
            raw = self.cb.split("\n")
            if self.options.verbose: print raw
            ## Filter out those trash in the gringo output
            for i in range(2, len(raw) - 2, 2):
                pws.append(raw[i].strip().replace(") ",");"))
                if self.options.verbose: print pws
        elif reasoner[self.options.reasoner] == reasoner["dlv"]:
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.com = "dlv -silent -filter=relout "+self.cbfile+" "+ self.pwswitch + " | "+path+"/muniq -u"
            self.cb = commands.getoutput(self.com)
            if self.isCbNone():
                self.remedy()
            if self.cb.find("error") != -1:
                print self.cb
                raise Exception(template.getEncErrMsg())
                return None
            raw = self.cb.replace("{","").replace("}","").replace(" ","").replace("),",");")
            if raw != "":
              pws = raw.split("\n")
        else:
            raise Exception("Reasoner:", self.options.reasoner, " is not supported !!")
        self.npw = len(pws)
        self.outPW(self.name, pws, self.options.output, "relout")
 
    def genASP(self):
        self.genAspConcept()
        self.genAspPC()
        self.genAspAr()
        if self.enc & encode["vr"] or self.enc & encode["dl"] or self.enc & encode["mn"]:
            self.genAspDc()
        if self.obs != [] and self.enc & encode["ob"]:
            self.genAspObs()
        fdlv = open(self.pwfile, 'w')
        fdlv.write(self.baseAsp)
        fdlv.close()
        pdlv = open(self.pwswitch, 'w')
        idlv = open(self.ixswitch, 'w')
        pdlv.write(self.basePw)
        pdlv.write("pw.")
        if self.options.hideOverlaps:
            pdlv.write("\nhide.")
        pdlv.write(self.baseIx)
        idlv.write("ix.")
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            if self.enc & encode["ob"]:
                pdlv.write("\n#hide.\n#show pp/" + self.obslen.__str__() + ".")
            elif self.enc & encode["pw"]:
                pdlv.write("\n#hide.\n#show rel/3.")
            elif self.enc & encode["cb"]:
                pdlv.write("\n#hide.\n#show relout/3.")
            idlv.write("\n#hide.\n#show ie/1.")
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
                        #if self.mirp.has_key(t1.dotName()+","+t2.dotName()+","+rcc5["overlaps"].__str__()) or\
                        #   self.mirp.has_key(t2.dotName()+","+t1.dotName()+","+rcc5["overlaps"].__str__()):
                        p1 = t1.dotName()+","+t2.dotName()
                        p2 = t2.dotName()+","+t1.dotName()
                        if self.mir.has_key(p1) and self.mir[p1] & rcc5["overlaps"] or\
                           self.mir.has_key(p2) and self.mir[p2] & rcc5["overlaps"]:
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
	    self.baseAsp  = "%%% Max Number of Euler Regions\n"
	    self.baseAsp += "#maxint=" + maxint.__str__() + ".\n\n"
	    self.baseAsp += "%%% Euler Regions\n"
	    self.baseAsp += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseAsp += con
	    self.baseAsp += "%%% Euler Bit\n"
	    self.baseAsp += "bit(M, V):-r(M),#mod(M," + int(num).__str__() + ",V).\n\n"
            self.baseAsp += template.getAspDlCon()
        elif self.enc & encode["mn"]:
            if len(self.taxonomies) == 1:
                raise Exception("Polynomial encoding is not applicable for singleton taxonomy" +\
                                " please use binary encoding for singleton example: eg. vrpw, vrve !!")
            maxint = prod
            if reasoner[self.options.reasoner] == reasoner["dlv"]:
	        self.baseAsp  = "%%% Max Number of Euler Regions\n"
	        self.baseAsp += "#maxint=" + maxint.__str__() + ".\n\n"
	        self.baseAsp += "%%% Euler Regions\n"
	        self.baseAsp += "r(M):- #int(M),M>=1,M<=#maxint.\n\n"

	        self.baseAsp += con

	        self.baseAsp += "\n%%% Euler Bit\n"
                for i in range(len(couArray)):
	            self.baseAsp += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", #mod(M1," + couArray[i].__str__() + ",V).\n"

            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
	        self.baseAsp  = "%%% Euler regions\n"
	        self.baseAsp += "r(1.."+maxint.__str__()+").\n\n"
	        self.baseAsp += con

	        self.baseAsp += "%%% Euler Bit\n"
                for i in range(len(couArray)):
	            self.baseAsp += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", V = M1 #mod " + couArray[i].__str__() + ".\n"
            self.baseAsp += template.getAspMnCon()

        elif self.enc & encode["vr"]:
            maxint = int(2**num)
            if reasoner[self.options.reasoner] == reasoner["dlv"]:
	        self.baseAsp = "#maxint=" + maxint.__str__() + ".\n\n"
	        self.baseAsp += "%%% regions\n"
	        self.baseAsp += "r(M):- #int(M),M>=0,M<#maxint.\n\n"
	        self.baseAsp += "%%% count of concepts\n"
	        self.baseAsp += "count(N):- #int(N),N>=0,N<"+num.__str__()+".\n\n"
	        self.baseAsp += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
	        self.baseAsp += con
            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
                # TODO vrpw may not be working for gringo, gringo 4 may be needed
                # raise Exception("Reasoner: vrpw is not supported for gringo !!")
	        self.baseAsp  = "%%% Euler regions\n"
	        self.baseAsp += "r(0.."+(maxint-1).__str__()+").\n\n"
	        self.baseAsp += "%%% count of concepts\n"
	        self.baseAsp += "count(0.."+(num-1).__str__()+").\n\n"
	        self.baseAsp += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P, 0 = M1 #mod 2.\n"
	        self.baseAsp += con
            self.baseAsp += template.getAspVrCon()

        elif self.enc & encode["direct"]:
            self.baseAsp  = con
            self.baseAsp += template.getAspDrCon()

        else:
            print "EXCEPTION: encode ",self.options.encode," not defined!!"

    def genAspPC(self):
        self.baseAsp += "\n%%% Parent-Child relations\n"
        for key in self.taxonomies.keys():
            queue = copy.deepcopy(self.taxonomies[key].roots)
            while len(queue) != 0:
                if self.options.verbose:
                    print "PC: ",queue
                t = queue.pop(0)
                # This is a nc flag
                if t.abbrev == "nc":
	            self.baseAsp += "ncf(" + t.dlvName() + ").\n"
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
			    self.baseAsp += "ir(X, r" + ruleNum.__str__() +") :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X), pw.\n"
		            self.baseAsp += "ir(X, prod(r" + ruleNum.__str__() + ",R)) :- in(" + t1.dlvName() + ",X), out3(" + t.dlvName() + ", X, R), ix.\n" 
                            if t1.abbrev.find("nc") == -1:
                              if reasoner[self.options.reasoner] == reasoner["dlv"]:
			          self.baseAsp += ":- #count{X: vrs(X), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X)} = 0, pw.\n"
                              elif reasoner[self.options.reasoner] == reasoner["gringo"]:
			          self.baseAsp += ":- [vrs(X): in(" + t1.dlvName() + ", X): in(" + t.dlvName() + ", X)]0.\n"
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
                                  if t.children[i].abbrev.find("nc") == -1:
				    self.baseAsp += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2+ ", X)} = 0, pw.\n"
                                  if t.children[j].abbrev.find("nc") == -1:
				    self.baseAsp += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2+ ", X)} = 0, pw.\n"
                                elif reasoner[self.options.reasoner] == reasoner["gringo"]:
                                  if t.children[i].abbrev.find("nc") == -1:
				    self.baseAsp += ":- [vrs(X): in(" + name1 + ", X): out(" + name2+ ", X)]0, pw.\n"
                                  if t.children[j].abbrev.find("nc") == -1:
				    self.baseAsp += ":- [vrs(X): out(" + name1 + ", X): in(" + name2+ ", X)]0, pw.\n"
                                if t.children[i].abbrev.find("nc") == -1:
			            self.baseAsp += "pie(r" + ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
			            self.baseAsp += "c(r" + ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                                if t.children[j].abbrev.find("nc") == -1:
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
            self.baseAsp += self.articulations[i].toASP(self.options.encode, self.options.reasoner, self)+ "\n"

    def genAspDc(self):
        self.baseCb  += self.baseAsp
        if self.allPairsNeeded():
            self.baseAsp += template.getAspAllDc()
        else:
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
        
        # used for input viz
        group2concepts = {}
        art = []
        
        for line in lines:

            if (re.match("taxonomy", line)):
                taxName = re.match("taxonomy (.*)", line).group(1) 
                taxonomy = Taxonomy()
                if (taxName.find(" ") == -1):
                    taxonomy.nameit(taxName)
                else:
                    taxName = re.match("(.*?)\s(.*)", taxName)
                    taxonomy.nameit(taxName.group(1), taxName.group(2))

                if self.firstTName == "":
                    self.firstTName = taxonomy.abbrev
                  
                self.taxonomies[taxonomy.abbrev] = taxonomy
                flag = "taxonomy"
                groups = []     # used for input viz

                
            elif (re.match("location", line)):
                flag = "location"
              
            elif (re.match("temporal", line)):
                flag = "temporal"
              
            # reads in lines of the form (a b c) where a is the parent
            # and b c are the children
            elif (re.match("\(.*\)", line)):
                if flag == "taxonomy":
                    taxonomy.addTaxaWithList(self, line)
                    groups.append(re.match("\((.*)\)", line).group(1).split(" "))
                elif flag == "location":
                    self.addLocation(line)
                elif flag == "temporal":
                    self.addTemporal(line)
                else:
                    None
                    
            elif (re.match("\s", line)):
                group2concepts.update({taxonomy.abbrev : groups})

            elif (re.match("articulation", line)):
                self.basetr = self.tr
                self.basemir = self.mir
              
            elif (re.match("\[.*?\]", line)):
                inside = re.match("\[(.*)\]", line).group(1)
                self.addArticulation(inside)
                art.append(re.match("\[(.*)\]", line).group(1)) # used for input viz
                
                # self.articulations += [Articulation(inside, self)]
		# if inside.find("{") != -1:
		#     r = re.match("(.*) \{(.*)\} (.*)", inside)
		#     self.addPMir(r.group(1), r.group(3), r.group(2).replace(" ",","), 0)
		# else:
		#     self.addAMir(inside, 0)
              
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
            
        # used for input viz
        self.inputVisualization(group2concepts, art)
                           
        return True              

    def addArticulation(self, artStr):
        self.articulations += [Articulation(artStr, self)]
	if artStr.find("{") != -1:
	    r = re.match("(.*) \{(.*)\} (.*)", artStr)
	    self.addPMir(r.group(1), r.group(3), r.group(2).replace(" ",","), 0)
	else:
	    self.addAMir(artStr, 0)

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


    def dotName2dlv(self, dotName):
        elems = re.match("(.*)\.(.*)", dotName)
        return "c" + elems.group(1) + "_" + elems.group(2)
                     
    def dlvName2dot(self, dlvName):
        if(dlvName.find("_not_") != -1):
            elems = re.match("(.*)_not_(.*)", dlvName)
            conc1 = re.match("c(.*)_(.*)", elems.group(1))
            conc2 = re.match("c(.*)_(.*)", elems.group(2))
            return conc1.group(1) + "." + conc1.group(2) + "\\\\"\
                  +conc2.group(1) + "." + conc2.group(2)
        elif(dlvName.find("not_") != -1):
            elems = re.match("not_(.*)__(.*)", dlvName)
            conc1 = re.match("c(.*)_(.*)", elems.group(1))
            conc2 = re.match("c(.*)_(.*)", elems.group(2))
            return conc2.group(1) + "." + conc2.group(2) + "\\\\"\
                  +conc1.group(1) + "." + conc1.group(2)
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

    def addEqMap(self, T1, T2):
        if not self.eq.has_key(T1):
            self.eq[T1] = sets.Set()
        self.eq[T1].add(T2)
        if not self.eq.has_key(T2):
            self.eq[T2] = sets.Set()
        self.eq[T2].add(T1)

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
            self.addEqMap(r[0], r[2])
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
            if (r[1] == "r4sum"):
                self.addIMir(r[0], r[2], provenance)
                self.addIMir(r[0], r[3], provenance)
                self.addIMir(r[0], r[4], provenance)
                self.addIMir(r[0], r[5], provenance)
                self.mir[r[0] + "," + r[2]] = rcc5["includes"]
                self.mir[r[0] + "," + r[3]] = rcc5["includes"]
                self.mir[r[0] + "," + r[4]] = rcc5["includes"]
                self.mir[r[0] + "," + r[5]] = rcc5["includes"]
                self.tr.append([r[2],r[0], provenance])
                self.tr.append([r[3],r[0], provenance])
                self.tr.append([r[4],r[0], provenance])
                self.tr.append([r[5],r[0], provenance])
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

    # Output all the mir relations in the csv file
    def genMir(self):       
        fmir = open(self.mirfile, 'w')
        # Get the pairs as needed
        pairs =      self.getAllTaxonPairs()\
                if self.allPairsNeeded()\
                else self.getAllArticulationPairs()
        for pair in pairs:
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
	if(self.eq.has_key(r[0]) and r[len(r)-1] in self.eq[r[0]]):
	    del self.eq[r[0]]
	if(self.eq.has_key(r[len(r)-1]) and r[0] in self.eq[r[len(r)-1]]):
	    del self.eq[r[len(r)-1]]
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
                    
    def remove_duplicate_string(self,li):
        if li:
            li.sort()
            last = li[-1]
            for i in range(len(li)-2, -1, -1):
                if last == li[i]:
                    del li[i]
                else:
                    last = li[i]

    def genAllPwRcg(self, numOfPws):
        rels = []
        for [T1, T2, P] in self.trlist:
            cnt = 0
            for [T3, T4, P] in self.trlist:
                if T1 == T3 and T2 == T4:
                    cnt = cnt + 1
            rels.append([T1, T2, cnt,""])
        self.remove_duplicate_string(rels)
        pointDG = (12,169,97) #dark green
        pointDR = (118,18,18) #dark red
        distR = pointDR[0] - pointDG[0]
        distG = pointDR[1] - pointDG[1]
        distB = pointDR[2] - pointDG[2]
        for i in range(len(rels)):
            relra = float(rels[i][2]) / float(numOfPws)
            newPointDec = (round(pointDG[0] + distR*relra), round(pointDG[1] + distG*relra), round(pointDG[2] + distB*relra))
            newColor = "#" + str(hex(int(newPointDec[0])))[2:] + str(hex(int(newPointDec[1])))[2:] + str(hex(int(newPointDec[2])))[2:]
            rels[i][3] = newColor
        # write to dot file
        rcgAllFile = os.path.join(self.options.outputdir, self.name+"_all.dot")
#        fAllDot = open(self.options.outputdir+self.name+"_all.dot", 'a')
        fAllDot = open(rcgAllFile, 'a')
        if self.options.simpAllView:
            for [T1, T2, cnt, color] in rels:
                if cnt == numOfPws:
                    fAllDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled,label=" + str(cnt) + ",color=\"#FF0000\"];\n")
                else:
                    fAllDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled,label=" + str(cnt) + ",color=\"#00FF00\"];\n")
        else:
            for [T1, T2, cnt, color] in rels:
                fAllDot.write("  \"" + T1 + "\" -> \"" + T2 + "\" [style=filled,label=" + str(cnt) + ",penwidth=" + str(cnt) + ",color=\"" + color + "\"];\n")
        fAllDot.write("}\n")
        fAllDot.close()
        
    def addInputVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        node.update({"name": "test" + str(randint(0,100))})
        if group != "(+)":
            self.inputVizNodes.update({group + "." + concept: node})
        else:
            self.inputVizNodes.update({concept: node})
    
    def addInputVizEdge(self, s, t, label):
        edge = {}
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"label" : label})
        self.inputVizEdges.update({s + "_" + t : edge})
        
    def inputVisualization(self, group2concepts, art):
        art2symbol = {"equals":"==","is_included_in":"<","includes":">","overlaps":"><","disjoint":"!"}
        
        for key, attr in group2concepts.iteritems():
            for value in attr:
                parent = value.pop(0)
                self.addInputVizNode(parent, key)
                for v in value:
                    self.addInputVizNode(v, key)
                    self.addInputVizEdge(key + "." + v, key + "." + parent, "isa")
        
        for a in art:
            a = a.replace("3sum", "sum")
            a = a.replace ("4sum", "sum")
            a = a.replace("3diff", "diff")
            a = a.replace ("4diff", "diff")
        
            if "{" in a:
                start = a.split(" {")[0]
                end = a.split("} ")[-1]
                ops = a.split("{", 1)[1].split("}")[0].split(" ")
                label = art2symbol.get(ops[0], ops[0])
                for i in range(1,len(ops)):
                    label = label + " OR " + art2symbol.get(ops[i], ops[i])
                self.addInputVizEdge(start, end, label)
            else:
                if any(l in a for l in ["lsum", "ldiff"]):
                    if "lsum" in a:
                        l = "lsum"
                        op = "+"
                    else:
                        l = "ldiff"
                        op = "-"
                    plus = a.split(l + " ")[-1].replace(".","") + op
                    self.addInputVizNode(plus, "(+)")
                    self.addInputVizEdge(plus, a.split(" " + l + " ")[-1], "out")
                    for i in range(0,len(a.split(" " + l)[0].split(" "))):
                        self.addInputVizEdge(a.split(" " + l)[0].split(" ")[i], plus, "in")
                elif any(l in a for l in ["rsum", "rdiff"]):
                    if "rsum" in a:
                        l = "rsum"
                        op = "+"
                    else:
                        l= "rdiff"
                        op = "-"
                    plus = a.split(" " + l)[0].replace(".","") + op
                    self.addInputVizNode(plus, "(+)")
                    self.addInputVizEdge(plus, a.split(" " + l + " ")[0], "out")
                    for i in range(1,len(a.split(" " + l)[-1].split(" "))):
                        self.addInputVizEdge(a.split(" " + l)[-1].split(" ")[i], plus,"in")
                else:
                    self.addInputVizEdge(a.split(" ")[0], a.split(" ")[2], art2symbol.get(a.split(" ")[1], a.split(" ")[1]))
                
        # create the yaml file
        inputYamlFile = os.path.join(self.options.outputdir, self.name+".yaml")
        inputDotFile = os.path.join(self.options.outputdir, self.name+".dot")
        inputPdfFile = os.path.join(self.options.outputdir, self.name+".pdf")
        
        fInputVizYaml = open(inputYamlFile, 'w')
        fInputVizYaml.write(yaml.safe_dump(self.inputVizNodes, default_flow_style=False))
        fInputVizYaml.write(yaml.safe_dump(self.inputVizEdges, default_flow_style=False))
        fInputVizYaml.close()        
        
        # apply the inputviz stylesheet
        commands.getoutput("cat "+inputYamlFile+" | y2d -s "+self.stylesheetdir+"inputstyle.yaml" + ">" + self.iv2dot)
        commands.getoutput("dot -Tpdf "+self.iv2dot+" -o "+self.iv2pdf)

    def addRcgVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        node.update({"name": "test" + str(randint(0,100))})
        self.rcgVizNodes.update({group + "." + concept: node})
    
    def addRcgVizEdge(self, s, t, label):
        edge = {}
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"label" : label})
        self.rcgVizEdges.update({s + "_" + t : edge})

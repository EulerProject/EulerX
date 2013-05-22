import os
import time
import sets
import inspect
import threading
import StringIO
from taxonomy import * 
from helper import *

class TaxonomyMapping:

    def __init__(self, options):
        self.mir = {}                          # MIR
        self.mirc = {}                         # MIRC
        self.obs = []                          # OBS
        self.obslen = 0                        # OBS time / location?
        self.location = []                     # location set
        self.temporal = []                     # temporal set
        self.exploc = False
        self.exptmp = False
        self.tr = []                           # transitive reduction
        self.eq = []                           # euqlities
        self.rules = {}
        self.taxonomies = {}
        self.articulations = []
        self.map = {}
        self.baseDlv = ""
        self.pw = ""
        self.npw = 0                           # # of pws
        self.options = options
        self.enc = encode[options.encode]
        self.name = os.path.splitext(os.path.basename(options.inputfile))[0]
        if options.outputdir is None:
            options.outputdir = options.inputdir
        if not os.path.exists(options.outputdir):
            os.mkdir(options.outputdir)
        self.aspdir = os.path.join(options.outputdir, "asp")
        if not os.path.exists(self.aspdir):
            os.mkdir(self.aspdir)
        self.pwfile = os.path.join(self.aspdir, self.name+"_pw.asp")
        self.pwswitch = os.path.join(self.aspdir, "pw.asp")
        self.ixswitch = os.path.join(self.aspdir, "ix.asp")
        self.pwout = os.path.join(options.outputdir, self.name+"_pw.txt")
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
        if not self.testConsistency():
            print "Input is inconsistent!!"
            self.inconsistencyExplanation()
            return
        if self.enc & encode["pw"]:
            self.genPW(True)
        elif self.enc & encode["ve"]:
            self.genVE()
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
        com = "dlv -silent -filter=rel -n=1 "+self.pwfile+" "+self.pwswitch
        if commands.getoutput(com) == "":
            return False
        return True

    def inconsistencyExplanation(self):
        com = "dlv -silent -filter=ie "+self.pwfile+" "+self.ixswitch
        ie = commands.getoutput(com)
        self.postProcessIE(ie);

    def postProcessIE(self, ie):
        print "Please see "+self.name+"_ie.pdf for the inconsistency relations between all the rules."
        print ie
        if ie.find("{}") == -1 and ie != "":
            ies = (re.match("\{(.*)\}", ie)).group(1).split(", ")
            tmpmap = {}
            for i in range(len(ies)):
               item = re.match("ie\(s\((.*),(.*),(.*)\)\)", ies[i])
               key = item.group(1)+","+item.group(3)
               if key in tmpmap.keys():
                   value = tmpmap[key]
                   value.append(item.group(2))
                   tmpmap[key] = value
               else:
                   tmpmap[key] = [item.group(1), item.group(2)]
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
                    fie.write("\""+value+"\" -> \"inconsistency="+tmpmap[key].__str__()+"\" \n")
            label=""
            for key in self.rules.keys():
                label += key+" : "+self.rules[key]+"\n"
            fie.write("graph [label=\""+label+"\"]\n")
            fie.write("}")
            fie.close()
            commands.getoutput("dot -Tpdf "+self.iefile+" -o "+self.iepdf)

    def genPW(self, pwflag):
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            com = "gringo "+self.pwfile+" "+ self.pwswitch+ " | claspD 0"
            outputstr = commands.getoutput(com)
            if self.options.output: print outputstr
            return None
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        com = "dlv -silent -filter=rel "+self.pwfile+" "+ self.pwswitch+ " | "+path+"/muniq -u"
        self.pw = commands.getoutput(com)
        raw = self.pw.replace("{","").replace("}","").replace(" ","").replace("),",");")
        pws = raw.split("\n")
        self.npw = len(pws)
        outputstr = ""
        # mirs for each pw
        if self.options.cluster: pwmirs = []
        for i in range(len(pws)):
            if self.options.cluster: pwmirs.append({})
            outputstr += "Possible world "+i.__str__()+": {"
            items = pws[i].split(";")
            for j in range(len(items)):
                rel = items[j].replace("rel(","").replace(")","").split(",")
                dotc1 = self.dlvName2dot(rel[0])
                dotc2 = self.dlvName2dot(rel[1])
                if j != 0: outputstr += ", "
                outputstr += dotc1+rel[2]+dotc2
                pair = dotc1+","+dotc2
                if self.options.cluster: pwmirs[i][pair] = rcc5[rel[2]]
                if i == 0:
                    self.mir[pair] = rcc5[rel[2]]
                    self.mirc[pair] = []
                    for k in range(5):
                        self.mirc[pair].append(0)
                else:
                    self.mir[pair] |= rcc5[rel[2]]
                self.mirc[pair][logmap[rcc5[rel[2]]]] += 1
            outputstr += "}\n"
        if pwflag:
            if self.options.output: print outputstr
            fpw = open(self.pwout, 'w')
            fpw.write(outputstr)
            fpw.close()
        self.genMir()
        if self.options.cluster: self.genPwCluster(pwmirs, False)

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
        com = "dlv -silent -filter=pinout "+self.pwfile+" "+ self.pwswitch+ " | "+path+"/muniq -u"
        raw = commands.getoutput(com).replace("{","").replace("}","").replace(" ","").replace("),",");")
        pws = raw.split("\n")
        self.npw = len(pws)
        outputstr = ""
        if self.options.cluster: pwobs = []
        for i in range(len(pws)):
            outputstr += "Possible world "+i.__str__()+": {"
            items = pws[i].split(";")
            pmapping = {}
            for j in range(len(items)):
                inout = items[j].replace("pinout(","").replace(")","").split(",")
                dotConcept = self.dlvName2dot(inout[0])
                key = ""
                for k in range(2,self.obslen+1):
                    if key != "": key += "@"
                    key += inout[k]
                if inout[1] == "in":
                    if pmapping.has_key(key):
                        pmapping[key].append("*"+dotConcept)
                    else:
                        pmapping[key]=[dotConcept]
                #else:
                 #   if pmapping.has_key(inout[1]):
                  #      pmapping[inout[1]].append("-"+dotConcept)
                  #  else:
                   #     pmapping[inout[1]]=["-"+dotConcept]
            keys = pmapping.keys()
            for j in range(len(keys)):
                if j != 0: outputstr += ", "
                values = pmapping[keys[j]]
                for k in range(len(values)):
                    outputstr += values[k]
                s = keys[j].find("@")
                if s != -1:
                    outputstr += keys[j][s:]
            if self.options.cluster: pwobs.append(sets.Set(keys))
            outputstr += "}\n"
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

    def genASP(self):
        if self.baseDlv != "":
            return  None
        self.genDlvConcept()
        self.genDlvPC()
        self.genDlvAr()
        if self.enc & encode["vr"] or self.enc & encode["dl"] or self.enc & encode["pl"] or self.enc & encode["mn"]:
            self.genDlvDc()
        if self.obs != [] and self.enc & encode["ob"]:
            self.genDlvObs()
        fdlv = open(self.pwfile, 'w')
        fdlv.write(self.baseDlv)
        fdlv.close()
        pdlv = open(self.pwswitch, 'w')
        idlv = open(self.ixswitch, 'w')
        pdlv.write("pw.")
        idlv.write("ix.")
        if reasoner[self.options.reasoner] == reasoner["gringo"]:
            pdlv.write("\n#hide.\n#show rel/3.")
            idlv.write("\n#hide.\n#show ie/3.")
        pdlv.close()
        idlv.close()

    def genDlvConcept(self):
        con = "%%% Concepts\n"

        # numbering concepts
        num = 0    # number of taxa
        prod = 0   # product
        n = 0      # number of taxonomies
        pro = 1    # product of num
        couArray = []
        proArray = []
        for key in self.taxonomies.keys():
            cou = 0
            con += "tax(" + self.taxonomies[key].dlvName() + "," + n.__str__() + ").\n"
            con += "concept2(A, B) :- concept(A,B,_).\n"
            for taxon in self.taxonomies[key].taxa.keys():
                t = self.taxonomies[key].taxa[taxon]
                if (self.enc & encode["dl"] or self.enc & encode["mn"]) and t.hasChildren():
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
	    self.baseDlv = "#maxint=" + maxint.__str__() + ".\n\n"
	    self.baseDlv += con
	    self.baseDlv += "%%% regions\n"
	    self.baseDlv += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

	    self.baseDlv += "%%% bit\n"
	    self.baseDlv += "bit(M, V):-r(M),#mod(M," + int(num).__str__() + ",V).\n\n"

	    self.baseDlv += "%%% Meaning of regions\n"
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
	    self.baseDlv += "vrs(X) :- r(X), not irs(X).\n"
	    self.baseDlv += ":- vrs(X), irs(X).\n\n"

        elif self.enc & encode["mn"]:
            maxint = prod
            if reasoner[self.options.reasoner] == reasoner["dlv"]:
	        self.baseDlv = "#maxint=" + maxint.__str__() + ".\n\n"
	        self.baseDlv += con
	        self.baseDlv += "%%% regions\n"
	        self.baseDlv += "r(M):- #int(M),M>=1,M<=#maxint.\n\n"

	        self.baseDlv += "%%% bit\n"
                for i in range(len(couArray)):
	            self.baseDlv += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", #mod(M1," + couArray[i].__str__() + ",V).\n"

            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
	        self.baseDlv = con
	        self.baseDlv += "%%% regions\n"
	        self.baseDlv += "r(1.."+maxint.__str__()+").\n\n"

	        self.baseDlv += "%%% bit\n"
                for i in range(len(couArray)):
	            self.baseDlv += "bit(M, " + i.__str__() + ", V):-r(M),M1=M/" + proArray[i].__str__() + ", V = M1 #mod " + couArray[i].__str__() + ".\n"

	    self.baseDlv += "\n\n%%% Meaning of regions\n"
	    self.baseDlv += "in(X, M) :- r(M),concept(X,T,N),N1=N+1,bit(M,T,N1).\n"
	    self.baseDlv += "out(X, M) :- r(M),concept(X,T,N),N1=N+1,not bit(M,T,N1).\n"
	    self.baseDlv += "in(X, M) :- r(M),concept2(X,_),not out(X, M).\n"
	    self.baseDlv += "ir(M, fi) :- in(X, M), out(X, M), r(M), concept2(X,_).\n\n"

	    self.baseDlv += "%%% Constraints of regions.\n"
	    self.baseDlv += "irs(X) :- ir(X, _).\n"
	    self.baseDlv += "vrs(X) :- vr(X, _).\n"
	    self.baseDlv += "vr(X, X) :- not irs(X), r(X).\n"
	    self.baseDlv += "ir(X, X) :- not vrs(X), r(X).\n"
	    self.baseDlv += "ie(prod(A,B)) :- vr(X, A), ir(X, B), ix.\n"
	    self.baseDlv += ":- vrs(X), irs(X), pw.\n\n"

	    self.baseDlv += "%%% Inconsistency Explanation.\n"
	    self.baseDlv += "ie(s(R, A, Y)) :- pie(R, A, Y), not cc(R, Y), ix.\n"
	    self.baseDlv += "cc(R, Y) :- c(R, _, Y), ix.\n"

        elif self.enc & encode["vr"]:
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
            self.baseDlv += "in(X, M) :- not out(X, M), r(M),concept(X,_,N),count(N).\n"
            self.baseDlv += "out(X, M) :- not in(X, M), r(M),concept(X,_,N),count(N).\n"
	    self.baseDlv += "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"
	    self.baseDlv += "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"
	    self.baseDlv += "ir(M, fi) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"

	    self.baseDlv += "%%% Constraints of regions.\n"
	    self.baseDlv += "irs(X) :- ir(X, _).\n"
	    self.baseDlv += "vrs(X) :- vr(X, _).\n"
	    self.baseDlv += "vr(X, X) :- not irs(X), r(X).\n"
	    self.baseDlv += "ir(X, X) :- not vrs(X), r(X).\n"
	    self.baseDlv += "ie(prod(A,B)) :- vr(X, A), ir(X, B), ix.\n"
	    self.baseDlv += ":- vrs(X), irs(X), pw.\n\n"

	    self.baseDlv += "%%% Inconsistency Explanation.\n"
	    self.baseDlv += "ie(s(R, A, Y)) :- pie(R, A, Y), not cc(R, Y), ix.\n"
	    self.baseDlv += "cc(R, Y) :- c(R, _, Y), ix.\n"
#	    self.baseDlv += "in(X, M) v out(X, M) :- r(M),concept(X,_,N),count(N).\n"
#	    self.baseDlv += "in(X, M) :- r(M),concept(X,_,N),bit(M,N,1).\n"
#	    self.baseDlv += "out(X, M) :- r(M),concept(X,_,N),bit(M,N,0).\n\n"
#	    self.baseDlv += "ir(M) :- in(X, M), out(X, M), r(M), concept(X,_,_).\n"
#
#	    self.baseDlv += "%%% Constraints of regions.\n"
#	    self.baseDlv += "ir(0).\n"
#	    self.baseDlv += "vrs(X) v irs(X):- r(X).\n"
#	    self.baseDlv += ":- vrs(X), irs(X).\n\n"

        elif self.enc & encode["direct"]:
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
                if self.options.verbose:
                    print "PC: ",queue
                t = queue.pop(0)
                if t.hasChildren():
                    if self.options.verbose:
                        print "PC: ",t.dlvName()
                    if self.enc & encode["vr"] or self.enc & encode["dl"] or self.enc & encode["mn"]:
			# ISA
			self.baseDlv += "%% ISA\n"
			coverage = ":- in(" + t.dlvName() + ", X)"
			coverin = ""
			coverout = "out(" + t.dlvName() + ", X) :- "
			for t1 in t.children:
                            queue.append(t1)
			    self.baseDlv += "% " + t1.dlvName() + " isa " + t.dlvName() + "\n"
                            ruleNum = len(self.rules)
			    self.rules["r" + ruleNum.__str__()] = t1.dotName() + " isa " + t.dotName()
			    #self.baseDlv += "in(" + t.dlvName() + ", X) :- in(" + t1.dlvName() + ", X).\n"
			    #self.baseDlv += "out(" + t1.dlvName() + ", X) :- out(" + t.dlvName() + ", X).\n"
			    #self.baseDlv += "in(" + t1.dlvName() + ", X) v out(" + t1.dlvName() + ", X) :- in(" + t.dlvName() + ", X).\n"
			    #self.baseDlv += "in(" + t.dlvName() + ", X) v out(" + t.dlvName() + ", X) :- out(" + t1.dlvName() + ", X).\n"
			    self.baseDlv += "ir(X, r" + ruleNum.__str__() +") :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n"
                            if reasoner[self.options.reasoner] == reasoner["dlv"]:
			        self.baseDlv += ":- #count{X: vrs(X), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X)} = 0, pw.\n"
                            elif reasoner[self.options.reasoner] == reasoner["gringo"]:
			        self.baseDlv += "1[vrs(X): in(" + t1.dlvName() + ", X): in(" + t.dlvName() + ", X)] :- pw.\n"
			    self.baseDlv += "pie(r" + ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X), ix.\n"
			    self.baseDlv += "c(r" + ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + t1.dlvName() + ", X), in(" + t.dlvName() + ", X), ix.\n\n"
			    coverage += ",out(" + t1.dlvName() + ", X)"
                            if coverin != "":
                                coverin += " v "
                                coverout += ", "
                            coverin += "in(" + t1.dlvName() + ", X)"
                            coverout += "out(" + t1.dlvName() + ", X)"
			# C
                        if self.options.enableCov:
			    self.baseDlv += "%% coverage\n"
                            ruleNum = len(self.rules)
		            self.rules["r" + ruleNum.__str__()] = t.dotName() + " coverage"
			    #self.baseDlv += coverin + " :- in(" + t.dlvName() + ", X).\n"
			    self.baseDlv += coverout + ".\n"
			    #self.baseDlv += "ir(X, r" + ruleNum.__str__() + ") " +coverage + ".\n\n"

			# D
			self.baseDlv += "%% sibling disjointness\n"
			for i in range(len(t.children) - 1):
			    for j in range(i+1, len(t.children)):
				name1 = t.children[i].dlvName()
				name2 = t.children[j].dlvName()
                                ruleNum = len(self.rules)
		                self.rules["r" + ruleNum.__str__()] = t.children[i].dotName() + " disjoint " + t.children[j].dotName()
				self.baseDlv += "% " + name1 + " ! " + name2+ "\n"
				#self.baseDlv += "out(" + name1 + ", X) :- in(" + name2+ ", X).\n"
				#self.baseDlv += "out(" + name2 + ", X) :- in(" + name1+ ", X).\n"
			        #self.baseDlv += "in(" + name1 + ", X) v out(" + name1 + ", X) :- out(" + name2 + ", X).\n"
			        #self.baseDlv += "in(" + name2 + ", X) v out(" + name2 + ", X) :- out(" + name1 + ", X).\n"
				self.baseDlv += "ir(X, r" + ruleNum.__str__() + ") :- in(" + name1 + ", X), in(" + name2+ ", X).\n"
                                if reasoner[self.options.reasoner] == reasoner["dlv"]:
				    self.baseDlv += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2+ ", X)} = 0, pw.\n"
				    self.baseDlv += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2+ ", X)} = 0, pw.\n"
                                elif reasoner[self.options.reasoner] == reasoner["gringo"]:
				    self.baseDlv += "1[vrs(X): in(" + name1 + ", X): out(" + name2+ ", X)] :- pw.\n"
				    self.baseDlv += "1[vrs(X): out(" + name1 + ", X): in(" + name2+ ", X)] :- pw.\n"
			        self.baseDlv += "pie(r" + ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
			        self.baseDlv += "c(r" + ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
			        self.baseDlv += "pie(r" + ruleNum.__str__() + ", A, 2) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
			        self.baseDlv += "c(r" + ruleNum.__str__() + ", A, 2) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                    elif self.enc & encode["direct"]:
			# ISA
			# C
			self.baseDlv += "\n%% ISA\n"
                        
			coverage = "irs(X) :- in(" + t.dlvName() + ", X)"
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
            ruleNum = len(self.rules)
            self.articulations[i].ruleNum = ruleNum
            self.rules["r" + ruleNum.__str__()] = self.articulations[i].string
            self.baseDlv += self.articulations[i].toASP(self.options.encode, self.options.reasoner)+ "\n"

    def genDlvDc(self):
        self.baseDlv += "%%% Decoding now\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"<\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \">\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"=\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \">\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"<\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \">\"), rel(X, Y, \"><\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \">\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- rel(X, Y, \"><\"), rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), pw.\n"
        self.baseDlv += ":- not rel(X, Y, \"=\"), not rel(X, Y, \"<\"), not rel(X, Y, \">\"), not rel(X, Y, \"><\"), not rel(X, Y, \"!\"), concept2(X, N1), concept2(Y, N2), N1 < N2, pw.\n\n"

        self.baseDlv += "hint(X, Y, 0) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), out(Y, R), pw.\n"
        self.baseDlv += "hint(X, Y, 1) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), in(X, R), in(Y, R), pw.\n"
        self.baseDlv += "hint(X, Y, 2) :- concept2(X, N1), concept2(Y, N2), N1 < N2, vrs(R), out(X, R), in(Y, R), pw.\n\n"

        self.baseDlv += "rel(X, Y, \"=\") :- not hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"
        self.baseDlv += "rel(X, Y, \"<\") :- not hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"
        self.baseDlv += "rel(X, Y, \">\") :- hint(X, Y, 0), hint(X, Y, 1), not hint(X, Y, 2), pw.\n"
        self.baseDlv += "rel(X, Y, \"><\") :- hint(X, Y, 0), hint(X, Y, 1), hint(X, Y, 2), pw.\n"
        self.baseDlv += "rel(X, Y, \"!\") :- hint(X, Y, 0), not hint(X, Y, 1), hint(X, Y, 2), pw.\n\n\n"

    def genDlvObs(self):
        self.baseDlv += "%% Observation Information\n\n"
        if self.location == []:
            self.baseDlv += "present(X) v absent(X) :- r(X).\n"
            self.baseDlv += ":- present(X), absent(X).\n"
            self.baseDlv += "absent(X) :- irs(X).\n"
        else:
            if self.exploc:
                self.baseDlv += "subl(X, Z) :- subl(X, Y), subl(Y, Z).\n" 
                for i in range(len(self.location)):
                    self.baseDlv += "l(" + self.location[i][0] + ").\n"
                    for j in range(1, len(self.location[i])):
                        self.baseDlv += "l(" + self.location[i][j] + ").\n"
                        self.baseDlv += "subl(" + self.location[i][j] + ", " + self.location[i][0] +").\n"
            else:
                for i in range(len(self.location)):
                    self.baseDlv += "l(" + self.location[i] + ").\n"
            if self.temporal == []:
                self.baseDlv += "present(X, L) v absent(X, L) :- r(X), l(L).\n"
                self.baseDlv += ":- present(X, L), absent(X, L).\n"
                self.baseDlv += "absent(X, L) :- irs(X), l(L).\n"
                self.baseDlv += "present(X, L) :- present(X, L1), subl(L1, L).\n"
                self.baseDlv += "absent(X, L) :- absent(X, L1), subl(L, L1).\n"
            else:
                if self.exptmp:
                    self.baseDlv += "subt(X, Z) :- subt(X, Y), subt(Y, Z).\n" 
                    for i in range(len(self.temporal)):
                        self.baseDlv += "l(" + self.temporal[i][0] + ").\n"
                        for j in range(1, len(sef.temporal[i])):
                            self.baseDlv += "t(" + self.temporal[i][j] + ").\n"
                            self.baseDlv += "subt(" + self.temporal[i][j] + ", " + self.temporal[i][0] +").\n"
                else:
                    for i in range(len(self.temporal)):
                        self.baseDlv += "t(" + self.temporal[i] + ").\n"
                self.baseDlv += "present(X, L, T) v absent(X, L, T) :- r(X), l(L), t(T).\n"
                self.baseDlv += ":- present(X, L, T), absent(X, L, T).\n"
                self.baseDlv += "absent(X, L, T) :- irs(X), l(L), t(T).\n"
                self.baseDlv += "present(X, L, T) :- present(X, L1, T), subl(L1, L), t(T).\n"
                self.baseDlv += "absent(X, L, T) :- absent(X, L1, T), subl(L, L1), t(T).\n"
                self.baseDlv += "present(X, L, T) :- present(X, L, T1), subt(T1, T), l(L).\n"
                self.baseDlv += "absent(X, L, T) :- absent(X, L, T1), subt(T, T1), l(L).\n"
                
        if self.obslen == 2:
            appendd = ""
        elif self.obslen == 3:
            appendd = ", Y"
        elif self.obslen == 4:
            appendd = ", Y, Z"
        else:
            print "Syntax error in observation portion of input file!!"
        for i in range(len(self.obs)):
            tmp = ""
            for j in range(len(self.obs[i][0])):
                if self.obs[i][0][j][1] == "Y":
                  pre = "in"
                else:
                  pre = "out"
                if tmp != "": tmp += ", "
                cpt = self.obs[i][0][j][0]
                tmp += pre + "(" + cpt + ", X)"
            pair = ""
	    if self.obslen > 2:
                pair += ", " + self.obs[i][2]
	        if self.obslen > 3:
                    pair += ", " + self.obs[i][3]
            if self.obs[i][1] == "N":
                self.baseDlv += ":- present(X" + pair + ")," + tmp + ".\n" 
            else:
                self.baseDlv += ":- #count{X: present(X" + pair + "), " + tmp + "} = 0.\n"
	self.baseDlv += "pinout(C, in, X" + appendd + ") :- present(X" + appendd + "), concept(C, _, N), #int(N), in(C, X).\n"
	self.baseDlv += "pinout(C, out, X" + appendd + ") :- present(X" + appendd + "), concept(C, _, N), #int(N), out(C, X).\n"
            

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
              if self.options.countOn:
                for i in range(5):
                  if self.mirc[pairkey][i] != 0:
                    fmir.write(pairkey+",opt," + findkey(relation, 1 << i)+","\
                               +self.mirc[pairkey][i].__str__()+","+self.npw.__str__()+"\n")
              else:
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
                

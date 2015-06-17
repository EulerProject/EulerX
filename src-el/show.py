# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#from helper import *
#from taxonomy import *
#from alignment import *
import os
import getpass
import socket
import inspect
import imp
import yaml
import re
import copy
import relations
from random import randint
from helper import *
from subprocess import call
from sets import Set

class ProductsShowing:
    
    def __init__(self, args):
        self.name = ''
        self.args = args
        self.rcc5 = relations.rcc5
        self.relation = relations.relation
        self.runningUser = getpass.getuser()
        self.runningHost = socket.gethostname()
        self.projectdir = ''      # initiate the project folder to be the current folder
        self.lastrundir = ''
        self.lastruntimestamp = os.path.join(self.projectdir, self.runningUser+'-'+self.runningHost+'-lastrun.timestamp')
        if os.path.isfile(self.lastruntimestamp):
            f = open(self.lastruntimestamp, "r")
            self.lastrundir = f.readline().strip()
            self.name = f.readline()
            f.close()
        
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.stylesheetdir = os.path.join(self.projectdir, "stylesheets/")
        if not os.path.exists(self.stylesheetdir):
            self.stylesheetdir = self.path + "/../default_stylesheet/"
        elif not os.listdir(self.stylesheetdir):
            self.stylesheetdir = self.path + "/../default_stylesheet/"
        
        # list all knowledge products subfolders
        self.inputfilesdir = os.path.join(self.lastrundir, "0-Input") 
        self.inputVizNodes = {}                # nodes for input visualization in stylesheet 
        self.inputVizEdges = {}                # edges for input visualization in stylesheet
        
        self.pwinternalfilesdir = os.path.join(self.lastrundir, "2-ASP-output")
                
        self.pwsvizdir = os.path.join(self.lastrundir, "4-PWs")
        self.rcgVizNodes = {}
        self.rcgVizEdges = {}
        self.trlist = []
        
        self.pwsaggregatedir = os.path.join(self.lastrundir, "5-Aggregates")
        self.allRcgNodesDict = {}
        self.allRcgEdgesDict = {}
        self.clusterVizNodes = {}
        self.clusterVizEdges = {}
        self.hierarchyVizNodes = {}
        self.hierarchyVizEdges = {}
        self.hrdot = os.path.join(self.pwsaggregatedir, self.name + "_hr.gv")
        
        self.latticedir = os.path.join(self.lastrundir, "6-Lattices")
        
        self.mergeinputdir = os.path.join(self.lastrundir, "7-Merge-input")
        
        
    def remove_duplicate_string(self,li):
        if li:
            li.sort()
            last = li[-1]
            for i in range(len(li)-2, -1, -1):
                if last == li[i]:
                    del li[i]
                else:
                    last = li[i]
        
    def show(self):
        #print "self.args", self.args
        
        if self.args['<inputfile>'] and self.args['iv']:
            self.showIV()
        
        elif not os.path.isfile(self.lastruntimestamp):
            print 'Nothing to show, need to run "euler2 align" first.\n'
            print 'Use "euler2 -h" to see more help.'
        else:
            # show other stuff
            if self.args['<name>'] == 'iv':
                self.showIV()
            if self.args['<name>'] == 'pw':    # possible worlds
                self.showPW()
            if self.args['<name>'] == 'av' or self.args['<name>'] == 'avStable' or self.args['<name>'] == 'avLabile':    # aggregate view
                self.showAV()
            if self.args['<name>'] == 'cv':    # cluster view
                self.showCV()
            if self.args['<name>'] == 'hv':    # hierarchy view
                self.showHV()
            if self.args['<name>'] == 'inconLat':   # inconsistency lattice 
                self.showInconLAT()
            if self.args['<name>'] == 'ambLat':   # ambiguity lattice 
                self.showAmbLAT()
            if self.args['<name>'] == 'pw2input':   # transfer PW to input 
                self.showPW2INPUT()
            
            return

    
    def showIV(self):
        print "******input visualization******"
        if self.args['<inputfile>'] and self.args['iv']:
            inputFile = self.args['<inputfile>'][0]
        else:
            inputFile = os.path.join(self.inputfilesdir, self.name+".txt")
        fileName = os.path.splitext(os.path.basename(inputFile))[0]
        
        group2concepts = {}
        art = []
        firstTName = ""
        secondTName = ""
        taxName = ""
        
        f = open(inputFile, 'r')
        lines = f.readlines()
        f.close()
        
        for line in lines:
            
            if (re.match("taxonomy", line)):
                taxName = re.match("taxonomy(\s+)(\S+)(.*)", line).group(2)

                if firstTName == "":
                    firstTName = taxName
                
                if firstTName != "" and secondTName == "" and firstTName != taxName:
                    secondTName = taxName
            
            elif (re.match("\(.*\)", line)):

                    if taxName in group2concepts:
                        group2concepts[taxName].append(re.match("\((.*)\)", line).group(1).split(" "))
                    else:
                        group2concepts[taxName] = [re.match("\((.*)\)", line).group(1).split(" ")]
              
            elif (re.match("\[.*?\]", line)):
                art.append(re.match("\[(.*)\]", line).group(1))
                
        art2symbol = {"equals":"==","is_included_in":"<","includes":">","overlaps":"><","disjoint":"!"}
        
        for key, attr in group2concepts.iteritems():
            for value in attr:
                parent = value.pop(0)
                self.addInputVizNode(parent, key, self.checkConceptRank(parent))
                for v in value:
                    self.addInputVizNode(v, key, self.checkConceptRank(v))
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
                    self.addInputVizNode(plus, "(+)", 0)
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
                    self.addInputVizNode(plus, "(+)", 0)
                    self.addInputVizEdge(plus, a.split(" " + l + " ")[0], "out")
                    for i in range(1,len(a.split(" " + l)[-1].split(" "))):
                        self.addInputVizEdge(a.split(" " + l)[-1].split(" ")[i], plus,"in")
                else:
                    self.addInputVizEdge(a.split(" ")[0], a.split(" ")[2], art2symbol.get(a.split(" ")[1], a.split(" ")[1]))
                
        # create the yaml file
        if self.args['<inputfile>'] and self.args['iv']:
            inputYamlFile = fileName+".yaml"
            inputDotFile = fileName+".gv"
            inputPdfFile = fileName+".pdf"
            inputSvgFile = fileName+".svg"
        else:
            inputYamlFile = os.path.join(self.inputfilesdir, self.name+".yaml")
            inputDotFile = os.path.join(self.inputfilesdir, self.name+".gv")
            inputPdfFile = os.path.join(self.inputfilesdir, self.name+".pdf")
            inputSvgFile = os.path.join(self.inputfilesdir, self.name+".svg")
        
        fInputVizYaml = open(inputYamlFile, 'w')
        if self.inputVizNodes:
            fInputVizYaml.write(yaml.safe_dump(self.inputVizNodes, default_flow_style=False))
        if self.inputVizEdges:
            fInputVizYaml.write(yaml.safe_dump(self.inputVizEdges, default_flow_style=False))
        fInputVizYaml.close()        
        
        # check whether stylesheet taxonomy names are in stylesheet
        global styles
        with open(self.stylesheetdir+"inputstyle.yaml") as inputStyleFileOld:
            styles = yaml.load(inputStyleFileOld)
                    
        # if taxonomy names are not in stylesheet, rewrite styesheet
        if firstTName not in styles["nodestyle"] or secondTName not in styles["nodestyle"]:
            fOld = open(self.stylesheetdir+"inputstyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
            
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if '"1":' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added
                
            value = '    "' + firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"',2) + '"\n    "' + secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"',2) + '"\n' 
                                
            contents.insert(index+1, value)

            fNew = open(self.stylesheetdir+"inputstyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.close()

        # Redo -- check whether stylesheet taxonomy names are in stylesheet
        # Redo -- if taxonomy names are not in stylesheet, rewrite styesheet, for single taxnomy        
        if not firstTName or not secondTName:
            with open(self.stylesheetdir+"singletoninputstyle.yaml") as inputStyleFileOld:
                styles = yaml.load(inputStyleFileOld)
            
            if firstTName not in styles["nodestyle"] or secondTName not in styles["nodestyle"]:
                fOld = open(self.stylesheetdir+"singletoninputstyle.yaml", "r")
                contents = fOld.readlines()
                fOld.close()
                
                for line in contents:
                    if "nodestyle" in line:
                        index = contents.index(line)
                    if '"1":' in line:
                        index2 = contents.index(line)
                
                del contents[index+1:index2]    # clean nodestyle previously added
                    
                value = '    "' + firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"',2) + '"\n    "' + secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"',2) + '"\n' 
                                    
                contents.insert(index+1, value)
    
                fNew = open(self.stylesheetdir+"singletoninputstyle.yaml", "w")
                contents = "".join(contents)
                fNew.write(contents)
                fNew.close()
        
        # apply the inputviz stylesheet
        if not firstTName or not secondTName:
            newgetoutput("cat "+inputYamlFile+" | y2d -s "+self.stylesheetdir+"singletoninputstyle.yaml" + ">" + inputDotFile)
        else:
            newgetoutput("cat "+inputYamlFile+" | y2d -s "+self.stylesheetdir+"inputstyle.yaml" + ">" + inputDotFile)
        if self.args['--all']:
            newgetoutput("dot -Tpdf "+inputDotFile+" -o "+inputPdfFile)
            newgetoutput("dot -Tsvg "+inputDotFile+" -o "+inputSvgFile)
        
    def addInputVizNode(self, concept, group, pathlen):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        node.update({"name": "test" + str(randint(0,100))})
        #if self.args.withrank:
        #    node.update({"pathlen": pathlen})
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
        
    def checkConceptRank(self, concept):
        if "_" in concept:
            return 1
        else:
            return 2

    def showPW(self):
        print "******pw visualization******"   
        
        if not os.path.exists(self.pwsvizdir):
            os.mkdir(self.pwsvizdir)
             
        numOfPws = len([f for f in os.walk(self.pwinternalfilesdir).next()[2] if f[0:11] == "pw.internal" and f[-1] != 'c'])
        avInternalFile = os.path.join(self.pwinternalfilesdir, 'av.internal')
        cvInternalFile = os.path.join(self.pwinternalfilesdir, 'cv.internal')
        pw2inputInternalFile = os.path.join(self.pwinternalfilesdir, 'pw2input.internal')

        for i in range(numOfPws):
            self.rcgVizNodes = {}
            self.rcgVizEdges ={}
            pwInternalFile = os.path.join(self.pwinternalfilesdir, 'pw.internal' + i.__str__())
            it = imp.load_source('it', pwInternalFile)
            
            
            #NOW BEGIN self.genPwRcg(it.fileName, allRcgNodesDict, it.pwIndex)
            
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
            for T1 in it.eq.keys():
                # it.eq is dynamically changed, so we need this check
                if not it.eq.has_key(T1):
                    continue
                tmpStr = ""
    
                T1s = T1.split(".")
                for T2 in it.eq[T1]:
                    T2s = T2.split(".")
                    
                    if tmpStr != "":
                        tmpStr = "\\n" + tmpStr
                    tmpStr = T2 + tmpStr
                if tmpStr != "":
                    tmpStr = "\\n" + tmpStr + "\\n"
    
                if T1s[0] == it.firstTName:
                    tmpStr = T1 + tmpStr
                else:
                    tmpStr = tmpStr + T1
                if tmpStr[0:2] == "\\n": tmpStr = tmpStr[2:]
                if tmpStr[-2:] == "\\n": tmpStr = tmpStr[:-2]
                it.eqConLi.append(tmpStr)
    
                tmpeqConLi2 = []
                for T in it.eqConLi:
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
                                    if T10 in it.eqConLi:
                                        it.eqConLi.remove(T10)
                                    if T11 in it.eqConLi:
                                        it.eqConLi.remove(T11)
                                    if ss not in it.eqConLi:
                                        it.eqConLi.append(ss)
                                    break 
    
                for T2 in it.eq[T1]:

                    tmpTr = list(it.tr)
                    for [T3, T4, P] in tmpTr:
                        if(T1 == T3 or T2 == T3):
                            if it.tr.count([T3, T4, P]) > 0:
                                it.tr.remove([T3, T4, P])
                                it.tr.append([tmpStr, T4, 0])
                        elif(T1 == T4 or T2 == T4):
                            if it.tr.count([T3, T4, P]) > 0:
                                it.tr.remove([T3, T4, P])
                                it.tr.append([T3, tmpStr, 0])
                        for T5 in it.eqConLi:
                            if(T3 != T5 and set(T3.split("\\n")).issubset(set(T5.split("\\n")))):
                                if it.tr.count([T3, T4, P]) > 0:
                                    it.tr.remove([T3, T4, P])
                                    it.tr.append([T5,T4,0])
                            elif(T4 != T5 and set(T4.split("\\n")).issubset(set(T5.split("\\n")))):
                                if it.tr.count([T3, T4, P]) > 0:
                                    it.tr.remove([T3, T4, P])
                                    it.tr.append([T3,T5,0])
            tmpeqConLi = []
            
            for T in it.eqConLi:
                tmpeqConLi.append(T)
            for T6 in tmpeqConLi:
                for T7 in tmpeqConLi:
                    if (set(T6.split("\\n")).issubset(set(T7.split("\\n"))) and T6 != T7 and T6 in it.eqConLi):
                        it.eqConLi.remove(T6)
            
            tmpTr = list(it.tr)
            
            for T in it.eqConLi:
                newT = self.restructureCbNames(T, it.firstTName)
                tmpComLi.append(newT)
                tmpCom += "  \""+newT+"\"\n"
                if self.isCbInterTaxonomy(newT):
                    self.addRcgVizNode(newT, "comb")
                self.addRcgAllVizNode(newT, "comb")
                
            # Duplicates
            tmpTr = list(it.tr)
            for [T1, T2, P] in tmpTr:
                if(it.tr.count([T1, T2, P]) > 1):
                    it.tr.remove([T1, T2, P])
            tmpTr = list(it.tr)
            for [T1, T2, P] in tmpTr:
                if(P == 0):
                    if(it.tr.count([T1, T2, 1]) > 0):
                        it.tr.remove([T1, T2, 1])
            tmpTr = list(it.tr)
            for [T1, T2, P] in tmpTr:
                if T1 == T2:
                    it.tr.remove([T1, T2, P])
                
            # Reductions
            tmpTr = list(it.tr)
            for [T1, T2, P1] in tmpTr:
                for [T3, T4, P2] in tmpTr:
                    if (T2 == T3):
                        if(it.tr.count([T1, T4, 0])>0):
                            it.tr.remove([T1, T4, 0])
                            it.tr.append([T1, T4, 2])
                        if(it.tr.count([T1, T4, 1])>0):
                            it.tr.remove([T1, T4, 1])
                            #it.tr.append([T1, T4, 3])
    
            #    print "Transitive reduction:"
            #    print it.tr
                
            # restructure for cb visualization
            for [T1, T2, P] in it.tr:
                if (T1.find("*") != -1 or T1.find("\\\\") != -1):
                    newT1 = self.restructureCbNames(T1, it.firstTName)
                    it.tr[it.tr.index([T1,T2,P])] = [newT1, T2, P]
            
            for [T1, T2, P] in it.tr:
                if (T2.find("*") != -1 or T2.find("\\\\") != -1):
                    newT2 = self.restructureCbNames(T2, it.firstTName)
                    it.tr[it.tr.index([T1,T2,P])] = [T1, newT2, P]
            
            # Node Coloring (Creating dot file, will be replaced by stylesheet processor)
            for [T1, T2, P] in it.tr:
                if(T1.find("*") == -1 and T1.find("\\") == -1 and T1.find("\\n") == -1 and T1.find(".") != -1):
                    T1s = T1.split(".")
                    if it.firstTName == T1s[0]:
                        taxa1 += "  \""+T1+"\"\n"               # used in old viz
                    else:
                        taxa2 += "  \""+T1+"\"\n"
                    self.addRcgVizNode(T1s[1], T1s[0])          # used in stylesheet
                    self.addRcgAllVizNode(T1s[1], T1s[0])
                else:

                    if T1[0] != T2[0]:
                        tmpComLi.append(T1)
                        tmpCom += "  \""+T1+"\"\n"
                        self.addRcgVizNode(T1, "comb")
                        self.addRcgAllVizNode(T1, "comb")
                if(T2.find("*") == -1 and T2.find("\\") == -1 and T2.find("\\n") == -1 and T2.find(".") != -1):
                    T2s = T2.split(".")
                    if it.firstTName == T2s[0]:
                        taxa1 += "  \""+T2+"\"\n"
                    else:
                        taxa2 += "  \""+T2+"\"\n"
                    self.addRcgVizNode(T2s[1], T2s[0])
                    self.addRcgAllVizNode(T2s[1], T2s[0])
                else:

                    if T1[0] != T2[0]:
                        tmpComLi.append(T2)
                        tmpCom += "  \""+T2+"\"\n"
                        self.addRcgVizNode(T2, "comb")
                        self.addRcgAllVizNode(T2, "comb")
            
            # prepare for pw2input
            fpw2input = open(pw2inputInternalFile + i.__str__(), "w")
            fpw2input.write("tr = " + repr(it.tr) + '\n')
            fpw2input.write('pwIndex = ' + repr(it.pwIndex) + '\n')
            fpw2input.close()
            
            
            
            for [T1, T2, P] in it.tr:
                if(P == 0):
                    self.addRcgVizEdge(T1, T2, "input")
                elif(P == 1):
                    self.addRcgVizEdge(T1, T2, "inferred")
                elif(P == 2):
                    if False:
                        self.addRcgVizEdge(T1, T2, "redundant")
            
            #if self.args.rcgo:
            if True:
    
                oskiplist = []
                for key in it.mir.keys():
                    if it.mir[key] == self.rcc5["overlaps"] and key not in oskiplist: # and key not in oskiplist
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
                        if "\\n" in replace1 or "\\\\" in replace1:
                            replace1 = self.restructureCbNames(replace1, it.firstTName)
                            self.addRcgVizNode(replace1, "comb")
                            self.addRcgAllVizNode(replace1, "comb")
                        else:
                            self.addRcgVizNode(re.match("(.*)\.(.*)", replace1).group(2), re.match("(.*)\.(.*)", replace1).group(1))
                            self.addRcgAllVizNode(re.match("(.*)\.(.*)", replace1).group(2), re.match("(.*)\.(.*)", replace1).group(1))
                        if "\\n" in replace2 or "\\\\" in replace2:
                            replace2 = self.restructureCbNames(replace2, it.firstTName)
                            self.addRcgVizNode(replace2, "comb")
                            self.addRcgAllVizNode(replace2, "comb")
                        else:
                            self.addRcgVizNode(re.match("(.*)\.(.*)", replace2).group(2), re.match("(.*)\.(.*)", replace2).group(1))
                            self.addRcgAllVizNode(re.match("(.*)\.(.*)", replace2).group(2), re.match("(.*)\.(.*)", replace2).group(1))
                        self.addRcgVizEdge(replace1, replace2, "overlaps")
                        # Skip the reverse pair for redundant edges
                        oskiplist.append(item.group(2)+","+item.group(1))
            
            # special case: only disjoint, no it.tr is empty, RCG will look like input visualization
            if len(it.tr) == 0:
                for key,value in it.mir.iteritems():
                    if it.mir[key] == self.rcc5["disjoint"]:
                        concept1 = key.split(",")[0]
                        concept2 = key.split(",")[1]
                        self.addRcgVizNode(concept1.split(".")[1], concept1.split(".")[0])
                        self.addRcgVizNode(concept2.split(".")[1], concept2.split(".")[0])
            
            
            # create the visualization file
            rcgYamlFile = os.path.join(self.pwsvizdir, it.fileName+".yaml")
            rcgDotFile = os.path.join(self.pwsvizdir, it.fileName+".gv")
            rcgPdfFile = os.path.join(self.pwsvizdir, it.fileName+".pdf")
            rcgSvgFile = os.path.join(self.pwsvizdir, it.fileName+".svg")
            fRcgVizYaml = open(rcgYamlFile, 'w')
            if self.rcgVizNodes:
                fRcgVizYaml.write(yaml.safe_dump(self.rcgVizNodes, default_flow_style=False))
            if self.rcgVizEdges:
                fRcgVizYaml.write(yaml.safe_dump(self.rcgVizEdges, default_flow_style=False))
            fRcgVizYaml.close()
            
            # check whether stylesheet taxonomy names are in stylesheet
            global styles
            with open(self.stylesheetdir+"rcgstyle.yaml") as rcgStyleFileOld:
                styles = yaml.load(rcgStyleFileOld)
                        
            # if taxonomy names are not in stylesheet, rewrite styesheet
            if it.firstTName not in styles["nodestyle"] or it.secondTName not in styles["nodestyle"]:
                fOld = open(self.stylesheetdir+"rcgstyle.yaml", "r")
                contents = fOld.readlines()
                fOld.close()
                
                for line in contents:
                    if "nodestyle" in line:
                        index = contents.index(line)
                    if '"1":' in line:
                        index2 = contents.index(line)
                
                del contents[index+1:index2]    # clean nodestyle previously added
                    
                value = '    "' + it.firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"',2) + '"\n    "' + it.secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"',2) + '"\n' 
                                    
                contents.insert(index+1, value)
    
                fNew = open(self.stylesheetdir+"rcgstyle.yaml", "w")
                contents = "".join(contents)
                fNew.write(contents)
                fNew.close()
            
            
            # apply the rcgviz stylesheet
            newgetoutput("cat "+rcgYamlFile+" | y2d -s "+self.stylesheetdir+"rcgstyle.yaml" + ">" + rcgDotFile)
            if self.args['--all']:
                newgetoutput("dot -Tpdf "+rcgDotFile+" -o "+rcgPdfFile)
                newgetoutput("dot -Tsvg "+rcgDotFile+" -o "+rcgSvgFile)
            
            # prepare for aggregate view
            for e in it.tr:
                self.trlist.append(e)
        
        # prepare for aggregate view
        fav = open(avInternalFile, "a")
        fav.write("allRcgNodesDict = " + repr(self.allRcgNodesDict) + '\n')
        fav.write('trlist = ' + repr(self.trlist) + '\n')
        fav.write('avFlag = ' + repr(True) + '\n')
        fav.close()
        
        # prepare for cluster view
        fcv = open(cvInternalFile, "a")
        fcv.write('cvFlag = ' + repr(True) + '\n')
        fcv.close()


    def restructureCbNames(self, cbName, firstTName):
        if cbName.find("*") != -1 or cbName.find("\\\\") != -1:
            newCbName = ""
            cbs = cbName.split("\\n")
            type1 = []              # individual input concepts
            type2 = []              # union merge concepts
            type3 = []              # unique regionss merge concepts
            tmpFirstTs = []
            tmpSecondTs = []

            for cb in cbs:
                if cb.find("\\\\") != -1:
                    type3.append(cb)
                elif cb.find("*") != -1:
                    if cb.split(".")[0] == firstTName:
                        type2.append(cb)
                    else:
                        tmpLi = cb.split("*")
                        type2.append(tmpLi[1] + "*" + tmpLi[0])
                else:
                    if cb.split(".")[0] == firstTName:
                        tmpFirstTs.append(cb)
                    else:
                        tmpSecondTs.append(cb)
            tmpFirstTs.sort()
            tmpSecondTs.sort()
            type1.extend(tmpFirstTs + tmpSecondTs)
            type2.sort()
            type3.sort()
            newCbName = "\\n".join(type1 + type2 + type3)
            return newCbName
        else:
            return cbName
        
    def isCbInterTaxonomy(self, cbName):
        if cbName.find("\\n") == -1:
            return False
        else:
            cbNameLi = cbName.split("\\n")
            for c1 in cbNameLi:
                for c2 in cbNameLi:
                    if c1.split(".")[0] != c2.split(".")[0]:
                        return True
            return False
        
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
        
    def showAV(self):
        print "******aggregates visualization******"
        
        if not os.path.exists(self.pwsaggregatedir):
            os.mkdir(self.pwsaggregatedir)
        
        avInternalFile = os.path.join(self.pwinternalfilesdir, 'av.internal')
        hvInternalFile = os.path.join(self.pwinternalfilesdir, 'hv.internal')
        it = imp.load_source('it', avInternalFile)
        
        # check whether showPW() run first
        if not it.avFlag:
            print 'Need to run "euler2 show pw" first.'
            return
        
        self.allRcgNodesDict = it.allRcgNodesDict
        self.allRcgEdgesDict = it.allRcgEdgesDict
        
        rels = []
        for [T1, T2, P] in it.trlist:
            cnt = 0
            for [T3, T4, P] in it.trlist:
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
            relra = float(rels[i][2]) / float(it.numOfPws)
            newPointDec = (round(pointDG[0] + distR*relra), round(pointDG[1] + distG*relra), round(pointDG[2] + distB*relra))
            newColor = "#" + str(hex(int(newPointDec[0])))[2:] + str(hex(int(newPointDec[1])))[2:] + str(hex(int(newPointDec[2])))[2:]
            rels[i][3] = newColor

        if self.args['<name>'] == 'avStable':
            tmprels = Set()
            removekey = Set()
            for [T1, T2, cnt, color] in rels:
                if cnt == it.numOfPws:
                    tmprels.add(T1)
                    tmprels.add(T2)
            for key, value in self.allRcgNodesDict.iteritems():
                if value['group']  == 'comb':
                    if value['concept'] not in tmprels:
                        removekey.add(key)
                else:
                    if key not in tmprels:
                        removekey.add(key)
            for key in removekey:
                del self.allRcgNodesDict[key]
            for [T1, T2, cnt, color] in rels:
                if cnt == it.numOfPws:
                    self.addRcgAllVizEdge(T1, T2, cnt, it.numOfPws)
        elif self.args['<name>'] == 'avLabile':
            tmprels = Set()
            removekey = Set()
            for [T1, T2, cnt, color] in rels:
                if cnt < it.numOfPws:
                    tmprels.add(T1)
                    tmprels.add(T2)
            for key, value in self.allRcgNodesDict.iteritems():
                if value['group']  == 'comb':
                    if value['concept'] not in tmprels:
                        removekey.add(key)
                else:
                    if key not in tmprels:
                        removekey.add(key)
            for key in removekey:
                del self.allRcgNodesDict[key]
            for [T1, T2, cnt, color] in rels:
                if cnt < it.numOfPws:
                    self.addRcgAllVizEdge(T1, T2, cnt, it.numOfPws)
        else:
            for [T1, T2, cnt, color] in rels:
                self.addRcgAllVizEdge(T1, T2, cnt, it.numOfPws)
        
        # prepare for hierarchy view
        fhv = open(hvInternalFile, "a")
        fhv.write('rels = ' + repr(rels) + '\n')
        fhv.write('hvFlag = ' + repr(True) + '\n')
        fhv.close()
        
        self.addRcgAllVizNumOfPws(it.numOfPws)
                
        rcgAllYamlFile = os.path.join(self.pwsaggregatedir, self.name+"_all.yaml")
        rcgAllDotFile = os.path.join(self.pwsaggregatedir, self.name+"_all.gv")
        rcgAllPdfFile = os.path.join(self.pwsaggregatedir, self.name+"_all.pdf")
        rcgAllSvgFile = os.path.join(self.pwsaggregatedir, self.name+"_all.svg")
        
        fRcgAllVizYaml = open(rcgAllYamlFile, 'w')
        if self.allRcgNodesDict:
            fRcgAllVizYaml.write(yaml.safe_dump(self.allRcgNodesDict, default_flow_style=False))
        if self.allRcgEdgesDict:
            fRcgAllVizYaml.write(yaml.safe_dump(self.allRcgEdgesDict, default_flow_style=False))
        fRcgAllVizYaml.close()
        
        # check whether stylesheet taxonomy names are in stylesheet
        global styles
        with open(self.stylesheetdir+"aggregatestyle.yaml") as rcgAllStyleFileOld:
            styles = yaml.load(rcgAllStyleFileOld)
                    
        # if taxonomy names are not in stylesheet, rewrite styesheet
        if it.firstTName not in styles["nodestyle"] or it.secondTName not in styles["nodestyle"]:
            fOld = open(self.stylesheetdir+"aggregatestyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
            
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if '"1":' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added
                
            value = '    "' + it.firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"',2) + '"\n    "' + it.secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"',2) + '"\n' 
                                
            contents.insert(index+1, value)

            fNew = open(self.stylesheetdir+"aggregatestyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.close()
        
        
        newgetoutput("cat "+rcgAllYamlFile+" | y2d -s "+self.stylesheetdir+"aggregatestyle.yaml" + ">" + rcgAllDotFile)
        if self.args['--all']:
            newgetoutput("dot -Tpdf "+rcgAllDotFile+" -o "+rcgAllPdfFile)
            newgetoutput("dot -Tsvg "+rcgAllDotFile+" -o "+rcgAllSvgFile)
        
    
    def addRcgAllVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        node.update({"name": "test" + str(randint(0,100))})
        self.allRcgNodesDict.update({group + "." + concept: node})

    def addRcgAllVizEdge(self, s, t, label, numOfPws): #here label is the frequency of the edge among all PWs
        edge = {}
        edge.update({"label" : label})
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"w" : label})
        self.allRcgEdgesDict.update({s + "_" + t : edge})
        
    def addRcgAllVizNumOfPws(self, numOfPws):
        pw = {}
        pw.update({"PW" : numOfPws})
        self.allRcgEdgesDict.update({"Graph" : pw})
        
        
    def showCV(self):
        print "******cluster visualization******"
        
        if not os.path.exists(self.pwsaggregatedir):
            os.mkdir(self.pwsaggregatedir)
        
        cvInternalFile = os.path.join(self.pwinternalfilesdir, 'cv.internal')
        it = imp.load_source('it', cvInternalFile)
        
        if not it.cvFlag:
            print 'Need to run "euler2 show pw" first.'
            return
        
        # if there is only one PW, showCV will return nothing
        if it.npw == 1:
            print "There is only ONE possible world, no cluster view."
            return
        
        obs = False
        simpCluster = True
        
        clfile = os.path.join(self.pwsaggregatedir, self.name+"_cl.csv")
        fcl = open(clfile, 'w')
        dmatrix = []
        for i in range(it.npw):
            dmatrix.append([])
            for j in range(i+1):
                if i == j :
                    dmatrix[i].append(0)
                    fcl.write("0 "); continue
                d = 0
                s = ""
                if obs:
                    for ob in it.pws[i]:
                        if ob not in it.pws[j]: d += 1
                    for ob in it.pws[j]:
                        if ob not in it.pws[i]: d += 1
                else:
                    for key in it.pws[i].keys():
                        if it.pws[i][key] != it.pws[j][key]: 
                            s = s + key\
                                  + " " + findkey(self.relation, it.pws[i][key]).__str__()\
                                  + " " + findkey(self.relation, it.pws[j][key]).__str__() + ";"
                            d += 1
                fcl.write(d.__str__()+" ")
                dmatrix[i].append(d)
                if i != j and not simpCluster:
                    self.addClusterVizNode('pw' + i.__str__())
                    self.addClusterVizNode('pw' + j.__str__())
                    self.addClusterVizEdge('pw' + i.__str__(), 'pw' + j.__str__(), d.__str__()+"; "+s)
            fcl.write("\n")
        if simpCluster:
            for i in range(it.npw):
                for j in range(i):
                    reduced = False
                    for k in range(it.npw):
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
                        self.addClusterVizNode('pw' + i.__str__())
                        self.addClusterVizNode('pw' + j.__str__())
                        self.addClusterVizEdge('pw' + i.__str__(), 'pw' + j.__str__(), dmatrix[i][j].__str__())

        fcl.close()
        
        clyaml = os.path.join(self.pwsaggregatedir, self.name+"_cl.yaml")
        cldot = os.path.join(self.pwsaggregatedir, self.name+"_cl.gv")
        cldotpdf = os.path.join(self.pwsaggregatedir, self.name+"_cl_dot.pdf")
        cldotsvg = os.path.join(self.pwsaggregatedir, self.name+"_cl_dot.svg")
        clneatopdf = os.path.join(self.pwsaggregatedir, self.name+"_cl_neato.pdf")
        clneatosvg = os.path.join(self.pwsaggregatedir, self.name+"_cl_neato.svg")
        
        fclyaml = open(clyaml, 'w')
        if self.clusterVizNodes:
            fclyaml.write(yaml.safe_dump(self.clusterVizNodes, default_flow_style=False))
        if self.clusterVizEdges:
            fclyaml.write(yaml.safe_dump(self.clusterVizEdges, default_flow_style=False))
        fclyaml.close()
        
        newgetoutput("cat "+clyaml+" | y2d -s "+self.stylesheetdir+"clusterstyle.yaml" + ">" + cldot)
        newgetoutput("neato -Tpdf "+cldot+" -o "+clneatopdf)
        if self.args['--all']:
            newgetoutput("dot -Tpdf "+cldot+" -o "+cldotpdf)
            newgetoutput("dot -Tsvg "+cldot+" -o "+cldotsvg)
            newgetoutput("neato -Tsvg "+cldot+" -o "+clneatosvg)        

        
        
    def addClusterVizNode(self, concept):
        node = {}
        node.update({"concept": concept})
        node.update({"group": "cluster"})
        node.update({"name": "test" + str(randint(0,100))})
        self.clusterVizNodes.update({concept: node})

    def addClusterVizEdge(self, s, t, label):
        edge = {}
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"label" : label})
        edge.update({"dist" : int(label)})
        self.clusterVizEdges.update({s + "_" + t : edge})
        
    def showHV(self):
        print "******hierarchy visualization******"
        
        if not os.path.exists(self.pwsaggregatedir):
            os.mkdir(self.pwsaggregatedir)
        
        hvInternalFile = os.path.join(self.pwinternalfilesdir, 'hv.internal')
        it = imp.load_source('it', hvInternalFile)
        
        if not it.hvFlag:
            print 'Need to run "euler2 show pw" and "euler2 show av" first.'
            return
        
        paths = []
        mergedNodes = []
        for rel in it.rels:
            if len(paths) == 0:
                paths.append([rel[0], rel[1]])
            else:
                update = []
                for path in paths:
                    if rel[0] in path:
                        tmp = path[0:path.index(rel[0])+1]
                        tmp.append(rel[1])
                        update.append(tmp)
                    if rel[1] in path:
                        tmp = path[path.index(rel[1]):len(path)]
                        tmp.insert(0,rel[0])
                        update.append(tmp)
                    if rel[0] not in path and rel[1] not in path:
                        update.append([rel[0], rel[1]])
                paths.extend(update)
                self.remove_duplicate_string(paths)
        cycles = []
        for path in paths:
            if path[0] == path[len(path)-1]:
                cycles.append(path)
        for cycle1 in cycles:
            mergedNode = cycle1
            for cycle2 in cycles:
                if cycle1 != cycle2 and set(cycle1) & set(cycle2):
                    mergedNode.extend(cycle2)
                    mergedNode = list(set(mergedNode))
            mergedNodes.append(sorted(mergedNode))
        self.remove_duplicate_string(mergedNodes)
        #self.genHierarchyDot(it.rels, mergedNodes)
        
        # generate dot file
        supernodes = []
        nodes = []
        tmprels = copy.deepcopy(it.rels)
        for rel in tmprels:
            for mergedNode in mergedNodes:
                if rel[0] in mergedNode:
                    newName = self.getCollapsedNode(mergedNode)
                    rel[0] = newName
                    supernodes.append(rel[0])
                if rel[1] in mergedNode:
                    newName = self.getCollapsedNode(mergedNode)
                    rel[1] = newName
                    supernodes.append(rel[1])
        self.remove_duplicate_string(supernodes)
        for rel in tmprels:
            if rel[0] not in supernodes:
                nodes.append(rel[0])
            if rel[1] not in supernodes:
                nodes.append(rel[1])
        self.remove_duplicate_string(nodes)
        
        # write to dot file
        fDot = open(self.hrdot, 'w')
        fDot.write("digraph {\n\nrankdir = RL\n\n")
        for node in nodes:
            if(node.find("*") == -1 and node.find("\\") == -1 and node.find("\\n") == -1 and node.find(".") != -1):
#                self.addHierarchyVizNode(node.split(".")[1], node.split(".")[0])
                if node.split(".")[0] == it.firstTName:
                    fDot.write('"' + node + '" [shape=box style="filled" fillcolor="#CCFFCC"]\n')
                else:
                    fDot.write('"' + node + '" [shape=octagon style="filled" fillcolor="#FFFFCC"]\n')
            else:
#                self.addHierarchyVizNode(node, 'comb')
                fDot.write('"' + node + '" [shape=box style="filled,rounded" fillcolor="#EEEEEE"]\n')
        for supernode in supernodes:
#            self.addHierarchyVizNode(node, 'supernode')
            fDot.write('"' + supernode + '" [shape=oval style="filled,rounded" fillcolor="#00BFFF"]\n')
        for rel in tmprels:
            if rel[0] != rel[1]:
#                self.addHierarchyVizEdge(rel[0], rel[1], rel[2])
                fDot.write("\"" + rel[0] + "\" -> \"" + rel[1] + "\" [style=filled,label=" + str(rel[2]) + ",color=\"" + rel[3] + "\"];\n")                     
        fDot.write("}\n")
        fDot.close()
        
#        hvyaml = os.path.join(self.pwsaggregatedir, self.name+"_hv.yaml")
#        hvdot = os.path.join(self.pwsaggregatedir, self.name+"_hv.gv")
#        hvdotpdf = os.path.join(self.pwsaggregatedir, self.name+"_hv.pdf")
#        hvdotsvg = os.path.join(self.pwsaggregatedir, self.name+"_hv.svg")
#        
#        fhvyaml = open(hvyaml, 'w')
#        if self.hierarchyVizNodes:
#            fhvyaml.write(yaml.safe_dump(self.hierarchyVizNodes, default_flow_style=False))
#        if self.hierarchyVizEdges:
#            fhvyaml.write(yaml.safe_dump(self.hierarchyVizEdges, default_flow_style=False))
#        fhvyaml.close()
#        
#        newgetoutput("cat "+hvyaml+" | y2d -s "+self.stylesheetdir+"hierarchystyle.yaml" + ">" + hvdot)
#        newgetoutput("dot -Tpdf "+hvdot+" -o "+hvdotpdf)
#        newgetoutput("dot -Tsvg "+hvdot+" -o "+hvdotsvg)

        
    def getCollapsedNode(self, mergedNode):
        name = ""
        for singleNode in mergedNode:
            name += singleNode + "\\n\\n"
        return name
    
    def addHierarchyVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        node.update({"name": "test" + str(randint(0,100))})
        self.hierarchyVizNodes.update({group + "." + concept: node})

    def addHierarchyVizEdge(self, s, t, label):
        edge = {}
        edge.update({"label" : label})
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"w" : label})
        self.hierarchyVizEdges.update({s + "_" + t : edge})
        
    def showInconLAT(self):
        
        #if not os.path.exists(self.latticedir):
        #    os.mkdir(self.latticedir)

        fileName = self.name + ".txt"
        call("lattice.sh " + fileName, shell=True)
        #call("maslattice.sh " + fileName, shell=True)

    def showAmbLAT(self):
        
        #if not os.path.exists(self.latticedir):
        #    os.mkdir(self.latticedir)

        fileName = self.name + ".txt"
        call("maslattice.sh " + fileName, shell=True)
        #call("maslattice.sh " + fileName, shell=True)
        
    def showPW2INPUT(self):
        print "******transfer possible worlds to input file******"
        
        if not os.path.isfile(os.path.join(self.pwinternalfilesdir, 'pw2input.internal0')):
            print 'Need to run "euler2 show pw" first.'
            return
        
        if not os.path.exists(self.mergeinputdir):
            os.mkdir(self.mergeinputdir)
            
        numOfPws = len([f for f in os.walk(self.pwinternalfilesdir).next()[2] if f[0:17] == "pw2input.internal" and f[-1] != 'c'])
        for i in range(numOfPws):

            pw2inputInternalFile = os.path.join(self.pwinternalfilesdir, 'pw2input.internal' + i.__str__())
            it = imp.load_source('it', pw2inputInternalFile)
            
            pcs = []
            tr = list(it.tr)
            
            # rename of all concepts in tr
            tmptr = list(tr)
            for [T1,T2,P] in tmptr:
                T1rename = T1.replace(".","_")
                T2rename = T2.replace(".","_")
                if tr.count([T1,T2,P]) > 0:
                    tr.remove([T1,T2,P])
                    tr.append([T1rename,T2rename,P])
            
            # get all parent-child relations
            for [T1,T2,P] in tr:
                if P != 2:
                    if len(pcs) == 0:
                        pcs.append([T2,T1])
                    else:
                        for pc in pcs:
                            if T2 == pc[0]:
                                pc.append(T1)
                                break
                            else:
                                pcs.append([T2,T1])
            
            # remove duplicates in each pc with order preserving
            tmptr = list(pcs)
            for pc in tmptr:
                noDupPc = []
                [noDupPc.append(i) for i in pc if not noDupPc.count(i)]
                if pcs.count(pc) > 0:
                    pcs.remove(pc)
                    pcs.append(noDupPc)
                    
            # remove duplicates in pcs
            tmptr1 = list(pcs)
            tmptr2 = list(pcs)
            for tr1 in tmptr1:
                for tr2 in tmptr2:
                    if tr1[0] == tr2[0] and tr1 != tr2 and set(tr1).issubset(set(tr2)):
                        if pcs.count(tr1):
                            pcs.remove(tr1)
            
            # generate merged input file
            
            fileName = os.path.join(self.mergeinputdir, self.name+"-merge-input"+it.pwIndex.__str__()+".txt")
            f = open(fileName, "w")
            f.write('taxonomy merge mergeTax\n')
            for pc in pcs:
                str = ""
                f.write('(')
                for e in pc:
                    str += e + " "
                f.write(str.strip())
                f.write(')\n')
            f.close()
        


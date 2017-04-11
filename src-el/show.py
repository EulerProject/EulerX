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
import operator
from random import randint
from helper import *
from subprocess import call
from sets import Set
from diaglattice import *

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
        self.userdir = ''
        self.lastruntimestamp = os.path.join(self.projectdir, self.runningUser+'-'+self.runningHost+'-lastrun.timestamp')
        self.exampleName = ''        
        if os.path.isfile(self.lastruntimestamp):
            f = open(self.lastruntimestamp, "r")
            self.lastrundir = f.readline().strip()
            self.userdir = re.match('(.*)/(.*)', self.lastrundir).group(1)
            self.name = f.readline()
            f.close()
        
        if args['-o']:
            self.lastrundir = args['-o']
            self.exampleName = os.path.join(args['-o'], 'lastrun.timestamp')
            if os.path.isfile(self.exampleName):
                f = open(self.exampleName, "r")
                self.name = f.readline().strip()
            else:
                if self.name == '':
                    self.name = os.path.splitext(os.path.basename(sys.argv[2]))[0]
        
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
        self.hvdot = os.path.join(self.pwsaggregatedir, self.name + "_hv.gv")
        
        self.latticedir = os.path.join(self.lastrundir, "6-Lattices")
        
        self.mergeinputdir = os.path.join(self.lastrundir, "7-Merge-input")
        
        self.logdir = os.path.join(self.lastrundir, "logs")
        self.output = os.path.join(self.logdir, self.name + ".stdout")
        
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
        
        if self.args['<inputfile>'] and (self.args['iv'] or self.args['tv']):
            self.showIV()
        
        elif not os.path.isfile(self.lastruntimestamp) and not os.path.isfile(self.exampleName):
            print 'Nothing to show, need to run "euler2 align" first.\n'
            print 'Use "euler2 -h" to see more help.'
        else:
            # show other stuff
            if self.args['<name>'] == 'iv' or self.args['<name>'] == 'tv':
                self.showIV()
            if self.args['<name>'] == 'pw':    # possible worlds
                self.showPW()
            if self.args['<name>'] == 'sv':    # summary view, including av (stable and labile), cv, hv
                # if this is an inconsistent example (there is no PW)
                if not os.path.isfile(os.path.join(self.pwinternalfilesdir, self.name+".pw")):
                    print "This is an inconsistent example, no summary view of possible worlds."
                    return
                # if not run align first
                if not self.checkPwFlag():
                    print 'Need to run "euler2 show pw" first.'
                    return
                self.showAV("regular")
                self.showAV("avStable")
                self.showAV("avLabile")
                self.showCV()
                self.showHV()
            #if self.args['<name>'] == 'cv':    # cluster view
            #    self.showCV()
            #if self.args['<name>'] == 'hv':    # hierarchy view
            #    self.showHV()
            if self.args['<name>'] == 'inconLat':   # inconsistency lattice 
                self.showInconLAT()
            if self.args['<name>'] == 'fourinone':   # 4-in-1 lattice 
                self.showFourinoneLAT()
            if self.args['<name>'] == 'ambLat':   # ambiguity lattice 
                self.showAmbLAT()
            if self.args['<name>'] == 'pw2input':   # transfer PW to input 
                self.showPW2INPUT()
            
        self.refreshStylesheets()
        
        return

    def refreshStylesheets(self):            
        if (os.path.isfile(self.stylesheetdir+"inputstyle.yaml")):
            fOld = open(self.stylesheetdir+"inputstyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
                
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'all:' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added        
            fNew = open(self.stylesheetdir+"inputstyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()
        
        if (os.path.isfile(self.stylesheetdir+"rcgstyle.yaml")):
            fOld = open(self.stylesheetdir+"rcgstyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
                
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'default:' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added
            fNew = open(self.stylesheetdir+"rcgstyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()
            
        if (os.path.isfile(self.stylesheetdir+"zoominstyle.yaml")):
            fOld = open(self.stylesheetdir+"zoominstyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
                
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'default:' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added
            fNew = open(self.stylesheetdir+"zoominstyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()
        
        if (os.path.isfile(self.stylesheetdir+"aggregatestyle.yaml")):
            fOld = open(self.stylesheetdir+"aggregatestyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
                
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'default:' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added
            fNew = open(self.stylesheetdir+"aggregatestyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()
    
        if (os.path.isfile(self.stylesheetdir+"inputtaxonomystyle.yaml")):
            fOld = open(self.stylesheetdir+"inputtaxonomystyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
                
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'all:' in line:
                    index2 = contents.index(line)
            
            del contents[index+1:index2]    # clean nodestyle previously added        
            fNew = open(self.stylesheetdir+"inputtaxonomystyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()       
            
        return
    

    
    def showIV(self):
        print "******input visualization******"
        if self.args['<inputfile>'] and (self.args['iv'] or self.args['tv']):
            inputData = []
            for eachFile in self.args['<inputfile>']:
                inputData += open(eachFile).readlines()
        else:
            inputFile = os.path.join(self.inputfilesdir, self.name+".txt")
        fileName = ""
        for i in range(len(self.args['<inputfile>'])):
            fileName += os.path.splitext(os.path.basename(self.args['<inputfile>'][i]))[0] + "-"
        fileName = fileName[:-1] 
        
        group2concepts = {}
        art = []
        firstTName = ""
        secondTName = ""
        thirdTName = ""
        fourthTName = ""
        fifthTName = ""
        taxName = ""
        
        if self.args['<inputfile>'] and (self.args['iv'] or self.args['tv']):
            lines = inputData
        else:
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
                    
                if firstTName != "" and secondTName != "" and thirdTName == "" \
                    and firstTName != taxName and secondTName != taxName:
                    thirdTName = taxName
                    
                if firstTName != "" and secondTName != "" and thirdTName != "" \
                    and fourthTName == "" and firstTName != taxName and secondTName != taxName and thirdTName != taxName:
                    fourthTName = taxName
                
                if firstTName != "" and secondTName != "" and thirdTName != "" \
                    and fourthTName != "" and fifthTName == "" and firstTName != taxName and secondTName != taxName \
                    and thirdTName != taxName and fourthTName != taxName:
                    fifthTName = taxName
            
            elif (re.match("\(.*\)", line)):
                
                conceptsToAdd = re.match("\((.*)\)", line).group(1).split(" ")
                # check multiple nc
                for c in conceptsToAdd:
                    if c == 'nc':
                        conceptsToAdd[conceptsToAdd.index(c)] = 'nc_' + conceptsToAdd[0]
                        
                if taxName in group2concepts:
                    group2concepts[taxName].append(conceptsToAdd)
                else:
                    group2concepts[taxName] = [conceptsToAdd]
                    
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
        
        if self.args['<inputfile>'] and self.args['iv'] or self.args['<name>'] == 'iv':
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
        if self.args['<inputfile>'] and self.args['iv'] or self.args['<name>'] == 'iv':
            if self.args['<inputfile>'] and self.args['iv'] and not self.args['-o']:
                inputYamlFile = fileName+".yaml"
                inputDotFile = fileName+".gv"
                inputPdfFile = fileName+".pdf"
                inputSvgFile = fileName+".svg"
            else:
                if not os.path.exists(self.inputfilesdir):
                    os.makedirs(self.inputfilesdir)
                inputYamlFile = os.path.join(self.inputfilesdir, self.name+".yaml")
                inputDotFile = os.path.join(self.inputfilesdir, self.name+".gv")
                inputPdfFile = os.path.join(self.inputfilesdir, self.name+".pdf")
                inputSvgFile = os.path.join(self.inputfilesdir, self.name+".svg")
            
        if self.args['<inputfile>'] and self.args['tv'] or self.args['<name>'] == 'tv':
            if self.args['<inputfile>'] and self.args['tv'] and not self.args['-o']:
                inputYamlFile = fileName+"_tax.yaml"
                inputDotFile = fileName+"_tax.gv"
                inputPdfFile = fileName+"_tax.pdf"
                inputSvgFile = fileName+"_tax.svg"
            else:
                if not os.path.exists(self.inputfilesdir):
                    os.makedirs(self.inputfilesdir)
                inputYamlFile = os.path.join(self.inputfilesdir, self.name+"_tax.yaml")
                inputDotFile = os.path.join(self.inputfilesdir, self.name+"_tax.gv")
                inputPdfFile = os.path.join(self.inputfilesdir, self.name+"_tax.pdf")
                inputSvgFile = os.path.join(self.inputfilesdir, self.name+"_tax.svg")
        
        fInputVizYaml = open(inputYamlFile, 'w')
        if self.inputVizNodes:
            fInputVizYaml.write(yaml.safe_dump(self.inputVizNodes, default_flow_style=False))
        if self.inputVizEdges:
            fInputVizYaml.write(yaml.safe_dump(self.inputVizEdges, default_flow_style=False))
        fInputVizYaml.close()        
        
        # check whether stylesheet taxonomy names are in stylesheet
        global styles
        if self.args['iv'] or self.args['<name>'] == 'iv':
            styleFilesToRead = self.stylesheetdir+"inputstyle.yaml"
        if self.args['tv'] or self.args['<name>'] == 'tv':
            styleFilesToRead = self.stylesheetdir+"inputtaxonomystyle.yaml"
            
        with open(styleFilesToRead) as inputStyleFileOld:
            styles = yaml.load(inputStyleFileOld)
                    
#        # if taxonomy names are not in stylesheet, rewrite styesheet
        if firstTName not in styles["nodestyle"] or secondTName not in styles["nodestyle"] \
           or thirdTName not in styles["nodestyle"] or fourthTName not in styles["nodestyle"] \
           or fifthTName not in styles["nodestyle"]:
            value = ""
            fOld = open(styleFilesToRead, "r")
            contents = fOld.readlines()
            fOld.close()
            
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'all:' in line:
                    index2 = contents.index(line)
            
            #del contents[index+1:index2]    # clean nodestyle previously added
            
            if firstTName != "" and firstTName not in styles["nodestyle"]:
                value += '    "' + firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"') + '"\n'
            if secondTName != "" and secondTName not in styles["nodestyle"]:
                value += '    "' + secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"') + '"\n'
            if thirdTName != "" and thirdTName not in styles["nodestyle"]:
                value += '    "' + thirdTName + '": "' + styles["nodestyle"]["3"].replace('"','\\"') + '"\n' 
            if fourthTName != "" and fourthTName not in styles["nodestyle"]:
                value += '    "' + fourthTName + '": "' + styles["nodestyle"]["4"].replace('"','\\"') + '"\n'
            if fifthTName != "" and fifthTName not in styles["nodestyle"]: 
                value += '    "' + fifthTName + '": "' + styles["nodestyle"]["5"].replace('"','\\"') + '"\n' 
                                
            contents.insert(index+1, value)

            fNew = open(styleFilesToRead, "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
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
                    if 'all:' in line:
                        index2 = contents.index(line)
                
                #del contents[index+1:index2]    # clean nodestyle previously added
                    
                value = '    "' + firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"',2) + '"\n    "' + secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"',2) + '"\n' 
                                    
                contents.insert(index+1, value)
    
                fNew = open(self.stylesheetdir+"singletoninputstyle.yaml", "w")
                contents = "".join(contents)
                fNew.write(contents)
                fNew.flush()
                fNew.close()
        
        # apply the inputviz stylesheet
        if not firstTName or not secondTName:
            newgetoutput("cat "+inputYamlFile+" | y2d -s "+self.stylesheetdir+"singletoninputstyle.yaml" + ">" + inputDotFile)
        else:
            newgetoutput("cat "+inputYamlFile+" | y2d -s "+styleFilesToRead + ">" + inputDotFile)
        if self.args['--svg']:
            newgetoutput("dot -Tsvg "+inputDotFile+" -o "+inputSvgFile)
        else:
            newgetoutput("dot -Tpdf "+inputDotFile+" -o "+inputPdfFile)
        
    def addInputVizNode(self, concept, group, pathlen):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
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
        # if this is an inconsistent example (there is no PW)
        if not os.path.isfile(os.path.join(self.pwinternalfilesdir, self.name+".pw")) \
        and not os.path.isfile(os.path.join(self.pwinternalfilesdir, "pw.internal0")):
            print "This is an inconsistent example, no possible worlds generated."
            return
        
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
#            taxa1 = ""     # cache of taxa in the first taxonomy
#            taxa2 = ""     # cache of taxa in the second taxonomy
            tmpComLi = [] # cache of list of combined taxa for --rcgo option in RCG
            replace1 = "" # used for replace combined concept in --rcgo option in RCG
            replace2 = "" # used for replace combined concept in --rcgo option in RCG
            rcgVizNodes = {} # used for rcg nodes visualization in stylesheet
            rcgVizEdges = {} # used for rcg edges visualization in stylesheet

            alias = {}
            
            
            # create it.eqConLi
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
                
                    
                for T2 in it.eq[T1]:

                    tmpTr = list(it.tr)
                    for [T3, T4, P] in tmpTr:
                        if(T1 == T3 or T2 == T3):
                            if it.tr.count([T3, T4, P]) > 0:
                                it.tr.remove([T3, T4, P])
                                it.tr.append([tmpStr, T4, P])
                        elif(T1 == T4 or T2 == T4):
                            if it.tr.count([T3, T4, P]) > 0:
                                it.tr.remove([T3, T4, P])
                                it.tr.append([T3, tmpStr, P])
            
            tmpTr = list(it.tr)
            for [T3, T4, P] in tmpTr:
                for T5 in it.eqConLi:
                    if(T3 != T5 and set(T3.split("\\n")).issubset(set(T5.split("\\n")))):
                        if it.tr.count([T3, T4, P]) > 0:
                            it.tr.remove([T3, T4, P])
                            it.tr.append([T5,T4,P])
            tmpTr = list(it.tr)
            for [T3, T4, P] in tmpTr:
                for T5 in it.eqConLi:
                    if(T4 != T5 and set(T4.split("\\n")).issubset(set(T5.split("\\n")))):
                        if it.tr.count([T3, T4, P]) > 0:
                            it.tr.remove([T3, T4, P])
                            it.tr.append([T3,T5,P])
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
                g = self.defineCombConceptGroup(newT, it.firstTName, it.secondTName, it.thirdTName, it.fourthTName, it.fifthTName)
                #if self.isCbInterTaxonomy(newT):
                self.addRcgVizNode(newT, g)
                self.addRcgAllVizNode(newT, g)
                
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
#                    if it.firstTName == T1s[0]:
#                        taxa1 += "  \""+T1+"\"\n"               # used in old viz
#                    else:
#                        taxa2 += "  \""+T1+"\"\n"
                    self.addRcgVizNode(T1s[1], T1s[0])          # used in stylesheet
                    self.addRcgAllVizNode(T1s[1], T1s[0])
                else:
                    tmpComLi.append(T1)
                    tmpCom += "  \""+T1+"\"\n"
                    g = self.defineCombConceptGroup(T1, it.firstTName, it.secondTName, it.thirdTName, it.fourthTName, it.fifthTName)
                    self.addRcgVizNode(T1, g)
                    self.addRcgAllVizNode(T1, g)
                
                if(T2.find("*") == -1 and T2.find("\\") == -1 and T2.find("\\n") == -1 and T2.find(".") != -1):
                    T2s = T2.split(".")
#                    if it.firstTName == T2s[0]:
#                        taxa1 += "  \""+T2+"\"\n"
#                    else:
#                        taxa2 += "  \""+T2+"\"\n"
                    self.addRcgVizNode(T2s[1], T2s[0])
                    self.addRcgAllVizNode(T2s[1], T2s[0])
                else:
                    tmpComLi.append(T2)
                    tmpCom += "  \""+T2+"\"\n"
                    g = self.defineCombConceptGroup(T2, it.firstTName, it.secondTName, it.thirdTName, it.fourthTName, it.fifthTName)
                    self.addRcgVizNode(T2, g)
                    self.addRcgAllVizNode(T2, g)
            
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
            if not self.args['--hideoverlaps']:
    
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
                        if "\\n" in replace1 or "\\\\" in replace1 or "*" in replace1:
                            replace1 = self.restructureCbNames(replace1, it.firstTName)
                            g = self.defineCombConceptGroup(replace1, it.firstTName, it.secondTName, it.thirdTName, it.fourthTName, it.fifthTName)
                            self.addRcgVizNode(replace1, g)
                            self.addRcgAllVizNode(replace1, g)
                        else:
                            self.addRcgVizNode(re.match("(.*)\.(.*)", replace1).group(2), re.match("(.*)\.(.*)", replace1).group(1))
                            self.addRcgAllVizNode(re.match("(.*)\.(.*)", replace1).group(2), re.match("(.*)\.(.*)", replace1).group(1))
                        if "\\n" in replace2 or "\\\\" in replace2 or "*" in replace2:
                            replace2 = self.restructureCbNames(replace2, it.firstTName)
                            g = self.defineCombConceptGroup(replace2, it.firstTName, it.secondTName, it.thirdTName, it.fourthTName, it.fifthTName)
                            self.addRcgVizNode(replace2, g)
                            self.addRcgAllVizNode(replace2, g)
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
                        flagConcept1 = False
                        flagConcept2 = False
                        for k,v in self.rcgVizNodes.iteritems():
                            if concept1 in k:
                                flagConcept1 = True
                            if concept2 in k:
                                flagConcept2 = True
                        if not flagConcept1:
                            self.addRcgVizNode(concept1.split(".")[1], concept1.split(".")[0])
                        if not flagConcept2:
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
            stylesheetname = ""
            if "mncb" in it.fileName:
                stylesheetname = "zoominstyle.yaml"
            else:
                stylesheetname = "rcgstyle.yaml"
            
            global styles    
            with open(self.stylesheetdir+stylesheetname) as rcgStyleFileOld:
                styles = yaml.load(rcgStyleFileOld)
                        
            # if taxonomy names are not in stylesheet, rewrite styesheet
            if it.firstTName not in styles["nodestyle"] or it.secondTName not in styles["nodestyle"] \
                or it.thirdTName not in styles["nodestyle"] or it.fourthTName not in styles["nodestyle"] \
                or it.fifthTName not in styles["nodestyle"]:
                value = ""
                fOld = open(self.stylesheetdir+stylesheetname, "r")
                contents = fOld.readlines()
                fOld.close()
                
                for line in contents:
                    if "nodestyle" in line:
                        index = contents.index(line)
                    if 'default:' in line:
                        index2 = contents.index(line)
                
                #del contents[index+1:index2]    # clean nodestyle previously added
                
                if it.firstTName != "" and it.firstTName not in styles["nodestyle"]:
                    value += '    "' + it.firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"') + '"\n'
#                     value += '    "comb' + it.firstTName + '": "' + styles["nodestyle"]["combT1"].replace('"','\\"') + '"\n'
#                     value += '    "sub' + it.firstTName + '": "' + styles["nodestyle"]["subT1"].replace('"','\\"') + '"\n'
                if it.secondTName != "" and it.secondTName not in styles["nodestyle"]:
                    value += '    "' + it.secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"') + '"\n' 
#                     value += '    "comb' + it.secondTName + '": "' + styles["nodestyle"]["combT2"].replace('"','\\"') + '"\n'
#                     value += '    "sub' + it.secondTName + '": "' + styles["nodestyle"]["subT2"].replace('"','\\"') + '"\n'
                if it.thirdTName != "" and it.thirdTName not in styles["nodestyle"]:
                    value += '    "' + it.thirdTName + '": "' + styles["nodestyle"]["3"].replace('"','\\"') + '"\n' 
#                     value += '    "comb' + it.thirdTName + '": "' + styles["nodestyle"]["combT3"].replace('"','\\"') + '"\n'
#                     value += '    "sub' + it.thirdTName + '": "' + styles["nodestyle"]["subT3"].replace('"','\\"') + '"\n'
                if it.fourthTName != "" and it.fourthTName not in styles["nodestyle"]:
                    value += '    "' + it.fourthTName + '": "' + styles["nodestyle"]["4"].replace('"','\\"') + '"\n'
#                     value += '    "comb' + it.fourthTName + '": "' + styles["nodestyle"]["combT4"].replace('"','\\"') + '"\n'
#                     value += '    "sub' + it.fourthTName + '": "' + styles["nodestyle"]["subT4"].replace('"','\\"') + '"\n'
                if it.fifthTName != "" and it.fifthTName not in styles["nodestyle"]: 
                    value += '    "' + it.fifthTName + '": "' + styles["nodestyle"]["5"].replace('"','\\"') + '"\n' 
#                     value += '    "comb' + it.fifthTName + '": "' + styles["nodestyle"]["combT5"].replace('"','\\"') + '"\n'
#                     value += '    "sub' + it.fifthTName + '": "' + styles["nodestyle"]["subT5"].replace('"','\\"') + '"\n'
                                    
                contents.insert(index+1, value)
    
                fNew = open(self.stylesheetdir+stylesheetname, "w")
                contents = "".join(contents)
                fNew.write(contents)
                fNew.flush()
                fNew.close()
            
            
            # apply the rcgviz stylesheet
            newgetoutput("cat "+rcgYamlFile+" | y2d -s "+self.stylesheetdir+stylesheetname + ">" + rcgDotFile)
            if self.args['--svg']:
                newgetoutput("dot -Tsvg "+rcgDotFile+" -o "+rcgSvgFile)
            else:
                newgetoutput("dot -Tpdf "+rcgDotFile+" -o "+rcgPdfFile)
            
            # prepare for aggregate view
            for e in it.tr:
                self.trlist.append(e)
        
        # prepare for aggregate view
        fav = open(avInternalFile, "a")
        fav.write("allRcgNodesDict = " + repr(self.allRcgNodesDict) + '\n')
        fav.write('trlist = ' + repr(self.trlist) + '\n')
        fav.write('avFlag = ' + repr(True) + '\n')
        fav.flush()
        fav.close()
        
        # prepare for cluster view
        #fcv = open(cvInternalFile, "a")
        #fcv.write('cvFlag = ' + repr(True) + '\n')
        #fcv.close()
        
    def defineCombConceptGroup(self, conceptStr, firstTName, secondTName, thirdTName, fourthTName, fifthTName):
        if "\\n" not in conceptStr and (conceptStr.count("\\\\") == 1 or "*" in conceptStr):
            return "newComb"
        elif "\\\\" not in conceptStr:
            return "comb"
        else:
            taxNames = Set()
            concepts = conceptStr.split("\\n")
            for concept in concepts:
                if "\\\\" not in concept and "*" not in concept:
                    return concept.split(".")[0]
            return "newComb"
        
# for old stylesheets
#         if conceptStr.count("\\\\") == 1 and "\\n" not in conceptStr:
#             taxName = conceptStr.split(".")[0]
#             return taxName
# #             if taxName == firstTName:
# #                 return "subT1"
# #             if taxName == secondTName:
# #                 return "subT2"
# #             if taxName == thirdTName:
# #                 return "subT3"
# #             if taxName == fourthTName:
# #                 return "subT4"
# #             if taxName == fifthTName:
# #                 return "subT5"
# #             return "sub"+taxName
#         elif "*" in conceptStr and "\\n" not in conceptStr:
#             return "intersectComb"
#         elif "\\\\" in conceptStr or "*" in conceptStr:
#             return "comb"
#         taxNames = Set()
#         concepts = conceptStr.split("\\n")
#         for concept in concepts:
#             taxNames.add(concept.split(".")[0])
#         if firstTName == "2" and secondTName == "1":
#             if firstTName in taxNames and secondTName not in taxNames:
#                 return "combT2"
#             elif firstTName not in taxNames and secondTName in taxNames:
#                 return "combT1"
#         if firstTName in taxNames and len(taxNames) == 1:
#             return "combT1"
#         if secondTName in taxNames and len(taxNames) == 1:
#             return "combT2"
#         if thirdTName in taxNames and len(taxNames) == 1:
#             return "combT3"
#         if fourthTName in taxNames and len(taxNames) == 1:
#             return "combT4"
#         if fifthTName in taxNames and len(taxNames) == 1:
#             return "combT5"
#         else:
#             return "comb"



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
        self.rcgVizNodes.update({group + "." + concept: node})
    
    def addRcgVizEdge(self, s, t, label):
        edge = {}
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"label" : label})
        self.rcgVizEdges.update({s + "_" + t : edge})
        
    def checkPwFlag(self):
        avInternalFile = os.path.join(self.pwinternalfilesdir, 'av.internal')
        it = imp.load_source('it', avInternalFile)
        # check whether showPW() run first
        if not it.avFlag:
            return False
        else:
            return True
    
    def showAV(self, avType):
        print "******aggregates visualization "+ avType +" ******"
        
        if not os.path.exists(self.pwsaggregatedir):
            os.mkdir(self.pwsaggregatedir)
        
        avInternalFile = os.path.join(self.pwinternalfilesdir, 'av.internal')
        hvInternalFile = os.path.join(self.pwinternalfilesdir, 'hv.internal')
        it = imp.load_source('it', avInternalFile)
        
        # check whether showPW() run first
        #if not it.avFlag:
        #    print 'Need to run "euler2 show pw" first.'
        #    return
        
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

        if avType == 'avStable':
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
        elif avType == 'avLabile':
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
        #fhv.write('hvFlag = ' + repr(True) + '\n')
        fhv.close()
        
        self.addRcgAllVizNumOfPws(it.numOfPws)
                
        rcgAllYamlFile = os.path.join(self.pwsaggregatedir, self.name+"_"+avType+"_all.yaml")
        rcgAllDotFile = os.path.join(self.pwsaggregatedir, self.name+"_"+avType+"_all.gv")
        rcgAllPdfFile = os.path.join(self.pwsaggregatedir, self.name+"_"+avType+"_all.pdf")
        rcgAllSvgFile = os.path.join(self.pwsaggregatedir, self.name+"_"+avType+"_all.svg")
        
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
        if it.firstTName not in styles["nodestyle"] or it.secondTName not in styles["nodestyle"] \
            or it.thirdTName not in styles["nodestyle"] or it.fourthTName not in styles["nodestyle"] \
            or it.fifthTName not in styles["nodestyle"]:
            value = ""
            fOld = open(self.stylesheetdir+"aggregatestyle.yaml", "r")
            contents = fOld.readlines()
            fOld.close()
            
            for line in contents:
                if "nodestyle" in line:
                    index = contents.index(line)
                if 'default:' in line:
                    index2 = contents.index(line)
            
            #del contents[index+1:index2]    # clean nodestyle previously added
            
            if it.firstTName != "" and it.firstTName not in styles["nodestyle"]:
                value += '    "' + it.firstTName + '": "' + styles["nodestyle"]["1"].replace('"','\\"') + '"\n'
#                 value += '    "comb' + it.firstTName + '": "' + styles["nodestyle"]["combT1"].replace('"','\\"') + '"\n'
#                 value += '    "sub' + it.firstTName + '": "' + styles["nodestyle"]["subT1"].replace('"','\\"') + '"\n'
            if it.secondTName != "" and it.secondTName not in styles["nodestyle"]:
                value += '    "' + it.secondTName + '": "' + styles["nodestyle"]["2"].replace('"','\\"') + '"\n' 
#                 value += '    "comb' + it.secondTName + '": "' + styles["nodestyle"]["combT2"].replace('"','\\"') + '"\n'
#                 value += '    "sub' + it.secondTName + '": "' + styles["nodestyle"]["subT2"].replace('"','\\"') + '"\n'
            if it.thirdTName != "" and it.thirdTName not in styles["nodestyle"]:
                value += '    "' + it.thirdTName + '": "' + styles["nodestyle"]["3"].replace('"','\\"') + '"\n' 
#                 value += '    "comb' + it.thirdTName + '": "' + styles["nodestyle"]["combT3"].replace('"','\\"') + '"\n'
#                 value += '    "sub' + it.thirdTName + '": "' + styles["nodestyle"]["subT3"].replace('"','\\"') + '"\n'
            if it.fourthTName != "" and it.fourthTName not in styles["nodestyle"]:
                value += '    "' + it.fourthTName + '": "' + styles["nodestyle"]["4"].replace('"','\\"') + '"\n'
#                 value += '    "comb' + it.fourthTName + '": "' + styles["nodestyle"]["combT4"].replace('"','\\"') + '"\n'
#                 value += '    "sub' + it.fourthTName + '": "' + styles["nodestyle"]["subT4"].replace('"','\\"') + '"\n'
            if it.fifthTName != "" and it.fifthTName not in styles["nodestyle"]: 
                value += '    "' + it.fifthTName + '": "' + styles["nodestyle"]["5"].replace('"','\\"') + '"\n'  
#                 value += '    "comb' + it.fifthTName + '": "' + styles["nodestyle"]["combT5"].replace('"','\\"') + '"\n'
#                 value += '    "sub' + it.fifthTName + '": "' + styles["nodestyle"]["subT5"].replace('"','\\"') + '"\n'
                                
            contents.insert(index+1, value)

            fNew = open(self.stylesheetdir+"aggregatestyle.yaml", "w")
            contents = "".join(contents)
            fNew.write(contents)
            fNew.flush()
            fNew.close()
        
        
        newgetoutput("cat "+rcgAllYamlFile+" | y2d -s "+self.stylesheetdir+"aggregatestyle.yaml" + ">" + rcgAllDotFile)
        if self.args['--svg']:
            newgetoutput("dot -Tsvg "+rcgAllDotFile+" -o "+rcgAllSvgFile)
        else:
            newgetoutput("dot -Tpdf "+rcgAllDotFile+" -o "+rcgAllPdfFile)
        
        
    
    def addRcgAllVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
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
        
        #if not it.cvFlag:
        #    print 'Need to run "euler2 show pw" first.'
        #    return
        
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
        if self.args['--svg']:
            newgetoutput("neato -Tsvg "+cldot+" -o "+clneatosvg)
        else:
            newgetoutput("neato -Tpdf "+cldot+" -o "+clneatopdf)
        #newgetoutput("dot -Tpdf "+cldot+" -o "+cldotpdf)
        #newgetoutput("dot -Tsvg "+cldot+" -o "+cldotsvg)        

        
        
    def addClusterVizNode(self, concept):
        node = {}
        node.update({"concept": concept})
        node.update({"group": "cluster"})
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
        
        #if not it.hvFlag:
        #    print 'Need to run "euler2 show pw" and "euler2 show av" first.'
        #    return
        
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
        fDot = open(self.hvdot, 'w')
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
        hvdot = os.path.join(self.pwsaggregatedir, self.name+"_hv.gv")
        hvdotpdf = os.path.join(self.pwsaggregatedir, self.name+"_hv.pdf")
        hvdotsvg = os.path.join(self.pwsaggregatedir, self.name+"_hv.svg")
#        
#        fhvyaml = open(hvyaml, 'w')
#        if self.hierarchyVizNodes:
#            fhvyaml.write(yaml.safe_dump(self.hierarchyVizNodes, default_flow_style=False))
#        if self.hierarchyVizEdges:
#            fhvyaml.write(yaml.safe_dump(self.hierarchyVizEdges, default_flow_style=False))
#        fhvyaml.close()
#        
#        newgetoutput("cat "+hvyaml+" | y2d -s "+self.stylesheetdir+"hierarchystyle.yaml" + ">" + hvdot)
        if self.args['--svg']:
            newgetoutput("dot -Tsvg "+hvdot+" -o "+hvdotsvg)
        else:
            newgetoutput("dot -Tpdf "+hvdot+" -o "+hvdotpdf)

        
    def getCollapsedNode(self, mergedNode):
        name = ""
        for singleNode in mergedNode:
            name += singleNode + "\\n\\n"
        return name
    
    def addHierarchyVizNode(self, concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        self.hierarchyVizNodes.update({group + "." + concept: node})

    def addHierarchyVizEdge(self, s, t, label):
        edge = {}
        edge.update({"label" : label})
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"w" : label})
        self.hierarchyVizEdges.update({s + "_" + t : edge})
        
    def showInconLAT(self):
        # if this is a consistent example (there is at least one PW)
        if os.path.isfile(os.path.join(self.pwinternalfilesdir, self.name+".pw")):
            print "This is a consistent example, no diagnostic lattice generated."
            return
        
        # read mis internal files
        misInternalFile = os.path.join(self.pwinternalfilesdir, 'mis.internal')
        if not os.path.isfile(misInternalFile):
            print 'No MIS generated for this example, run "euler2 align" first'
            return

        # create 6-Lattice/ folder
        if not os.path.exists(self.latticedir):
            os.mkdir(self.latticedir)
        inputFile = os.path.abspath(os.path.join(self.inputfilesdir, self.name+".txt"))
        
        allMIS = set()
        fMIS = open(misInternalFile, "r")
        lines = fMIS.readlines()
        for line in lines:
            aMISString = re.match("(.*)\[(.*)\](.*)", line).group(2).split(",")
            aMIS = frozenset(map(int, aMISString))
            allMIS.add(aMIS)
        fMIS.close()
        
        diagShower = DiagnosticLattice(allMIS, inputFile)
        diagShower.genLattice()
        
        # create the visualization file
        if self.args['--full'] or (not self.args['--full'] and not self.args['--reduced']):
            fullLatstr = diagShower.fullLatViz()
            fullLatDotFile = os.path.join(self.latticedir, self.name+"_fulllat.gv")
            fullLatPdfFile = os.path.join(self.latticedir, self.name+"_fulllat.pdf")
            fullLatSvgFile = os.path.join(self.latticedir, self.name+"_fulllat.svg")
            fullLatViz = open(fullLatDotFile, 'w')
            fullLatViz.write(fullLatstr)
            fullLatViz.close()
            if self.args['--svg']:
                newgetoutput("dot -Tsvg "+fullLatDotFile+" -o "+fullLatSvgFile)
            else:
                newgetoutput("dot -Tpdf "+fullLatDotFile+" -o "+fullLatPdfFile)
            
        if self.args['--reduced'] or (not self.args['--full'] and not self.args['--reduced']):
            redLatstr = diagShower.reducedLatViz()    
            redLatDotFile = os.path.join(self.latticedir, self.name+"_lat.gv")
            redLatPdfFile = os.path.join(self.latticedir, self.name+"_lat.pdf")
            redLatSvgFile = os.path.join(self.latticedir, self.name+"_lat.svg")
            redLatViz = open(redLatDotFile, 'w')
            redLatViz.write(redLatstr)
            redLatViz.close()
            if self.args['--svg']:
                newgetoutput("dot -Tsvg "+redLatDotFile+" -o "+redLatSvgFile)
            else:
                newgetoutput("dot -Tpdf "+redLatDotFile+" -o "+redLatPdfFile)
        
#         inputFile = os.path.abspath(os.path.join(self.inputfilesdir, self.name+".txt"))
#         latticeFolder = os.path.abspath(self.latticedir)
#         outputMIS = os.path.abspath(self.output)
#         call("lattice2.sh " + inputFile + " " + latticeFolder + " " + outputMIS, shell=True)
#         #call("maslattice.sh " + fileName, shell=True)
#         
#         # visualization transform
#         fileDot = os.path.join(self.latticedir, self.name+"_lat.dot")
#         filePdf = os.path.join(self.latticedir, self.name+"_lat.pdf")
#         fileSvg = os.path.join(self.latticedir, self.name+"_lat.svg")
#         fileFullDot = os.path.join(self.latticedir, self.name+"_fulllat.dot")
#         fileFullPdf = os.path.join(self.latticedir, self.name+"_fulllat.pdf")
#         fileFullSvg = os.path.join(self.latticedir, self.name+"_fulllat.svg")
#         if os.path.isfile(fileDot):
#             if self.args['--svg']:
#                 newgetoutput("dot -Tsvg "+fileDot+" -o "+fileSvg)
#             else:
#                 newgetoutput("dot -Tpdf "+fileDot+" -o "+filePdf)
#         if os.path.isfile(fileFullDot):
#             if self.args['--svg']:
#                 newgetoutput("dot -Tsvg "+fileFullDot+" -o "+fileFullSvg)
#             else:
#                 newgetoutput("dot -Tpdf "+fileFullDot+" -o "+fileFullPdf)        

    def showFourinoneLAT(self):
#         # if this is a consistent example (there is at least one PW)
#         if os.stat(os.path.join(self.pwinternalfilesdir, "mis.internal")).st_size == 0:
#             print "This is a consistent example, no 4-in-1 lattice generated."
#             return
        
        # read fourinone internal files
        fourinoneInternalFile = os.path.join(self.pwinternalfilesdir, 'fourinone.internal')
        if not os.path.isfile(fourinoneInternalFile):
            print 'Need to run "euler2 align" with option "--fourinone" first'
            return

        # create 6-Lattice/ folder
        if not os.path.exists(self.latticedir):
            os.mkdir(self.latticedir)
            
        it = imp.load_source('it', fourinoneInternalFile)
    
        nodesBin = []
        for node in it.nodes:
            nodeBin = bin(node)[2:]
            tmp = ""
            if len(nodeBin) < it.power:
                for k in range(it.power-len(nodeBin)):
                    tmp = '0' + tmp
            nodeBin = tmp + nodeBin
            nodesBin.append(nodeBin)
        #print "nodesBin", nodesBin
        
        fourinoneLatDotFile = os.path.join(self.latticedir, self.name+"_fourinonelat.gv")
        fDot = open(fourinoneLatDotFile, 'w')
        fDot.write("digraph {\n\nrankdir = BT\n\n")
         
        for nodeBin in nodesBin:
            if nodeBin in it.misBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=box style="filled" fillcolor="#FF0000"];\n')
            elif nodeBin in it.mcsBin and nodeBin in it.musBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=octagon style="filled" fillcolor="#00FF00"];\n')
            elif nodeBin in it.mcsBin and nodeBin in it.maaBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=diamond style="filled" fillcolor="#00FFCC"];\n')
            elif nodeBin in it.mcsBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=box style="filled" fillcolor="#00FF00"];\n')
            elif nodeBin in it.musBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=octagon style="filled" fillcolor="#00FF00"];\n')
            elif nodeBin in it.maaBin:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=diamond style="filled" fillcolor="#00FFCC"];\n')
            else:
                fDot.write(self.convertToIndex(nodeBin, it.power) + ' [shape=box style="filled" fillcolor="#FFFFFF"];\n')
        
        for edge in it.edges:
            fDot.write(self.convertToIndex(edge[0], it.power) +  ' -> ' + self.convertToIndex(edge[1], it.power) + ' [arrowhead=none]\n')
        
        # lengend
        artsLabels = ""
        sorted_artDictbin = sorted(it.artDictbin.items(), key=operator.itemgetter(1))
        for pair in sorted_artDictbin:
            artsLabels += "<TR> \n <TD>" + self.convertToIndex(str(bin(pair[1])[2:]),it.power)[1:-1] + "</TD> \n <TD>" + pair[0] + "</TD> \n </TR> \n"
        fDot.write("node[shape=box] \n")
        fDot.write('{rank=top Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
        fDot.write(artsLabels)
        fDot.write("</TABLE> \n >] } \n")
        fDot.write('Legend -> "None" [style=invis]\n')
        fDot.write("node[shape=box] \n")
        fDot.write('{rank=top Intro [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> \n' )
        intro = "<TR> \n <TD> Minimal Inconsistent Subsets (MIS) </TD> \n <TD> Red box </TD> \n </TR> \n" \
              + "<TR> \n <TD> Maximal Consistent Subsets </TD> \n <TD> Green box </TD> \n </TR> \n" \
              + "<TR> \n <TD> Minimal Unique Subsets </TD> \n <TD> Green octagon</TD> \n </TR> \n" \
              + "<TR> \n <TD> Maximal Ambiguous Subsets </TD> \n <TD> Cyan diamond </TD> \n </TR> \n"
        fDot.write(intro)
        fDot.write("</TABLE> \n >] } \n")
        fDot.write('}')
        fDot.close()
        
        # create the visualization file
        fourinoneLatPdfFile = os.path.join(self.latticedir, self.name+"_fourinonelat.pdf")
        fourinoneLatSvgFile = os.path.join(self.latticedir, self.name+"_fourinonelat.svg")
        if self.args['--svg']:
            newgetoutput("dot -Tsvg "+fourinoneLatDotFile+" -o "+fourinoneLatSvgFile)
        else:
            newgetoutput("dot -Tpdf "+fourinoneLatDotFile+" -o "+fourinoneLatPdfFile)

    def convertToIndex(self, s, power):
        result = ""
        num = int(s,2)
        for i in range(power):
            if num & 1 << i:
                result += str(i) + ','
        if len(result) == 0:
            result = 'None'
        else:
            result = '"' + result[:-1] + '"'
        return result

    def showAmbLAT(self):
        # if this is a inconsistent example (there is at least one PW)
        if os.path.isfile(os.path.join(self.pwinternalfilesdir, 'mis.internal')):
            print "This is an inconsistent example, no ambiguity lattice generated."
            return
        
        # read mas internal files or pw files
        masInternalFile = os.path.join(self.pwinternalfilesdir, 'mas.internal')
        secondPwInternalFile = os.path.join(self.pwinternalfilesdir, 'pw.internal1')
        if not os.path.isfile(masInternalFile):
            if os.path.isfile(secondPwInternalFile):
                print 'This example has more than one possible world, no ambiguity lattice generated.'
            else:
                print 'No MUS generated for this example, run "euler2 align" with --artRem first.'
            return

        # create 6-Lattice/ folder
        if not os.path.exists(self.latticedir):
            os.mkdir(self.latticedir)
        inputFile = os.path.abspath(os.path.join(self.inputfilesdir, self.name+".txt"))
        
        allMUS = set()
        fMUS = open(masInternalFile, "r")
        lines = fMUS.readlines()
        for line in lines:
            aMUSString = re.match("(.*)\[(.*)\](.*)", line).group(2).split(",")
            aMUS = frozenset(map(int, aMUSString))
            allMUS.add(aMUS)
        fMUS.close()
        
        # prepare the arts2NumPW
        arts2NumPWinternalfiles = os.path.join(self.pwinternalfilesdir, 'arts2NumPW.internal')
        it = imp.load_source('it', arts2NumPWinternalfiles)

        diagShower = DiagnosticLattice(allMUS, inputFile)
        diagShower.genLattice()
        fullAmbLatstr = diagShower.fullAmbLatViz(it.arts2NumPW)
        
        # create the visualization file
        fullAmbLatDotFile = os.path.join(self.latticedir, self.name+"_amblat.gv")
        fullAmbLatPdfFile = os.path.join(self.latticedir, self.name+"_amblat.pdf")
        fullAmbLatSvgFile = os.path.join(self.latticedir, self.name+"_amblat.svg")
        fullAmbLatViz = open(fullAmbLatDotFile, 'w')
        fullAmbLatViz.write(fullAmbLatstr)
        fullAmbLatViz.close()
        if self.args['--svg']:
            newgetoutput("dot -Tsvg "+fullAmbLatDotFile+" -o "+fullAmbLatSvgFile)
        else:
            newgetoutput("dot -Tpdf "+fullAmbLatDotFile+" -o "+fullAmbLatPdfFile)
        
    def showPW2INPUT(self):
        # if this is an inconsistent example (there is no PW)
        if not os.path.isfile(os.path.join(self.pwinternalfilesdir, self.name+".pw")):
            print "This is an inconsistent example, no possible worlds generated."
            return
        
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
        


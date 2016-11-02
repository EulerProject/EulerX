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


import sys
import os
import sets
import collections
import operator
import re

class DiagnosticLattice:
    
    def __init__(self, allMIS, inputFile):
        self.inputFile = inputFile
        self.art = []
        self.allMIS = allMIS
        self.allMCS = set()
        self.otherRed = set()
        self.allGreen = set()
        self.otherGreen = set()
        self.nodesBin = set()
        self.edgesBin = []
        self.latVizNodes = {}
        self.latVizEdges = {}
        
    def findSupSets(self, aFrozenset, setOfFronzensets):
        supSets = set()
        for fronzenset in setOfFronzensets:
            if len(aFrozenset) < len(fronzenset):
                if aFrozenset.issubset(fronzenset):
                    supSets.add(fronzenset)
        return supSets

    def isPower2(self, num):
        return num != 0 and ((num & (num - 1)) == 0)
    
    def turnBin(self, num, power):
        binRep = []
        for p in range(power):
            if num & 1 << p:
                binRep.append(p)
        return frozenset(binRep)
                
    def createUncoloredLat(self, numOfArts):
        numOfNodes = 2**numOfArts
        nodes = []
        edges = []
        
        for i in range(numOfNodes):
            nodes.append(i)
            self.nodesBin.add(self.turnBin(i, numOfArts))
            
        for i in nodes:
            for j in nodes:
                if i<j and self.isPower2(i^j):
                    edges.append([i,j])
        
        for edge in edges:
            self.edgesBin.append([self.turnBin(edge[0], numOfNodes), self.turnBin(edge[1], numOfNodes)])

    def eliminate_subsets(self, sequence_of_sets):
        """Return a list of the elements of `sequence_of_sets`, removing all
        elements that are subsets of other elements.  Assumes that each
        element is a set or frozenset and that no element is repeated."""
        # The code below does not handle the case of a sequence containing
        # only the empty set, so let's just handle all easy cases now.
        if len(sequence_of_sets) <= 1:
            return list(sequence_of_sets)
        # We need an indexable sequence so that we can use a bitmap to
        # represent each set.
        if not isinstance(sequence_of_sets, collections.Sequence):
            sequence_of_sets = list(sequence_of_sets)
        # For each element, construct the list of all sets containing that
        # element.
        sets_containing_element = {}
        for i, s in enumerate(sequence_of_sets):
            for element in s:
                try:
                    sets_containing_element[element] |= 1 << i
                except KeyError:
                    sets_containing_element[element] = 1 << i
        # For each set, if the intersection of all of the lists in which it is
        # contained has length != 1, this set can be eliminated.
        out = [s for s in sequence_of_sets
               if s and self.isPower2(reduce(
                   operator.and_, (sets_containing_element[x] for x in s)))]
        return out
    
#     def addLatVizNode(self, concept, group):
#         node = {}
#         node.update({"concept": concept})
#         node.update({"group": group})
#         self.latVizNodes.update({concept: node})
#     
#     def addLatVizEdge(self, s, t, label):
#         edge = {}
#         edge.update({"s" : s})
#         edge.update({"t" : t})
#         edge.update({"label" : label})
#         self.latVizEdges.update({s + "_" + t : edge})    
    
    def genLattice(self):
        # get articulations from input
        f = open(self.inputFile, 'r')
        lines = f.readlines()
        for line in lines:
            if (re.match("\[.*?\]", line)):
                self.art.append(re.match("\[(.*)\]", line).group(1))
        f.close()
        self.createUncoloredLat(len(self.art))
        
        # find other red or green nodes
        for aMIS in self.allMIS:
            supSets = self.findSupSets(aMIS, self.nodesBin)
            self.otherRed.update(supSets)
         
        self.allGreen = self.nodesBin.difference(self.otherRed).difference(self.allMIS)        
        self.allMCS = set(self.eliminate_subsets(self.allGreen))
        self.otherGreen = self.allGreen.difference(self.allMCS)
    
    # generate the full lattice
    def fullLatViz(self):
        outstr = ""
        outstr += "digraph{\n"
        outstr += "rankdir=BT\n"
        
        # add nodes
        outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=filled]\n'
        for solidRed in self.allMIS:
            label = ','.join(str(s) for s in solidRed)
            outstr += '"' + label +'"\n'
        outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=dashed]\n'
        for otherRed in self.otherRed:
            label = ','.join(str(s) for s in otherRed)
            outstr += '"' + label +'"\n'
        outstr += 'node[shape=box color="#006400" fillcolor="#A0FFA0" style="rounded,filled"]\n'
        for solidGreen in self.allMCS:
            if len(solidGreen) == 0:
                outstr += '"None"\n'
            else:
                label = ','.join(str(s) for s in solidGreen)
                outstr += '"' + label +'"\n'
        outstr += 'node[shape=box color="#006400" style=dashed]\n'
        for otherGreen in self.otherGreen:
            if len(otherGreen) == 0:
                outstr += '"None"\n'
            else:
                label = ','.join(str(s) for s in otherGreen)
                outstr += '"' + label +'"\n'
        
        # add edges
        for edge in self.edgesBin:
            if (edge[0] in self.allMIS or edge[0] in self.otherRed) \
                and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                start = ','.join(str(s) for s in edge[0])
                end = ','.join(str(s) for s in edge[1])
                outstr += '"' + start + '" -> "' + end +'" [color="#CC0000" style=dashed]\n'
            if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                and (edge[1] in self.allMCS or edge[1] in self.otherGreen):
                if len(edge[0]) == 0:
                    start = 'None'
                else:
                    start = ','.join(str(s) for s in edge[0])
                end = ','.join(str(s) for s in edge[1])
                outstr += '"' + start + '" -> "' + end +'" [dir=back color="#006400" style=dashed]\n'
            if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                if len(edge[0]) == 0:
                    start = 'None'
                else:
                    start = ','.join(str(s) for s in edge[0])
                end = ','.join(str(s) for s in edge[1])
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#0000FF" style=filled]\n'
                
        # add legend
        artsLabels = ""
        for art in self.art:
            artsLabels += "<TR> \n <TD>" + str(self.art.index(art)) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
        outstr += "node[shape=box] \n"
        outstr += '{rank=top Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" \
                    CELLPADDING="4"> \n'
        outstr += artsLabels
        outstr += "</TABLE> \n >] } \n"
        outstr += 'Legend -> "None" [style=invis]\n'   
        outstr += "}"
        return outstr
    
    def reducedLatViz(self):
        outstr = ""
        outstr += "digraph{\n"
        outstr += "rankdir=BT\n"
        
        # add nodes
        if len(self.otherRed) > 0:
            outstr += '"AllOtherRed" [shape=octagon color="#FFB0B0" style=dashed]\n'
        if len(self.otherGreen) > 0:
            outstr += '"AllOtherGreen" [shape=box color="#006400" style="rounded,dashed"]\n'
        outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=filled]\n'
        for solidRed in self.allMIS:
            label = ','.join(str(s) for s in solidRed)
            outstr += '"' + label +'"\n'
        outstr += 'node[shape=box color="#006400" fillcolor="#A0FFA0" style="rounded,filled"]\n'
        for solidGreen in self.allMCS:
            if len(solidGreen) == 0:
                outstr += '"None"\n'
            else:
                label = ','.join(str(s) for s in solidGreen)
                outstr += '"' + label +'"\n'
                
        # add edges
        if len(self.otherRed) > 0:
            for solidRed in self.allMIS:
                start = ','.join(str(s) for s in solidRed)
                end = 'AllOtherRed'
                outstr += '"' + start + '" -> "' + end +'" [color="#CC0000" style=dashed]\n'
        if len(self.otherGreen) > 0:
            for solidGreen in self.allMCS:
                start = 'AllOtherGreen'
                if len(solidGreen) == 0:
                    end = '"None"\n'
                else:
                    end = ','.join(str(s) for s in solidGreen)
                outstr += '"' + start + '" -> "' + end +'" [dir=back color="#006400" style=dashed]\n'
        for edge in self.edgesBin:
            if edge[0] in self.allMCS and edge[1] in self.allMIS:
                if len(edge[0]) == 0:
                    start = 'None'
                else:
                    start = ','.join(str(s) for s in edge[0])
                end = ','.join(str(s) for s in edge[1])
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#0000FF" style=filled]\n'
        if len(self.otherGreen) > 0:
            for mis in self.allMIS:
                start = 'AllOtherGreen'
                end = ','.join(str(s) for s in mis)
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#0000FF" style=filled]\n'
        if len(self.otherRed) > 0:
            for mcs in self.allMCS:
                start = ','.join(str(s) for s in mcs)
                end = 'AllOtherRed'
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#0000FF" style=filled]\n'
        
        # add legend
        artsLabels = ""
        for art in self.art:
            artsLabels += "<TR> \n <TD>" + str(self.art.index(art)) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
        outstr += "node[shape=box] \n"
        outstr += '{rank=top Legend [fillcolor= white margin=0 label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" \
                    CELLPADDING="4"> \n'
        outstr += artsLabels
        outstr += "</TABLE> \n >] } \n"
        if len(self.otherGreen) > 0:
            outstr += 'Legend -> "AllOtherGreen" [style=invis]\n'
        else:
            outstr += 'Legend -> "None" [style=invis]\n'
        outstr += "}"
        return outstr
        
         
#         # generate the full lattice
#         for solidRed in self.allMIS:
#             tmp = ""
#             for s in solidRed:
#                 tmp = tmp + "a" + str(s)
#             self.addLatVizNode(tmp, "solidRed")
#         for solidGreen in self.allMCS:
#             tmp = ""
#             if len(solidGreen) == 0:
#                 self.addLatVizNode('None', "solidGreen")
#             else:
#                 for s in solidGreen:
#                     tmp = tmp + "a" + str(s)
#                 self.addLatVizNode(tmp, "solidGreen")
#         for otherRed in self.otherRed:
#             tmp = ""
#             for s in otherRed:
#                 tmp = tmp + "a" + str(s)
#             self.addLatVizNode(tmp, "otherRed")
#         for otherGreen in self.otherGreen:
#             tmp = ""
#             if len(otherGreen) == 0:
#                 self.addLatVizNode('None', "otherGreen")
#             else:
#                 for s in otherGreen:
#                     tmp = tmp + "a" + str(s)
#                 self.addLatVizNode(tmp, "otherGreen")
#         for edge in self.edgesBin:
#             if edge[0]
#             if len(edge[0]) == 0:
#                 startNode = 'None'
#             else:
#                 startNode = ""
#                 for s in edge[0]:
#                     startNode = startNode + "a" + str(s)    
#             endNode = ""
#             for s in edge[1]:
#                 endNode = endNode + "a" + str(s)
#             self.addLatVizEdge(startNode, endNode, '1')
#             
#         print "self.latVizNodes", self.latVizNodes
#         print "self.latVizEdges", self.latVizEdges
        
#         # create the visualization file
#         latYamlFile = os.path.join(self.latticedir, self.name+"_fulllat.yaml")
#         latDotFile = os.path.join(self.latticedir, self.name+"_fulllat.gv")
#         latPdfFile = os.path.join(self.latticedir, self.name+"_fulllat.pdf")
#         latSvgFile = os.path.join(self.latticedir, self.name+"_fulllat.svg")
#         fLatVizYaml = open(latYamlFile, 'w')
#         if self.latVizNodes:
#             fLatVizYaml.write(yaml.safe_dump(self.latVizNodes, default_flow_style=False))
#         if self.latVizEdges:
#             fLatVizYaml.write(yaml.safe_dump(self.latVizEdges, default_flow_style=False))
#         fLatVizYaml.close()

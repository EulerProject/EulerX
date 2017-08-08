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

# import sys
# import commands
# import os
from relations import *
from helper2 import findkey

class RCC2Verbose:
    
#     def __init__(self):
    
    def getStep(self, step):
        print "------------ Step ", step, " ------------"
        
    def getPair(self, fileName, step, t1, t2, givenRel):
        print "Pick pair: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name
        
        # visualize reasoning
        f = open(fileName, "w")
        f.write("digraph {\n\nrankdir = LR\n\n")
        f.write('node [shape=box]\n')
        f.write('"'+t1.taxonomy.abbrev+'.'+t1.name + '" -> "' + t2.taxonomy.abbrev+'.'+t2.name + '" [color=blue, label="'+ findkey(relation,givenRel) +'"];\n')
        f.close()
        
    def getROPart1(self, fileName, t1, t2, t2Parent, givenRel, deducedPair, deducedRel, allPairsMir):
        print "\nPart (I):"
        print t2.taxonomy.abbrev+'.'+t2.name + " has parent " + t2Parent.taxonomy.abbrev+'.'+t2Parent.name + ", then look at pair (" + t1.taxonomy.abbrev+'.'+t1.name + ", " + t2Parent.taxonomy.abbrev+'.'+t2Parent.name + ")"
        print "Original relation: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, allPairsMir[deducedPair]), t2Parent.taxonomy.abbrev+'.'+t2Parent.name
        print "Using R32 comp table: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, "R32COMP", t2.taxonomy.abbrev+'.'+t2.name, "<", t2Parent.taxonomy.abbrev+'.'+t2Parent.name, \
                "-->", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, deducedRel), t2Parent.taxonomy.abbrev+'.'+t2Parent.name
        f = open(fileName, "a")
        f.write('"'+t2.taxonomy.abbrev+'.'+t2.name + '" -> "' + t2Parent.taxonomy.abbrev+'.'+t2Parent.name + '" [label="< (parent)"];\n')
        f.write('"'+t1.taxonomy.abbrev+'.'+t1.name + '" -> "' + t2Parent.taxonomy.abbrev+'.'+t2Parent.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
    
    def getROPart2Intro(self, t2, t2Siblings):
        print "\nPart (II)"
        if t2Siblings:
            print t2.taxonomy.abbrev+'.'+t2.name + " has the following siblings:"
        else:
            print t2.taxonomy.abbrev+'.'+t2.name + " has no siblings"
        
    def getROPart2(self, fileName, t1, t2, t2Sibling, givenRel, deducedPair, deducedRel, allPairsMir):
        print "Sibling: " + t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name + ", then look at pair (" + t1.taxonomy.abbrev+'.'+t1.name + ", " + t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name + ")"
        print "Original relation: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, allPairsMir[deducedPair]), t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name
        print "Using R32 comp table: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, "R32COMP", t2.taxonomy.abbrev+'.'+t2.name, "!", t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name, \
                "-->", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, deducedRel), t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name
        f = open(fileName, "a")
        f.write('"'+t2.taxonomy.abbrev+'.'+t2.name + '" -> "' + t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name + '" [label="! (sibling)"];\n')
        f.write('"'+t1.taxonomy.abbrev+'.'+t1.name + '" -> "' + t2Sibling.taxonomy.abbrev+'.'+t2Sibling.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
        
    def getROPart3Intro(self, t2, t2Children):
        print "\nPart (III)"
        if t2Children:
            print t2.taxonomy.abbrev+'.'+t2.name + " has the following children:"
        else:
            print t2.taxonomy.abbrev+'.'+t2.name + " has no children"
        
    def getROPart3(self, fileName, t1, t2, t2Child, givenRel, deducedPair, deducedRel, allPairsMir):
        print "Child: " + t2Child.taxonomy.abbrev+'.'+t2Child.name + ", then look at pair (" + t1.taxonomy.abbrev+'.'+t1.name + ", " + t2Child.taxonomy.abbrev+'.'+t2Child.name + ")"
        print "Original relation: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, allPairsMir[deducedPair]), t2Child.taxonomy.abbrev+'.'+t2Child.name
        print "Using R32 comp table: ", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, "R32COMP", t2.taxonomy.abbrev+'.'+t2.name, ">", t2Child.taxonomy.abbrev+'.'+t2Child.name, \
                "-->", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, deducedRel), t2Child.taxonomy.abbrev+'.'+t2Child.name
        f = open(fileName, "a")
        f.write('"'+t2.taxonomy.abbrev+'.'+t2.name + '" -> "' + t2Child.taxonomy.abbrev+'.'+t2Child.name + '" [label="> (children)"];\n')
        f.write('"'+t1.taxonomy.abbrev+'.'+t1.name + '" -> "' + t2Child.taxonomy.abbrev+'.'+t2Child.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
    
    def getROPart4(self, fileName, t1, t2, t1Parent, givenRel, deducedPair, deducedRel, allPairsMir):
        print "\nPart (IV):"
        print t1.taxonomy.abbrev+'.'+t1.name + " has parent " + t1Parent.taxonomy.abbrev+'.'+t1Parent.name + ", then look at pair (" + t1Parent.taxonomy.abbrev+'.'+t1Parent.name + ", " + t2.taxonomy.abbrev+'.'+t2.name + ")"
        print "Original relation: ", t1Parent.taxonomy.abbrev+'.'+t1Parent.name, findkey(relation, allPairsMir[deducedPair]), t2.taxonomy.abbrev+'.'+t2.name
        print "Using R32 comp table: ", t1Parent.taxonomy.abbrev+'.'+t1Parent.name, ">", t1.taxonomy.abbrev+'.'+t1.name, "R32COMP", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, \
                "-->", t1Parent.taxonomy.abbrev+'.'+t1Parent.name, findkey(relation, deducedRel), t2.taxonomy.abbrev+'.'+t2.name
        f = open(fileName, "a")
        f.write('"'+t1Parent.taxonomy.abbrev+'.'+t1Parent.name + '" -> "' + t1.taxonomy.abbrev+'.'+t1.name + '" [label="> (parent)"];\n')
        f.write('"'+t1Parent.taxonomy.abbrev+'.'+t1Parent.name + '" -> "' + t2.taxonomy.abbrev+'.'+t2.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
    
    def getROPart5Intro(self, t1, t1Siblings):
        print "\nPart (V):"
        if t1Siblings:
            print t1.taxonomy.abbrev+'.'+t1.name + " has the following siblings:"
        else:
            print t1.taxonomy.abbrev+'.'+t1.name + " has no siblings"

    def getROPart5(self, fileName, t1, t2, t1Sibling, givenRel, deducedPair, deducedRel, allPairsMir):
        print "Sibling: " + t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name + ", then look at pair (" + t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name + ", " + t2.taxonomy.abbrev+'.'+t2.name + ")"
        print "Original relation: ", t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name, findkey(relation, allPairsMir[deducedPair]), t2.taxonomy.abbrev+'.'+t2.name
        print "Using R32 comp table: ", t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name, "!", t1.taxonomy.abbrev+'.'+t1.name, "R32COMP", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, \
                "-->", t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name, findkey(relation, deducedRel), t2.taxonomy.abbrev+'.'+t2.name
        f = open(fileName, "a")
        f.write('"'+t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name + '" -> "' + t1.taxonomy.abbrev+'.'+t1.name + '" [label="! (sibling)"];\n')
        f.write('"'+t1Sibling.taxonomy.abbrev+'.'+t1Sibling.name + '" -> "' + t2.taxonomy.abbrev+'.'+t2.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
        
    def getROPart6Intro(self, t1, t1Children):
        print "\nPart (VI)"
        if t1Children:
            print t1.taxonomy.abbrev+'.'+t1.name + " has the following children:"
        else:
            print t1.taxonomy.abbrev+'.'+t1.name + " has no children"
        
    def getROPart6(self, fileName, t1, t2, t1Child, givenRel, deducedPair, deducedRel, allPairsMir):
        print "Child: " + t1Child.taxonomy.abbrev+'.'+t1Child.name + ", then look at pair (" + t1Child.taxonomy.abbrev+'.'+t1Child.name + ", " + t2.taxonomy.abbrev+'.'+t2.name + ")"
        print "Original relation: ", t1Child.taxonomy.abbrev+'.'+t1Child.name, findkey(relation, allPairsMir[deducedPair]), t2.taxonomy.abbrev+'.'+t2.name
        print "Using R32 comp table: ", t1Child.taxonomy.abbrev+'.'+t1Child.name, "<", t1.taxonomy.abbrev+'.'+t1.name, "R32COMP", t1.taxonomy.abbrev+'.'+t1.name, findkey(relation, givenRel), t2.taxonomy.abbrev+'.'+t2.name, \
                "-->", t1Child.taxonomy.abbrev+'.'+t1Child.name, findkey(relation, deducedRel), t2.taxonomy.abbrev+'.'+t2.name
        f = open(fileName, "a")
        f.write('"'+t1Child.taxonomy.abbrev+'.'+t1Child.name + '" -> "' + t1.taxonomy.abbrev+'.'+t1.name + '" [label="< (children)"];\n')
        f.write('"'+t1Child.taxonomy.abbrev+'.'+t1Child.name + '" -> "' + t2.taxonomy.abbrev+'.'+t2.name + '" [color=red, label="'+ findkey(relation,deducedRel) +'"];\n')
        f.close()
        
    def getAssertNewViz(self, fileName, part, deducedPair, deducedRel, oldRel, newRel, cnt):
        f = open(fileName, "a")
        print deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + " " + findkey(relation, oldRel) + " " + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name + " & " + \
            deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + " " + findkey(relation, deducedRel) + " " + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name + " --> " + \
            deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + " " + findkey(relation, newRel) + " " + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name
        f.write('intersect' + part + str(cnt) + ' [shape=point];\n')
        f.write('node1'+part+str(cnt)+'[label="'+ deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + ' ' + findkey(relation, oldRel) + ' ' + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name + '"];\n')
        f.write('node2'+part+str(cnt)+'[label="'+ deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + ' ' + findkey(relation, deducedRel) + ' ' + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name + '"];\n')
        f.write('node3'+part+str(cnt)+'[label="'+ deducedPair[0].taxonomy.abbrev+'.'+deducedPair[0].name + ' ' + findkey(relation, newRel) + ' ' + deducedPair[1].taxonomy.abbrev+'.'+deducedPair[1].name + '"];\n')
        f.write('node1'+part+str(cnt)+' -> intersect'+part+str(cnt)+' [label="original"];\n')
        f.write('node2'+part+str(cnt)+' -> intersect'+part+str(cnt)+' [label="deduced"];\n')
        f.write('intersect'+part+str(cnt)+' -> node3'+part+str(cnt)+' [label="intersection"];\n')
        f.close()
        
    def getNoPart12(self, t2):
        print "\nPart (I) and Part (II) do not exist, because " + t2.taxonomy.abbrev+'.'+t2.name + " has no parent or siblings"
        
    def getNoPart56(self, t1):
        print "\nPart (IV) and Part (V) do not exist, because " + t1.taxonomy.abbrev+'.'+t1.name + " has no parent or siblings"
    
    def getNoChange(self):
        print "No change..."
        
    def getFinish(self, fileName):
        print ""
        f = open(fileName, "a")        
        f.write("}\n")
        f.close()

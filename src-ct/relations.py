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

class BasicRelation:

    def __init__(self, name, latex, logic):
        self.latexSymbol = latex
        self.name = name
        self.logicSymbol = logic

    def __str__(self):
        return self.name
    
class RelationSet:
    
    def __init__(self, name="", relations=[]):
      self.name = name
      self.relations = relations  ## a list of basic relations
    

class RCCType:
    
    def __init__(self, name="", relationSets=[]):
        self.name = ""
        self.relationSets = []  ## a list of relations sets, RCC5 would be a RCCType
    
relationDict = {}    
relationDict["+="] = BasicRelation("+=","$x $y lsum $z","($x(x) | $y(x) <-> $z(x))")
relationDict["++="] = BasicRelation("++=","$x $y $u lsum $z","($x(x) | $y(x) | $u(x) <-> $z(x))")
relationDict["+=+"] = BasicRelation("+=+","$x $y e4sum $z $u","($x(x) | $y(x) <-> $z(x) | $u(x))")
relationDict["+<=+"] = BasicRelation("+<=+","$x $y i4sum $z $u","($x(x) | $y(x) -> $z(x) | $u(x))")
relationDict["=+"] = BasicRelation("=+","$x rsum $y $z","($x(x) <-> $y(x) | $z(x))")
relationDict["-="] = BasicRelation("-=","$x $y ldiff $z","($x(x) & -$y(x) <-> $z(x))")
relationDict["=-"] = BasicRelation("=-","$x rdiff $y $z","($x(x) <-> $y(x) & -$z(x))")
relationDict["equals"] = BasicRelation("equals","$x \leftrightarrow $y","(all x ($x(x) <-> $y(x)))")
relationDict["includes"] = BasicRelation("includes","$y \rightarrow $x","(all x ($y(x) -> $x(x))) & (exists x ($x(x) & -$y(x)))")
relationDict["is_included_in"] = BasicRelation("is_included_in","$x \rightarrow $y","(all x ($x(x) -> $y(x))) & (exists x ($y(x) & -$x(x)))")
relationDict["disjoint"] = BasicRelation("disjoint","$x ! $y","(all x ($x(x) -> -$y(x)))")
relationDict["overlaps"] = BasicRelation("overlaps","$x \otimes $y","(exists a exists b exists c ($x(a) & $y(a) & $x(b) & -$y(b) & -$x(c) & $y(c)))")  
relationDict["overlaps includes is_included_in disjoint"] = BasicRelation("does_not_equal","$x != $y","-(all x ($x(x) <-> $y(x)))")

isa = RelationSet()
isa.name = "is a"
isa.relations = [relationDict["equals"], relationDict["is_included_in"]]

    
    
    
    

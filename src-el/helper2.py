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
import commands
import os

class Callable:
    def __init__(self, callable):
        self.__call__ = callable

def findkey(mapp, value):
#    tmplist = [k for k, v in mapp.iteritems() if v == value]
#    if tmplist is []:
#        return None
#    return tmplist[0]
    return mapp.keys()[mapp.values().index(value)]


class Logger(object):
    # filename may have proper path
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        
    def __del__(self):
        self.log.close()
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

def newgetoutput(cmd):
    result = commands.getstatusoutput(cmd)
    if result[0] != 0:
        print "cmd: ", cmd
        print "exit status: ", result[0]
        return
    else:
        return result[1]

def createLastRunTimeStamp(fileName, user, host, timestamp, name):
    f = open(fileName, "w")
    s = os.path.join(user + '-' + host, timestamp + '-' + name)
    f.write(s)
    f.write('\n')
    f.write(name)
    f.close()

def createLastRunName(fileName, name):
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    f = open(fileName, "w")
    f.write(name)
    f.close()

# to create aggregation rule for articulation and alignment
class AggregationRule:
    def __init__(self, firstVar, secondVar, lowerBound="", startPred="vrs", firstPredIsIn=True, secondPredIsIn=True,
                 isConstraint=True, addPW=True, variableName="X"):
        baseFormat = '{}#count {{X : {}(X), {}({},X), {}({},X)}}{}{}'
        firstPred = "in" if firstPredIsIn else "out"
        secondPred = "in" if secondPredIsIn else "out"
        # lowerBoundString = "" if lowerBound == -100 else str(lowerBound) + " <= "
        upperBound = " <= 0" if lowerBound == "" else ""
        addPWTail = ", pw" if addPW else ""
        baseRule = baseFormat.format(lowerBound, startPred, firstPred, firstVar, secondPred, secondVar,
                                     upperBound, addPWTail)
        if variableName != "X":
            baseRule = baseRule.replace("X", variableName)
        self.rule = ":- " + baseRule + ".\n" if isConstraint else baseRule

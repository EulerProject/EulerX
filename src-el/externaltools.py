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

from subprocess import call

def runLattice(fileName):
    call("lattice.sh " + fileName, shell=True)
    
def runAddID(fileName):
    s = ""
    for i in range(len(fileName)):
        s = s + " -i " + fileName[i]
    call("addID" + s, shell=True)
    
def runAddIsa(fileName):
    call("addIsa -i " + fileName, shell=True)

def runP2C(fileName):
    call("p2c -i " + fileName, shell=True)

def runP2CT(fileName):
    call("p2c -i " + fileName[0] + " -t " + fileName[1], shell=True)

def runAddArt(fileName):
    call("addArt -i " + fileName, shell=True)

def runAddArtT(fileName):
    s = ""
    for i in range(1, len(fileName)):
        s = s + " -t " + fileName[i]
    call("addArt -i " + fileName[0] + s, shell=True)

def runC2CSV(fileName):
    call("c2csv -i " + fileName, shell=True)

def runAddRank(fileName):
    call("cat " + fileName + " | addRank", shell=True)

def runMirStats(fileName):
    call("mirStats -i " + fileName[0] + " -r " + fileName[1], shell=True)
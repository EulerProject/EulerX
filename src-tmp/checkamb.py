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

import re
import itertools
import sys

fileName = sys.argv[1]
f = open(fileName, 'r')
inputs = f.readlines()
f.close()

noDisjuncLines = []
disjuncLines = []
ambArts = []
repArts = []
i = 0

for inputLine in inputs:
    if "{" in inputLine:
        disjuncLines.append(inputLine)
        r = re.match("\[(.*) \{(.*)\} (.*)\]", inputLine)
        arts = r.group(2).split(" ")
        ambArts.append(arts)
    else:
        noDisjuncLines.append(inputLine)
            

repArts = list(itertools.product(*ambArts))


for repArt in repArts:
    fOut = open(fileName.replace(".txt","") + "_rep"+i.__str__()+".txt", "w")
    for line in noDisjuncLines:
        fOut.write(line)
    for j in range(len(disjuncLines)):
        r = re.match("\[(.*) \{(.*)\} (.*)\]", disjuncLines[j])
        artStr = "[" + r.group(1) + " " + repArt[j] + " " + r.group(3) + "]\n"
        fOut.write(artStr)
    
    fOut.close()
    i = i + 1

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

#=============================================================================================
# Main program: awf.py All-Worlds-Filter 
# Post-processing within ASP system: write out all PWs as new "facts" 
# Post-processing can be used to answer, e.g. which facts are true in more than X% of the PWs;
# Solution 1 (might be quite practical) : write out all PWs as new facts of the form
# pw(0,...), pw(0, ...).
# pw(1,...), pw(1,..)
# Input: DLV program 
# Output: All refined possible worlds
# Usage: 
# 	with filter: python awf.py -filter=FILTER1,FILTER2... input.dlv
# 	without filter: python awf.py input.dlv
#=============================================================================================
from subprocess import call
import sys

#filter = sys.argv[1]
#fileName = sys.argv[2]
for arg in sys.argv:
	if "-filter=" in arg:
		filter = arg
		fileName = sys.argv[sys.argv.index(arg) + 1]
		break
	filter = "-filter="
	fileName = sys.argv[1]

fileNameOut = fileName + ".out"
s = "dlv -silent " + filter + " " + fileName + " > " + fileNameOut
#call("dlv -silent -filter=" + filter + " " + fileName + " > " + fileName + ".out", shell=True)
call(s, shell=True)
f_in = open(fileNameOut, "r")
f_out = open(fileName[:-4] + "_aw.asp", "w")
outList = []
not_EOF = True
line = f_in.readline()
i= 0

while not_EOF:
    preds = []
    #print "i=", i, "line=", line[1:-2]
    preds = line[1:-2].split(", ")
    #print preds
    
    for pred in preds:
        try:
            index = pred.index("(")
            outStr = pred[:index+1] + str(i) + "," + pred[index+1:]
            outList.append(outStr)
        except ValueError:
            print "*WARNING* World", i, "is empty!"
        
    i = i + 1
    line = f_in.readline()    
    if len(line) == 0:
        not_EOF = False

#print outList

for e in outList:
    f_out.write(e+".\n")

f_in.close()
f_out.close()
#=============================================================================================
# Main program: awf.py All-Worlds-Filter 
# Post-processing within ASP system: write out all PWs as new "facts" 
# Post-processing can be used to answer, e.g. which facts are true in more than X% of the PWs;
# Solution 1 (might be quite practical) : write out all PWs as new facts of the form
# pw(0,...), pw(0, ...).
# pw(1,...), pw(1,..)
# Input: DLV program 
# Output: All refined possible worlds
# Usage: python save_all_worlds.py input.dlv
#=============================================================================================
from subprocess import call
import sys

filter = sys.argv[1]
fileName = sys.argv[2]
fileNameOut = fileName + ".out"

call("dlv -silent -filter=" + filter + " " + fileName + " > " + fileName + ".out", shell=True)
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
    # print preds
    
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





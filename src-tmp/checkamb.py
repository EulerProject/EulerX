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
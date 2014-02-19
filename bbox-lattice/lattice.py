from subprocess import call
import sys

def removeRed(originList,removeList):
    delNodes = []
    for e in removeList:
        for node in originList:
            if e[:-1] == node:
                delNodes.append(node)
    for delNode in delNodes:
        if originList.index(delNode) != -1:
            originList.remove(delNode)

def remove_duplicate_string(li):
    if li:
        li.sort()
        last = li[-1]
        for i in range(len(li)-2, -1, -1):
            if last == li[i]:
                del li[i]
            else:
                last = li[i]

fileName = sys.argv[1]+".txt"
misArts = []
arts = []
f = open("output.txt","r")
lines = f.readlines()
for line in lines:
    if line.split(" ")[0] == "Min":
        index1 = line.index("[")
        index2 = line.index("]")
        line = line[index1+1:index2-1]
        mises = line.split(" , ")
        tmpmis = ""
        for mis in mises:
            tmpmis = tmpmis + mis[mis.index(":")+2:] + ","
        misArts.append(tmpmis[:-1])
f.close()
#print misArts
f = open(fileName, "r")
lines = f.readlines()
for line in lines:
    if line[0] == "[":
        arts.append(line[1:-2])
f.close()
#print "arts=",arts, len(arts)
misArtIds = []
misList = []
for mis in misArts:
    tmpindexes = []
    tmpindexesList = []
    tmpAs = mis.split(",")
    for tmpA in tmpAs:
        for a in arts:
            if tmpA == a:
                tmpindex = arts.index(a)+1
        tmpindexes.append(tmpindex)
        tmpindexesList.append(str(tmpindex))
    misArtIds.append(tmpindexes)
    misList.append(tmpindexesList)
#print misArtId
i = 0
fileName = ""
fileList = []
for misArtId in misArtIds:
    s = ""
    for e in misArtId:
        s = s + "i(W," + str(e) + "),"
    f = open("query.asp","w")
    f.write(s[:-1]+"?")
    f.close()
    fileName = "mis" + str(i) + ".txt"
    call("dlv -silent -brave expWorlds_aw.asp query.asp > " + fileName, shell=True)
    fileList.append(fileName)
    i = i + 1
    

allNodes = []
for i in range(2**len(arts)):
    allNodes.append(str(i))
    
for fileName in fileList:
    f = open(fileName,"r")
    miss = f.readlines()
    f.close()
    removeRed(allNodes,miss)

#print allNodes, len(allNodes)

#f = open("result.txt","w")
#i = 0
#for node in allNodes:
#    f = open("query.asp","w")
#    f.write("ai(A) :- i(" + node +",A).\n")
#    f.write("ai(A)?")
#    f.close()
#    com ="dlv -silent expWorlds_aw.asp query.asp -brave >> result.txt" 
#    call(com, shell=True)
#    com = "echo \"\n\" >> \"result.txt\""
#    call(com, shell=True)
#    print "done",i
#    i = i+1
#f.close() 

with open("result_tmp.txt", "wt") as fout:
    with open("result.txt","rt") as fin:
        for line in fin:
            s = line.replace("\n",",")
            fout.write(s)

with open("result_new.txt", "wt") as fout:
    with open("result_tmp.txt","rt") as fin:
        for line in fin:
            s = line.replace(",,,","\n")
            fout.write(s)

call("rm result_tmp.txt", shell=True)

allGreens = []

f = open("result_new.txt","r")
lines = f.readlines()
for line in lines:
    if line != ",,":
        oneGreen = line[:-1].split(",")
        allGreens.append(oneGreen)
    
delNodes = []
for e1 in allGreens:
    for e2 in allGreens:
        if set(e1).issubset(set(e2)) and set(e1) != set(e2):
            delNodes.append(e1)
remove_duplicate_string(delNodes)
#print "delNodes=",delNodes

for delNode in delNodes:
    if allGreens.index(delNode) != -1:
        allGreens.remove(delNode)


print "MIS=",misList, len(misList)
print "MCS=",allGreens,len(allGreens)
f.close()

# get lattice
fileDot = sys.argv[1]+"_lat.dot"
f = open(fileDot,"w")
f.write("digraph{\n")
f.write("rankdir=TB\n")
f.write('"AllOtherRed" [shape=octagon color="#FF0000" style=dashed]\n')
f.write('"AllOtherGreen" [shape=box color="#00FF00" style=dashed]\n')
for mcs in allGreens:
    f.write('"' + str(mcs) + '" [shape=box color="#00FF00" style="rounded,filled"];\n')
for mis in misList:
    f.write('"' + str(mis) + '" [shape=octagon color="#FF0000" style="filled"];\n')
for mcs in allGreens:
    f.write('"AllOtherRed" -> "' + str(mcs) + '" [color=blue, arrowhead=none, label='+ str(len(arts)-len(mcs)) +'];\n')
    f.write('"' + str(mcs) + '" -> "AllOtherGreen" [color=green, style=dashed, label='+ str(len(mcs)) +'];\n')
for mis in misList:
    f.write('"AllOtherRed" -> "' + str(mis) + '" [color=red, style=dashed, dir=back, label='+ str(len(arts)-len(mis)) +'];\n')
    f.write('"' + str(mis) + '" -> "AllOtherGreen" [color=blue, arrowhead=none, label='+ str(len(mis)) +'];\n')
for mcs in allGreens:
    for mis in misList:
        if set(mcs).issubset(set(mis)):
            f.write('"' + str(mis) + '" -> "' + str(mcs) + '" [color=blue, arrowhead=none, label=1];\n')
        elif set(mis).issubset(set(mcs)):
            f.write('"' + str(mcs) + '" -> "' + str(mis) + '" [color=blue, arrowhead=none, label=1];\n')

f.write("}")
f.close()

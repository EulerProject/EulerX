
# Euler diff receives a path of Euler run as input and outputs a diff file for each pair of cleanTax files in that path 
# __author__ = "Parisa Kianmajd"
#__version__ = "1.0.1"

import difflib
import sys
import os

def diff(f1,f2,t):
    filename = {f1:"", f2: ""}
    diff = difflib.ndiff(open(f1).readlines(), open(f2).readlines())
    for f in [f1,f2]:
        if "/" in f:
            filename[f] = f.split("/")[-1]
        else:
            filename[f] = f
        
    out = open('diff_' + t + "_" + filename[f1].split(".")[0] + "_" + filename[f2] , "w")
    try:
        while 1:
            out.write(diff.next(),)
    except:
        pass
    out.close()

def findDiff():
    filesList = list()

    try:
        arg1 = sys.argv[1]
    except IndexError:
        print "Usage: diff.py <arg1>"
        sys.exit(1)

    rootdir = sys.argv[1]

    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if name.endswith(".txt"):
                timestamp = root.split("/")[-2]
                filesList.append([os.path.join(root, name),timestamp])
    i = 0
    while i < len(filesList) - 1:
        time = filesList[i][1] + "_" + filesList[i+1][1]
        diff(filesList[i][0],filesList[i+1][0],time)
        i += 2

findDiff()

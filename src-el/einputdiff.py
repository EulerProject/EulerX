
# Euler diff receives filename as input and outputs diff file showing the difference between the pair of files with this filename
# in the current directory
# __author__ = "Parisa Kianmajd"
#__version__ = "1.0.1"

import difflib
import sys
import os

def diff(f1,f2,t,c):
    filename = {f1:"", f2: ""}
    diff = difflib.ndiff(open(f1).readlines(), open(f2).readlines())
    for f in [f1,f2]:
        if "/" in f:
            filename[f] = f.split("/")[-1]
        else:
            filename[f] = f
        
    out = open('diff_' + str(c) + "_" + filename[f1]  , "w")
    out.write('timestamp #1:' + t[0] + '\n')
    out.write('timestamp #2:' + t[1] + '\n')
    out.write('\n')

    try:
        while 1:
            out.write(diff.next(),)
    except:
        pass
    out.close()

def einputdiff():
    filesList = list()

    try:
        arg1 = sys.argv[1]
    except IndexError:
        print "Usage: diff.py <arg1>"
        sys.exit(1)

    filename = sys.argv[1]

    for root, dirs, files in os.walk('.'):
        for name in files:
            if name == filename:
                timestamp = root [2:20]
                filesList.append([os.path.join(root, name),timestamp])
    i = 0
    c = 1
    while i < len(filesList) - 1:
        time = (filesList[i][1], filesList[i+1][1])
        diff(filesList[i][0],filesList[i+1][0],time,c)
        i += 2
        c += 1

einputdiff()

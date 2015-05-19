
# Euler Input diff (einputdiff) receives filename as input and outputs diff files
# showing the difference between the pair of files with this filename in the current
# directory
# It also generates a csv file called "sum.csv" in the current directory that lists
# all of the cleanTax files in the current directory and their timestamps
# __author__ = "Parisa Kianmajd"
#__version__ = "1.0.2"

import difflib
import sys
import os
import csv

def diff(f1,f2,t,c):
    filename = {f1:"", f2: ""}
    diff = difflib.ndiff(open(f1).readlines(), open(f2).readlines())
    
    for f in [f1,f2]:
        if "/" in f:
            filename[f] = f.split("/")[-1]
        else:
            filename[f] = f
            
    out = open('diff_' + str(c) + "_" + filename[f1]  , "w")
    out.write('File #1: ' + f1 + ' Timestamp #1:' + t[0] + '\n')
    out.write('File #2: ' + f2 + 'Timestamp #2:' + t[1] + '\n')
    out.write('\n')
    
    try:
        while 1:
            out.write(diff.next(),)
    except:
        pass
    
    out.close()

def einputdiff():
    filesList = list()
    compareList = list()

    try:
        arg1 = sys.argv[1]
    except IndexError:
        print "Usage: diff.py <arg1>"
        sys.exit(1)
        
    filename = sys.argv[1]
    
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.txt'):
                timestamp = root [2:20]
                if root != '.':
                    filesList.append([os.path.join(root, name),timestamp])
                if name == filename:
                    compareList.append([os.path.join(root, name),timestamp])

    with open("sum.csv","w") as reportFile:
        writer = csv.writer(reportFile, delimiter=',')
        writer.writerow (["Filename", "TimeStamp"])
        for n in filesList:
            writer.writerow([n[0],n[1]])
        
    i = 0
    c = 1
    while i < len(compareList) - 1:
        time = (compareList[i][1], compareList[i+1][1])
        diff(compareList[i][0],compareList[i+1][0],time,c)
        i += 2
        c += 1

einputdiff()

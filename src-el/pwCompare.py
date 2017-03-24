#!/usr/bin/env python
import sys
import re
from itertools import count

def usage():
    print "USAGE: python pwCompare.py dlv_pw_file gringo_pw_file"

def main():
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    pws1 = []
    pws2 = []
    
    # the first file
    f1 = open(file1, "r")
    lines = f1.readlines()
    for line in lines:
        if (re.match("\{(.*)\}", line)):
            rels = re.split(", " , (re.match("\{(.*)\}", line)).group(1))
            pws1.append(sorted(rels))
            
    # the second file
    f2 = open(file2, "r")
    lines = f2.readlines()
    for line in lines:
        if (re.match("\{(.*)\}", line)):
            rels = re.split(", " , (re.match("\{(.*)\}", line)).group(1))
            pws2.append(sorted(rels))
            
    # compare the two possible worlds
    for pw1 in pws1:
        if pw1 not in pws2:
            print "PWs in these two reasoners are NOT MATCH"
            exit()
    
    print "PWs in these two reasoners are MATCH"

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main()
    else:
        usage()
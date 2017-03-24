#! /usr/bin/env python

# Euler checker receives a Cleantax file as input
# and reports multiple roots per taxonomy, children with multiple parents, and unmatched leaves
# __author__ = "Parisa Kianmajd"
#__version__ = "1.0.1"


#import wizardParser
import re

def checkInputFiles(iFiles):
    inputData = list()
    taxonDict = dict()
    unmatched = dict()
    parents = list()
    leaves = list()
    errors = list()
    flag = False
    for f in iFiles:
        inputData += open(f).readlines()
    for line in inputData:
        if (re.match("taxonomy", line)):
            if flag:
                taxonDict[g]['parents'] += list(set(parents) - set(leaves))
                taxonDict[g]['leaves'] += list(set(leaves) - set(parents))
                leaves = []
                parents = []
            g = re.match("taxonomy\s+(\S+)\s(.*)", line).group(1)
            if g not in taxonDict:
                taxonDict.update({g:{'parents':[], 'leaves': [], 'arts': []}})
            flag = True
        if (re.match("\(.*\)", line)):
            elements = re.match("\((.*)\)", line).group(1).split(" ")
            parents.append(elements[0])
            for e in elements[1:]:
                if e in leaves:
                    errors.append('Child with multiple parents in taxonomy ' + str(g) + ": " + str(e))
                else:
                    leaves.append(e)
        if (re.match("articulations", line)):
                taxonDict[g]['parents'] += list(set(parents) - set(leaves))
                taxonDict[g]['leaves'] += list(set(leaves) - set(parents))
                leaves = []
                parents = []
        if (re.match("\[.*?\]", line)):
            art = re.match("\[(.*)\]", line).group(1).split(" ")
            for a in art:
                if "." in a: 
                    node = a.split('.')
                    taxonDict[node[0]]['arts'].append(node[1])

    for g in taxonDict:
        if len(taxonDict[g]['parents']) > 1:
            errors.append('Multiple roots in taxonomy ' + str(g) + ": " + ', '.join(taxonDict[g]['parents']) + ".")

    for g in taxonDict:
        for c in taxonDict[g]['leaves']:
            if c not in taxonDict[g]['arts']:
                if g not in unmatched:
                    unmatched.update({g:[]})
                unmatched[g].append(c)

    for g in unmatched:
        if len(unmatched[g]) > 0:
            errors.append('There are unmatched leaves in taxonomy ' + str(g) + ": " + ', '.join(unmatched[g]) + ".")
    if len(errors) == 0:
        print "The input is valid"
    else:
        print "Warnings:"
        for e in errors:
            print e

# MAIN
#if __name__ == '__main__':
#    checkInputFiles(wizardParser.args.iFile)

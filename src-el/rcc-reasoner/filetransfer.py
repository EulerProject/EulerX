#!/usr/bin/env python
import sys
import re

#remove the duplicate string in list li
def remove_duplicate_string(li):
    if li:
        li.sort()
        last = li[-1]
        for i in range(len(li)-2, -1, -1):
            if last == li[i]:
                del li[i]
            else:
                last = li[i]

# replace concepts names with integers (start from 0)
def replace_names(c_li, li_1, li_2, a_li, ch_li):
    rep_list = []
    i = 0
    for e in c_li:
        rep_tuple = (e, i)
        rep_list.append(rep_tuple)
        i = i + 1
    for e1 in li_1:
        for e2 in rep_list:
            if e1[0] == e2[0]:
                e1[0] = e2[1]
            if e1[1] == e2[0]:
                e1[1] = e2[1]
    for e1 in li_2:
        for e2 in rep_list:
            if e1[0] == e2[0]:
                e1[0] = e2[1]
            if e1[1] == e2[0]:
                e1[1] = e2[1]  
    for e1 in a_li:
        for e2 in rep_list:
            if e1[0] == e2[0]:
                e1[0] = e2[1]
            if e1[1] == e2[0]:
                e1[1] = e2[1]
    for children in ch_li:
        for i in range(len(children)):
            for e2 in rep_list:
                if children[i] == e2[0]:
                    children[i] = e2[1]                  
    return rep_list

def replace_art_names(s):
    inputs = s.split(" ")
    outputs = ""
    for e in inputs:
        if e == "equals":
            outputs = outputs + "=,"
        elif e == "is_included_in":
            outputs = outputs + "<,"
        elif e == "includes":
            outputs = outputs + ">,"
        elif e == "overlaps":
            outputs = outputs + "o,"
        elif e == "disjoints":
            outputs = outputs + "!,"
    outputs = outputs[:-1]
    return outputs 

# open the files
fileName = sys.argv[1]
uberMirFileName = fileName[:-4] + "_uber.txt"
f_in = open(fileName, "r")
f_out = open(uberMirFileName, "w")

# initialize variables
pc_list1 =[]
pc_list2 = []
art_list = []
concept_list = []
replace_list = []
children_list = []
name1 = ""          # first taxonomy name
name2 = ""          # second taxonomy name

# read CleanTax input file
lines = f_in.readlines()

for line in lines:
    
    if (re.match("taxonomy", line)):
        if name1 == "":
            name1 = re.match("taxonomy (.*) (.*)", line).group(1)
        else:
            name2 = re.match("taxonomy (.*) (.*)", line).group(1)
    
    elif (re.match("\(.*\)", line)):
        conceptLine = re.match("\((.*)\)", line).group(1)
        concepts = re.split("\s", conceptLine)
        children = []
        
        # read taxonomy1 section
        if name1 != "" and name2 == "":
            parent = name1 + "." + concepts[0]
            concept_list.append(parent)
            
            for i in range(1, len(concepts)):
                child = name1 + "." + concepts[i]
                concept_list.append(child)
                children.append(child)
                pc_item = [parent, child]
                pc_list1.append(pc_item)
            for e in children:
                children_list.append(children)
                
        # read taxonomy2 section
        else:
            parent = name2 + "." + concepts[0]
            concept_list.append(parent)
            
            for i in range(1, len(concepts)):
                child = name2 + "." + concepts[i]
                concept_list.append(child)
                children.append(child)
                pc_item = [parent, child]
                pc_list2.append(pc_item)
            for e in children:
                children_list.append(children)
                
    elif (re.match("\[.*?\]", line)):
        inside = re.match("\[(.*)\]", line).group(1)
        inside = inside.replace("{","").replace("}","")
        temp_list = re.split("\s", inside)
        art_type = ""
        
        # articulation key words
        for i in range(1, len(temp_list)-1):
            art_type = art_type + temp_list[i] + " "
        art_item = [temp_list[0], temp_list[len(temp_list)-1], art_type[:-1]]
        art_list.append(art_item)
            
remove_duplicate_string(concept_list)
remove_duplicate_string(children_list)
replace_list = replace_names(concept_list, pc_list1, pc_list2, art_list, children_list)
print "Hash of concepts:", replace_list

# write the title
f_out.write(str(len(concept_list)) + "\n")

# write the parent-child relation
for e in pc_list1:
    s = str(e[0]) + " " + str(e[1]) + " [>]\n"
    f_out.write(s)
for e in pc_list2:
    s = str(e[0]) + " " + str(e[1]) + " [>]\n"
    f_out.write(s)

# update the art names in the articulation list
for e in art_list:
    if " " in e[2]:
        s = ""
        temp_list = e[2].split(" ")
        for e2 in temp_list:
            e2 = replace_art_names(e2)
            s = s + e2 + ","
        e[2] = s[:-1]
    else:
        e[2] = replace_art_names(e[2])
        
#print "modified_art_list=", art_list
# write articulations
for e in art_list:
    s = str(e[0]) + " " + str(e[1]) + " [" + e[2] + "]\n"
    f_out.write(s)
#print "children_list=", children_list
# write sibling-disjointness
for children in children_list:
    for i in range(len(children)-1):
        for j in range(i+1,len(children)):
            s = str(children[i]) + " " + str(children[j]) + " [!]\n"
            f_out.write(s)
            

f_in.close()
f_out.close()
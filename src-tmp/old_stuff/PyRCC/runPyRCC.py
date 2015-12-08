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
# Main program: Read from CleanTax input file to generate a .csp file for PyRCC8
# In order to convert RCC5 to RCC8, we join the tangential and non-tangential relations 
#=============================================================================================
import sys
import re
import commands


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
            outputs = outputs + "EQ "
        elif e == "is_included_in":
            outputs = outputs + "TPP NTPP "
        elif e == "includes":
            outputs = outputs + "TPPI NTPPI "
        elif e == "overlaps":
            outputs = outputs + "PO "
        elif e == "disjoints":
            outputs = outputs + "DC EC "
    outputs = outputs[:-1]
    return outputs 
#    if s == "equals":
#        return "EQ"
#    if s == "is_included_in":
#        return "TPP NTPP"
#    if s == "includes":
#        return "TPPI NTPPI"
#    if s == "overlaps":
#        return "PO"
#    if s == "disjoints":
#        return "DC EC"

def containLsumRsum(li):
    for e in li:
        if e == "rsum":
            return "rsum"
        if e == "lsum":
            return "lsum"
    return "none"


def findConcept(n, rep_list):
    for t in rep_list:
        if n == t[1]:
            return t[0] 
    

def findRelation(s):
    relation = ""
    if "DC" in s and "EC" in s:
        relation = relation + "!"
    if "EQ" in s:
        relation = relation + "="
    if "PO" in s:
        relation = relation + "o"
    if "TPP" in s and "NTPP" in s and "TPPI" not in s and "NTPPI" not in s:
        relation = relation + "<"
    if "TPPI" in s and "NTPPI" in s:
        relation = relation + ">"
    
    relation2 = ""
    if len(relation) > 1:
        relation2 = "{"
        for r in relation:
            relation2 = relation2 + r + ", "
        relation2 = relation2[:-2]+"}"
    else:
        relation2 = relation
    
    relation2 = relation2.replace("o","><")
    return relation2

def newgetoutput(cmd):
    result = commands.getstatusoutput(cmd)
    if result[0] != 0:
        print "cmd: ", cmd
        print "exit status: ", result[0]
        return
    else:
        return result[1]

# open the files
fileName = sys.argv[1]
pyrccFileName = fileName[:-4] + "_pyrcc.csp"
f_in = open(fileName, "r")
f_out = open(pyrccFileName, "w")

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
        
#print "pc_list1=", pc_list1
#print "pc_list2=", pc_list2
#print "art_list=", art_list

remove_duplicate_string(concept_list)
#print "concept_list=", concept_list
remove_duplicate_string(children_list)
#print "children_list=", children_list
#print "pc_list1=", pc_list1
#print "pc_list2=", pc_list2
#print "art_list=", art_list
#print "children_list=", children_list


replace_list = replace_names(concept_list, pc_list1, pc_list2, art_list, children_list)
#print "AFTERRRRRR"
#print "replace_list=", replace_list
#print "pc_list1=", pc_list1
#print "pc_list2=", pc_list2
#print "art_list=", art_list
#print "children_list=", children_list


### create the output file
# write the title
f_out.write(str(len(concept_list)-1) + " #" + fileName[:-4] + "\n")

# write the parent-child relation
for e in pc_list1:
    s = str(e[0]) + " " + str(e[1]) + " ( TPPI NTPPI )\n"
    f_out.write(s)
for e in pc_list2:
    s = str(e[0]) + " " + str(e[1]) + " ( TPPI NTPPI )\n"
    f_out.write(s)

# update the art names in the articulation list
for e in art_list:
    if " " in e[2]:
        s = ""
        temp_list = e[2].split(" ")
        for e2 in temp_list:
            e2 = replace_art_names(e2)
            s = s + e2 + " "
        e[2] = s[:-1]
    else:
        e[2] = replace_art_names(e[2])
        
#print "modified_art_list=", art_list
# write articulations
for e in art_list:
    s = str(e[0]) + " " + str(e[1]) + " ( " + e[2] + " )\n"
    f_out.write(s)
#print "children_list=", children_list
# write sibling-disjointness
for children in children_list:
    for i in range(len(children)-1):
        for j in range(i+1,len(children)):
            s = str(children[i]) + " " + str(children[j]) + " ( DC EC )\n"
            f_out.write(s)
            
f_out.write(".")


f_in.close()
f_out.close()

# execute PyRCC8
newgetoutput("rcc8 -d < " + pyrccFileName + " > output.txt")

mir = []
f = open("output.txt", "r")
lines = f.readlines()

for line in lines:
    if '[' in line:
        pair = []

        rels = re.match('(.*)\s(.*)\s\[(.*)\](.*)', line)
        
        pair.append(findConcept(int(rels.group(1)), replace_list))
        pair.append(findRelation(rels.group(3)))
        pair.append(findConcept(int(rels.group(2)), replace_list))
        
        print pair
        mir.append(pair)
        

#print mir


newgetoutput("rm output.txt")




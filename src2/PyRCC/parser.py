#=============================================================================================
# Main program: Read from CleanTax input file to generate a .csp file for PyRCC8
# In order to convert RCC5 to RCC8, we join the tangential and non-tangential relations 
#=============================================================================================
import sys

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

# open the files
fileName = sys.argv[1]
f_in = open(fileName, "r")
f_out = open(fileName[:-4] + "_pyrcc.csp", "w")

# initialize variables
not_EOF = True
pc_list1 =[]
pc_list2 = []
art_list = []
concept_list = []
replace_list = []
children_list = []

while not_EOF:
    # read taxonomy 1 keywords
    line = f_in.readline()
    name1 = line[:-1].split(" ")[1]
    
    # read concepts in taxonomy 1
    line = f_in.readline()
    while len(line) != 1:
        children = []
        temp_list = line[1:-2].split(" ")
        parent = name1 + "." + temp_list[0]
        concept_list.append(parent)
        for i in range(1,len(temp_list)):
            child = name1 + "." + temp_list[i]
            concept_list.append(child)
            children.append(child)
            pc_item = [parent, child]
            pc_list1.append(pc_item)
        for e in children:
            children_list.append(children)
        line = f_in.readline()

    # read taxonomy 2 keywords
    line = f_in.readline()
    name2 = line[:-1].split(" ")[1]
    
    # read concepts in taxonomy 2
    line = f_in.readline()
    while len(line) != 1:
        children = []
        temp_list = line[1:-2].split(" ")
        parent = name2 + "." + temp_list[0]
        concept_list.append(parent)
        for i in range(1,len(temp_list)):
            child = name2 + "." + temp_list[i]
            concept_list.append(child)

            children.append(child)
            pc_item = [parent, child]
            pc_list2.append(pc_item)
        for e in children:
            children_list.append(children)
        line = f_in.readline()
        
    # read articulation keyword
    line = f_in.readline()
    
    # read articulation pairs
    line = f_in.readline()
    while len(line) != 0:
        art_type = ""
        if line[-1] == "\n":
            line = line[1:-2].replace("{","").replace("}","")
        else:
            line = line[1:-1].replace("{","").replace("}","")
        temp_list = line.split(" ")
        if len(temp_list) > 1:
            if containLsumRsum(temp_list) == "none": 
                for i in range(1, len(temp_list)-1):
                    art_type = art_type + temp_list[i] + " "
                art_item = [temp_list[0], temp_list[len(temp_list)-1], art_type[:-1]]
                art_list.append(art_item)
            elif containLsumRsum(temp_list) == "rsum":
                for i in range(2, len(temp_list)):
                    art_item = [temp_list[0], temp_list[i], "includes"]
                    art_list.append(art_item)
#                children_list.append(temp_list[2:])
            elif containLsumRsum(temp_list) == "lsum":
                for i in range(0, len(temp_list)-2):
                    art_item = [temp_list[i], temp_list[len(temp_list)-1], "is_included_in"]
                    art_list.append(art_item)
#                children_list.append(temp_list[0:-2])            
            line = f_in.readline()      
    if len(line) == 0:
        not_EOF = False
        
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
print "rep_list=", replace_list
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

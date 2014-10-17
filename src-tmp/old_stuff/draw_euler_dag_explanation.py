import psycopg2
import itertools

#check whether string s1 and s2 are same but different order of characters
def check_same_string(s1,s2):
    return sorted(s1) == sorted(s2)

#check whether string s1 and s2 have the same characters
def not_have_same_char(s1,s2):
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i:i+1] == s2[j:j+1]:
                return False
    return True

#check whether tuple t1 and t2 have the same characters
def tuple_not_have_same_char(t1,t2):
    for member1 in t1:
        for member2 in t2:
            if member1 == member2:
                return False
    return True

#check whether string s is in list li, regardless of ordering of characters in string
def not_in_list(s,li):
    for i in range(len(li)):
        if check_same_string(s,li[i]):
            return False
    return True

#check whether tuple t is in list li
def tuple_not_in_list(t,li):
    for aTuple in li:
        if t == aTuple:
            return False
    return True

#check whether string s is in list li, considering about the ordering of characters in string
def not_in_list_with_order(s,li):
    for i in range(len(li)):
        if s == li[i]:
            return False
    return True
        
#check whether the two string s1, s2 can join without leads to a disjoint 
def check_string_join(s1,s2,li):
    for i in range (len(s1)-1):
        for j in range(len(s2)-1):
            if (not_in_list(s1[i:i+1]+s2[j+1:j+2],li)) == False or (not_have_same_char(s1[:-1],s2[1:])) == False:
                return False
    return True

#check whether the two tuple t1,t2 can join without leads to a disjoint
def check_tuple_join(t1,t2,li):
    for i in range(len(t1)-1):
        for j in range(len(t2)-1):
            if (tuple_not_in_list(t1[i:i+1] + t2[j+1:j+2], li)) == False or (tuple_not_have_same_char(t1[:-1],t2[1:])) == False:
                return False
    return True


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

#check the list available to continue to do the concept combine
def check_list(li,li2):
    for i in range(len(li)):
        for j in range(len(li)):
            if li[i][-1:] == li[j][0:1] and check_string_join(li[i],li[j],li2) and li[i][0:1] != li[j][-1:] and not_in_list(li[i]+li[j][1:],li):
                print "Still has =", li[i], li[j], li[i]+li[j][1:]           
                return True
    return False

#check the tuple list still available to continue to do the concept combine
def tuple_check_list(li1,li2):
    for i in range(len(li1)):
        for j in range(len(li2)):
            if li1[i][-1] == li1[j][0] and check_tuple_join(li1[i],li1[j],li2) and li1[i][0] != li1[j][-1] and tuple_not_in_list(li1[i]+li1[j][1:],li1):
                print "Still has =", li1[i], li1[j], li1[i] + li1[j][1:]
                return True
    return False

#check whether string sub is the substring of s
def check_substring(sub,s):
    if s.find(sub) != -1 and sub != s:
        return True
    else:
        return False

#remove the duplicate tuples in list
def remove_dup_tuples_in_list(l):
    l.sort()
    return list(l for l,_ in itertools.groupby(l))

#check whether the two tuples have the same characters
def tuple_same_char(t1,t2):
    for member1 in t1:
        if (member1 in t2) == False:
            return False
    for member2 in t2:
        if (member2 in t1) == False:
            return False
    if len(t1) != len(t2):
        return False
    else:
        return True


#################### Main program strat here ##################################(We renew it here)
#initial the db
conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' port='5432' password='19870906'")
cur = conn.cursor()

#initialize the list
list1 = []
list2 = []
list_inferred = []

#execute the SQL to get all inferred pair of concepts, put them into list_inferred (it has 2-tuple with reversing order)
cur.execute("select distinct concept1,concept2 from test where arttype = 'inferred'")
results = cur.fetchall()
for result in results:
    list_inferred.append(result)
    
cur.execute("select distinct concept2,concept1 from test where arttype = 'inferred'")
results = cur.fetchall()
for result in results:
    list_inferred.append(result)
    
#execute the SQL for all disjoint relation, put them into list2
cur.execute("select distinct concept1,concept2 from test where relation = 'disjoint'")
results = cur.fetchall()

for result in results:
    list2.append(result)

list2 = remove_dup_tuples_in_list(list2)
print "list2 =", list2, len(list2)

        
#execute the SQL for all non-disjoint relation
cur.execute("select distinct concept1,concept2 from test where relation = 'is_included_in'")
results = cur.fetchall()
add_list = []
for result in results:
    add_list.append(result)
add_list = remove_dup_tuples_in_list(add_list)
list1.extend(add_list)
print "list1 =", list1, len(list1)

cur.execute("select distinct concept1,concept2 from test where relation = 'includes'")
results = cur.fetchall()
add_list = []
for result in results:
    add_tuple = (result[1], result[0])
    add_list.append(add_tuple)
add_list = remove_dup_tuples_in_list(add_list)
list1.extend(add_list)
print "list1 =", list1, len(list1)

cur.execute("select distinct concept1,concept2 from test where relation = 'overlaps'")
results = cur.fetchall()

# create overlaps list
overlaps_list = []
add_list = []

for result in results:
    add_list.append(result)
    add_tuple = (result[1], result[0])
    add_list.append(add_tuple)
    overlaps_list.append(result)
    overlaps_tuple = (result[1], result[0])
    overlaps_list.append(overlaps_tuple)
add_list = remove_dup_tuples_in_list(add_list)    
overlaps_list = remove_dup_tuples_in_list(overlaps_list)
list1.extend(add_list)

print "Now finish list initialization"
print "list1 =", list1, len(list1)
print "list2 =", list2, len(list2)

# Begin to do the list operations
list_begin = list1

print "Here we begin do the list operations"

while True:
    temp_list = []
    for i in range(len(list1)):
        for j in range(len(list1)):
            if list1[i][-1] == list1[j][0] and check_tuple_join(list1[i],list1[j],list2) and list1[i][0] != list1[j][-1] and tuple_not_in_list(list1[i]+list1[j][1:],list1):
                new_item = list1[i] + list1[j][1:]
                print new_item
                temp_list.append(new_item)
                
    print "temp_list =", temp_list
    list1.extend(temp_list)
    list1 = remove_dup_tuples_in_list(list1)
    print "list1 =", list1, len(list1)
    
    if tuple_check_list(list1,list2) == False:
        break
    

#clean the list1
print "Now cleaning"

#remove the not_hexie
drop_list = []
for minterm in list1:
    for i in range(len(minterm)-1):
        for j in range(i+1,len(minterm)):
            if tuple_not_in_list(minterm[i:i+1] + minterm[j:j+1], list_begin):
                print minterm[i:i+1] + minterm[j:j+1], minterm
                drop_list.append(minterm)
drop_list = remove_dup_tuples_in_list(drop_list)
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
    
print "list1 =", list1, len(list1)
 
#remove substring
print "clean the substring"
drop_list = []

# convert list1 with tuples to list1_str with strings
list1_str = []
for i in range(len(list1)):
    list1_str.append("")
for i in range(len(list1)):
    for member in list1[i]:
        list1_str[i] = list1_str[i] + member
    
for i in range(len(list1_str)):
    for j in range(len(list1_str)):
        if check_substring(list1_str[i],list1_str[j]):
            drop_list.append(list1[i])
drop_list = remove_dup_tuples_in_list(drop_list)
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
    
print "list1 =", list1, len(list1)


#remove the same head-end, but shorter ones
print "clean the same head-end, but shorter ones"
drop_list = []
for i in range(len(list1)):
    for j in range(len(list1)):
        if list1[i][0] == list1[j][0] and list1[i][-1] == list1[j][-1] and len(list1[i]) < len(list1[j]):
            drop_list.append(list1[i])
drop_list = remove_dup_tuples_in_list(drop_list)
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
    
print "list1 =", list1, len(list1)

#get the final list
print "Here we have the final list"
final_list = []
for minterm in list1:
    for i in range(len(minterm)):
        final_list.append(minterm[i:])
final_list = remove_dup_tuples_in_list(final_list)
print "final_list = ", final_list, len(final_list)

print "remove the duplicates with same but different orders of characters"
drop_list = []
for i in range(len(final_list)-1):
    for j in range(i+1,len(final_list)):
        if tuple_same_char(final_list[i],final_list[j]):
            drop_list.append(final_list[i])
drop_list = remove_dup_tuples_in_list(drop_list)
for i in range(len(drop_list)):
    final_list.remove(drop_list[i])

print "final_list =", final_list, len(final_list)        


#close the file and db
cur.close()
conn.close()


######################### Now let's generate the dot file for Euler_DAG ########################
print "Now let's generate the dot file for Euler_DAG"
fDAG = open("result.dot", 'w')
fDAG.write("digraph {\n\n")
fDAG.write("rankdir = LR;ranksep=2;nodesep=.5\n\n")
# copy the overlaps_list to comb_node_list
comb_node_list = []
#print overlaps_list
for member in overlaps_list:
    comb_node_list.append(member)
#print comb_node_list

# remove the same pair of concepts (same characters but with different orders)
drop_list = []
for i in range(len(comb_node_list)-1):
    for j in range(i+1,len(comb_node_list)):
        if tuple_same_char(comb_node_list[i],comb_node_list[j]):
            drop_list.append(comb_node_list[i])
drop_list = remove_dup_tuples_in_list(drop_list)
for i in range(len(drop_list)):
    comb_node_list.remove(drop_list[i])
 
print "overlaps_list = ", overlaps_list
print "comb_node_list = ", comb_node_list
print "final_list = ", final_list, len(final_list)

# separate MIR and INFERRED articulations
print "First we separate MIR and INFERRED articulations"
comb_node_list_mir = []
comb_node_list_inferred = []

for member in comb_node_list:
    if tuple_not_in_list(member,list_inferred):
        comb_node_list_mir.append(member)
    else:
        comb_node_list_inferred.append(member)

print "comb_node_list_mir = ", comb_node_list_mir
print "comb_node_list_inferred = ", comb_node_list_inferred

# draw the MIR combination nodes and the edges among them
comb_node_list_mir_str = []
for i in range(len(comb_node_list_mir)):
    comb_node_list_mir_str.append("")
for i in range(len(comb_node_list_mir)):
    for member in comb_node_list_mir[i]:
        comb_node_list_mir_str[i] = comb_node_list_mir_str[i] + member + ","
    comb_node_list_mir_str[i] = comb_node_list_mir_str[i][:-1]

print "comb_node_list_mir_str =", comb_node_list_mir_str        
for member_str in comb_node_list_mir_str:
    fDAG.write("\"" + member_str + "\"" + " [style=dashed];\n")

for member_str in comb_node_list_mir_str:   
    for member in comb_node_list_mir:
        temp_str = "" 
        for letter in member:
            temp_str = temp_str + letter + ","
        temp_str = temp_str[:-1]
        if member_str == temp_str:
            for letter in member:
                fDAG.write("\"" + letter + "\"" + " -> " + "\"" + member_str + "\"" + " [arrowsize=.5,style=dashed];\n")

# draw the INFERRED combination nodes and the edges among them
comb_node_list_inferred_str = []
for i in range(len(comb_node_list_inferred)):
    comb_node_list_inferred_str.append("")
for i in range(len(comb_node_list_inferred)):
    for member in comb_node_list_inferred[i]:
        comb_node_list_inferred_str[i] = comb_node_list_inferred_str[i] + member + ","
    comb_node_list_inferred_str[i] = comb_node_list_inferred_str[i][:-1]

print "comb_node_list_inferred_str =", comb_node_list_inferred_str        
for member_str in comb_node_list_inferred_str:
    fDAG.write("\"" + member_str + "\"" + " [style=dashed,color=green];\n")

for member_str in comb_node_list_inferred_str:   
    for member in comb_node_list_inferred:
        temp_str = "" 
        for letter in member:
            temp_str = temp_str + letter + ","
        temp_str = temp_str[:-1]
        if member_str == temp_str:
            for letter in member:
                fDAG.write("\"" + letter + "\"" + " -> " + "\"" + member_str + "\"" + " [arrowsize=.5,style=dashed,color=green];\n")


# draw the other nodes and the edge among them
edge_list = []
o_list = []

for member in final_list:
    i = 1
    while i < len(member):
        t = (member[-i], member[-i-1])
        if tuple_not_in_list(t, overlaps_list):
            o_list.append(t)
        i = i + 1
        
o_list = remove_dup_tuples_in_list(o_list)

print "o_list=", o_list
            
transi_tuple = ()
transi_list = []
update_transi_list = [("","")]
drop_list = []

# remove the transitive reductions in original_list in first round
for i in range(len(o_list)-1):
    for j in range(i+1,len(o_list)):
        if o_list[i][1] == o_list[j][0]:
            transi_list.append((o_list[i][0], o_list[j][1]))
        elif o_list[i][0] == o_list[j][1]:
            transi_list.append((o_list[j][0],o_list[i][1]))
transi_list = remove_dup_tuples_in_list(transi_list)

for member in transi_list:
    if tuple_not_in_list(member, o_list) == False:
        drop_list.append(member)

# remove the transitive reductions in original_list and transi_list for following rounds
while len(update_transi_list) != 0:
    update_transi_list = []
    for member1 in o_list:
        for member2 in transi_list:
            if member1[1] == member2[0]:
                update_transi_list.append((member1[0], member2[1]))
            elif member1[0] == member2[1]:
                update_transi_list.append((member2[0],member1[1]))
    update_transi_list = remove_dup_tuples_in_list(update_transi_list)
    
    for member in update_transi_list:
        if tuple_not_in_list(member, o_list) == False:
            drop_list.append(member) 
    
    transi_list = update_transi_list

drop_list = remove_dup_tuples_in_list(drop_list)

for member in drop_list:
    if tuple_not_in_list(member,o_list) == False:
        o_list.remove(member)

print "o_list = ", o_list
print "transi_list = ", transi_list
print "drop_list = ", drop_list            
            
# write into the dot file
edge_string = ""
edge_list = []
for member in o_list:
    if tuple_not_in_list(member,list_inferred):
        edge_string = "\"" + member[0] + "\"" + " -> " + "\"" + member[1] + "\"" + "[arrowsize=.5,style=filled];\n"
    else:
        edge_string = "\"" + member[0] + "\"" + " -> " + "\"" + member[1] + "\"" + "[arrowsize=.5,style=filled,color=green];\n" 
    edge_list.append(edge_string)
remove_duplicate_string(edge_list) 

for line in edge_list:
    fDAG.write(line)

            
print "done"
fDAG.write("}\n")
fDAG.close()

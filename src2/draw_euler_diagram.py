import psycopg2
#import string

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

#check whether string s is in list li, regardless of ordering of characters in string
def not_in_list(s,li):
    for i in range(len(li)):
        if check_same_string(s,li[i]):
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
#check the list available
def check_list(li,li2):
    for i in range(len(li)):
        for j in range(len(li)):
            if li[i][-1:] == li[j][0:1] and check_string_join(li[i],li[j],li2) and li[i][0:1] != li[j][-1:] and not_in_list(li[i]+li[j][1:],li):
                print "Still has =", li[i], li[j], li[i]+li[j][1:]           
                return True
    return False

#check whether string sub is the substring of s
def check_substring(sub,s):
    if s.find(sub) != -1 and sub != s:
        return True
    else:
        return False

#################### Main program strat here ##################################
#initial the db
conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' port='5432' password='19870906'")
cur = conn.cursor()

#execute the SQL for all disjoint relation
cur.execute("select distinct concept1,concept2 from test where relation = 'disjoint'")
results = cur.fetchall()

list1 = []
list2 = []
drop_list = []
for result in results:
    list2.append(result[0] + result[1])
for i in range(len(list2)-1):
    for j in range(i+1,len(list2)):
        if check_same_string(list2[i],list2[j]):
            drop_list.append(list2[i])
remove_duplicate_string(drop_list)
for i in range(len(drop_list)):
    list2.remove(drop_list[i])
        
#execute the SQL for all non-disjoint relation
cur.execute("select distinct concept1,concept2 from test where relation = 'is_included_in'")
results = cur.fetchall()
add_list = []
drop_list = []
for result in results:
    add_list.append(result[0] + result[1])
for i in range(len(add_list)-1):
    for j in range(i+1,len(add_list)):
        if add_list[i] == add_list[j]:
            drop_list.append(add_list[i])
remove_duplicate_string(drop_list)
for i in range(len(drop_list)):
    add_list.remove(drop_list[i])
list1.extend(add_list)

cur.execute("select distinct concept1,concept2 from test where relation = 'includes'")
results = cur.fetchall()
add_list = []
drop_list = []
for result in results:
    add_list.append(result[1] + result[0])
print add_list
for i in range(len(add_list)-1):
    for j in range(i+1,len(add_list)):
        if add_list[i] == add_list[j]:
            drop_list.append(add_list[i])
remove_duplicate_string(drop_list)
for i in range(len(drop_list)):
    add_list.remove(drop_list[i])
list1.extend(add_list)

cur.execute("select distinct concept1,concept2 from test where relation = 'overlaps'")
results = cur.fetchall()
add_list = []
drop_list = []
for result in results:
    add_list.append(result[0] + result[1])
    add_list.append(result[1] + result[0])
for i in range(len(add_list)-1):
    for j in range(i+1,len(add_list)):
        if add_list[i] == add_list[j]:
            drop_list.append(add_list[i])
remove_duplicate_string(drop_list)
for i in range(len(drop_list)):
    add_list.remove(drop_list[i])
list1.extend(add_list)
remove_duplicate_string(list1)
remove_duplicate_string(list2)

print "list1 = ", list1, len(list1)
print "list2 = ", list2, len(list2)

list_begin = list1


while True:
    temp_list = []
    for i in range(len(list1)):
        for j in range(len(list1)):
            if list1[i][-1:] == list1[j][0:1] and check_string_join(list1[i],list1[j],list2) and list1[i][0:1] != list1[j][-1:] and not_in_list(list1[i]+list1[j][1:],list1):
                new_item = list1[i]+list1[j][1:]
                print new_item
                temp_list.append(new_item)
    print "list1 = ", list1, "length = ", len(list1)
    print "temp_list = ", temp_list, "length = ", len(temp_list)

    list1.extend(temp_list)
    remove_duplicate_string(list1)

    print "list1 = ", list1, "length = ", len(list1)

    if check_list(list1,list2) == False:
        break


#clean the list1
print "Now cleaning"
drop_list = []

#remove the not_hexie
for minterm in list1:
    for i in range(len(minterm)-1):
        for j in range(i+1,len(minterm)):
            if not_in_list_with_order(minterm[i:i+1]+minterm[j:j+1],list_begin):
                print minterm[i:i+1],minterm[j:j+1],minterm
                drop_list.append(minterm)
remove_duplicate_string(drop_list)
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
    

print "list1 = ", list1, "length = ", len(list1)
        
#remove substring
print "clean the substring"
drop_list = []
for i in range(len(list1)):
    for j in range(len(list1)):
        if check_substring(list1[i],list1[j]):
            drop_list.append(list1[i])
remove_duplicate_string(drop_list)
print drop_list
        
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
print "list1 = ", list1, "length = ", len(list1)

#remove the same head-end, but shorter ones
print "clean the same head-end, but shorter ones"
drop_list = []
for i in range(len(list1)):
    for j in range(len(list1)):
        if list1[i][0:1] == list1[j][0:1] and list1[i][-1:] == list1[j][-1:] and len(list1[i]) < len(list1[j]):
            drop_list.append(list1[i])
remove_duplicate_string(drop_list)
print drop_list
        
for i in range(len(drop_list)):
    list1.remove(drop_list[i])
print "list1 = ", list1, "length = ", len(list1)

#get the final list
print "Here we have the final list"
final_list = []
for minterm in list1:
    for i in range(len(minterm)):
        print minterm[i:]
        final_list.append(minterm[i:])
remove_duplicate_string(final_list)
print "final_list = ", final_list, "length = ", len(final_list)

print "remove the duplicates with same but different orders of characters"
drop_list = []
for i in range(len(final_list)-1):
    for j in range(i+1,len(final_list)):
        if check_same_string(final_list[i],final_list[j]):
#            print final_list[i]
            drop_list.append(final_list[i])
remove_duplicate_string(drop_list)
print "drop_list = ", drop_list, "length = ", len(drop_list)

for i in range(len(drop_list)):
    final_list.remove(drop_list[i])

print "final_list = ", final_list, "length = ", len(final_list)

#close the file and db

cur.close()
conn.close()


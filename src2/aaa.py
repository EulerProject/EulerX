import itertools

#remove the duplicate tuples in list
def remove_dup_tuples_in_list(l):
    l.sort()
    return list(l for l,_ in itertools.groupby(l))

def tuple_not_in_list(t,li):
    for aTuple in li:
        if t == aTuple:
            return False
    return True

o_list = [("B","C"),("A","B"),("C","D"),("D","E"),("A","E")]
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

print "o_list = ", o_list
print "transi_list = ", transi_list
print "drop_list = ", drop_list




# read from inconsistent_articulation.txt
f_incon = open("inconsist_articulation.txt","r")

# get the inconsistent articulation
incon_list = []
incon_art = f_incon.readline()
temp_list = incon_art[1:-3].split(" ")
art_type = temp_list[0]
incon_tuple = (temp_list[1],temp_list[2])
incon_list.append(incon_tuple)


print "art_type = ", art_type
print "incon_list = ", incon_list

# get the explanation
explan_list_equals = []
explan_list_overlaps = []
explan_list_includes = []
for line in f_incon:
    explan_art = line[1:-2].split(" ")
    if explan_art[0] == "equals":
        explan_list_equals.append(explan_art[1]+explan_art[2])
        explan_list_equals.append(explan_art[2]+explan_art[1])
    elif explan_art[0] == "overlaps":
        explan_list_overlaps.append((explan_art[1],explan_art[2]))
        explan_list_overlaps.append((explan_art[2],explan_art[1]))
    elif explan_art[0] == "includes":
        explan_list_includes.append((explan_art[1],explan_art[2]))
        explan_list_includes.append((explan_art[2],explan_art[1]))

print "explan_list_equals = ", explan_list_equals
print "explan_list_overlaps = ",explan_list_overlaps
print "explan_list_includes = ",explan_list_includes


f_incon.close()
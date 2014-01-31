import psycopg2
import string

#initial the db
conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' port='5433' password='19870906'")
cur = conn.cursor()

#get the user's choice on parent-child taxonomy
author1 = raw_input("Please enter the first author for parent-child hierachy: ")
print author1
author2 = raw_input("Please enter the second author for parent-child hierachy: ")
print author2

#execute the SQL for first parent-child taxonomy
f = open('test.txt','a')

cur.execute("select distinct from_tc from pc_relation where from_accto=%s order by from_tc;", (author1,))
parents = cur.fetchall()
print parents
f.write("taxonomy 1 " + author1 + "\n")

for parent in parents:
    cur.execute("select to_tc from pc_relation where from_accto=%s and from_tc=%s;",(author1, parent))
    children = cur.fetchall()
    print parent
    print children

    f.write("(")
    f.writelines(parent)
    for child in children:
        f.write(" ")
        f.writelines(child)       
    f.write(")")
    f.write("\n")


#execute the SQL for second parent-child taxonomy
f.write("\ntaxonomy 2 " + author2 + "\n")

cur.execute("select distinct from_tc from pc_relation where from_accto=%s order by from_tc;", (author2,))
parents = cur.fetchall()
print parents

for parent in parents:
    cur.execute("select to_tc from pc_relation where from_accto=%s and from_tc=%s;",(author2, parent))
    children = cur.fetchall()
    print parent
    print children

    f.write("(")
    f.writelines(parent)
    for child in children:
        f.write(" ")
        f.writelines(child)       
    f.write(")")
    f.write("\n")



#execute the SQL for horizontal articulations
f.write("\narticulation abs abstract\n")

cur.execute("select from_tc, relationship_symbol, to_tc from concepts_full c1, lat_relation, concepts_full c2 where ((from_tc = c1.taxonconceptguid and to_tc = c2.taxonconceptguid) or (from_tc = c2.taxonconceptguid and to_tc = c1.taxonconceptguid)) and c1.accordingtosimple = %s and c2.accordingtosimple = %s;",(author1, author2))
articulations = cur.fetchall()

for articulation in articulations:
    print articulation

    if articulation[0].find(" ") == -1 and articulation[2].find(" ") == -1:
        if articulation[1] == "==":
            relation = "equals"
        elif articulation[1] == ">":
            relation = "includes"
        elif articulation[1] == "<":
            relation = "is_included_in"
        elif articulation[1] == "><":
            relation = "overlaps"
        elif articulation[1] == "|":
            relation = "disjoints"
        elif articulation[1] == "<==":
            relation = "{is_included_in equals}"
        elif articulation[1] == "==>" or articulation[1] == ">==":
            relation = "{equals includes}"
        elif articulation[1] == "<><":
            relation = "{is_included_in overlaps}"
##        elif articulation[1] == ">>":
##            relation = ""
##        elif articulation[1] == "<|":
##            relation = ""
##        elif articulation[1] == ">|":
##            relation = ""


        articulation_string = "[" + "1_" + articulation[0] + " " + relation + " " + "2_" + articulation[2] + "]"

        f.write(articulation_string)
        f.write("\n")

    elif articulation[0].find(" ") != -1 and articulation[2].find(" ") == -1 and articulation[0].find("-") == -1 :
        relation = "lsum"
        articulation_string = "[" + "1_" + articulation[0].replace("  +  "," 1_") + " " + relation + " " + "2_" + articulation[2] + "]"

        f.write(articulation_string)
        f.write("\n")
        
    elif articulation[0].find(" ") == -1 and articulation[2].find(" ") != -1 and articulation[2].find("-") == -1:
        relation = "rsum"
        articulation_string = "[" + "1_" + articulation[0] + " " + relation + " " + "2_" + articulation[2].replace("  +  "," 2_") + "]"

        f.write(articulation_string)
        f.write("\n")    

    elif articulation[0].find(" ") != -1 and articulation[2].find(" ") == -1 and articulation[0].find("+") == -1:
        relation = "ldiff"
        articulation_string = "[" + "1_" + articulation[0].replace("  -  "," 1_") + " " + relation + " " + "2_" + articulation[2] + "]"

        f.write(articulation_string)
        f.write("\n")
        
    elif articulation[0].find(" ") == -1 and articulation[2].find(" ") != -1 and articulation[2].find("+") == -1:
        relation = "rdiff"
        articulation_string = "[" + "1_" + articulation[0] + " " + relation + " " + "2_" + articulation[2].replace("  -  "," 2_") + "]"

        f.write(articulation_string)
        f.write("\n")    




#close the file and db
f.close()
cur.close()
conn.close()


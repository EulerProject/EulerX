import itertools

l = ["equals", "disjoint"]

arts = []
r = []
for p1 in l:
    for p2 in l:
        for p3 in l:
            for p4 in l:
                for p5 in l:
                    for p6 in l:
                        for p7 in l:
                            for p8 in l:
                                for p9 in l:
                                    for p10 in l:
                                        r.append(p1)
                                        r.append(p2)
                                        r.append(p3)
                                        r.append(p4)
                                        r.append(p5)
                                        r.append(p6)
                                        r.append(p7)
                                        r.append(p8)
                                        r.append(p9)
                                        r.append(p10)
                                        arts.append(r)
                                        r = []
#print "arts=", arts, len(arts)

pairs0 = []
pairs1 = []
pairs2 = []
pairs3 = []
allpairs = []
# a
rank0 = ['a']
l = list(itertools.permutations(rank0))
for e in l:
    pairs0.append([(rank0[0], e[0])])

# b,c
rank1 = ['b','c']
l = list(itertools.permutations(rank1))
for e in l:
    pairs1.append([(rank1[0], e[0]), (rank1[1], e[1])])

# d,e,f
rank2 = ['d','e','f']
l = list(itertools.permutations(rank2))
for e in l:
    pairs2.append([(rank2[0], e[0]), (rank2[1], e[1]), (rank2[2], e[2])])

# g,h,i,j 
rank3 = ['g','h','i','j']
l = list(itertools.permutations(rank3))
for e in l:
    pairs3.append([(rank3[0], e[0]), (rank3[1], e[1]), (rank3[2], e[2]), (rank3[3], e[3])])

for e0 in pairs0:
    for e1 in pairs1:
        for e2 in pairs2:
            for e3 in pairs3:
                allpairs.append(e0 + e1 + e2 + e3)
        
#print "allpairs=", allpairs, len(allpairs)

i = 0
for allpair in allpairs:
    for art in arts:
        f = open("case_"+ str(i) + ".txt", "w")
        f.write("articulation tw1 tw1\n")
        f.write('[1.' + allpair[0][0] + ' ' + art[0] + ' 2.' + allpair[0][1] + ']\n')
        f.write('[1.' + allpair[1][0] + ' ' + art[1] + ' 2.' + allpair[1][1] + ']\n')
        f.write('[1.' + allpair[2][0] + ' ' + art[2] + ' 2.' + allpair[2][1] + ']\n')
        f.write('[1.' + allpair[3][0] + ' ' + art[3] + ' 2.' + allpair[3][1] + ']\n')
        f.write('[1.' + allpair[4][0] + ' ' + art[4] + ' 2.' + allpair[4][1] + ']\n')
        f.write('[1.' + allpair[5][0] + ' ' + art[5] + ' 2.' + allpair[5][1] + ']\n')
        f.write('[1.' + allpair[6][0] + ' ' + art[6] + ' 2.' + allpair[6][1] + ']\n')
        f.write('[1.' + allpair[7][0] + ' ' + art[7] + ' 2.' + allpair[7][1] + ']\n')
        f.write('[1.' + allpair[8][0] + ' ' + art[8] + ' 2.' + allpair[8][1] + ']\n')
        f.write('[1.' + allpair[9][0] + ' ' + art[9] + ' 2.' + allpair[9][1] + ']\n')
        f.close()
        i += 1

#for art in arts:
#    f = open("case_"+'_'.join(art)+".txt", "w")
#    f.write("articulation tw1 tw1\n")
#    f.write("[1.a " + art[0] + " 2.a]\n")
#    f.write("[1.b " + art[1] + " 2.b]\n")
#    f.write("[1.c " + art[2] + " 2.c]\n")
#    f.write("[1.d " + art[3] + " 2.d]\n")
#    f.write("[1.e " + art[4] + " 2.e]\n")



import os
import random
import math
from helper import *
from relations import *

class CtiGenerator:

    global inst
    inst = None

    def __init__(self):
	return None

    # Currently only generate N-ary Cti input files
    def run(self, options):
        self.mednodes = []
	if options.projectname is None:
	    options.projectname = "foo"
	if not os.path.exists(options.outputdir):
	    os.mkdir(options.outputdir)

        # Create a complete n-nary tree
	if options.nary != 0:
	    self.ofile = os.path.join(options.outputdir, options.projectname+"_n"+options.nary.__str__()+"_"+options.depth.__str__()+".txt")
	    fcti = open(self.ofile, 'w')
	    for i in range(1,3):
		fcti.write("taxonomy "+i.__str__()+" T"+i.__str__()+"\n")
		for j in range(options.depth):
		    slfidx =  int((options.nary ** j - 1) / (options.nary - 1)) + 1
		    kididx =  int((options.nary ** (j+1) - 1) / (options.nary - 1)) + 1
		    for k in range(options.nary ** j):
			fcti.write("("+slfidx.__str__())
			for t in range(options.nary):
			    fcti.write(" "+kididx.__str__())
			    kididx += 1
		        fcti.write(")\n")
			slfidx += 1
                fcti.write("\n")
            nnodes = (options.nary**(options.depth+1) - 1)/(options.nary-1)
            self.mednodes = range((options.nary**options.depth - 1)/(options.nary-1) + 1,
                        (options.nary**options.depth - 1)/(options.nary-1) + options.nary + 1)
            print "LALA"


        # Create a balanced tree
        elif options.nnodes != 0:
            if options.nnodes <= options.depth+1:
                print "Wrong input: -m should be larger than -d"
                return None
            self.ofile = os.path.join(options.outputdir, options.projectname+"_m"+options.nnodes.__str__()+"_"+options.depth.__str__()+".txt")
            fcti = open(self.ofile, 'w')
            noded = []
            kids = []
            kids.append([])
            self.fillBalanced(noded, kids, options)
            if options.verbose:
                print "Generating a balanced tree:"
                for i in range(1,options.nnodes+1):
                    print "Node",i,": list of kids",kids[i]

	    for i in range(1,3):
		fcti.write("taxonomy "+i.__str__()+" T"+i.__str__()+"\n")
		for j in range(options.depth):
		    for k in noded[j]:
			fcti.write("("+k.__str__())
			for t in kids[k]:
			    fcti.write(" "+t.__str__())
		        fcti.write(")\n")
                fcti.write("\n")
            nnodes = options.nnodes

        fcti.write("articulation ar "+options.projectname)
        if(not relation.has_key(options.relation) or options.relation == "no"):
	    myrel = int(random.randint(0,4))
	else:
	    myrel = int(math.log(relation[options.relation],2))
        # get rel string
	myrelstr = relstr[myrel]
	for i in range(1, nnodes+1):
            if options.incEx and i in self.mednodes:
                fcti.write("\n[1."+i.__str__()+" equals 2."+i.__str__()+"]")
            else:
                fcti.write("\n[1."+i.__str__()+" "+myrelstr+" 2."+i.__str__()+"]")
        fcti.close()

    def fillBalanced(self, noded, kids, options):
        tmpnnodes = options.nnodes - 1
        for i in range(options.depth+1):
            noded.append([])
            noded[i] = []
        for i in range(1,options.nnodes+1):
            kids.append([])
            kids[i] = []
        noded[0] = [1]
        tmpd = 0
        options.nary = 1
        while True:
            for i in noded[tmpd]:
                while len(kids[i]) < options.nary:
                    tmpnnodes -= 1
                    kids[i].append(options.nnodes-tmpnnodes)
                    noded[tmpd+1].append(options.nnodes-tmpnnodes)
                    if i == options.depth and tmpd == options.depth - 1:
                        self.mednodes.append(options.nnodes-tmpnnodes)
                    if tmpnnodes == 0:
                        return None
            tmpd = (tmpd+1) % options.depth
            if tmpd == 0:
                options.nary += 1

    def instance():
	global inst
	if inst is None:
	    inst = CtiGenerator()
	return inst

    instance = Callable(instance)


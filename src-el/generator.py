import os
from helper import *

class CtiGenerator:

    global inst
    inst = None

    def __init__(self):
        return None

    # Currently only generate N-ary Cti input files
    def run(self, options):
        if options.projectname is None:
            options.projectname = "foo"
        if not os.path.exists(options.outputdir):
            os.mkdir(options.outputdir)
        self.ofile = os.path.join(options.outputdir, options.projectname+"_"+options.nary.__str__()+"_"+options.depth.__str__()+".txt")
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
        fcti.write("articulation ar "+options.projectname)
        for i in range(1, (options.nary**(options.depth+1) - 1)/(options.nary-1)+1):
            fcti.write("\n[1."+i.__str__()+" is_included_in 2."+i.__str__()+"]")
        
        fcti.close()

    def instance():
        global inst
        if inst is None:
            inst = CtiGenerator()
	return inst

    instance = Callable(instance)


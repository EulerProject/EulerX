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

import os
import random
import math
from helper import *
from relations import *

class CtiGenerator:
    
    inst = None
    
    def __init__(self):
        return None
    
    # Currently only generate N-ary Cti input files
    def run(self, args):
        self.mednodes = []
        projectname = "foo"
        if args.outputdir is None:
            args.outputdir = "./"
        if not os.path.exists(args.outputdir):
            os.mkdir(args.outputdir)
            
        # Create a complete n-nary tree
        if args.nary != 0:
            self.ofile = os.path.join(args.outputdir, projectname+"_n"+args.nary.__str__()+"_"+args.depth.__str__()+".txt")
            fcti = open(self.ofile, 'w')
            for i in range(1,3):
                fcti.write("taxonomy "+i.__str__()+" T"+i.__str__()+"\n")
                for j in range(args.depth):
                    slfidx =  int((args.nary ** j - 1) / (args.nary - 1)) + 1
                    kididx =  int((args.nary ** (j+1) - 1) / (args.nary - 1)) + 1
                    for k in range(args.nary ** j):
                        fcti.write("("+slfidx.__str__())
                        for t in range(args.nary):
                            fcti.write(" "+kididx.__str__())
                            kididx += 1
                        fcti.write(")\n")
                        slfidx += 1
                fcti.write("\n")
            nnodes = (args.nary**(args.depth+1) - 1)/(args.nary-1)
            self.mednodes = range((args.nary**args.depth - 1)/(args.nary-1) + 1,
                        (args.nary**args.depth - 1)/(args.nary-1) + args.nary + 1)
        
        # Create a balanced tree
        elif args.nnodes != 0:
            if args.nnodes <= args.depth+1:
                print "Wrong input: -m should be larger than -d"
                return None
            self.ofile = os.path.join(args.outputdir, projectname+"_m"+args.nnodes.__str__()+"_"+args.depth.__str__()+".txt")
            fcti = open(self.ofile, 'w')
            noded = []
            kids = []
            kids.append([])
            self.fillBalanced(noded, kids, args)
#            if args.verbose:
#                print "Generating a balanced tree:"
#                for i in range(1,args.nnodes+1):
#                    print "Node",i,": list of kids",kids[i]
                    
            for i in range(1,3):
                fcti.write("taxonomy "+i.__str__()+" T"+i.__str__()+"\n")
                for j in range(args.depth):
                    for k in noded[j]:
                        fcti.write("("+k.__str__())
                        for t in kids[k]:
                            fcti.write(" "+t.__str__())
                        fcti.write(")\n")
                fcti.write("\n")
            nnodes = args.nnodes
                
        fcti.write("articulation ar "+projectname)
        if(not relation.has_key(args.relation) or args.relation == "no"):
            myrel = int(random.randint(0,4))
        else:
            myrel = int(math.log(relation[args.relation],2))
        # get rel string
        myrelstr = relstr[myrel]
        for i in range(1, nnodes+1):
            if args.incEx and i in self.mednodes:
                fcti.write("\n[1."+i.__str__()+" equals 2."+i.__str__()+"]")
            else:
                fcti.write("\n[1."+i.__str__()+" "+myrelstr+" 2."+i.__str__()+"]")
        fcti.close()
        
    def fillBalanced(self, noded, kids, args):
        tmpnnodes = args.nnodes - 1
        for i in range(args.depth+1):
            noded.append([])
            noded[i] = []
        for i in range(1,args.nnodes+1):
            kids.append([])
            kids[i] = []
        noded[0] = [1]
        tmpd = 0
        args.nary = 1
        while True:
            for i in noded[tmpd]:
                while len(kids[i]) < args.nary:
                    tmpnnodes -= 1
                    kids[i].append(args.nnodes-tmpnnodes)
                    noded[tmpd+1].append(args.nnodes-tmpnnodes)
                    if i == args.depth and tmpd == args.depth - 1:
                        self.mednodes.append(args.nnodes-tmpnnodes)
                    if tmpnnodes == 0:
                        return None
            tmpd = (tmpd+1) % args.depth
            if tmpd == 0:
                args.nary += 1
    
    @Callable
    def instance():
        if CtiGenerator.inst is None:
            CtiGenerator.inst = CtiGenerator()
        return CtiGenerator.inst

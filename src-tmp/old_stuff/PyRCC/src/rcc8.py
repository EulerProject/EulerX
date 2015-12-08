#!/usr/bin/env python

#############################################################################
####                                                                     ####
####    RCC8 Reasoner ( v1.2.2 - July 2012 )                             ####
####                                                                     ####
####    Michael Sioutis                                                  ####
####    e-mail: sioutis@di.uoa.gr                                        ####
####                                                                     ####
####                        http://www.di.uoa.gr/                        ####
####                                                                     ####
####           National and Kapodistrian University of Athens            ####
####          Department of Informatics and Telecommunications           ####
####                      Panepistimiopolis, Ilisia                      ####
####                            Athens, 157 84                           ####
####                                                                     ####
#############################################################################

from glob import setGlobals
from bitcoding import EQ, DALL
from iconsistency import iconsistency
from consistency import consistency
from assignment import staticUnassignedVars
from parsecsp import parsecsp
from optparse import OptionParser
from printm import printMatrix
import sys
from array import array
from counters import conCount, arcCount, nodeCount

def init():
   # create spatial variables of specified number
   temp = sys.stdin.readline()
   Vars = int(temp.split()[0].strip())+1
   TypeId = temp.split()[1].strip()
   
   # initialize constraints
   ConMatrix = tuple([array('B',[DALL if i != j else EQ for i in xrange(Vars)]) for j in xrange(Vars)])
  
   # parse spatial CSP
   parsecsp(ConMatrix)

   return TypeId, ConMatrix

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

# main function
def main(argv=None):

   if argv is None:
        argv = sys.argv

   # set some sys useful stuff
   sys.setrecursionlimit(1<<30)
   sys.setcheckinterval(10000)

   # initialize parser for command line arguments
   parser = OptionParser()
   
   # set parsing options
   parser.add_option("-m", "--method", type="string", dest="method", default="recursive", help="interaction mode: recursive, or iterative [default: %default]")
   parser.add_option("-v", "--varheuristic", type="string", dest="varheuristic", default="cardinality", help="interaction mode: none, cardinality, or random [default: %default]")
   parser.add_option("-p", "--pcheuristic", type="string", dest="pcheuristic", default="weighted", help="interaction mode: none, weighted, or smart [default: %default]")
   parser.add_option("-s", "--split", type="string", dest="split", default="horn", help="interaction mode: base, or horn [default: %default]")
   parser.add_option("-l", "--valheuristic", type="string", dest="valheuristic", default="lcv", help="interaction mode: none, or lcv [default: %default]")
   parser.add_option("-r", "--process", type="string", dest="process", default="dynamic", help="interaction mode: static, or dynamic [default: %default]")
   parser.add_option("-o", "--scope", type="string", dest="scope", default="local", help="interaction mode: local, or global [default: %default]")
   parser.add_option("-d", "--print", action="store_true", dest="printsol", help="print solution to output")

   # parse command line arguments
   options, args = parser.parse_args()

   try:
      TypeId, ConMatrix = init()

      # check and set globals for spliting information
      if options.split == "base":
         setGlobals('split',0)
      elif options.split == "horn":
         setGlobals('split',1)
      else:
         raise Usage("Invalid option: " + options.split)

      # check and set globals for patch consistency heuristic information
      if options.pcheuristic == "none":
         setGlobals('pcheuristic',0)
      elif options.pcheuristic == "weighted":
         setGlobals('pcheuristic',1)
      elif options.pcheuristic == "smart":
         setGlobals('pcheuristic',2)
      else:
         raise Usage("Invalid option: " + options.pcheuristic)

      # check and set globals for value decision heuristic information
      if options.valheuristic == "none":
         setGlobals('valheuristic',0)
      elif options.valheuristic == "lcv":
         setGlobals('valheuristic',1)
      else:
         raise Usage("Invalid option: " + options.valheuristic)

      # check and set globals for variable decision information
      if options.varheuristic == "none":
         setGlobals('varheuristic',0)
      elif options.varheuristic == "cardinality":
         setGlobals('varheuristic',1)
      elif options.varheuristic == "random":
         setGlobals('varheuristic',2)
      else:
         raise Usage("Invalid option: " + options.varheuristic)

      # check and set globals for scope information
      if options.scope == "local":
         setGlobals('scope',0)
      elif options.scope == "global":
         setGlobals('scope',1)
      else:
         raise Usage("Invalid option: " + options.scope)

      # check and set globals for processing information
   
      if options.process == "static":
         setGlobals('process',0)
         staticUnassignedVars(ConMatrix)
      elif options.process == "dynamic":
         setGlobals('process',1)
      else:
         raise Usage("Invalid option: " + options.process)

      # check and set globals for method decision information
      if options.method == "recursive":
         solution = consistency(ConMatrix)     
      elif options.method == "iterative": 
         solution = iconsistency(ConMatrix)   
      else:
         raise Usage("Invalid option: " + options.method)

   except Usage, err:
        print err.msg
        parser.print_help()
        return 1

   # print values of complexity counters
   print '--------------------------------------'
   print 'Type ID: ', TypeId
   print '--------------------------------------'
   print 'Visited nodes: ', next(nodeCount)
   print 'Visited arcs: ', next(arcCount)
   print 'Checked constraints: ', next(conCount)
   print '--------------------------------------'
  
   # print solution  
   if solution != None:
      print 'Consistent'
      if options.printsol == True:
         printMatrix(solution)
   else:
      print 'Inconsistent'
   print '--------------------------------------'

if __name__ == '__main__':
   sys.exit(main())


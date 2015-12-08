from helpfuncs import bitdecoding
from random import shuffle, random, randint
from baserels import B
from glob import globs
from hornsplit import hsplit
from basesplit import bsplit
from vbweights import w
from weights import ew

stL = [] # declare static list for unassigned variables

# calculate average serum of weights for the neighborhood of a specified arc
def neighborCons(ConMatrix, i, j):
   nw = 0
   count = 1
   for k in xrange(len(ConMatrix)):
      if k != i and k != j: # for all k,i,j and i,j,k triplets
         count += 1
         nw += ew[(ConMatrix[k][i] if k < i else ConMatrix[i][k])-1]
         nw += ew[(ConMatrix[j][k] if j < k else ConMatrix[k][j])-1]

   return float(nw)/count*2.0

# static evaluation of constrainedness
def staticUnassignedVars(Matrix):

   global stL
 
   # check variable decision heuristic to be used 
   if globs['varheuristic'] == 0: # none
      # check for splitting to be used
      if globs['split'] == 0: # splitting based on set of base relations
         stL.extend(sorted([(0,(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))

      elif globs['split'] == 1: # splitting based on horn set
         stL.extend(sorted([(0,(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))

   elif globs['varheuristic'] == 1: # cardinality
      # check for splitting to be used
      if globs['split'] == 0: # splitting based on set of base relations
         # check for scope of constrainedness
         if globs['scope'] == 0: # local scope
            stL.extend(sorted([(16*len(bsplit[Matrix[i][j]-1][1]) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))
         elif globs['scope'] == 1: #global scope
            stL.extend(sorted([(neighborCons(Matrix, i, j) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))

      elif globs['split'] == 1: # splitting based on horn set
         # check for scope of constrainedness
         if globs['scope'] == 0: # local scope
            stL.extend(sorted([(16*len(hsplit[Matrix[i][j]-1][1]) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))
         elif globs['scope'] == 1: #global scope           
            stL.extend(sorted([(neighborCons(Matrix, i, j) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))]))

   elif globs['varheuristic'] == 2: # random
      # check for splitting to be used
      if globs['split'] == 0: # splitting based on set of base relations
         stL.extend([(0,(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))])
         shuffle(stL)

      elif globs['split'] == 1: # splitting based on horn set
         stL.extend([(0,(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix))])
         shuffle(stL)
  
# dynamic evaluation of constrainedness
def dynamicUnassignedVars(Matrix):

   # check variable decision heuristic to be used 
   if globs['varheuristic'] == 0: # none
      return findUnassignVar(Matrix)

   elif globs['varheuristic'] == 1: # cardinality
      return findUnassignVarCH(Matrix)

   elif globs['varheuristic'] == 2: # random
      return findUnassignVarR(Matrix)

# find first unassigned variable
def findUnassignVar(ConMatrix):
 
   for i in xrange(len(ConMatrix)):
       for j in xrange(i+1,len(ConMatrix)):
    
           # check for splitting to be used
           if globs['split'] == 0: # splitting based on set of base relations
              if bsplit[ConMatrix[i][j]-1][0] > 1:  
                 return 0, (i, j)

           elif globs['split'] == 1: # splitting based on horn set
              if hsplit[ConMatrix[i][j]-1][0] > 1:  
                 return 0, (i, j)

   return None

# find first unassigned variable using cardinality heuristic
def findUnassignVarCH(ConMatrix):
   l = findAllUnAssignVarCH(ConMatrix)

   if l: 
      return min(l)
        
   return None

# find first random unassigned variable using cardinality heuristic
def findUnassignVarR(ConMatrix):
   l = findAllUnAssignVarR(ConMatrix)
 
   if l:
      (i,j) = l.pop()
      return 0, (i,j)
        
   return None

# Find all unassigned variables sorted by their cardinality
def findAllUnAssignVarCH(Matrix):

   # check for splitting to be used
   if globs['split'] == 0: # splitting based on set of base relations
      # check for scope of constrainedness
      if globs['scope'] == 0: # local
         l = [(16*len(bsplit[Matrix[i][j]-1][1]) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if bsplit[Matrix[i][j]-1][0] > 1]
      if globs['scope'] == 1: # global
         l = [(neighborCons(Matrix, i, j) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if bsplit[Matrix[i][j]-1][0] > 1]
   
   elif globs['split'] == 1: # splitting based on horn set
      # check for scope of constrainedness
      if globs['scope'] == 0: # local
         l = [(16*len(hsplit[Matrix[i][j]-1][1]) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if hsplit[Matrix[i][j]-1][0] > 1]
      if globs['scope'] == 1: # global
         l = [(neighborCons(Matrix, i, j) + ew[Matrix[i][j]-1],(i,j)) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if hsplit[Matrix[i][j]-1][0] > 1]

   #l.sort(reverse=True) # reverse the list to pop smallest item - poppleft could also be used
   return l

# Find all unassigned variables (randomly) sorted
def findAllUnAssignVarR(Matrix):
 
   # check for splitting to be used
   if globs['split'] == 0: # splitting based on set of base relations
      l = [(i,j) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if bsplit[Matrix[i][j]-1][0] > 1] 
   elif globs['split'] == 1: # splitting based on horn set
      l = [(i,j) for i in xrange(len(Matrix)) for j in xrange(i+1,len(Matrix)) if hsplit[Matrix[i][j]-1][0] > 1] 

   shuffle(l)   

   return l


               


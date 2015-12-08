from pc import PC
from pcw import PCw
from pcew import PCew 
from assignment import dynamicUnassignedVars, stL
from inverse import inv
from hornsplit import hsplit
from basesplit import bsplit
from glob import globs
from weights import ew
from counters import nodeCount

pc_alg = {0:PC,1:PCw,2:PCew}

# backtracking consistency
def consistency(ConMatrix, m = -1, n = -1):  

   next(nodeCount) # increment visited nodes counter

   # check for path consistency to be used 
   if not pc_alg[globs['pcheuristic']](ConMatrix,m,n):
      return None
   
   # check for processing to be used
   if globs['process'] == 1: # dynamic processing
      res = dynamicUnassignedVars(ConMatrix)
      
      if not res:
         return ConMatrix # solution found

      dummy, (i,j) = res # grab unassigned variable

   elif globs['process'] == 0: # static processing
      
      # check for splitting to be used
         if globs['split'] == 0: # splitting based on set of base relations
            for dummy, (i,j) in stL:
               if bsplit[ConMatrix[i][j]-1][0] > 1:
                  break
            else:
               return ConMatrix # solution found
         elif globs['split'] == 1: # splitting based on horn set
            for dummy, (i,j) in stL:
               if hsplit[ConMatrix[i][j]-1][0] > 1:
                  break
            else:
               return ConMatrix # solution found

   # check for splitting to be used
   if globs['split'] == 0: # splitting based on set of base relations
      d = bsplit[ConMatrix[i][j]-1][1]
   elif globs['split'] == 1: # splitting based on horn set
      d = hsplit[ConMatrix[i][j]-1][1]
   
   # check for value decision heuristic to be used
   if globs['valheuristic'] == 0: # non heuristic
      dw = d
   elif globs['valheuristic'] == 1: # least constraining value heuristic
      dw = [(-ew[a-1],a) for a in d]
      dw.sort()
      dw = [a[1] for a in dw]

   # as long as a consistent variable-value pair in not found, search for it
   for v in dw:
       # assignment takes place
       ConMatrix[i][j] = v
       ConMatrix[j][i] = inv[v-1]
       result = consistency(tuple([ic[:] for ic in ConMatrix]), i, j) # keep copy of the constraint matrix in case an inconsistency happens
       if (result != None):
          return result

   return None # no solution found

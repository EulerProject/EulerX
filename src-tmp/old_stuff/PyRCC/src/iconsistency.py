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

# iterative consistency
def iconsistency(ConMatrix, m = -1, n = -1):
   
   stack = [] # initialize stack to simulate backtracking

   next(nodeCount)
   
   # check for path consistency to be used for first step
   if globs['pcheuristic'] == 0: # simple path consistency
      if not PC(ConMatrix, m, n): 
         return None   
   elif globs['pcheuristic'] == 2: # exact weighted path consistency
      if not PCew(ConMatrix, m, n): 
         return None
   elif globs['pcheuristic'] == 1: # van Beek weighted path consistency
      if not PCw(ConMatrix, m, n): 
         return None

   # as long as the consistency problem is not decided, process it
   while 1:
 
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
         values = bsplit[ConMatrix[i][j]-1][1][:]
      elif globs['split'] == 1: # splitting based on horn set
         values = hsplit[ConMatrix[i][j]-1][1][:]

      # check for value decision heuristic to be used
      if globs['valheuristic'] == 0: # non heuristic
         valuesw = values
         valuesw.reverse()
      elif globs['valheuristic'] == 1: # least constraining value heuristic
         valuesw = [(-ew[a-1],a) for a in values]
         valuesw.sort(reverse=True)
         valuesw = [a[1] for a in valuesw]
     
      # as long as a consistent variable-value pair in not found, search for it
      while 1:

         next(nodeCount) # increment visited nodes counter
 
         # check if current variable has any variables left, if not backtrack to a previous variable assignment
         if not valuesw:
            # check if any previous variable assignments are left in the stack
            while stack:
               ConMatrix, (i, j), valuesw, dummy = stack.pop()
               # check if newly grabbed variable has any variables left, if not backtrack to a previous variable assignment
               if valuesw: 
                  break
            else:
              return None
               
         value = valuesw.pop() # grab first value from variable
         
         c = tuple([ic[:] for ic in ConMatrix]) if valuesw else () # keep copy of the constraint matrix in case an inconsistency happens

         # assignment takes place
         ConMatrix[i][j] = value
         ConMatrix[j][i] = inv[value-1]
            
         # check for path consistency to be used 
         if globs['pcheuristic'] == 0: # simple path consistency
            if PC(ConMatrix, i, j):   
               break 
         elif globs['pcheuristic'] == 2: # exact weighted path consistency
            if PCew(ConMatrix, i, j): 
               break
         elif globs['pcheuristic'] == 1: # van Beek weighted path consistency
            if PCw(ConMatrix, i, j): 
               break

         ConMatrix = c # revert contraint mantrix to previous state
  
      stack.append((c, (i, j), valuesw[:], dummy)) # save current state (function call) in a stack
     
   raise RuntimeError, "Can't happen"

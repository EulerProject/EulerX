from comptab import fcomp
from bitcoding import DALL
from inverse import inv
from conjunction import l_and
from collections import deque
from counters import arcCount, conCount

# path consistency using van Beek weights
def PC(ConMatrix, m = -1, n = -1):
   pq = deque([])                         # list of entries arranged in a heap
   entry_finder = set([])               # mapping of tasks to entries
   Vars = len(ConMatrix)

   def add_task(task):
       'Add a new task or update the priority of an existing task'
       if task not in entry_finder:
          entry_finder.add(task)
          pq.append(task)
          
   def pop_task():
       'Remove and return the lowest priority task. Raise KeyError if empty.'
       task = pq.popleft()
       entry_finder.discard(task)
       return task

   # check if it is the first time the path consistency is ever ran, thus, all useful arcs should be taken into account
   if m == -1 and n == -1:
      # initialize queue
      map(add_task,[(i,j) for i in xrange(Vars) for j in xrange(i+1,Vars) if ConMatrix[i][j] != DALL])
   else:
      add_task((m,n))


   # as long as the queue is not empty, process it
   while pq:

      (i,j) = pop_task() # grab the appropriate relation
      
      next(arcCount) # increment visited arcs counter 
  
      # create all triplets to be checked for path consistency
      for k in xrange(Vars):
          if (ConMatrix[k][i] != DALL) and i != k != j:

             next(conCount) # increment checked constraints counter
  
             # constrain arc (k,i,j)
             temp = fcomp[ConMatrix[k][i]-1][ConMatrix[i][j]-1]
             if temp != DALL:
                if k < j:
                   temp = l_and[temp-1][ConMatrix[k][j]-1]
                   if temp != ConMatrix[k][j]:
                      if not temp: 
                         return False # inconsistency
                      ConMatrix[k][j] = temp
                      ConMatrix[j][k] = inv[temp-1]
                      add_task((k, j))
                else:
                   temp = l_and[inv[temp-1]-1][ConMatrix[j][k]-1]
                   if temp != ConMatrix[j][k]:
                      if not temp: 
                         return False # inconsistency
                      ConMatrix[j][k] = temp
                      ConMatrix[k][j] = inv[temp-1]
                      add_task((j, k))

          if (ConMatrix[j][k] != DALL) and i != k != j:

             next(conCount) # increment checked constraints counter
          
             # constrain arc (i,j,k)
             temp = fcomp[ConMatrix[i][j]-1][ConMatrix[j][k]-1]
             if temp != DALL:
                if i < k:  
                   temp = l_and[temp-1][ConMatrix[i][k]-1] 
                   if temp != ConMatrix[i][k]:
                      if not temp: 
                         return False # inconsistency
                      ConMatrix[i][k] = temp
                      ConMatrix[k][i] = inv[temp-1]
                      add_task((i, k))
                else:   
                   temp = l_and[inv[temp-1]-1][ConMatrix[k][i]-1]  
                   if temp != ConMatrix[k][i]:
                      if not temp: 
                          return False # inconsistency
                      ConMatrix[k][i] = temp
                      ConMatrix[i][k] = inv[temp-1]
                      add_task((k, i))

   # the network is concistent and can't be refined further
   return True    

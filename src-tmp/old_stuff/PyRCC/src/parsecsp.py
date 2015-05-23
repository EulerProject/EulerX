import sys
from helpfuncs import translateR
from inverse import inv

# parse spatial CSP and fill in the constraint matrix
def parsecsp(ConMatrix):
   
   while True:
      
      # assure not interrupted parsing 
      try:
         line = sys.stdin.readline()
      except KeyboardInterrupt:
         break

      if not line:
         break

      l = line.strip().replace('(','').replace(')','').split()
      # condition to end parsing
      if l == ['.']:
         break
 
      s = reduce(lambda x, y: x | y, [translateR(i) for i in l[2:]])
      ConMatrix[int(l[0])][int(l[1])] = s
      ConMatrix[int(l[1])][int(l[0])] = inv[s-1]
    



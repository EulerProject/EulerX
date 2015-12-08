from bitcoding import DC, EC, PO, TPP, NTPP, TPPI, NTPPI, EQ
from basesplit import bsplit
from baserels import B

# initializing van Beek weights
w = [None for i in xrange(255)]

# van Beek weights for base relations
w[DC-1] = 4
w[EC-1] = 3
w[PO-1] = 5
w[TPP-1] = 2
w[NTPP-1] = 2
w[TPPI-1] = 2
w[NTPPI-1] = 2
w[EQ-1] = 1

# calculate van Beek weights for non base relations 
def relWeight(r):

   l = bsplit[r-1][1]
   
   return sum([w[i-1] for i in l])

# setting van Beek weights for non base relations
for i in xrange(255):
   if (i+1 not in B):
      w[i] = relWeight(i+1)




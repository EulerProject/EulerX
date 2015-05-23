from bitcoding import DC, EC, PO, TPP, NTPP, TPPI, NTPPI, EQ, DALL
from baserels import B

# translate a base relation from integer to its string representation
def translate(BR):

    if BR == DC:
       return 'DC'
    if BR == EC:
       return 'EC'
    if BR == PO:
       return 'PO'
    if BR == TPP:
       return 'TPP'
    if BR == TPPI:
       return 'TPPI'
    if BR == NTPP:
       return 'NTPP'
    if BR == NTPPI:
       return 'NTPPI'
    if BR == EQ:
       return 'EQ'

# translate a base relation from its string representation to integer
def translateR(BR):

    if BR == 'DC':
       return DC
    if BR == 'EC':
       return EC
    if BR == 'PO':
       return PO
    if BR == 'TPP':
       return TPP
    if BR == 'TPPI':
       return TPPI
    if BR == 'NTPP':
       return NTPP
    if BR == 'NTPPI':
       return NTPPI
    if BR == 'EQ':
       return EQ

# compute the inverse of a base relation
def inverseL(L):

   return ((DC if L&DC else 0) | (EC if L&EC else 0) | (PO if L&PO else 0) | (TPPI if L&TPP else 0) | (TPP if L&TPPI else 0) | (NTPPI if L&NTPP else 0) | (NTPP if L&NTPPI else 0) | (EQ if L&EQ else 0))

# split a relation into its base relation representation
def bitdecoding(b):
   l = []

   if b in B: return [b]

   if b == DALL: return B[:]

   l = [i for i in B if b&i != 0 and i <=b]

   return l

# copy a matrix
def copyMatrix(Matrix):
   temp = []
   for i in xrange(len(Matrix)):
       temp.append([])
       for j in xrange(len(Matrix)):
           temp[i].append(Matrix[i][j])

   return temp


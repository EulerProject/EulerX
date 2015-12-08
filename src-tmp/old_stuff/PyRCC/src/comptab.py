from bitcoding import DC, EC, PO, TPP, NTPP, TPPI, NTPPI, EQ, DALL
from basesplit import bsplit
from baserels import B
from inverse import inv

# calculate composition between two relations
def calcComp(l,u):

   comp = 0   

   a = bsplit[l-1][1]
   b = bsplit[u-1][1]
   
   for i in a:
      for j in b:
         comp |= fcomp[i-1][j-1]
         if comp == DALL: return DALL # stop calculating if the global relation

   return comp      

# initialize matrix to hold compositions between all 256 possible relations
fcomp = [[None for i in xrange(255)] for j in xrange(255)]
  
# DC
fcomp[DC-1][DC-1] = DALL
fcomp[DC-1][EC-1] = (DC|EC|PO|TPP|NTPP)   
fcomp[DC-1][PO-1] = (DC|EC|PO|TPP|NTPP)
fcomp[DC-1][TPP-1] = (DC|EC|PO|TPP|NTPP)
fcomp[DC-1][NTPP-1] = (DC|EC|PO|TPP|NTPP)
fcomp[DC-1][TPPI-1] = DC
fcomp[DC-1][NTPPI-1] = DC
fcomp[DC-1][EQ-1] = DC

# EC    
fcomp[EC-1][DC-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[EC-1][EC-1] = (DC|EC|PO|TPP|TPPI|EQ)
fcomp[EC-1][PO-1] = (DC|EC|PO|TPP|NTPP)
fcomp[EC-1][TPP-1] = (EC|PO|TPP|NTPP)
fcomp[EC-1][NTPP-1] = (PO|TPP|NTPP)
fcomp[EC-1][TPPI-1] = (DC|EC)
fcomp[EC-1][NTPPI-1] = DC
fcomp[EC-1][EQ-1] = EC

# PO
fcomp[PO-1][DC-1] = (DC|EC|PO|TPPI|NTPPI) 
fcomp[PO-1][EC-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[PO-1][PO-1] = DALL
fcomp[PO-1][TPP-1] = (PO|TPP|NTPP)
fcomp[PO-1][NTPP-1] = (PO|TPP|NTPP)
fcomp[PO-1][TPPI-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[PO-1][NTPPI-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[PO-1][EQ-1] = PO
  
# TPP
fcomp[TPP-1][DC-1] = DC
fcomp[TPP-1][EC-1] = (DC|EC)
fcomp[TPP-1][PO-1] = (DC|EC|PO|TPP|NTPP)
fcomp[TPP-1][TPP-1] = (TPP|NTPP)  
fcomp[TPP-1][NTPP-1] = NTPP  
fcomp[TPP-1][TPPI-1] = (DC|EC|PO|TPP|TPPI|EQ)
fcomp[TPP-1][NTPPI-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[TPP-1][EQ-1] = TPP
  
# NTPP
fcomp[NTPP-1][DC-1] = DC
fcomp[NTPP-1][EC-1] = DC
fcomp[NTPP-1][PO-1] = (DC|EC|PO|TPP|NTPP)
fcomp[NTPP-1][TPP-1] = NTPP
fcomp[NTPP-1][NTPP-1] = NTPP
fcomp[NTPP-1][TPPI-1] = (DC|EC|PO|TPP|NTPP)
fcomp[NTPP-1][NTPPI-1] = DALL
fcomp[NTPP-1][EQ-1] = NTPP
  
# TPPI
fcomp[TPPI-1][DC-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[TPPI-1][EC-1] = (EC|PO|TPPI|NTPPI)
fcomp[TPPI-1][PO-1] = (PO|TPPI|NTPPI)
fcomp[TPPI-1][TPP-1] = (PO|TPP|TPPI|EQ)
fcomp[TPPI-1][NTPP-1] = (PO|TPP|NTPP)
fcomp[TPPI-1][TPPI-1] = (TPPI|NTPPI)
fcomp[TPPI-1][NTPPI-1] = NTPPI
fcomp[TPPI-1][EQ-1] = TPPI
  
# NTPPI
fcomp[NTPPI-1][DC-1] = (DC|EC|PO|TPPI|NTPPI)
fcomp[NTPPI-1][EC-1] = (PO|TPPI|NTPPI)   
fcomp[NTPPI-1][PO-1] = (PO|TPPI|NTPPI)
fcomp[NTPPI-1][TPP-1] = (PO|TPPI|NTPPI)
fcomp[NTPPI-1][NTPP-1] = (PO|TPP|TPPI|NTPP|NTPPI|EQ)
fcomp[NTPPI-1][TPPI-1] = NTPPI
fcomp[NTPPI-1][NTPPI-1] = NTPPI
fcomp[NTPPI-1][EQ-1] = NTPPI

# EQ
fcomp[EQ-1][DC-1] = DC
fcomp[EQ-1][EC-1] = EC
fcomp[EQ-1][PO-1] = PO
fcomp[EQ-1][TPP-1] = TPP
fcomp[EQ-1][NTPP-1] = NTPP
fcomp[EQ-1][TPPI-1] = TPPI   
fcomp[EQ-1][NTPPI-1] = NTPPI
fcomp[EQ-1][EQ-1] = EQ

# finalize matrix with non base relation compositions
for i in xrange(255):
   for j in xrange(255):
      if (i+1 not in B) or (j+1 not in B):
         fcomp[i][j] = calcComp(i+1, j+1)



from basesplit import bsplit
from helpfuncs import translate

# print matrix with relations split into base relations
def printMatrix(Matrix):

   for i in xrange(len(Matrix)):
       for j in xrange(i+1,len(Matrix)):
           print i, j, [translate(p) for p in bsplit[Matrix[i][j]-1][1]]


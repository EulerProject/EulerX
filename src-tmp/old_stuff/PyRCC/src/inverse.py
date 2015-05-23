from helpfuncs import inverseL

# initialize list with the inverses of all 256 possible relations
inv = [inverseL(i+1) for i in range(255)]

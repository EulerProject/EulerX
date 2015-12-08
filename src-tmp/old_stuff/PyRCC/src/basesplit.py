from helpfuncs import bitdecoding

# initialize and fill list for set based on base relations
bsplit = [(len(bitdecoding(i+1)),bitdecoding(i+1)) for i in xrange(255)]


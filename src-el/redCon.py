import re
from relations import *
from helper import *

class RedCon():
    def __init__(self, pair, mir):
	self.returnValue = {}
        for i in range(5):
	    self.returnValue[i] = 0
        taxa = re.match("(.*),(.*)", pair)
	print "What is the relation between "+taxa.group(1)+" and "\
              +taxa.group(2)+"?"
        
        j = 0
	for i in range(5):
	    if mir & (1 << i):
              print j,'.',relstr[i]
              self.returnValue[j] = 1 << i
              j += 1
        val = raw_input("(Choose those possible ones, e.g. 0 or 1 or 0,1)?\n")
        ans = re.split(',', val.replace(' ', ''))
        for i in range(j):
            if i.__str__() not in ans:
              self.returnValue[i] = 0 

    def main(self):
        val = 0
        for i in range(5):
            val |= self.returnValue[i]
        return val

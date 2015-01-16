# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
from relations import *
from helper import *

class RedCon():
    def __init__(self, pair, mir):
        self.returnValue = {}
        for i in range(5):
            self.returnValue[i] = 0
        taxa = re.match("(.*),(.*)", pair)
        print "What is the relation between "+taxa.group(1)+" and "+taxa.group(2)+"?"
        
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

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

def decompose(inputfile, outputfile):
    lines = []
    count = 0
    
    fIn = open(inputfile, "r")
    fOut = open(outputfile, "w")
    lines = fIn.readlines()
    
    for line in lines:
        # reads in lines of the form (a b c) where a is the parent
        # and b c are the children
        if (re.match("\(.*\)", line)):
            ttList = []
            line = line.replace('(','').replace(')','').strip()
            concepts = line.split()
            
            if len(concepts) == 1 or len(concepts) == 2:
                ttList.append(concepts)
            
            while len(concepts) > 3:
                newConcepts = []
                newConcepts.append(concepts[0])
                
                for i in range(1, len(concepts)-1, 2):
                    tmp = []
                    newFakeNode = "fake" + str(count)
                    count = count + 1
                    tmp.append(newFakeNode)
                    tmp.append(concepts[i])
                    tmp.append(concepts[i+1])
                    ttList.append(tmp)
                    newConcepts.append(newFakeNode)
                
                # still one concept left
                if i == len(concepts) - 3:
                    newConcepts.append(concepts[i+2])
                
                concepts = newConcepts
            
            if len(concepts) == 3:
                ttList.append(concepts)
                
            for tt in ttList:
                fOut.write('(')
                fOut.write(' '.join(tt))
                fOut.write(')\n')
        
        else:
            fOut.write(line)
                
    return True
    
# def main():
#     decompose("decompose.txt", "output.txt")
# 
# if __name__ == '__main__':
#     main()
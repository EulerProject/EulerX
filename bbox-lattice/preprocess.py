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

from subprocess import call
import sys

fileName = sys.argv[1]
arts = []

f = open(fileName, "r")
lines = f.readlines()
for line in lines:
    if line[0] == "[":
        arts.append(line[1:-2])
f.close()

f = open("expWorlds.asp","w")
f.write("% Define the domain (universe of discourse): 1,2,...\n")
f.write("u(1.." + len(arts).__str__() + ").\n")
f.write("% every element is either in or out\n")
f.write("i(X) :- u(X), not o(X).\n")
f.write("o(X) :- u(X), not i(X).\n")
f.close()

com = "python powerset.py " + len(arts).__str__()
call(com, shell=True)

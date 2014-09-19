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

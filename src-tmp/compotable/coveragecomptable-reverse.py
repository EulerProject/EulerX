from itertools import chain, combinations
from sets import Set
#Coverage composition table:
#Given rel(A,B) ==> rel(a1,B), rel(a2,B)
#< ==> < , < 
#> ==> !<=>o , !<=>o
#= ==> < , <
#! ==> ! , !
#o ==> !<o , !<o

#Given rel(A,B) ==> rel(A,b1), rel(A,b2)
#< ==> !<=>o , !<=>o 
#> ==> > , >
#= ==> > , >
#! ==> ! , !
#o ==> !>o , !>o

#Given rel(A,B) ==> rel(a1,b1), rel(a1,b2), rel(a2,b1), rel(a2,b2)
#< ==> !<=>o , !<=>o , !<=>o , !<=>o 
#> ==> !<=>o , !<=>o , !<=>o , !<=>o
#= ==> !<=>o , !<=>o , !<=>o , !<=>o
#! ==> ! , ! , ! , !
#o ==> !<=>o , !<=>o , !<=>o , !<=>o


def hash_a1_B(r):
    if r == "<":
        return "<"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "<"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<o"

def hash_a2_B(r):
    if r == "<":
        return "<"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "<"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<o"

def hash_A_b1(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return ">"
    elif r == "=":
        return ">"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!>o"

def hash_A_b2(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return ">"
    elif r == "=":
        return ">"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!>o"

def hash_a1_b1(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "!<=>o"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<=>o"

def hash_a1_b2(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "!<=>o"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<=>o"

def hash_a2_b1(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "!<=>o"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<=>o"

def hash_a2_b2(r):
    if r == "<":
        return "!<=>o"
    elif r == ">":
        return "!<=>o"
    elif r == "=":
        return "!<=>o"
    elif r == "!":
        return "!"
    elif r == "o":
        return "!<=>o"

def powerset_generator(s):
    for subset in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)):
        yield set(subset)
        
base_AB = ["<",">","=","!","o"]
badguys = []
badguys.append(set("<>"))
badguys.append(set("!<>"))
badguys.append(set("=<>"))
badguys.append(set("!=<>"))

for s in powerset_generator(set(base_AB)):
#    print s
    str = ""
    for r in s:
        str = str + hash_a2_b2(r)
#    print set(str)
    if set(str) in badguys:
        print "FIND BAD GUY!!!"
#    print ""
    
from rccrelations import *

#def rcc5compTab(r1, r2):
#    if r1 == rcc["<"] and r2 == rcc["<"]: return rcc["<"]
#    if r1 == rcc["<"] and r2 == rcc[">"]: return rcc["!<=>o"]
#    if r1 == rcc["<"] and r2 == rcc["!"]: return rcc["!"]
#    if r1 == rcc["<"] and r2 == rcc["o"]: return rcc["!<o"]
#    if r1 == rcc["<"] and r2 == rcc["="]: return rcc["<"]
#
#    if r1 == rcc[">"] and r2 == rcc["<"]: return rcc["<=>o"]
#    if r1 == rcc[">"] and r2 == rcc[">"]: return rcc[">"]
#    if r1 == rcc[">"] and r2 == rcc["!"]: return rcc["!>o"]
#    if r1 == rcc[">"] and r2 == rcc["o"]: return rcc[">o"]
#    if r1 == rcc[">"] and r2 == rcc["="]: return rcc[">"]
#
#    if r1 == rcc["!"] and r2 == rcc["<"]: return rcc["!<o"]
#    if r1 == rcc["!"] and r2 == rcc[">"]: return rcc["!"]
#    if r1 == rcc["!"] and r2 == rcc["!"]: return rcc["!<=>o"]
#    if r1 == rcc["!"] and r2 == rcc["o"]: return rcc["!<o"]
#    if r1 == rcc["!"] and r2 == rcc["="]: return rcc["!"]
#
#    if r1 == rcc["o"] and r2 == rcc["<"]: return rcc["<o"]
#    if r1 == rcc["o"] and r2 == rcc[">"]: return rcc["!>o"]
#    if r1 == rcc["o"] and r2 == rcc["!"]: return rcc["!>o"]
#    if r1 == rcc["o"] and r2 == rcc["o"]: return rcc["!<=>o"]
#    if r1 == rcc["o"] and r2 == rcc["="]: return rcc["o"]
#
#    if r1 == rcc["="] and r2 == rcc["<"]: return rcc["<"]
#    if r1 == rcc["="] and r2 == rcc[">"]: return rcc[">"]
#    if r1 == rcc["="] and r2 == rcc["!"]: return rcc["!"]
#    if r1 == rcc["="] and r2 == rcc["o"]: return rcc["o"]
#    if r1 == rcc["="] and r2 == rcc["="]: return rcc["="]

def containsymb(rel, symb):
    return rel & symb
#    if symb == rcc["<"]: return rel & rcc["<"]
#    if symb == rcc[">"]: return rel & rcc[">"]
#    if symb == rcc["!"]: return rel & rcc["!"]
#    if symb == rcc["o"]: return rel & rcc["o"]
#    if symb == rcc["="]: return rel & rcc["="]        
    
def r32compTab(r1, r2):
    rel = 0
    if containsymb(r1, rcc["<"]) and containsymb(r2, rcc["<"]): rel = rel | rcc["<"]
    if containsymb(r1, rcc["<"]) and containsymb(r2, rcc[">"]): rel = rel | rcc["!<=>o"]
    if containsymb(r1, rcc["<"]) and containsymb(r2, rcc["!"]): rel = rel | rcc["!"]
    if containsymb(r1, rcc["<"]) and containsymb(r2, rcc["o"]): rel = rel | rcc["!<o"]
    if containsymb(r1, rcc["<"]) and containsymb(r2, rcc["="]): rel = rel | rcc["<"]
    
    if containsymb(r1, rcc[">"]) and containsymb(r2, rcc["<"]): rel = rel | rcc["<=>o"]
    if containsymb(r1, rcc[">"]) and containsymb(r2, rcc[">"]): rel = rel | rcc[">"]
    if containsymb(r1, rcc[">"]) and containsymb(r2, rcc["!"]): rel = rel | rcc["!>o"]
    if containsymb(r1, rcc[">"]) and containsymb(r2, rcc["o"]): rel = rel | rcc[">o"]
    if containsymb(r1, rcc[">"]) and containsymb(r2, rcc["="]): rel = rel | rcc[">"]
    
    if containsymb(r1, rcc["!"]) and containsymb(r2, rcc["<"]): rel = rel | rcc["!<o"]
    if containsymb(r1, rcc["!"]) and containsymb(r2, rcc[">"]): rel = rel | rcc["!"]
    if containsymb(r1, rcc["!"]) and containsymb(r2, rcc["!"]): rel = rel | rcc["!<=>o"]
    if containsymb(r1, rcc["!"]) and containsymb(r2, rcc["o"]): rel = rel | rcc["!<o"]
    if containsymb(r1, rcc["!"]) and containsymb(r2, rcc["="]): rel = rel | rcc["!"]
    
    if containsymb(r1, rcc["o"]) and containsymb(r2, rcc["<"]): rel = rel | rcc["<o"]
    if containsymb(r1, rcc["o"]) and containsymb(r2, rcc[">"]): rel = rel | rcc["!>o"]
    if containsymb(r1, rcc["o"]) and containsymb(r2, rcc["!"]): rel = rel | rcc["!>o"]
    if containsymb(r1, rcc["o"]) and containsymb(r2, rcc["o"]): rel = rel | rcc["!<=>o"]
    if containsymb(r1, rcc["o"]) and containsymb(r2, rcc["="]): rel = rel | rcc["o"]
    
    if containsymb(r1, rcc["="]) and containsymb(r2, rcc["<"]): rel = rel | rcc["<"]
    if containsymb(r1, rcc["="]) and containsymb(r2, rcc[">"]): rel = rel | rcc[">"]
    if containsymb(r1, rcc["="]) and containsymb(r2, rcc["!"]): rel = rel | rcc["!"]
    if containsymb(r1, rcc["="]) and containsymb(r2, rcc["o"]): rel = rel | rcc["o"]
    if containsymb(r1, rcc["="]) and containsymb(r2, rcc["="]): rel = rel | rcc["="]
    
    return rel
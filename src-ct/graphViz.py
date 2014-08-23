import os
import sys
import re
from config import *
from utility import *
def colors(i):
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    return colors[i]

def children(infilename):
    infile = open(infilename, "r")
    children = []
    for line in infile:
        if line[0] == "(":
            nodes = line[1:-2].split()
            children = children + nodes[1:]
    infile.close()
    return children

def relations(infilename):
    infile = open(infilename, "r")
    relations = ["isa"]
    for line in infile:
        if line[0] == "[":
            edges = line[1:-2].split()
            if edges[1] not in relations:
                relations = relations + [edges[1]]
    infile.close()
    return relations

def makeColor(theEdge, theColor):
    if (theEdge.find("color = ") != -1):
        regExp = re.compile('color = [\w]*')
        theEdge = regExp.sub('color = red', theEdge)
        #regExp = re.compile('fontcolor = [\w]*?')
        #theEdge = regExp.sub('fontcolor = red', theEdge)
    return theEdge
        
    
    
def main(infilename, outfilename):
    print "outfilename is " + outfilename
    infile = open(infilename, "r")
    outfile = open(outfilename, "w")
    #print relations(infilename)
    #relationships = input("List of relationships: ")
    relationships = ["equals","includes","is_included_in","disjoint","overlaps","isa"]
    outfile.write("digraph foo {\n\n")
    outfile.write("rankdir = TD\n\n")
    i = 0
    parents = []
    for line in infile:
        if line[0] == "t":
                
            words = line[:-1].split()
            outfile.write("subgraph cluster_" + words[1] + " {\n")
            outfile.write("node [color = " + colors(i) + ", style = filled]\n")
            i = i + 1
            if "isa" in relationships:
                outfile.write("edge [dir = back]\n")
            else:
                outfile.write("edge [style = invisible, arrowhead = none]\n")
        elif line[0] == "(":
            nodes = line[1:-2].split()
            if nodes[0] not in children(infilename):
                parents = parents + [nodes[0]] + [" "]
            linechildren = []
            for child in nodes[1:]:
                linechildren = linechildren + [child] + [" "]
            outfile.writelines([nodes[0]] + [" -> {"] + linechildren + ["}\n"])
            outfile.writelines(["{rank = same; "] + linechildren + ["}\n"])
                
        elif line[0] == "\n":
            outfile.write("}\n\n")
            
        elif line[0] == "a":
            words = line[:-1].split()
        elif (line[0] == "[" or line[0] == "*") and (line.find("{") == -1):
            edges = line[1:-2].split()
            node1 = edges[0].split("_")[1]
            node2 = edges[2].split("_")[1]
            thisEdge = ""
            if edges[1] == "equals":
                if "equals" in relationships:
                    thisEdge = node1 + " -> " + node2 + \
    " [dir = both, color = darkgreen, label = equals, fontcolor = darkgreen]\n"
            elif edges[1] == "includes":
                if "includes" in relationships:
                    thisEdge = node1 + " -> " + node2 + \
    " [color = darkviolet, label = includes, fontcolor = darkviolet]\n"
            elif edges[1] == "is_included_in":
                if "is_included_in" in relationships:
                    thisEdge = node1 + " -> " + node2 + \
    " [color = darkorange, label = is_included_in, fontcolor = darkorange]\n"
            elif edges[1] == "disjoint":
                if "disjoint" in relationships:
                    thisEdge = node1 + " -> " + node2 + \
    " [arrowhead = none, style = dashed, color = gold, \
    label = disjoint, fontcolor = gold]\n"
            elif edges[1] == "overlaps":
                if "overlaps" in relationships:
                    thisEdge = node1 + " -> " + node2 + \
    " [arrowhead = none, color = navy, label = overlaps, fontcolor = navy]\n"
            
            if line[0] == "*":
                thisEdge = makeColor(thisEdge, "red")
            outfile.write(thisEdge)
            #else:
                #print line
        #else:
            #print line
    outfile.writelines(["{rank = same; "] + parents + ["}\n"])
    keys = {"isa" : ": black", "equals" : ": darkgreen", \
    "includes" : ": darkviolet", "is_included_in" : ": darkorange", \
    "disjoint" : ": gold", "overlaps" : ":navy"}
    labels = []
    for relationship in relationships:
        labels = labels + ["\\n" + relationship + keys[relationship]]
    #outfile.writelines(["graph [label = \""] + labels + ["\"]"])
    outfile.write("\n}\n")
    infile.close()
    outfile.close()

    directory = os.getcwd()
    # os.chdir("C:\Documents and Settings\Owner\Desktop")
    #outfiledirectory = raw_input("Directory of dotfile: ")
    #os.chdir(outfiledirectory)
    #outfile,graphfile,errorfile=os.popen3("dot -Tgif -o graph.gif "+outfilename)
    if (not(os.path.exists(directory + "/output/figures/"))):
        os.mkdir(directory + "/output/figures/")
    os.chdir(directory + "/output/figures/")
    graphFile = getNameFromFile(outfilename)[:-3] + ".gif"
    one,two,three = os.popen3("dot -Tgif -o " + quoteSpacesInPath(graphFile) + " " + quoteSpacesInPath(outfilename))
    #print errorfile
    #graph = os.popen("graph.gif")
    os.chdir(directory)



def makeGraph(infilename):
        outfilename = infilename[:-4]+"_out.txt"
	print outfilename
        main(infilename, outfilename)       

if __name__ == "__main__":
    if(len(sys.argv) == 2):
	makeGraph(sys.argv[1])
    else:
	main(sys.argv[1], sys.argv[2])
         
#more = True
#while more:
#    infilename = raw_input("Infilename? ")
#    outfilename = infilename[:-4] + "out.txt"
#    main()
#    response = raw_input("See another graph? (y or n) ")
#    if response == "n":
#        more = False

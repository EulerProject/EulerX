#=============================================================================================
# Main program: Read from CleanTax/EulerDLV input file; Generate .dot file for visualization
# Black: First Taxonomy
# Blue: Second Taxonomy
# Solid arrow: parent-child relation
# Dashed arrow: articulation relation
#=============================================================================================
import sys
import os
from helper import *

class InputVisual:
    
    inst = None
    
    def __init__(self):
        return None
    
    def instance():
        return InputVisual()
    
    instance = Callable(instance)
    
    #remove the duplicate string in list li
    def remove_duplicate_string(self,li):
        if li:
            li.sort()
            last = li[-1]
            for i in range(len(li)-2, -1, -1):
                if last == li[i]:
                    del li[i]
                else:
                    last = li[i]
    
    def run(self, inputdir, inputfile, ivout):
        # open the file
        f_in = open(os.path.join(inputdir,inputfile), 'r')
        f_out = open(ivout, 'w')
    
        # initialize variables
        not_EOF = True
        pc_list1 = []
        pc_list2 = []
        art_list = []
    
        # read each line of the file and update list
        while not_EOF:
            # read taxonomy1 keywords
            line = f_in.readline()
            name1 = line[:-1].split(" ")[1]
        
            # read (concept in taxonomy1)
            line = f_in.readline()
            while len(line) != 1:
                temp_list = line[1:-2].split(" ")
                parent = name1 + "." + temp_list[0]
                for i in range(1,len(temp_list)):
                    child = name1 + "." + temp_list[i]
                    pc_tuple = (parent, child)
                    pc_list1.append(pc_tuple)
                
                line = f_in.readline()
        
            # read taxonomy2 keywords
            line = f_in.readline()
            name2 = line[:-1].split(" ")[1]
        
            # read (concept in taxonomy2)
            line = f_in.readline()
            while len(line) != 1:
                temp_list = line[1:-2].split(" ")
                parent = name2 + "." + temp_list[0]
                for i in range(1,len(temp_list)):
                    child = name2 + "." + temp_list[i]
                    pc_tuple = (parent, child)
                    pc_list2.append(pc_tuple)
                
                line = f_in.readline()
            
            # read articulation keywords
            line = f_in.readline()
        
            # read articulation pairs
            line = f_in.readline()
            while len(line) != 0:
                art_type = ""
                line = line[1:-2].replace("{","").replace("}","")
                temp_list = line.split(" ")
                if len(temp_list) > 1:
                    for i in range(1,len(temp_list)-1):
                        art_type = art_type + temp_list[i] + " "
                    art_tuple = (temp_list[0], temp_list[len(temp_list)-1], art_type[:-2])
                    art_list.append(art_tuple)
                 
                line = f_in.readline()
                  
            # stop if it reaches the end of the file
            if len(line) == 0:
                not_EOF = False
                
        ##### Generate .dot file
        f_out.write("digraph {\n")
        f_out.write("rankdir = BT\n")
        
        f_out.write("subgraph cluster_t1 {\n")
        f_out.write("style=invis;\n")
        f_out.write("node [shape=box style=\"filled, rounded\" fillcolor=\"#CCFFCC\"];\n")
        node_list = []
        for e in pc_list1:
            node_list.append(e[0])
            node_list.append(e[1])
            self.remove_duplicate_string(node_list)
        for e in node_list:
            f_out.write("\"" + e + "\";\n")
        for e in pc_list1:
            f_out.write("\"" + e[1] + "\" -> \"" + e[0] + "\" [color=black];\n")
        f_out.write("}\n")
    
        f_out.write("subgraph cluster_t2 {\n")
        f_out.write("style=invis;\n")
        f_out.write("node [shape=box style=\"filled, rounded\" fillcolor=\"#FFFFCC\"];\n")
        node_list = []
        for e in pc_list2:
            node_list.append(e[0])
            node_list.append(e[1])
            self.remove_duplicate_string(node_list)
        for e in node_list:
            f_out.write("\"" + e + "\";\n")
        for e in pc_list2:
            f_out.write("\"" + e[1] + "\" -> \"" + e[0] + "\" [color=black];\n")
        f_out.write("}\n")
            
        for e in art_list:
            f_out.write("\"" + e[0] + "\" -> \"" + e[1] + "\" [color=grey, style=dashed, label=\"" + e[2] + "\"];\n")
        
        f_out.write("}")
        f_in.close()
        f_out.close()
    

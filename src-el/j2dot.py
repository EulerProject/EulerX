import json
import random
from collections import defaultdict
from pprint import pprint

nodes = defaultdict(list)
edges = defaultdict(list)
cluster = {}

# parse the stylesheet file
def readStyleSheet(stylefile):
    global styles
    with open(stylefile) as style_file:    
        styles = json.load(style_file)

def parse(datafile, output):
    f= open(output,"w")
    f.write("digraph{\n")
    with open('data.json') as data_file:    
        data = json.load(data_file)
        f.write('rankdir=' + styles["Graph"]["rankdir"] + '\n')
        f.write('labelloc=' + styles["Graph"]["labelloc"] + '\n')
        f.write('labeljust=' + styles["Graph"]["labeljust"] + '\n')
        f.write('fontsize=' + styles["Graph"]["fontsize"] + '\n')
        f.write('label="' + styles["Graph"]["label"] + '"\n')
        # seperate different node, edge, cluster, ... objects
        for item, attr in data.iteritems():
            if data[item]["type"] == "node":
                nodes[data[item]['group']].append(data[item]["concept"])
            elif data[item]["type"] == "edge":
                key = attr.items()
                edges[data[item]['l']].append(key)
            elif data[item]["type"] == "cluster":
                cluster[item]= attr
    for g in nodes:
        f.write('node[shape="' +styles[g]["shape"] + '", style="' +styles[g]["style"] + '", color="' + styles[g]["color"] + '", fillcolor="' + styles[g]["fillcolor"] +'"]' +'\n')
        for n in nodes[g]:
            if g!= "common":
               f.write('"'+ g + "." + n + '"\n')
            else:
               f.write(n + '\n')           
    for key, value in cluster.iteritems():
       r = lambda: random.randint(0,255)
       color = "#" + hex(r())[2:] + hex(r())[2:] + hex(r())[2:]
       f.write('subgraph cluster' + str(random.randint(0,100)) + '{\n')
       f.write('label=""\n')
       f.write('color="' + color + '"\n')
       c = cluster[key]['s'].split(",")
       for i in range(0, len(c)):
           f.write('"' + c[i] + '"\n')
       f.write('}\n')
       f.write('edge[style="' + styles["lsum"]["style"] + '", color="' + color + '", penwidth="' + cluster[key]["w"] + '"]' +'\n')
       f.write('"' + c[1] + '" -> "' + cluster[key]['t'] + '" [label="' + cluster[key]["l"] + '"]\n')
    for l in edges:
        if l in styles:
            f.write('edge[style="' + styles[l]["style"] + '", color="' + styles[l]["color"] + '"]\n')
        else:
            f.write('edge[style="' + styles["default"]["style"] + '", color="' + styles["default"]["color"] + '"]\n')
        for e in edges[l]:
            f.write('penwidth="' + e[3][1] + '"\n')
            f.write('"' + e[0][1] + '" -> "' + e[2][1] + '"')
            if l!= "isa":
                f.write(' [label="' + l + '"]')
            f.write('\n')
    f.write('}')            
    f.close()
    
readStyleSheet('stylesheet.json')
parse('data.json', 'out.dot')











import json
from collections import defaultdict

nodes = defaultdict(list)
edges = defaultdict(list)

# parse the stylesheet file
def read_stylesheet(stylefile):
    global styles
    with open(stylefile) as style_file:    
        styles = json.load(style_file)
        
def parse(datafile, output):
    f= open(output,"w")
    f.write("digraph{\n")
    f.write(str(styles["graphstyle"]["graph"]))
    with open(datafile) as data_file:    
        data = json.load(data_file)
    #separate nodes from edges
        for key, value in data.iteritems():
            if data[key]["type"] == "node":
                nodes[data[key]['group']].append(data[key]["concept"])
            elif data[key]["type"] == "edge":
                edges[data[key]['l']].append(value.items())
    for g in nodes:
    # if the style is not defined use the default
        if (styles["graphstyle"]["subgraph"] == "on" and g!="none"):
            f.write('subgraph cluster' + g + '{ label= "" style=invis\n')
        if g in styles["nodestyle"]:
            group = g
        else:
            group = "default"
        f.write('node[' + styles["nodestyle"][group] + '] \n')
        for n in nodes[g]:
            if (g!= "common" and g!= "none"):
               f.write('"'+ g + "." + n + '"\n')
            else:
               f.write('"'+ n + '"\n')
        if (styles["graphstyle"]["subgraph"] == "on"and g!="none"):
            f.write('}')
    for l in edges:
        if l in styles["edgestyle"]:
            label = l
        else:
            label = "default"
        f.write('edge['+ styles["edgestyle"][label] +']\n')
        for e in edges[l]:
            f.write('"' + e[0][1] + '" -> "' + e[2][1] + '"')
            f.write('[penwidth=' + e[3][1] + ']')
        # some of the labels are not shown in the output
            if (l!= "isa"and l!="inplus" and l!="outplus"):
                f.write(' [label="' + l + '"]')
            f.write('\n')
    f.write('}')            
    f.close()
    
read_stylesheet('stylesheet.json')
parse('data.json', 'out.dot')









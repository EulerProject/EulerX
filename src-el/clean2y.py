import yaml

nodes = {}
edges = {}

def add_edge(s,t,label):
        edge = {}
        edge.update({"s" : s})
        edge.update({"t" : t})
        edge.update({"label" : label})
        edges.update({s + "_" + t : edge})

def add_node(concept, group):
        node = {}
        node.update({"concept": concept})
        node.update({"group": group})
        if group!="none":
            nodes.update({group + "." + concept: node})
        else:
            nodes.update({concept: node})
g = []
groups = []
art = []
f = open("in.txt", 'r')
data= f.readlines()
for line in data:
    if line.startswith("taxonomy"):
       g.append(line.split(" ")[1])
    if line.startswith("("):
        groups.append(line[1:-2].split(" "))
    if line.startswith("["):
        art.append (line[1:-2])
dictionary = dict (zip(g, groups))
for key, value in dictionary.iteritems():
    parent = value.pop(0)
    add_node(parent, key)
    for v in value:
        add_node(v, key)
        add_edge(key + "." + parent, key + "." + v, "isa")
for a in art:
    if "{" in a:
        start = a.split(" {")[0]
        end = a.split("} ")[-1]
        articulations = a.split('{', 1)[1].split('}')[0].split(" ")
        for i in range(0,len(articulations)):
            add_edge(start, end, articulations[i])
    else:
        if "lsum" in a or "ldiff" in a:
            if "lsum" in a:
                    l = "lsum"
                    op = "+"
            else:
                    l = "ldiff"
                    op = "-"
            plus = a.split(" " + l)[-1][-1] + op
            add_node(plus, "none")
            add_edge(plus, a.split(" " + l + " ")[-1], "out")
            for i in range(0,len(a.split(" " + l)[0].split(" "))):
                add_edge(a.split(" " + l)[0].split(" ")[i], plus, "in")
        elif "rsum" in a or "rdiff" in a:
            if "rsum" in a:
                    l = "rsum"
                    op = "+"
            else:
                    l= "rdiff"
                    op = "-"
            plus = a.split(" " + l)[0][-1] + op
            add_node(plus, "none")
            add_edge(plus, a.split(" " + l + " ")[0], "out")
            for i in range(1,len(a.split(" " + l)[-1].split(" "))):
                add_edge(a.split(" " + l)[-1].split(" ")[i], plus,"in")

        else:
            add_edge(a.split(" ")[0], a.split(" ")[2], a.split(" ")[1])

f.close()
with open('out.yaml', 'w') as outfile:
   outfile.write(yaml.safe_dump(nodes, default_flow_style=False))
   outfile.write(yaml.safe_dump(edges, default_flow_style=False))        

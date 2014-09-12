import sys

def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

n = int(sys.argv[1])
numOfNodes = 2**n
nodes = []
edges = []

for i in range(numOfNodes):
    nodes.append(i)

for i in nodes:
    for j in nodes:
        if i<j and is_power2(i^j):
            edges.append([i,j])
print edges
            
f = open("powerset.dot","w")
f.write("digraph{\n")
f.write("rankdir = BT\n")
f.write("node [shape=box]\n")
for node in nodes:
    f.write(node.__str__() + "\n")
f.write("edge [style=solid]\n")
for edge in edges:
    f.write(edge[0].__str__() + "->" + edge[1].__str__() + "\n")

f.write("}")
f.close()

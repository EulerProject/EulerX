import sys

def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

n = int(sys.argv[1])
numOfNodes = 2**n
nodes = []
edges = []
ups = []

for i in range(numOfNodes):
    nodes.append(i)

for i in nodes:
    for j in nodes:
        if i<j and is_power2(i^j):
            edges.append([i,j])

# tweak edges
for edge in edges:
    tmp = "up(" + edge[1].__str__() + "," + edge[0].__str__() + ")"
    ups.append(tmp)

f = open("up.dlv","w")
f.write("{")
for up in ups:
    f.write(up)
    if ups.index(up) != (len(ups) - 1):
        f.write(", ")
f.write("}")
f.close()
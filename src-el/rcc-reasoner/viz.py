import csv

rows = []
with open("output.csv", "rb") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        rows.append(row)

rows.sort(key=lambda x: x[2])

for row in rows:
    print row
    
f = open("pic.dot", "w")
f.write("digraph {\n\nrankdir = TB\n\n")

#print rows[0][4] + ' ** ' + rows[0][5] + ' ** ' + rows[0][6]

f.write('0 [label="' + rows[0][2] + '\\n' + rows[0][4] + '" shape=box style="filled" fillcolor="#CCCCFF"]\n')
f.write('1 [label="' + rows[0][0] + rows[0][1] + '\\n' + rows[0][5] + '" shape=box style="filled" fillcolor="#FFFFCC"]\n')
f.write('2 [shape=point width = 0.2]\n')
f.write('3 [label="' + rows[0][2] + '\\n' + rows[0][6] + '" shape=box style="filled" fillcolor="#CCFFCC"]\n')
f.write('0 -> 2;\n')
f.write('1 -> 2 [style="dashed"];\n')
f.write('2 -> 3;\n')

index = 3
for i in range(1, len(rows)):
#    print rows[i-1][6] + ' ** ' + rows[i][5] + ' ** ' + rows[0][6]
    f.write(str(index+1) + ' [label="' + rows[i][0] + rows[i][1] + '\\n' + rows[i][5] + '" shape=box style="filled" fillcolor="#FFFFCC"]\n')
    f.write(str(index+2) + ' [shape=point width = 0.2]\n')
    f.write(str(index+3) + ' [label="' + rows[i][2] + '\\n' + rows[i][6] + '" shape=box style="filled" fillcolor="#CCFFCC"]\n')
    f.write(str(index) + ' -> ' + str(index+2) + ';\n')
    f.write(str(index+1) + ' -> ' + str(index+2) + ' [style="dashed"];\n')
    f.write(str(index+2) + ' -> ' + str(index+3) + ';\n')
    index = index + 3
    
f.write('}\n')
f.close()
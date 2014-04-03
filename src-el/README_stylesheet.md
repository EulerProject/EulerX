To apply the stylesheet file on a graph use the following command (The default inputs are "data.yaml" and "stylesheet.yaml"):

cat data.yaml|y2d -s [stylesheetfile.yaml]> [result.dot]


Example. Input visualization

cat [cleantaxfile.txt]|./c2y|./y2d -s [stylesheetfile.yaml]> [result.dot]





YAML / Json Data File Format:

1- Nodes:
Nodes are defined using two keys: concept, group. Example:
1.A:
  concept: A
  group: 1
2- Edges:
Edges are defined using 4 keys: label, s (source), t (target), w (penwidth). w is optional. Example:

1.F_2.B:
  label: overlaps
  s: 1.F
  t: 2.B
  w: '1'
  
YAML/Json Stylesheet Format:

1- graphstyle:
Graph attributes for dot file, example:
 graph: "rankdir=TB\n labelloc=t\n labeljust=left\n fontsize=20\n label=\"Sample Graph\"\n"
And a switch for subgraph. Example:
    subgraph: "on"
If the value of subgraph is “on”, nodes will be clustered based on their “group” in the output dot file. Anything other than “on” (e.g. “off”) means no subgraph in the output. 
2- nodestyle:
Maps each “group” to a dot string. Example:
    '1': "shape=box style=\"filled,rounded\" color=black fillcolor=\"#CCFFCC\""
3- edgestyle:
Maps each “label” to a dot string. 
There are 3 options for showing label: 
(w) penwidth: show penwidth as label
“label”: show the label from data file 
“ “: no label

Example:
      label: "isa"
      dot: "style=solid color=black"
      display: "(w)display"


“default” style will be applied if no style is defined for a node group or edge label. 

To apply the stylesheet file on a graph use the following command (The default inputs are "data.yaml" and "stylesheet.yaml"):

cat data.yaml|y2d -s [stylesheetfile.yaml]> [result.dot]


Example. Input visualization

cat [cleantaxfile.txt]|./c2y|./y2d -s [stylesheetfile.yaml]> [result.dot]





YAML / Json Data File Format:
--------------------------
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
  
YAML/Json Stylesheet Format
--------------------------

1- graphstyle:
Graph attributes for dot file. Example:
 graph: "rankdir=TB"
 (if rankdir= LR, in the the "second" taxonomy source and target will be swapped with backward "isa" edges, so that the two taxonomies face each other) 
 subgraph: a switch for subgraph. Example:
    subgraph: "on"
  If the value of subgraph is “on”, nodes will be clustered based on their “group” in the output dot file. Anything other than “on” (e.g. “off”) means no subgraph in the output. 
  legend: a switch similar to subgraph
   If the value of legend is "on", a table showing the number of nodes an edges will be added to the output dot file. 
wmap: a switch for penwidth scaling. The value "on" here means the penwidths in the input graph get mapped to the speified range in the stylesheet.
wmin, wmax: range of penwidth

Note: penwidth ("w") in the input graph is an optional key so if penwidth is not defined for an edge, when scaling the penwith values, the code assumes pendiwth of 1 for that edge. 
2- nodestyle:
Maps each “group” to a dot string. Example:
    '1': "shape=box style=\"filled,rounded\" color=black fillcolor=\"#CCFFCC\""

3- edgestyle:
Maps each “label” to a dot string. 
There are 3 options for showing label that are defined by assigning the following values to "display" key in edgestyle 
(w)display: show penwidth as label
“label”: show the label from data file 
"[displaystring]": show the specified string as label (special caseL: "" means no label)
 
 If the value of "penwidth" is on and "w" is defined in the datafile, the penwidth of edges is assigned accordingly. "w" is set to 1 if it is not defined in the data file.
Example:
      label: "isa"
      dot: "style=solid color=black"
      display: "(w)display"
      
Also, "(w)display" means apply the penwidth value
“default” style will be applied if no style is defined for a node group or edge label. 


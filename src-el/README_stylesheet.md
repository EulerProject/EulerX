To apply the stylesheet file on a graph use the following command (The default inputs are "data.yaml" and "stylesheet.yaml"):

cat data.yaml|y2d -s [stylesheetfile.yaml]> [result.dot]


Example. Input visualization

cat [cleantaxfile.txt]|./c2y|./y2d -s [stylesheetfile.yaml]> [result.dot]




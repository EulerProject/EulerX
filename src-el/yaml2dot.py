import yaml
import optparse
from collections import defaultdict

nodes = defaultdict(list)
edges = defaultdict(list)

# parse the stylesheet file
def read_stylesheet(stylefile):
    global styles
    with open(stylefile) as style_file:    
        styles = yaml.load(style_file)      
def apply_style(datafile, output):
    f= open(output,"w")
    f.write("digraph{\n")
    f.write(str(styles["graphstyle"]["graph"]))
    with open(datafile) as data_file:    
        data = yaml.load(data_file)
    #separate nodes from edges
        for key, value in data.iteritems():
            if "group" in data[key]:
                nodes[data[key]["group"]].append(data[key]["concept"])
            elif "label" in data[key]:
                if not any(d["label"] == value["label"] for d in styles["edgestyle"]):
                    edges["default"].append(value.items())
                else:
                    edges[data[key]["label"]].append(value.items())
    for g in nodes:
    # if the style is not defined use the default
        if (styles["graphstyle"]["subgraph"] == "on" and g!="none"):
            f.write("subgraph cluster" + g + '{ style=invis\n')
        if g in styles["nodestyle"]:
            group = g
        else:
            group = "default"
        f.write("node[" + styles["nodestyle"][group] + '] \n')
        for n in nodes[g]:
            if (g!= "common" and g!= "none"):
               f.write('"'+ g + "." + n + '"\n')
            else:
                f.write('"'+ n + '"')
                if "+" in n:
                    f.write(' [label="+"]')
                elif "-" in n:
                    f.write(' [label="-"]')
                f.write("\n")
        if (styles["graphstyle"]["subgraph"] == "on"and g != "none"):
            f.write("}\n")
    for l in edges:
        style = (item for item in styles["edgestyle"] if item["label"] == l).next()
        f.write("edge["+ style["dot"] +"]\n")
        for e in edges[l]:
            f.write('"' + e[0][1] + '" -> "' + e[1][1] + '"')
            if (style["display"] == "(w)display"):
                f.write('[penwidth=' + e[2][1] + "]")
        # check options for displaying label
            if (style["display"] == "(w)penwidth") or (style["display"] == "(w)display"):
                f.write(' [label="' + e[2][1] + '"]')
            elif (style["display"] == "label"):
                f.write(' [label="' + e[-1][1] + '"]')
            else:
                f.write(' [label="' + style["display"] + '"]')
            f.write("\n")
    f.write("}")            
    f.close()
def parse_options():
	# parse options
	parser = optparse.OptionParser(usage = "%prog [options]", version = "%prog 0.1")
	parser.add_option("-s","--sfile",type="string",dest="sfile",
					  default=None,
					  help="file")
	parser.add_option("-d","--dfile",type="string",dest="dfile",
					  default=None,
					  help="file")
	(options,args) = parser.parse_args()
	return (options,args)
			
if __name__ == '__main__':
	(options,args) = parse_options()
	if options.sfile == None:
		options.sfile = "stylesheet.yaml"
	if options.dfile == None:
		options.dfile = "data.yaml"
	read_stylesheet(options.sfile)
	apply_style(options.dfile, "out.dot")











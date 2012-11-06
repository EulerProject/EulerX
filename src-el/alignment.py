from taxonomy import * 

class TaxonomyMapping:

    def __init__(self):
        self.mir = {}                          # MIR
        self.tr = []                           # transitive reduction
        self.eq = []                           # euqlities
        self.taxonomies = {}
        self.articulations = []
        self.map = {}
        self.baseDlv = ""

    def addDMir(self, tName, child, sibling):
	self.mir[tName + "." + child +"," + tName + "." + sibling] ="{disjoint}"
	self.mir[tName + "." + sibling +"," + tName + "." + child] ="{disjoint}"

    def getTaxon(self, taxonomyName="", taxonName=""):
        taxonomy = self.taxonomies[taxonomyName]
        taxon = taxonomy.getTaxon(taxonName)
        return taxon

    def run(self):
        self.genDlv()
        com = "dlv -silent -filter=vr tmp.dlv"
        print commands.getoutput(com)

    def genDlv(self):
        if self.baseDlv != "":
            return  None
        self.genDlvConcept()
        self.genDlvPC()
        self.genDlvAr()
        fdlv = open("tmp.dlv", 'w')
        fdlv.write(self.baseDlv)
        fdlv.close()

    def genDlvConcept(self):
        con = "%%% Concepts\n"

        # numbering concepts
        num = 0
        for key in self.taxonomies.keys():
            for taxon in self.taxonomies[key].taxa.keys():
                t = self.taxonomies[key].taxa[taxon]
                self.map[t.dlvName()] = num
                con += "concept(" + t.dlvName() + "," + num.__str__()+").\n"
                num += 1

        self.baseDlv = "#maxint=" + int(2**num).__str__() + ".\n\n"
        self.baseDlv += con
        self.baseDlv += "\n%%% power\n"
        self.baseDlv += "p(0,1).\n"
        self.baseDlv += "p(N,M) :- #int(N),N>0,#succ(N1,N),p(N1,M1),M=M1*2.\n\n"

        self.baseDlv += "%%% regions\n"
        self.baseDlv += "r(M):- #int(M),M>=0,M<#maxint.\n\n"

        self.baseDlv += "%%% count of concepts\n"
        self.baseDlv += "count(N):- #int(N),N>=0,N<#count{Y:concept(Y,_)}.\n\n"

        self.baseDlv += "%%% bit\n"
        self.baseDlv += "bit(M, N, 0):-r(M),count(N),p(N,P),M1=M/P,#mod(M1,2,0).\n"
        self.baseDlv += "bit(M, N, 1):-r(M),count(N),not bit(M,N,0).\n\n"

        self.baseDlv += "%%% Meaning of regions\n"
        self.baseDlv += "in(X, M) v out(X, M) :- r(M),concept(X,N),count(N).\n"
        self.baseDlv += "in(X, M) :- r(M),concept(X,N),bit(M,N,1).\n"
        self.baseDlv += "out(X, M) :- r(M),concept(X,N),bit(M,N,0).\n\n"

        self.baseDlv += "%%% Constraints of regions.\n"
        self.baseDlv += "vr(X) :- r(X), not ir(X).\n"
        self.baseDlv += ":- vr(X), ir(X).\n\n"

    def genDlvPC(self):
        self.baseDlv += "%%% PC relations\n"
        for key in self.taxonomies.keys():
            queue = copy.deepcopy(self.taxonomies[key].roots)
            while len(queue) != 0:
                t = queue.pop(0)
                if t.hasChildren:
                    # ISA
                    self.baseDlv += "%% ISA\n"
                    coverage = "ir(X) :- in(" + t.dlvName() + ", X)"
                    for t1 in t.children:
                        self.baseDlv += "% " + t1.dlvName() + " isa " + t.dlvName() + "\n"
                        self.baseDlv += "ir(X) :- in(" + t1.dlvName() + ", X), out(" + t.dlvName() + ", X).\n\n"
                        coverage += ",out(" + t1.dlvName() + ", X)"
                    # C
                    self.baseDlv += "%% coverage\n"
                    self.baseDlv += coverage + ".\n\n"
                    # D
                    self.baseDlv += "%% sibling disjointness\n"
                    for i in range(len(t.children) - 1):
                        for j in range(i+1, len(t.children)):
                            name1 = t.children[i].dlvName()
                            name2 = t.children[j].dlvName()
                            self.baseDlv += "% " + name1 + " ! " + name2+ "\n"
                            self.baseDlv += "ir(X) :- in(" + name1 + ", X), in(" + name2+ ", X).\n\n"


    def genDlvAr(self):
        self.baseDlv += "%%% Articulations\n"
        for i in range(len(self.articulations)):
            self.baseDlv += "% " + self.articulations[i].string + "\n"
            self.baseDlv += self.articulations[i].toDlv()+ "\n"

        #print self.baseDlv

    def readFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        for line in lines:

            if (re.match("taxonomy", line)):
                taxName = re.match("taxonomy (.*)", line).group(1) 
                taxonomy = Taxonomy()
                if (taxName.find(" ") == -1):
                    taxonomy.nameit(taxName)
                else:
                    taxName = re.match("(.*?)\s(.*)", taxName)
                    taxonomy.nameit(taxName.group(1), taxName.group(2))
                  
                self.taxonomies[taxonomy.abbrev] = taxonomy
              
            # reads in lines of the form (a b c) where a is the parent
            # and b c are the children
            elif (re.match("\(.*\)", line)):
                taxonomy.addTaxaWithList(self, line)

            elif (re.match("articulation", line)):
                None
              
            elif (re.match("\[.*?\]", line)):
                inside = re.match("\[(.*)\]", line).group(1)
                # TODO add articulation
                self.articulations += [Articulation(inside, self)]
		if inside.find("{") != -1:
		    r = re.match("(.*) \{(.*)\} (.*)", inside)
		    #self.addPMir(r.group(1), r.group(3), r.group(2).replace(" ",","), 0)
		else:
                    None
		    #self.addAMir(inside, 0)
              
           # elif (re.match("\<.*\>", line)):
            #    inside = re.match("\<(.*)\>", line).group(1)
             #   hypElements = re.split("\s*\?\s*", inside)
              #  self.hypothesisType = hypElements[0]
               # hyp = hypElements[1]
               # hypArticulation = Articulation(hyp, self)
               # self.hypothesis = hypArticulation
                   
        return True              
 

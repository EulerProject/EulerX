# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from optparse import OptionParser
import argparse
from helper import *

class CtiParser:

    inst = None

    @staticmethod
    def instance():
        if CtiParser.inst is None:
            CtiParser.inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            CtiParser.inst.add_option("-v", action="store_true", dest="verbose")
	return CtiParser.inst

class EulerParser:
    
    inst = None
    
    @staticmethod
    def instance():
        if EulerParser.inst is None:
            #EulerParser.inst = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
            EulerParser.inst = argparse.ArgumentParser()
            EulerParser.inst.add_argument("-v", action="store_true", dest="verbose",\
                                        help="verbose mode")
            EulerParser.inst.add_argument("function", nargs="?", default="genpws", help="generate artificial input file")
            EulerParser.inst.add_argument("-p", dest="projectname", help="project name for artificial example generator, by default foo")
            #EulerParser.inst.add_argument("-i", dest="inputfile", help="input file")
            EulerParser.inst.add_argument("-i", nargs="*", dest="inputfile", help="input file")
            EulerParser.inst.add_argument("-r", dest="inputdir", default="",\
                                         help="input directory, by default ./")
            EulerParser.inst.add_argument("-w", dest="workingdir", default=None,\
                                         help="working directory, by default ./")
            EulerParser.inst.add_argument("-o", dest="outputdir", default=None,\
                                              help="output directory, by default ./")
            EulerParser.inst.add_argument("-e", dest="encode", default=0, \
                                              help="""
													encoding, supports both dlv and gringo 
													by default mnpw
													Options:
													mn, use polynomial encoding, get mir only
													mnpw, use polynomial encoding, get possible worlds
													mnve, use polynomial encoding, get valid euler regions
													mncb, use polynomial encoding, get possible worlds with combined concepts
													vr, use binary encoding, get mir only
													vrpw, use binary encoding, get possible worlds
													vrve, use binary encoding, get valid euler regions
													""")
            EulerParser.inst.add_argument("-b", dest="dl", default=2, help="dl encoding spare parameter")
            EulerParser.inst.add_argument("--reasoner", dest="reasoner", type=str, default="dlv",\
                                              help="choose a reasoner between dlv and gringo, by deafult using dlv")
            EulerParser.inst.add_argument("--repair", dest="repair", type=str, default=None,\
                                              help="""
													choose a repairing approach in case of inconsistency:
													topdown, fix and output possible worlds
													bottomup, fix and output possible worlds
													HST, ouput all MIRs
													""")
            EulerParser.inst.add_argument("--mirall", action="store_true", dest="allRelations", default=False,\
                                                help = "generate all the relations including intra-/inter-"\
                                                     + "taxonomies (by default, inter-taxonomy only)")
            EulerParser.inst.add_argument("--cc", action="store_true", dest="consCheck", default=False,\
                                                help="consistency check only")
            EulerParser.inst.add_argument("--dc", action="store_false", dest="enableCov", default=True,\
                                                help="disable coverage globally, or use \"nc\" to do it in some parent-child relation")
            EulerParser.inst.add_argument("--dd", action="store_false", dest="enableSD", default=True,\
                                                help="disable sibling disjointness globally, can be used with vr encoding only")
            EulerParser.inst.add_argument("--pdd", action="store_true", dest="disableSDP", default=False,\
                                                help="disable sibling disjointness partially, need to show pairs in inputs, can be used with vr encoding only")            
            EulerParser.inst.add_argument("--ur", action="store_true", dest="reduction", default=False,\
                                              help="turn on uncertainty reduction")
            EulerParser.inst.add_argument("--ho", action="store_true", dest="hideOverlaps", default=False,\
                                              help="hide the concepts that are involved in overlapping, used with cb encoding")
            EulerParser.inst.add_argument("--ie", action="store_true", dest="ie", default=False,\
                                                help="inconsistency explanation")
            EulerParser.inst.add_argument("--ieo", action="store_true", dest="ieo", default=False,\
                                                help="white-box provenance")
            EulerParser.inst.add_argument("--countmir", action="store_true", dest="countOn", default=False,\
                                              help="count # of occurrence for each of rcc5")
            EulerParser.inst.add_argument("--rcgo", action="store_true", dest="rcgo", default=False,\
                                              help="reduced containment graphs with overlaps")
            EulerParser.inst.add_argument("--pwcluster", action="store_true", dest="cluster", default=False,\
                                              help="output the distance between possible worlds")
            EulerParser.inst.add_argument("--simpcluster", action="store_true", dest="simpCluster", default=False,\
                                              help="simplify the possible world cluster, by default switch off")
            EulerParser.inst.add_argument("--hierarchy", action="store_true", dest="hierarchy", default=False,\
                                              help="hierarchical aggregate view, by default switch off")
            EulerParser.inst.add_argument("-N", action="store_false", dest="output", default=True,\
                                              help="no output")
            #EulerParser.inst.add_argument("-g", action="store_true", dest="generateCti", default=False,\
            #                                  help="artificial example generator, cannot be used with -I option")
            EulerParser.inst.add_argument("-n", dest="nary", type=int, default=0, help="N-nary, used with -g")
            EulerParser.inst.add_argument("-m", dest="nnodes", type=int, default=0, help="#nodes, used with -g")
            EulerParser.inst.add_argument("-d", dest="depth", type=int, default=2, help="depth, used with -g")
            EulerParser.inst.add_argument("-t", dest="relation", type=str, default="<",\
                                              help="artificial articulation rel, used with -g")
            EulerParser.inst.add_argument("-I", action="store_true", dest="incEx", default=False,\
                                              help="generate an inconsistent example, used with -g")
            EulerParser.inst.add_argument("--iv", action="store_true", dest="inputViz", default=False,\
                                              help="input visualization")
            EulerParser.inst.add_argument("--withrank", action="store_true", dest="withrank", default=False,\
                                              help="input visualization with concept rank")
            EulerParser.inst.add_argument("--simpall", action="store_true", dest="simpAllView", default=False,\
                                              help="simplify the pw aggregate view")
            EulerParser.inst.add_argument("--artRem", action="store_true", dest="artRem", default=False,\
                                              help="articulation remover")
            EulerParser.inst.add_argument("--xia", action="store_true", dest="xia", default=False,\
                                              help="extract input articulations")
            EulerParser.inst.add_argument("--diaglat", dest="diaglat", help="diagnostic lattice for inconsistent example")
            EulerParser.inst.add_argument("--mualat", dest="mualat", help="lattice for articulation sets that generates unique PW")
            EulerParser.inst.add_argument("--addID", nargs="*", dest="addID", help="input wizard, addID")
            EulerParser.inst.add_argument("--addIsa", dest="addIsa", help="input wizard, addIsa")
            EulerParser.inst.add_argument("--p2c", dest="p2c", help="input wizard, p2c")
            EulerParser.inst.add_argument("--p2ct", nargs="*", dest="p2ct", help="input wizard, p2c -t")
            EulerParser.inst.add_argument("--addArt", dest="addArt", help="input wizard, addArt")
            EulerParser.inst.add_argument("--c2csv", dest="c2csv", help="input wizard, c2csv")
            EulerParser.inst.add_argument("--addArtT", nargs="*", dest="addArtT", help="input wizard, addArt -t")
            EulerParser.inst.add_argument("--addRank", dest="addRank", help="input wizard, addRank")
            EulerParser.inst.add_argument("--mirStats", nargs="*", dest="mirStats", help="input wizard, mirStats")
            EulerParser.inst.add_argument('--version', action='version', version='<the version>')
        return EulerParser.inst

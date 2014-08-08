from optparse import OptionParser
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
            EulerParser.inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            EulerParser.inst.add_option("-v", action="store_true", dest="verbose",\
                                        help="verbose mode")
            EulerParser.inst.add_option("-p", dest="projectname", help="project name")
            EulerParser.inst.add_option("-i", dest="inputfile", help="input file")
            EulerParser.inst.add_option("-r", dest="inputdir", default="",\
                                         help="input directory, by default ./")
            EulerParser.inst.add_option("-o", dest="outputdir", default=None,\
                                              help="output directory, by default ./")
            EulerParser.inst.add_option("-e", dest="encode", default=0, \
                                              help="encoding, e.g. mnpw, drpw, dlpw, etc.")
            EulerParser.inst.add_option("-b", dest="dl", default=2, help="dl encoding spare parameter")
            EulerParser.inst.add_option("--reasoner", dest="reasoner", type="string", default="dlv",\
                                              help="choose a reasoner")
            EulerParser.inst.add_option("--repair", dest="repair", type="string", default="topdown",\
                                              help="choose a repairing approach in case of inconsistency")
            EulerParser.inst.add_option("--all", action="store_true", dest="allRelations", default=False,\
                                                help = "generate all the relations including intra-/inter-"\
                                                     + "taxonomies (by default, inter-taxonomy only)")
            EulerParser.inst.add_option("--cc", action="store_true", dest="consCheck", default=False,\
                                                help="consistency check only")
            EulerParser.inst.add_option("--dc", action="store_false", dest="enableCov", default=True,\
                                                help="disable coverage")
            EulerParser.inst.add_option("--ur", action="store_true", dest="reduction", default=False,\
                                              help="turn on uncertainty reduction")
            EulerParser.inst.add_option("--ho", action="store_true", dest="hideOverlaps", default=False,\
                                              help="hide the concepts that are involved in overlapping, used with cb encoding")
            EulerParser.inst.add_option("--ie", action="store_true", dest="ie", default=False,\
                                                help="inconsistency explanation")
            EulerParser.inst.add_option("--ieo", action="store_true", dest="ieo", default=False,\
                                                help="white-box provenance")
            EulerParser.inst.add_option("--countmir", action="store_true", dest="countOn", default=False,\
                                              help="count # of occurance for each of rcc5")
            EulerParser.inst.add_option("--rcgo", action="store_true", dest="rcgo", default=False,\
                                              help="Reduced containment graphs with overlaps")
            EulerParser.inst.add_option("--pwcluster", action="store_true", dest="cluster", default=False,\
                                              help="output the distance between pairwise possible world")
            EulerParser.inst.add_option("--simpcluster", action="store_true", dest="simpCluster", default=False,\
                                              help="simplify the possible world cluster")
            EulerParser.inst.add_option("-N", action="store_false", dest="output", default=True,\
                                              help="no output")
            EulerParser.inst.add_option("-g", action="store_true", dest="generateCti", default=False,\
                                              help="artifitial example generator, cannot be used with -i option")
            EulerParser.inst.add_option("-n", dest="nary", type="int", default=0, help="N-nary, used with -g")
            EulerParser.inst.add_option("-m", dest="nnodes", type="int", default=0, help="#nodes, used with -g")
            EulerParser.inst.add_option("-d", dest="depth", type="int", default=2, help="depth, used with -g")
            EulerParser.inst.add_option("-t", dest="relation", type="string", default="<",\
                                              help="artifitial articulaiton rel, used with -g")
            EulerParser.inst.add_option("-I", action="store_true", dest="incEx", default=False,\
                                              help="generate an inconsistent example, used with -g")
            EulerParser.inst.add_option("--iv", action="store_true", dest="inputViz", default=False,\
                                              help="input visualization")
            EulerParser.inst.add_option("--simpall", action="store_true", dest="simpAllView", default=False,\
                                  help="simplify the pw aggregate view")
	return EulerParser.inst

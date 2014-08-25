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
            EulerParser.inst.add_option("-p", dest="projectname", help="project name for artificial example generator, by default foo")
            EulerParser.inst.add_option("-i", dest="inputfile", help="input file")
            EulerParser.inst.add_option("-r", dest="inputdir", default="",\
                                         help="input directory, by default ./")
            EulerParser.inst.add_option("-o", dest="outputdir", default=None,\
                                              help="output directory, by default ./")
            EulerParser.inst.add_option("-e", dest="encode", default=0, \
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
            EulerParser.inst.add_option("-b", dest="dl", default=2, help="dl encoding spare parameter")
            EulerParser.inst.add_option("--reasoner", dest="reasoner", type="string", default="dlv",\
                                              help="choose a reasoner between dlv and gringo, by deafult using dlv")
            EulerParser.inst.add_option("--repair", dest="repair", type="string", default="topdown",\
                                              help="""
													choose a repairing approach in case of inconsistency:
													topdown, fix and output possible worlds
													bottomup, fix and output possible worlds
													HST, ouput all MIRs
													""")
            EulerParser.inst.add_option("--mirall", action="store_true", dest="allRelations", default=False,\
                                                help = "generate all the relations including intra-/inter-"\
                                                     + "taxonomies (by default, inter-taxonomy only)")
            EulerParser.inst.add_option("--cc", action="store_true", dest="consCheck", default=False,\
                                                help="consistency check only")
            EulerParser.inst.add_option("--dc", action="store_false", dest="enableCov", default=True,\
                                                help="disable coverage globally, or use \"nc\" to do it in some parent-child relation")
            EulerParser.inst.add_option("--ur", action="store_true", dest="reduction", default=False,\
                                              help="turn on uncertainty reduction")
            EulerParser.inst.add_option("--ho", action="store_true", dest="hideOverlaps", default=False,\
                                              help="hide the concepts that are involved in overlapping, used with cb encoding")
            EulerParser.inst.add_option("--ie", action="store_true", dest="ie", default=False,\
                                                help="inconsistency explanation")
            EulerParser.inst.add_option("--ieo", action="store_true", dest="ieo", default=False,\
                                                help="white-box provenance")
            EulerParser.inst.add_option("--countmir", action="store_true", dest="countOn", default=False,\
                                              help="count # of occurrence for each of rcc5")
            EulerParser.inst.add_option("--rcgo", action="store_true", dest="rcgo", default=False,\
                                              help="reduced containment graphs with overlaps")
            EulerParser.inst.add_option("--pwcluster", action="store_true", dest="cluster", default=False,\
                                              help="output the distance between possible worlds")
            EulerParser.inst.add_option("--simpcluster", action="store_true", dest="simpCluster", default=False,\
                                              help="simplify the possible world cluster, by default switch off")
            EulerParser.inst.add_option("-N", action="store_false", dest="output", default=True,\
                                              help="no output")
            EulerParser.inst.add_option("-g", action="store_true", dest="generateCti", default=False,\
                                              help="artificial example generator, cannot be used with -I option")
            EulerParser.inst.add_option("-n", dest="nary", type="int", default=0, help="N-nary, used with -g")
            EulerParser.inst.add_option("-m", dest="nnodes", type="int", default=0, help="#nodes, used with -g")
            EulerParser.inst.add_option("-d", dest="depth", type="int", default=2, help="depth, used with -g")
            EulerParser.inst.add_option("-t", dest="relation", type="string", default="<",\
                                              help="artificial articulation rel, used with -g")
            EulerParser.inst.add_option("-I", action="store_true", dest="incEx", default=False,\
                                              help="generate an inconsistent example, used with -g")
            EulerParser.inst.add_option("--iv", action="store_true", dest="inputViz", default=False,\
                                              help="input visualization")
            EulerParser.inst.add_option("--simpall", action="store_true", dest="simpAllView", default=False,\
                                  help="simplify the pw aggregate view")
	return EulerParser.inst

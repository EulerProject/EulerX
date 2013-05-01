from optparse import OptionParser
from helper import *

class CtiParser:

    inst = None

    def instance():
        if CtiParser.inst is None:
            CtiParser.inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            CtiParser.inst.add_option("-v", action="store_true", dest="verbose")
	return CtiParser.inst

    instance = Callable(instance)

class EulerParser:

    global inst
    inst = None

    def instance():
        global inst
        if inst is None:
            inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            inst.add_option("-v", action="store_true", dest="verbose",\
                                  help="verbose mode")
            inst.add_option("-p", dest="projectname", help="project name")
            inst.add_option("-e", dest="encode", default="vr",\
                                  help="encoding, e.g. mnpw, drpw, dlpw, etc.")
            inst.add_option("-b", dest="dl", default=2, help="dl encoding spare parameter")
            inst.add_option("-g", action="store_true", dest="generateCti", default=False,\
                                  help="artifitial example generator")
            inst.add_option("--dc", action="store_false", dest="enableCov", default=True,\
                                    help="disable coverage")
            inst.add_option("--countmir", action="store_true", dest="countOn", default=False,\
                                  help="count # of occurance for each of rcc5")
            inst.add_option("--pwcluster", action="store_true", dest="cluster", default=False,\
                                  help="output the distance between pairwise possible world")
            inst.add_option("-N", action="store_false", dest="output", default=True,\
                                  help="no output")
            inst.add_option("-n", dest="nary", type="int", default=0, help="N-nary, used with -g")
            inst.add_option("-m", dest="nnodes", type="int", default=0, help="#nodes, used with -g")
            inst.add_option("-d", dest="depth", type="int", default=2, help="depth, used with -g")
            inst.add_option("-t", dest="relation", type="string", default="<",\
                                  help="artifitial articulaiton rel, used with -g")
            inst.add_option("-i", dest="inputfile", help="input file")
            inst.add_option("-r", dest="inputdir", default="",\
                                  help="input directory, by default ./")
            inst.add_option("-o", dest="outputdir", default="./",\
                                  help="output directory, by default ./")
	return inst

    instance = Callable(instance)

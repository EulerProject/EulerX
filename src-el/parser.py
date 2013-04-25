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
            inst.add_option("-v", action="store_true", dest="verbose")
            inst.add_option("-p", dest="projectname")
            inst.add_option("-e", dest="encode", default="vr")
            inst.add_option("-b", dest="dl", default=2)
            inst.add_option("-g", action="store_true", dest="generateCti", default=False)
            inst.add_option("-dc", action="store_false", dest="enableCov", default=True)
            inst.add_option("-N", action="store_false", dest="output", default=True)
            inst.add_option("-n", dest="nary", type="int", default=0)
            inst.add_option("-m", dest="nnodes", type="int", default=0)
            inst.add_option("-d", dest="depth", type="int", default=2)
            inst.add_option("-t", dest="relation", type="string", default="<")
            inst.add_option("-i", dest="inputfile")
            inst.add_option("-r", dest="inputdir", default="")
            inst.add_option("-o", dest="outputdir", default="./")
	return inst

    instance = Callable(instance)

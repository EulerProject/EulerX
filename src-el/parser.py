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
            inst.add_option("-i", dest="inputfile")
            inst.add_option("-r", dest="inputdir", default="")
	return inst

    instance = Callable(instance)

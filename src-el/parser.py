from optparse import OptionParser

class Callable:
    def __init__(self, callable):
        self.__call__ = callable

class CtiParser:

    inst = None

    def instance():
        if CtiParser.inst is None:
            CtiParser.inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            CtiParser.inst.add_option("-v", action="store_true", dest="verbose")
	return CtiParser.inst

    instance = Callable(instance)

class EulerCliParser:

    global inst
    inst = None

    def instance():
        global inst
        if inst is None:
            inst = OptionParser(usage="usage: %prog [options]",
                                version="%prog 1.0")
            inst.add_option("-v", action="store_true", dest="verbose")
	return inst

    instance = Callable(instance)

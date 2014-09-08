import sys

class Callable:
    def __init__(self, callable):
        self.__call__ = callable

def findkey(mapp, value):
#    tmplist = [k for k, v in mapp.iteritems() if v == value]
#    if tmplist is []:
#        return None
#    return tmplist[0]
    return mapp.keys()[mapp.values().index(value)]


class Logger(object):
    # filename may have proper path
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        
    def __del__(self):
        self.log.close()
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
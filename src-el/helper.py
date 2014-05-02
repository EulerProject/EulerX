class Callable:
    def __init__(self, callable):
        self.__call__ = callable

def findkey(mapp, value):
#    tmplist = [k for k, v in mapp.iteritems() if v == value]
#    if tmplist is []:
#        return None
#    return tmplist[0]
     return mapp.keys()[mapp.values().index(value)]

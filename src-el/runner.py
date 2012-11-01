from helper import *
from taxonomy import *

class EulerRunner:

    inst = None

    def __init__(self):
        self.name = "Euler Runner"

    def instance():
	return EulerRunner()

    instance = Callable(instance)

    def run(self, options):
        taxMap = TaxonomyMapping()
        taxMap.readFile(options.inputdir+options.inputfile)
        taxMap.run()


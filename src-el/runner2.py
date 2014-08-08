from helper import *
from taxonomy import *
from alignment import *

class EulerRunner:

    inst = None

    def __init__(self):
        self.name = "Euler Runner"

    def instance():
	return EulerRunner()

    instance = Callable(instance)

    def run(self, options):
        taxMap = TaxonomyMapping(options)
        # Parse the cti file
        taxMap.readFile()
        taxMap.run()


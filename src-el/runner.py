from helper import *
from taxonomy import *
from alignment import *

class EulerRunner:

    inst = None

    def __init__(self):
        self.name = "Euler Runner"

    @Callable
    def instance():
	return EulerRunner()

    def run(self, options):
        taxMap = TaxonomyMapping(options, True)
        # Parse the cti file
        taxMap.readFile()
        taxMap.run()


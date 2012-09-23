from latent_tax_assumption import *

global config

config = {
    "reasonerDir" : "",
    "reasonerTimeout" :  10,
    "inputLocation" : "",
    "outputDir" : "",
    "inputDir" : "",
    "htmlDir" : "..",
    "inputType" : "",
    "outputType" : "text",
    "outputFile" : "console",
    "taxonomies" : [],
    "species" : [],
    "goals" : [],
    "ltaList" : [],
    "goalTypes" : [],
    "goalRelations" : ["includes","equals","disjoint","overlaps","is_included_in"],
    "ltaString" :"",
    "compression" : False,
    "memory" : False,
    "ltas" :LatentTaxAssumption(),
    "uncertaintyRed" : False,
    "pw" : False,
}




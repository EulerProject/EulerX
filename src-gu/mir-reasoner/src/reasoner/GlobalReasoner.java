package reasoner;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import common_classes.*;

public class GlobalReasoner {
	// articulations map for the decomposed taxnomies
	private Map<TaxonPair, String> decomposedArticulations;
	// list of microreasoners to run over each tiny tree in the decomposed taxonomies
	private List<MicroReasoner> microreasoners;

	public GlobalReasoner(Taxonomy T1, Taxonomy T2){
		// decompose the taxonomies into binary trees
		Taxonomy _T1 = T1.decompose();
		Taxonomy _T2 = T2.decompose();

		// place in the articulations map all TaxonPair objects from the decomposed taxonomies
		decomposedArticulations = new HashMap<TaxonPair, String>();
		for ( Taxon _t1 : _T1.getAllTaxa() )
			for ( Taxon _t2 : _T2.getAllTaxa() )
				decomposedArticulations.put(new TaxonPair(_t1, _t2), "<>=!o");

		// create the ordered list of MicroReasoner objects
		microreasoners = new LinkedList<MicroReasoner>();
		for (TaxonPair _taxonPair : orderTaxonPairs(_T1, _T2))
			microreasoners.add(new MicroReasoner(_taxonPair));
	}

	/** Run the reasoner and return true if new information was found.
	 * @param articulations The map of taxon pairs to their articulations.
	 * @pre articulations is not null.
	 * @post articulations now contains the articulations discovered by this run.
	 * @return True is new information was found, else false.
	 * @throws InvalidTaxonomyException If the taxonomy is inconsistent.
	 */
	public boolean runReasoner(Map<TaxonPair, String> articulations) throws InvalidTaxonomyException{
		// update the working map of articulations and clear the map of new articulations
		decomposedArticulations.putAll(articulations);

		// run each microreasoner, storing new relations in decomposedNewArticulations
		boolean foundNew = false;
		for (MicroReasoner microreasoner : microreasoners){
			microreasoner.updateRelations(decomposedArticulations);
			if (foundNew |= microreasoner.runReasoner())
				microreasoner.putNewRelationsInMap(decomposedArticulations);
		}

		// store the new relations between the non-false taxa in the map of articulations
		for (TaxonPair _t : decomposedArticulations.keySet())
			if (!_t.isFalse())
				articulations.put(_t, decomposedArticulations.get(_t));

		// return whether the reasoner found new information
		return foundNew;
	}

	/** Returns an ordered list of taxon pairs between T1 and T2 for bottom-up traversals. */
	private static List<TaxonPair> orderTaxonPairs(Taxonomy T1, Taxonomy T2){
		List<Taxon> T1OrderedTaxa = new LinkedList<Taxon>();
		List<Taxon> T2OrderedTaxa = new LinkedList<Taxon>();
		List<TaxonPair> sortedPairs   = new LinkedList<TaxonPair>();

		// order the T1 taxa by their level
		for (int i=T1.getHeight(); i>0; i--)
			for (Taxon t1 : T1.getAllTaxa())
				if (t1.getLevel() == i-1)
					T1OrderedTaxa.add(t1);

		// order the T2 taxa by their level
		for (int i=T2.getHeight(); i>0; i--)
			for (Taxon t2 : T2.getAllTaxa())
				if (t2.getLevel() == i-1)
					T2OrderedTaxa.add(t2);

		// create a list of taxon pairs sorted for bottom-up traversal
		for (Taxon t1 : T1OrderedTaxa)
			for (Taxon t2 : T2OrderedTaxa)
				sortedPairs.add(new TaxonPair(t1, t2));

		return sortedPairs;
	}
}

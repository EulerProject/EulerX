package converter;

import java.util.List;
import java.util.Set;

import common_classes.*;

/**
 * Wrapper class for the information found in the parser and relevant to the seeder.
 * @author cbryan2
 */
public class SeederInitializer {
				/* Class fields */

	// the two taxonomies
	private Taxonomy T1;
	private Taxonomy T2;
	// list of all relations
	private Set<SimpleRelation> allRelations;
	// list of the inter-taxonomical relations
	private List<SimpleRelation> interrelations;


				/* Class methods */

	/** 6-arg constructor.
	 * @param allRelations List of all the relations from the input file, in order.
	 * @param interrelations List of all the inter-taxonomical relations from the input file.
	 * @param T1Namespace Namespace of the first taxonomy.
	 * @param T1intrarelations List of the intra-taxonomical relations from the first taxonomy.
	 * @param T2Namespace Namespace of the second taxonomy.
	 * @param T2intrarelations List of intra-taxonomical relations from the second taxonomy.
	 * @throws InvalidTaxonomyException If the only parentless taxon is not connected to the other taxa.	*/
	public SeederInitializer(Taxonomy T1, Taxonomy T2, Set<SimpleRelation> allRelations, List<SimpleRelation> interrelations)
						throws InvalidTaxonomyException{
		this.T1 = T1;
		this.T2 = T2;
		this.allRelations = allRelations;
		this.interrelations = interrelations;
	}


				/* Getters */

	public Set<SimpleRelation> getAllRelations() { return allRelations; }
	public List<SimpleRelation> getInterrelations() { return interrelations; }
	public Taxon getT1Taxon(String taxonName) { return T1.getTaxon(taxonName); }
	public Taxon getT2Taxon(String taxonName) { return T2.getTaxon(taxonName); }
	public List<Taxon> getT1Taxa() { return T1.getAllTaxa(); }
	public List<Taxon> getT2Taxa() { return T2.getAllTaxa(); }
	public String getT1Namespace() { return T1.getNamespace(); }
	public int getNumInterrelations() { return ( T1.getSize() * T2.getSize() ); }
}

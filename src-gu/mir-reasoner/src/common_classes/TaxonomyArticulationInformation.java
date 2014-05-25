package common_classes;

import java.util.List;

public class TaxonomyArticulationInformation {
				/* Class fields */

	// the two taxonomies
	private Taxonomy T1;
	private Taxonomy T2;

	// list of the inter-taxonomical relations
	private List<SimpleRelation> interrelations;


				/* Class methods */
	
	public TaxonomyArticulationInformation(Taxonomy T1, Taxonomy T2, List<SimpleRelation> interrelations){
		this.T1 = T1;
		this.T2 = T2;
		this.interrelations = interrelations;
	}


				/* Getters */

	// getters for the taxonomies
	public Taxonomy getT1() { return T1; }
	public Taxonomy getT2() { return T2; }

	// getter for the interrelations
	public List<SimpleRelation> getInterrelations() { return interrelations; }
}

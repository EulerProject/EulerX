package reasoner;

import common_classes.*;

public class DeducibleArticulations {
				/* Class fields */

	// the articulations which can be deduced from the articulation between two taxa t1 and t2 
	private String t1_to_t2Parent,  t1_to_t2Sibling, t1_to_t2Children,
				   t1Parent_to_t2,  t1Sibling_to_t2, t1Children_to_t2;

	// the relations to seed for each of the five basic set relations
	private static final String[] PROPER_PART =        {"<", "!", "<>=!o", "<>=o", "<!o", "<"};
	private static final String[] INVERSE_PROPER_PART = {"<>=o", ">!o", ">", ">", "!", "<>=!o"};
	private static final String[] EQUALS =            {"<", "!", ">", ">", "!", "<"};
	private static final String[] DISJOINT =          {"<!o", "<>=!o", "!", ">!o", "<>=!o", "!"};
	private static final String[] OVERLAPS =          {"<o", ">!o", ">!o", ">o", "<!o", "<!o"};


				/* Class methods */

	public DeducibleArticulations(String articulation){
		t1_to_t2Parent = "";
		t1_to_t2Sibling = "";
		t1_to_t2Children = "";
		t1Parent_to_t2 = "";
		t1Sibling_to_t2 = "";
		t1Children_to_t2 = "";

		if ( articulation.contains("<") )  this.union(PROPER_PART);
		if ( articulation.contains(">") )  this.union(INVERSE_PROPER_PART);
		if ( articulation.contains("=") )  this.union(EQUALS);
		if ( articulation.contains("!") )  this.union(DISJOINT);
		if ( articulation.contains("o") )  this.union(OVERLAPS);
	}

	private void union(String[] newRelations){
		t1_to_t2Parent   = Articulations.union(t1_to_t2Parent,   newRelations[0]);
		t1_to_t2Sibling  = Articulations.union(t1_to_t2Sibling,  newRelations[1]);
		t1_to_t2Children = Articulations.union(t1_to_t2Children, newRelations[2]);
		t1Parent_to_t2   = Articulations.union(t1Parent_to_t2,   newRelations[3]);
		t1Sibling_to_t2  = Articulations.union(t1Sibling_to_t2,  newRelations[4]);
		t1Children_to_t2 = Articulations.union(t1Children_to_t2, newRelations[5]);
	}


				/* Getters */

	// getters for the articulations
	public String getArticulationBetween_t1_and_t2Parent()   { return t1_to_t2Parent; }
	public String getArticulationBetween_t1_and_t2Sibling()  { return t1_to_t2Sibling; }
	public String getArticulationBetween_t1_and_t2Children() { return t1_to_t2Children; }
	public String getArticulationBetween_t1Parent_and_t2()   { return t1Parent_to_t2; }
	public String getArticulationBetween_t1Sibling_and_t2()  { return t1Sibling_to_t2; }
	public String getArticulationBetween_t1Children_and_t2() { return t1Children_to_t2; }
}
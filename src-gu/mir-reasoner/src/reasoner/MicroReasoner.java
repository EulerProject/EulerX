package reasoner;

import java.util.Map;

import common_classes.*;

public class MicroReasoner {
	private boolean AHasChildren, BHasChildren;

	private TaxonPair AB, Ab1, Ab2;
	private TaxonPair a1B, a1b1, a1b2;
	private TaxonPair a2B, a2b1, a2b2;

	private String A_to_B, A_to_b1, A_to_b2;
	private String a1_to_B, a1_to_b1, a1_to_b2;
	private String a2_to_B, a2_to_b1, a2_to_b2;


	public MicroReasoner(TaxonPair pair){
		Taxon A = pair.getTaxon1();
		Taxon B = pair.getTaxon2();
		Taxon a1, a2, b1, b2;

		AHasChildren = A.getChildren().size() > 1;
		BHasChildren = B.getChildren().size() > 1;

		AB =  new TaxonPair(A, B);
		if (AHasChildren){
			a1 = A.getChildren().get(0);
			a2 = A.getChildren().get(1);
			a1B =  new TaxonPair(a1, B);
			a2B =  new TaxonPair(a2, B);
		}
		if (BHasChildren){
			b1 = B.getChildren().get(0);
			b2 = B.getChildren().get(1);
			Ab1 = new TaxonPair(A, b1);
			Ab2 = new TaxonPair(A, b2);
		}
		if (AHasChildren && BHasChildren){
			a1 = A.getChildren().get(0);
			a2 = A.getChildren().get(1);
			b1 = B.getChildren().get(0);
			b2 = B.getChildren().get(1);
			a1b1 = new TaxonPair(a1, b1);
			a1b2 = new TaxonPair(a1, b2);
			a2b1 = new TaxonPair(a2, b1);
			a2b2 = new TaxonPair(a2, b2);
		}
	}
 
	public boolean runReasoner() throws InvalidTaxonomyException{
		// reason from the relations up to R
		boolean foundNewToR = reasonToR();
		// reason from R down to the relations
		boolean foundNewFromR = reasonFromR();
		// if the tree is inconsistent, throw an exception
		if (isInconsistent())
			throw new InvalidTaxonomyException("Inconsistency somewhere in the tiny trees for " + 
							   AB.getTaxon1() + " and " + AB.getTaxon2() + '.');
	 	// else return whether new information was found
	 	return foundNewToR || foundNewFromR;

		/* TODO to run continuously
		// if new information was discovered, run the reasoner again
		if (foundNewToR || foundNewFromR){
			//reasonOverTinyTrees(); // TODO do we want to do this?  Or shall we just run it once?
			if (reasonOverTinyTrees())
				System.out.println("Actually discovered something the second time around..."); // TODO
			return true;
		}

		return false;
		*/
	}

	public void updateRelations(Map<TaxonPair, String> articulations){
		A_to_B = articulations.get(AB);

		if (AHasChildren){
			a1_to_B  = articulations.get(a1B);
			a2_to_B  = articulations.get(a2B);			
		}

		if (BHasChildren){
			A_to_b1  = articulations.get(Ab1);
			A_to_b2  = articulations.get(Ab2);
		}

		if (AHasChildren && BHasChildren){
			a1_to_b1 = articulations.get(a1b1);
			a1_to_b2 = articulations.get(a1b2);
			a2_to_b1 = articulations.get(a2b1);
			a2_to_b2 = articulations.get(a2b2);
		}
	}

	public void putNewRelationsInMap(Map<TaxonPair, String> articulations){
		articulations.put(AB,  A_to_B);

		if (AHasChildren){
			articulations.put(a1B,  a1_to_B);
			articulations.put(a2B,  a2_to_B);
		}

		if (BHasChildren){
			articulations.put(Ab1, A_to_b1);
			articulations.put(Ab2, A_to_b2);
		}

		if (AHasChildren && BHasChildren){
			articulations.put(a1b1, a1_to_b1);
			articulations.put(a1b2, a1_to_b2);
			articulations.put(a2b1, a2_to_b1);
			articulations.put(a2b2, a2_to_b2);
		}
	}

	private boolean reasonToR(){
		String R, newR;
		R = A_to_B;

		// further specify R using children-to-parent reasoning
		if (AHasChildren){
			newR = ChildrenToParentPatterns.getRFromRelations(a1_to_B, a2_to_B);
			R = Articulations.intersect(R, newR);
		}

		// further specify R using parent-to-children reasoning
		if (BHasChildren){
			newR = ParentToChildrenPatterns.getRFromRelations(A_to_b1, A_to_b2);
			R = Articulations.intersect(R, newR);
		}

		// further specify R using children-to-children reasoning
		if (AHasChildren && BHasChildren){
			newR = ChildrenToChildrenPatterns.getRFromRelations(a1_to_b1, a1_to_b2, a2_to_b1, a2_to_b2);
			R = Articulations.intersect(R, newR);
		}

		// if a new R was discovered, set A_to_B as the new R and return true
		if (R.length() < A_to_B.length()){
			A_to_B = R;
			return true;
		}

		return false;
	}

	private boolean reasonFromR(){
		String[] newRelations;
		boolean foundNew = false;

		if (AHasChildren){
			// deduce the relations between the children of A and B
			newRelations = ChildrenToParentPatterns.getRelationsFromR(A_to_B, a1_to_B, a2_to_B);
			String newa1_to_B = newRelations[0];
			String newa2_to_B = newRelations[1];
			newa1_to_B = Articulations.intersect(newa1_to_B, a1_to_B);
			newa2_to_B = Articulations.intersect(newa2_to_B, a2_to_B);

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newa1_to_B.length() < a1_to_B.length()) { a1_to_B = newa1_to_B;  foundNew = true; }
			if (newa2_to_B.length() < a2_to_B.length()) { a2_to_B = newa2_to_B;  foundNew = true; }
		}

		if (BHasChildren){
			// deduce the relations between A and the children of B
			newRelations = ParentToChildrenPatterns.getRelationsFromR(A_to_B, A_to_b1, A_to_b2);
			String newA_to_b1 = newRelations[0];
			String newA_to_b2 = newRelations[1];
			newA_to_b1 = Articulations.intersect(newA_to_b1, A_to_b1);
			newA_to_b2 = Articulations.intersect(newA_to_b2, A_to_b2);

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newA_to_b1.length() < A_to_b1.length()) { A_to_b1 = newA_to_b1;  foundNew = true; }
			if (newA_to_b2.length() < A_to_b2.length()) { A_to_b2 = newA_to_b2;  foundNew = true; }
		}

		if (AHasChildren && BHasChildren){
			// deduce the relations between the children A and the children of B
			newRelations = ChildrenToChildrenPatterns.getRelationsFromR(A_to_B, a1_to_b1, a1_to_b2, a2_to_b1, a2_to_b2);
			String newa1_to_b1 = newRelations[0];
			String newa1_to_b2 = newRelations[1];
			String newa2_to_b1 = newRelations[2];
			String newa2_to_b2 = newRelations[3];
			newa1_to_b1 = Articulations.intersect(newa1_to_b1, a1_to_b1);
			newa1_to_b2 = Articulations.intersect(newa1_to_b2, a1_to_b2);
			newa2_to_b1 = Articulations.intersect(newa2_to_b1, a2_to_b1);
			newa2_to_b2 = Articulations.intersect(newa2_to_b2, a2_to_b2);

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newa1_to_b1.length() < a1_to_b1.length()) { a1_to_b1 = newa1_to_b1;  foundNew = true; }
			if (newa1_to_b2.length() < a1_to_b2.length()) { a1_to_b2 = newa1_to_b2;  foundNew = true; }
			if (newa2_to_b1.length() < a2_to_b1.length()) { a2_to_b1 = newa2_to_b1;  foundNew = true; }
			if (newa2_to_b2.length() < a2_to_b2.length()) { a2_to_b2 = newa2_to_b2;  foundNew = true; }
		}

		return foundNew;
	}

	private boolean isInconsistent(){
		boolean isInconsistent = false;
		isInconsistent |= A_to_B.isEmpty();

		if (AHasChildren){
			isInconsistent |= a2_to_B.isEmpty();
			isInconsistent |= a1_to_B.isEmpty();
		}
		if (BHasChildren){
			isInconsistent |= A_to_b1.isEmpty();
			isInconsistent |= A_to_b2.isEmpty();
		}
		if (AHasChildren && BHasChildren){
			isInconsistent |= a1_to_b1.isEmpty();
			isInconsistent |= a1_to_b2.isEmpty();
			isInconsistent |= a2_to_b1.isEmpty();
			isInconsistent |= a2_to_b2.isEmpty();
		}

		return isInconsistent;
	}

	public String getA_to_B() { return A_to_B; }
	public String getA_to_b1() { return A_to_b1; }
	public String getA_to_b2() { return A_to_b2; }

	public String geta1_to_B() { return a1_to_B; }
	public String geta1_to_b1() { return a1_to_b1; }
	public String geta1_to_b2() { return a1_to_b2; }

	public String geta2_to_B() { return a2_to_B; }
	public String geta2_to_b1() { return a2_to_b1; }
	public String geta2_to_b2() { return a2_to_b2; }
}

package reasoner;

import java.util.Map;
import java.util.HashMap;

import common_classes.*;

public class MicroReasoner {
	private boolean AHasChildren, BHasChildren;

	private TaxonPair AB, Ab1, Ab2;
	private TaxonPair a1B, a1b1, a1b2;
	private TaxonPair a2B, a2b1, a2b2;

	private String A_to_B, A_to_b1, A_to_b2;
	private String a1_to_B, a1_to_b1, a1_to_b2;
	private String a2_to_B, a2_to_b1, a2_to_b2;

	private Map<TaxonPair, String> provenance;


	public MicroReasoner(TaxonPair pair){
		Taxon A = pair.getTaxon1();
		Taxon B = pair.getTaxon2();
		Taxon a1, a2, b1, b2;
		provenance = new HashMap<TaxonPair, String>();

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
 
	public boolean runReasoner(Map<TaxonPair, String> provenance) throws InvalidTaxonomyException{
		this.provenance = provenance;
		// reason from the relations up to R
		boolean foundNewToR = reasonToR();
		// reason from R down to the relations
		boolean foundNewFromR = reasonFromR();
		// if the tree is inconsistent, throw an exception
		if (isInconsistent())
			throw new InvalidTaxonomyException("Inconsistency somewhere in the tiny trees for " + AB.getTaxon1() + " and " + AB.getTaxon2() + '.');
	 	// else return whether new information was found
	 	return foundNewToR || foundNewFromR;
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

	public void putProvenanceInMap(Map<TaxonPair, String> explanations){
		for(Map.Entry<TaxonPair, String> entry : provenance.entrySet()){
			if(explanations.containsKey(entry.getKey()))
				explanations.put(entry.getKey(), explanations.get(entry.getKey()) + " " + entry.getValue());
			else
				explanations.put(entry.getKey(), entry.getValue());
		}
	}

	//Adds provenance to the map
	private void addProvenance(TaxonPair tp, Taxon t1, String articulation, Taxon t2){
		if(!t1.isFalse() && !t2.isFalse()){
			TaxonPair provTP = new TaxonPair(t1, t2);
			String reason = t1.toString() + " " + articulation + " " + t2.toString() + ", ";
			if(provenance.containsKey(tp)){
				if(!provenance.get(tp).equals("Given"))
					if(!provenance.get(tp).contains(reason) && !containsPair(tp, provTP))
						provenance.put(tp, provenance.get(tp) + reason);
					else if(containsPair(tp, provTP)){
						String replaceThis = ".*" + provTP.getTaxon1() + " [=o<>!]+ " + provTP.getTaxon2() + ".*"; //removes multiple instances of the articulation
						provenance.put(tp, provenance.get(tp).replaceFirst(replaceThis, reason));
					}
			}
			else{
				provenance.put(tp, reason);
			}
		}
	}

	//returns true if tp2 is in the provenance for tp1
	private boolean containsPair(TaxonPair tp, TaxonPair tp2){
		String articulation = ".*" + tp2.getTaxon1() + " [=o<>!]+ " + tp2.getTaxon2() + ".*";
		if(provenance.get(tp).matches(articulation))
			return true;
		else
			return false;
	}

	public void printProvenance(){
		for(Map.Entry<TaxonPair, String> entry : provenance.entrySet())
			System.out.println(entry.getKey().toString() + ": " + entry.getValue());
	}

	private boolean reasonToR() throws InvalidTaxonomyException{
		String R, newR;
		R = A_to_B;

		// further specify R using children-to-parent reasoning
		if (AHasChildren){
			newR = ChildrenToParentPatterns.getRFromRelations(a1_to_B, a2_to_B);
			//System.out.println(AB.getTaxon1() + " " + newR + " " + AB.getTaxon2() + " because " + a1B.getTaxon1() + " " + a1_to_B + " " + a1B.getTaxon2() + " and " + a2B.getTaxon1() + " " + a2_to_B + " " + a2B.getTaxon2());
			R = Articulations.intersect(R, newR);
			if(R.length() == 0){
				cleanProvenance();
				String inconsistency = reasonToRInconsistency(AB, A_to_B, a1B, a1_to_B, a2B, a2_to_B);
				throw new InvalidTaxonomyException(inconsistency);
			}
			addProvenance(AB, a1B.getTaxon1(), a1_to_B, a1B.getTaxon2());
			addProvenance(AB, a2B.getTaxon1(), a2_to_B, a2B.getTaxon2());
		}

		// further specify R using parent-to-children reasoning
		if (BHasChildren){
			newR = ParentToChildrenPatterns.getRFromRelations(A_to_b1, A_to_b2);
			//System.out.println(AB.getTaxon1() + " " + newR + " " + AB.getTaxon2() + " because " + Ab1.getTaxon1() + " " + A_to_b1 + " " + Ab1.getTaxon2() + " and " + Ab2.getTaxon1() + " " + A_to_b2 + " " + Ab2.getTaxon2());
			R = Articulations.intersect(R, newR);
			if(R.length() == 0){
				cleanProvenance();
				String inconsistency = reasonToRInconsistency(AB, A_to_B, Ab1, A_to_b1, Ab2, A_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
			addProvenance(AB, Ab1.getTaxon1(), A_to_b1, Ab1.getTaxon2());
			addProvenance(AB, Ab2.getTaxon1(), A_to_b2, Ab2.getTaxon2());
		}

		// further specify R using children-to-children reasoning
		if (AHasChildren && BHasChildren){
			newR = ChildrenToChildrenPatterns.getRFromRelations(a1_to_b1, a1_to_b2, a2_to_b1, a2_to_b2);
			//System.out.println(AB.getTaxon1() + " " + newR + " " + AB.getTaxon2() + " because " + a1b1.getTaxon1() + " " + a1_to_b1 + " " + a1b1.getTaxon2() + ", " + a2b1.getTaxon1() + " " + a2_to_b1 + " " + a2b1.getTaxon2() + ", " + a1b2.getTaxon1() + " " + a1_to_b2 + " " + a1b2.getTaxon2() + ", " + a2b2.getTaxon1() + " " + a2_to_b2 + " " + a2b2.getTaxon2());
			R = Articulations.intersect(R, newR);
			if(R.length() == 0){
				cleanProvenance();
				String inconsistency = reasonToRInconsistency2(AB, A_to_B, a1b1, a1_to_b1, a1b2, a1_to_b2, a2b1, a2_to_b1, a2b2, a2_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
			addProvenance(AB, a1b1.getTaxon1(), a1_to_b1, a1b1.getTaxon2());
			addProvenance(AB, a1b2.getTaxon1(), a1_to_b2, a1b2.getTaxon2());
			addProvenance(AB, a2b1.getTaxon1(), a2_to_b1, a2b1.getTaxon2());
			addProvenance(AB, a2b2.getTaxon1(), a2_to_b2, a2b2.getTaxon2());
		}

		// if a new R was discovered, set A_to_B as the new R and return true
		if (R.length() < A_to_B.length()){
			A_to_B = R;
			return true;
		}
		return false;
	}

	private boolean reasonFromR() throws InvalidTaxonomyException{
		String[] newRelations;
		boolean foundNew = false;

		if (AHasChildren){
			// deduce the relations between the children of A and B
			newRelations = ChildrenToParentPatterns.getRelationsFromR(A_to_B, a1_to_B, a2_to_B);
			String newa1_to_B = newRelations[0];
			String newa2_to_B = newRelations[1];
			newa1_to_B = Articulations.intersect(newa1_to_B, a1_to_B);
			newa2_to_B = Articulations.intersect(newa2_to_B, a2_to_B);
			//System.out.println(a1B.getTaxon1() + " " + newa1_to_B + " " + a1B.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());
			//System.out.println(a2B.getTaxon1() + " " + newa2_to_B + " " + a2B.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newa1_to_B.length() < a1_to_B.length() && newa1_to_B.length() != 0) {
				a1_to_B = newa1_to_B;
				foundNew = true;
				addProvenance(a1B, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa1_to_B.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a1B, a1_to_B);
				throw new InvalidTaxonomyException(inconsistency);
			}
			if (newa2_to_B.length() < a2_to_B.length() && newa2_to_B.length() != 0) {
				a2_to_B = newa2_to_B;
				foundNew = true;
				addProvenance(a2B, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa2_to_B.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a2B, a2_to_B);
				throw new InvalidTaxonomyException(inconsistency);
			}
		}

		if (BHasChildren){
			// deduce the relations between A and the children of B
			newRelations = ParentToChildrenPatterns.getRelationsFromR(A_to_B, A_to_b1, A_to_b2);
			String newA_to_b1 = newRelations[0];
			String newA_to_b2 = newRelations[1];
			newA_to_b1 = Articulations.intersect(newA_to_b1, A_to_b1);
			newA_to_b2 = Articulations.intersect(newA_to_b2, A_to_b2);
			//System.out.println(Ab1.getTaxon1() + " " + newA_to_b1 + " " + Ab1.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());
			//System.out.println(Ab2.getTaxon1() + " " + newA_to_b2 + " " + Ab2.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newA_to_b1.length() < A_to_b1.length() && newA_to_b1.length() != 0) {
				A_to_b1 = newA_to_b1;
				foundNew = true;
				addProvenance(Ab1, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newA_to_b1.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, Ab1, A_to_b1);
				throw new InvalidTaxonomyException(inconsistency);
			}
			if (newA_to_b2.length() < A_to_b2.length() && newA_to_b2.length() != 0) {
				A_to_b2 = newA_to_b2;
				foundNew = true;
				addProvenance(Ab2, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newA_to_b2.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, Ab2, A_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
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

			/*System.out.println(a1b1.getTaxon1() + " " + newa1_to_b1 + " " + a1b1.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());
			System.out.println(a1b2.getTaxon1() + " " + newa1_to_b2 + " " + a1b2.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());
			System.out.println(a2b1.getTaxon1() + " " + newa2_to_b1 + " " + a2b1.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());
			System.out.println(a2b2.getTaxon1() + " " + newa2_to_b2 + " " + a2b2.getTaxon2() + " because " + AB.getTaxon1() + " " + A_to_B + " " + AB.getTaxon2());*/

			// if the deduced relations are more specific than the old, replace the old and set foundNew
			if (newa1_to_b1.length() < a1_to_b1.length() && newa1_to_b1.length() != 0) {
				a1_to_b1 = newa1_to_b1;
				foundNew = true;
				addProvenance(a1b1, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa1_to_b1.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a1b1, a1_to_b1);
				throw new InvalidTaxonomyException(inconsistency);
			}
			if (newa1_to_b2.length() < a1_to_b2.length() && newa1_to_b2.length() != 0) {
				a1_to_b2 = newa1_to_b2;
				foundNew = true;
				addProvenance(a1b2, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa1_to_b2.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a1b1, a1_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
			if (newa2_to_b1.length() < a2_to_b1.length() && newa2_to_b1.length() != 0) {
				a2_to_b1 = newa2_to_b1;
				foundNew = true;
				addProvenance(a2b1, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa2_to_b1.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a2b1, a2_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
			if (newa2_to_b2.length() < a2_to_b2.length() && newa2_to_b2.length() != 0) {
				a2_to_b2 = newa2_to_b2;
				foundNew = true;
				addProvenance(a2b2, AB.getTaxon1(), A_to_B, AB.getTaxon2());
			}
			if (newa2_to_b2.length() == 0) {
				cleanProvenance();
				String inconsistency = reasonFromRInconsistency(AB, A_to_B, a2b2, a2_to_b2);
				throw new InvalidTaxonomyException(inconsistency);
			}
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

	private String reasonToRInconsistency(TaxonPair firstPair, String firstArticulation, TaxonPair secondPair, String secondArticulation, TaxonPair thirdPair, String thirdArticulation){
		String prov1, prov2, prov3;
		if(provenance.get(firstPair) == null)
			prov1 = "Local";
		else
			prov1 = provenance.get(firstPair);
		if(provenance.get(secondPair) == null)
			prov2 = "Local";
		else
			prov2 = provenance.get(secondPair);
		if(provenance.get(thirdPair) == null)
			prov3 = "Local";
		else
			prov3 = provenance.get(thirdPair);
		String reason = "Conflict in global reasoner between ";
		reason += firstPair.getTaxon1() + " " + firstArticulation + " " + firstPair.getTaxon2() + " (" + prov1 + "), ";
		reason += secondPair.getTaxon1() + " " + secondArticulation + " " + secondPair.getTaxon2() + " (" + prov2 + "), and ";
		reason += thirdPair.getTaxon1() + " " + thirdArticulation + " " + thirdPair.getTaxon2() + " (" + prov3 + ")";
		return reason;
	}

	private String reasonToRInconsistency2(TaxonPair firstPair, String firstArticulation, TaxonPair secondPair, String secondArticulation, TaxonPair thirdPair, String thirdArticulation, TaxonPair fourthPair, String fourthArticulation, TaxonPair fifthPair, String fifthArticulation){
		String prov1, prov2, prov3, prov4, prov5;
		if(provenance.get(firstPair) == null)
			prov1 = "Local";
		else
			prov1 = provenance.get(firstPair);
		if(provenance.get(secondPair) == null)
			prov2 = "Local";
		else
			prov2 = provenance.get(secondPair);
		if(provenance.get(thirdPair) == null)
			prov3 = "Local";
		else
			prov3 = provenance.get(thirdPair);
		if(provenance.get(fourthPair) == null)
			prov4 = "Local";
		else
			prov4 = provenance.get(fourthPair);
		if(provenance.get(fifthPair) == null)
			prov5 = "Local";
		else
			prov5 = provenance.get(fifthPair);
		String reason = "Conflict in global reasoner between ";
		reason += firstPair.getTaxon1() + " " + firstArticulation + " " + firstPair.getTaxon2() + " (" + prov1 + "), ";
		reason += secondPair.getTaxon1() + " " + secondArticulation + " " + secondPair.getTaxon2() + " (" + prov2 + "), ";
		reason += thirdPair.getTaxon1() + " " + thirdArticulation + " " + thirdPair.getTaxon2() + " (" + prov3 + "), ";
		reason += fourthPair.getTaxon1() + " " + fourthArticulation + " " + fourthPair.getTaxon2() + " (" + prov4 + "), and ";
		reason += fifthPair.getTaxon1() + " " + fifthArticulation + " " + fifthPair.getTaxon2() + " (" + prov5 + ")";
		return reason;
	}

	private String reasonFromRInconsistency(TaxonPair firstPair, String firstArticulation, TaxonPair secondPair, String secondArticulation){
		String prov1, prov2;
		if(provenance.get(firstPair) == null)
			prov1 = "Local";
		else
			prov1 = provenance.get(firstPair);
		if(provenance.get(secondPair) == null)
			prov2 = "Local";
		else
			prov2 = provenance.get(secondPair);
		String reason = "Conflict in global reasoner between ";
		reason += firstPair.getTaxon1() + " " + firstArticulation + " " + firstPair.getTaxon2() + " (" + prov1 + ") and ";
		reason += secondPair.getTaxon1() + " " + secondArticulation + " " + secondPair.getTaxon2() + " (" + prov2 + ")";
		return reason;
	}

	private void cleanProvenance(){
		for(Map.Entry<TaxonPair, String> entry : provenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 2){
				if(value.substring(value.length() - 2).equals(", ")){
					value = value.substring(0, value.length() - 2);
					provenance.put(entry.getKey(), value);
				}
			}
		}
	}

	private Taxon findOriginalParent(Taxon placeholder){
		if(placeholder.isFalse())
			return findOriginalParent(placeholder.getParent());
		else
			return placeholder;
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

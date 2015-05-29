package reasoner;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

import common_classes.*;

public class LocalReasoner {
	// map from each taxon pair to the relation between those two taxa
	private Map<TaxonPair, String> articulations;
	// the list of taxon pairs over which to run the reasoner
	private List<TaxonPair> toDo = new LinkedList<TaxonPair>();
	// map from taxon pairs to the explanations of how the articulations came to be
	private Map<TaxonPair, String> provenance;
	// the boolean representing whether the local reasoner has discovered new relations
	boolean foundNew;
	private boolean isNewArticulation;
	private Map<TaxonPair, String> T1Intrarelations, T2Intrarelations;
	private String T1Namespace, T2Namespace;

	// @pre articulations not null
	public boolean runReasoner(Map<TaxonPair, String> articulations, Map<TaxonPair, String> provenance, Taxonomy T1, Taxonomy T2) throws InvalidTaxonomyException{
		this.articulations = articulations;
		this.provenance = provenance;
		T1Namespace = T1.getNamespace();
		T2Namespace = T2.getNamespace();
		T1Intrarelations = T1.setIntrarelationArticulations();
		T2Intrarelations = T2.setIntrarelationArticulations();
		fillToDoList();

		foundNew = false;
		while ( !toDo.isEmpty() )
			reasonOver(toDo.remove(0));
		return foundNew;
	}

	private void fillToDoList(){
		String articulation;
		for (TaxonPair taxonPair : articulations.keySet()){
			articulation = articulations.get(taxonPair);
			if ( (articulation != null) && (articulation.length() != 5) ){
				toDo.add(taxonPair);
			}
		}
	}

	private void reasonOver(TaxonPair taxonPair) throws InvalidTaxonomyException{
		String articulation = articulations.get(taxonPair);
		DeducibleArticulations articulationsToAssert = new DeducibleArticulations(articulation);

		// alias the variables for readability
		Taxon taxon1 = taxonPair.getTaxon1();
		Taxon taxon2 =  taxonPair.getTaxon2();
		Taxon taxon1Parent = taxon1.getParent();
		Taxon taxon2Parent =  taxon2.getParent();

		// seed the relations
		if (taxon2Parent != null){
			// assert the relations between the subject and the object's parent
			if (taxon2Parent.getChildren().size() == 1){
				// special one-child case
				assertNewArticulation(taxon1, articulation, taxon2Parent, taxon1, articulation, taxon2);
				//printProvenance(taxon1, articulation, taxon2Parent, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(taxon1, taxon2Parent), taxon1, articulation, taxon2);
			}
			else{
				assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Parent(), taxon2Parent, taxon1, articulation, taxon2);
				//printProvenance(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Parent(), taxon2Parent, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(taxon1, taxon2Parent), taxon1, articulation, taxon2);
			}

			// assert the relations between the subject and the object's siblings
			for ( Taxon objectSibling : taxon2Parent.getChildren() )
				if ( !objectSibling.equals(taxon2) ){
					assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Sibling(), objectSibling, taxon1, articulation, taxon2);
					//printProvenance(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Sibling(), objectSibling, taxon1, articulation, taxon2);
					addProvenance(new TaxonPair(taxon1, objectSibling), taxon1, articulation, taxon2);
				}
		}

		// assert the relations between the subject and the object's children
		if (taxon2.getChildren().size() == 1){
			// special one-child case
			assertNewArticulation( taxon1, articulation, taxon2.getChildren().get(0), taxon1, articulation, taxon2 );
			//printProvenance(taxon1, articulation, taxon2.getChildren().get(0), taxon1, articulation, taxon2);
			addProvenance(new TaxonPair(taxon1, taxon2.getChildren().get(0)), taxon1, articulation, taxon2);
		}
		else{
			for ( Taxon objectChild : taxon2.getChildren() ){
				assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Children(), objectChild, taxon1, articulation, taxon2);
				//printProvenance(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Children(), objectChild, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(taxon1, objectChild), taxon1, articulation, taxon2);
			}
		}

		if (taxon1Parent != null){
			// assert the relations between the subject's parent and the object
			if (taxon1Parent.getChildren().size() == 1){
				// special one-child case
				assertNewArticulation(taxon1Parent, articulation, taxon2, taxon1, articulation, taxon2);
				//printProvenance(taxon1Parent, articulation, taxon2, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(taxon1Parent, taxon2), taxon1, articulation, taxon2);
			}
			else{
				assertNewArticulation(taxon1Parent, articulationsToAssert.getArticulationBetween_t1Parent_and_t2(), taxon2, taxon1, articulation, taxon2);
				//printProvenance(taxon1Parent, articulationsToAssert.getArticulationBetween_t1Parent_and_t2(), taxon2, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(taxon1Parent, taxon2), taxon1, articulation, taxon2);
			}

			// assert the relations between the subject's siblings and the object
			for ( Taxon subjectSibling : taxon1Parent.getChildren() ){
				if ( !subjectSibling.equals(taxon1) ){
					assertNewArticulation(subjectSibling, articulationsToAssert.getArticulationBetween_t1Sibling_and_t2(), taxon2, taxon1, articulation, taxon2);
					//printProvenance(subjectSibling, articulationsToAssert.getArticulationBetween_t1Sibling_and_t2(), taxon2, taxon1, articulation, taxon2);
					addProvenance(new TaxonPair(subjectSibling, taxon2), taxon1, articulation, taxon2);
				}
			}
		}

		// assert the relations between the subject's children and the object
		if (taxon1.getChildren().size() == 1){
			// special one-child case
			assertNewArticulation(taxon1.getChildren().get(0), articulation, taxon2, taxon1, articulation, taxon2);
			//printProvenance(taxon1.getChildren().get(0), articulation, taxon2, taxon1, articulation, taxon2);
			addProvenance(new TaxonPair(taxon1.getChildren().get(0), taxon2), taxon1, articulation, taxon2);
		}
		else{
			for ( Taxon subjectChild : taxon1.getChildren() ){
				assertNewArticulation(subjectChild, articulationsToAssert.getArticulationBetween_t1Children_and_t2(), taxon2, taxon1, articulation, taxon2);
				//printProvenance(subjectChild, articulationsToAssert.getArticulationBetween_t1Children_and_t2(), taxon2, taxon1, articulation, taxon2);
				addProvenance(new TaxonPair(subjectChild, taxon2), taxon1, articulation, taxon2);
			}
		}
	}

	private void assertNewArticulation(Taxon taxon1, String newArticulation, Taxon taxon2, Taxon prevT1, String prevArticulation, Taxon prevT2) throws InvalidTaxonomyException{
		TaxonPair taxonPair = new TaxonPair(taxon1, taxon2);
		String oldArticulation = articulations.get(taxonPair);
		String deducedArticulation = Articulations.intersect(newArticulation, oldArticulation);

		// throw an exception if these two taxa have no possible articulation
		if (deducedArticulation.isEmpty()){
			cleanProvenance();
			String errorMessage = inconsistencyReason(taxon1, oldArticulation, taxon2, prevT1, prevArticulation, prevT2);
			throw new InvalidTaxonomyException(errorMessage);
		}

		// exit if the new articulation contains all the relations or is the same as the old articulation
		if ( deducedArticulation.length() == 5 || Articulations.areEqual(deducedArticulation, oldArticulation) ){
			isNewArticulation = false;
			return;
		}
		else
			isNewArticulation = true;
		foundNew = true;
		articulations.put(taxonPair, deducedArticulation);
		toDo.add(taxonPair);
	}

	private void printProvenance(Taxon dT1, String dArticulation, Taxon dT2, Taxon oT1, String oArticulation, Taxon oT2){
		System.out.println(dT1.toString() + " " + dArticulation + " " + dT2.toString() + " because " + oT1.toString() + " " + oArticulation + " " + oT2.toString());
	}

	public void printAllProvenance(){
		for(Map.Entry<TaxonPair, String> entry : provenance.entrySet()){
			System.out.println("local " + entry.getKey().getTaxon1() + " " + articulations.get(entry.getKey()) + " " + entry.getKey().getTaxon2() + ": " + entry.getValue());
		}
	}

	private String inconsistencyReason(Taxon taxon1, String articulation, Taxon taxon2, Taxon prevT1, String prevArticulation, Taxon prevT2){
		String reason = "Conflict in local reasoner between: ";
		reason += taxon1 + " " + articulation + " " + taxon2 + " ";
		reason += "(" + provenance.get(new TaxonPair(taxon1, taxon2)) + ")" + " and ";
		reason += prevT1 + " " + prevArticulation + " " + prevT2 + " " + "(" + provenance.get(new TaxonPair(prevT1, prevT2)) + ")";
		return reason;
	}

	//Adds to the provenance map if the articulation isn't Given
	private void addProvenance(TaxonPair tp, Taxon t1, String articulation, Taxon t2){
		if(isNewArticulation){
			String reason = t1.toString() + " " + articulation + " " + t2.toString() + ", ";
			if(provenance.containsKey(tp)){
				if(!provenance.get(tp).equals("Given")){
					if(!provenance.get(tp).contains(reason.substring(0, reason.length()-2)))
						provenance.put(tp, provenance.get(tp) + ", " + reason);
					else
						return;
				}
			}
			else{
				provenance.put(tp, reason);
			}
			if(tp.getTaxon1().equals(t1)){
				if(t1.getNamespace().equals(T1Namespace)){
					for(Map.Entry<TaxonPair, String> entry : T2Intrarelations.entrySet()){
						if(entry.getKey().getTaxon1().equals(t2) && entry.getKey().getTaxon2().equals(tp.getTaxon2())){
							String reason2 = entry.getKey().getTaxon1() + " " + entry.getValue() + " " + entry.getKey().getTaxon2() + ", ";
							if(!provenance.get(tp).equals("Given")){
								provenance.put(tp, provenance.get(tp) + reason2);
							}
						}
					}
				}
				else if(t1.getNamespace().equals(T2Namespace)){
					for(Map.Entry<TaxonPair, String> entry : T1Intrarelations.entrySet()){
						if(entry.getKey().getTaxon1().equals(t2) && entry.getKey().getTaxon2().equals(tp.getTaxon2())){
							String reason2 = entry.getKey().getTaxon1() + " " + entry.getValue() + " " + entry.getKey().getTaxon2() + ", ";
							if(!provenance.get(tp).equals("Given")){
								provenance.put(tp, provenance.get(tp) + reason2);
							}
						}
					}
				}
			}
			else if(tp.getTaxon2().equals(t2)){
				if(t2.getNamespace().equals(T1Namespace)){
					for(Map.Entry<TaxonPair, String> entry : T2Intrarelations.entrySet()){
						if(entry.getKey().getTaxon2().equals(t1) && entry.getKey().getTaxon1().equals(tp.getTaxon1())){
							String reason2 = entry.getKey().getTaxon1() + " " + entry.getValue() + " " + entry.getKey().getTaxon2() + ", ";
							if(!provenance.get(tp).equals("Given")){
								provenance.put(tp, provenance.get(tp) + reason2);
							}
						}
					}
				}
				else if(t2.getNamespace().equals(T2Namespace)){
					for(Map.Entry<TaxonPair, String> entry : T1Intrarelations.entrySet()){
						if(entry.getKey().getTaxon2().equals(t1) && entry.getKey().getTaxon1().equals(tp.getTaxon1())){
							String reason2 = entry.getKey().getTaxon1() + " " + entry.getValue() + " " + entry.getKey().getTaxon2() + ", ";
							if(!provenance.get(tp).equals("Given")){
								provenance.put(tp, provenance.get(tp) + reason2);
							}
						}
					}
				}
			}
		}
	}

	//Deletes (most) unncessary characters in the provenance
	private void cleanProvenance(){
		for(Map.Entry<TaxonPair, String> entry : provenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 5){
				value = value.substring(0, value.length() - 2);
				provenance.put(entry.getKey(), value);
			}
		}
	}
}

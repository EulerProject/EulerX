package reasoner;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import common_classes.*;

public class LocalReasoner {
	// map from each taxon pair to the relation between those two taxa
	private Map<TaxonPair, String> articulations;
	// the list of taxon pairs over which to run the reasoner
	private List<TaxonPair> toDo = new LinkedList<TaxonPair>();
	// the boolean representing whether the local reasoner has discovered new relations
	boolean foundNew;

	// @pre articulations not null
	public boolean runReasoner(Map<TaxonPair, String> articulations) throws InvalidTaxonomyException{
		this.articulations = articulations;
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
			if ( (articulation != null) && (articulation.length() != 5) )
				toDo.add(taxonPair);
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
			if (taxon2Parent.getChildren().size() == 1)
				// special one-child case
				assertNewArticulation(taxon1, articulation, taxon2Parent);
			else
				assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Parent(), taxon2Parent);

			// assert the relations between the subject and the object's siblings
			for ( Taxon objectSibling : taxon2Parent.getChildren() )
				if ( !objectSibling.equals(taxon2) )
					assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Sibling(), objectSibling);
		}

		// assert the relations between the subject and the object's children
		if (taxon2.getChildren().size() == 1)
			// special one-child case
			assertNewArticulation( taxon1, articulation, taxon2.getChildren().get(0) );
		else
			for ( Taxon objectChild : taxon2.getChildren() )
				assertNewArticulation(taxon1, articulationsToAssert.getArticulationBetween_t1_and_t2Children(), objectChild);

		if (taxon1Parent != null){
			// assert the relations between the subject's parent and the object
			if (taxon1Parent.getChildren().size() == 1)
				// special one-child case
				assertNewArticulation(taxon1Parent, articulation, taxon2);
			else
				assertNewArticulation(taxon1Parent, articulationsToAssert.getArticulationBetween_t1Parent_and_t2(), taxon2);

			// assert the relations between the subject's siblings and the object
			for ( Taxon subjectSibling : taxon1Parent.getChildren() )
				if ( !subjectSibling.equals(taxon1) )
					assertNewArticulation(subjectSibling, articulationsToAssert.getArticulationBetween_t1Sibling_and_t2(), taxon2);
		}

		// assert the relations between the subject's children and the object
		if (taxon1.getChildren().size() == 1)
			// special one-child case
			assertNewArticulation(taxon1.getChildren().get(0), articulation, taxon2);
		else
			for ( Taxon subjectChild : taxon1.getChildren() )
				assertNewArticulation(subjectChild, articulationsToAssert.getArticulationBetween_t1Children_and_t2(), taxon2);
	}

	private void assertNewArticulation(Taxon taxon1, String newArticulation, Taxon taxon2) throws InvalidTaxonomyException{
		TaxonPair taxonPair = new TaxonPair(taxon1, taxon2);
		String oldArticulation = articulations.get(taxonPair);
		String deducedArticulation = Articulations.intersect(newArticulation, oldArticulation);

		// throw an exception if these two taxa have no possible articulation
		if (deducedArticulation.isEmpty()){
			String errorMessage = "In local reasoner:"
					+ " the reasoner-generated relation " + newArticulation
					+ " contradicts the previous articulation " + oldArticulation
					+ " for the taxon pair " + taxonPair + ".";
			throw new InvalidTaxonomyException(errorMessage);
		}

		// exit if the new articulation contains all the relations or is the same as the old articulation
		if ( deducedArticulation.length() == 5 ||
				Articulations.areEqual(deducedArticulation, oldArticulation) )
			return;

		foundNew = true;
		articulations.put(taxonPair, deducedArticulation);
		toDo.add(taxonPair);
	}
}

package reasoner;

import java.io.IOException;
import java.io.PrintStream;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.Set;

import common_classes.*;

public class MIRReasoner {
	// map from each taxon pair to the relation between those two taxa
	private Map<TaxonPair, String> articulations;
	// the local and global reasoners
	LocalReasoner localReasoner;
	GlobalReasoner globalReasoner;
	// the taxonomies
	Taxonomy T1, T2;

	public MIRReasoner(TaxonomyInfo taxonomyFileContents){
		articulations = new LinkedHashMap<TaxonPair, String>();
		T1 = taxonomyFileContents.getT1();
		T2 = taxonomyFileContents.getT2();

		// map each taxon pair to a placeholder articulation,
		//  such that articulations.get() will never return null
		for ( Taxon t1 : T1.getAllTaxa() )
			for ( Taxon t2 : T2.getAllTaxa() )
				articulations.put(new TaxonPair(t1, t2), "<>=!o");

		// for each articulation from the taxonomy file, override "<>=!o" with the given articulation
		Taxon subjectTaxon, objectTaxon;
		for ( SimpleRelation rel : taxonomyFileContents.getInterrelations() ){
			subjectTaxon = taxonomyFileContents.getT1().getTaxon( rel.getSubjectClassname() );
			objectTaxon = taxonomyFileContents.getT2().getTaxon( rel.getObjectClassname() );
			articulations.put(
					new TaxonPair(subjectTaxon, objectTaxon),
					rel.getPredicate()
					);
		}

		localReasoner = new LocalReasoner();
		globalReasoner = new GlobalReasoner(taxonomyFileContents.getT1(), taxonomyFileContents.getT2());
	}

	public boolean runReasoner(){
		try{
			while(findNewRelations());
		} catch (InvalidTaxonomyException ex) { 
		    System.out.println(">>> Error: " + ex.getMessage());
		    articulations.clear(); 
		    return false; }

		return true;
	}

	private boolean findNewRelations() throws InvalidTaxonomyException{
		boolean localFoundNew = localReasoner.runReasoner(articulations);
		boolean globalFoundNew = globalReasoner.runReasoner(articulations);
		return localFoundNew || globalFoundNew;
	}

	public void printMIR(PrintStream output, int outputType) throws IOException{
		TaxonomyInfo.printTaxonomies(output, outputType, T1, T2, articulations);
	}

	public Set<SimpleRelation> getMIRRelations(){
		Set<SimpleRelation> MIRRelations = new LinkedHashSet<SimpleRelation>();
		for ( TaxonPair pair : articulations.keySet() )
			MIRRelations.add( new SimpleRelation(pair.getTaxon1().toString(), articulations.get(pair), pair.getTaxon2().toString()) );
		return MIRRelations;
	}
}

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
	private Map<TaxonPair, String> localProvenance;
	private Map<TaxonPair, String> globalProvenance;
	private boolean isPW;
	// the local and global reasoners
	LocalReasoner localReasoner;
	GlobalReasoner globalReasoner;
	// the taxonomies
	Taxonomy T1, T2;

	public MIRReasoner(boolean isProvenanceSet){
		articulations = new LinkedHashMap<TaxonPair, String>();
		if(!isProvenanceSet){
			localProvenance = new LinkedHashMap<TaxonPair, String>();
			globalProvenance = new LinkedHashMap<TaxonPair, String>();
		}
	}

	public MIRReasoner(TaxonomyInfo taxonomyFileContents){
		articulations = new LinkedHashMap<TaxonPair, String>();
		localProvenance = new LinkedHashMap<TaxonPair, String>();
		globalProvenance = new LinkedHashMap<TaxonPair, String>();
		setEverything(taxonomyFileContents);
	}

	public void setEverything(TaxonomyInfo taxonomyFileContents){
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
			subjectTaxon = T1.getTaxon( rel.getSubjectClassname() );
			objectTaxon = T2.getTaxon( rel.getObjectClassname() );
			articulations.put(
					new TaxonPair(subjectTaxon, objectTaxon),
					rel.getPredicate()
					);
			localProvenance.put(new TaxonPair(subjectTaxon, objectTaxon), "Given");
			globalProvenance.put(new TaxonPair(subjectTaxon, objectTaxon), "Given");
		}
		localReasoner = new LocalReasoner();
		globalReasoner = new GlobalReasoner(taxonomyFileContents.getT1(), taxonomyFileContents.getT2());
	}

	public void setEverythingPW(TaxonomyInfo original, TaxonomyInfo taxonomyFileContents, Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance){
		T1 = taxonomyFileContents.getT1();
		T2 = taxonomyFileContents.getT2();
		this.localProvenance = localProvenance;
		this.globalProvenance = globalProvenance;

		// map each taxon pair to a placeholder articulation,
		//  such that articulations.get() will never return null
		for ( Taxon t1 : T1.getAllTaxa() )
			for ( Taxon t2 : T2.getAllTaxa() )
				articulations.put(new TaxonPair(t1, t2), "<>=!o");

		// for each articulation from the taxonomy file, override "<>=!o" with the given articulation
		Taxon subjectTaxon, objectTaxon;
		for ( SimpleRelation rel : taxonomyFileContents.getInterrelations() ){
			subjectTaxon = T1.getTaxon( rel.getSubjectClassname() );
			objectTaxon = T2.getTaxon( rel.getObjectClassname() );
			articulations.put(
					new TaxonPair(subjectTaxon, objectTaxon),
					rel.getPredicate()
					);
		}
		for ( SimpleRelation rel : original.getInterrelations() ){
			subjectTaxon = T1.getTaxon( rel.getSubjectClassname() );
			objectTaxon = T2.getTaxon( rel.getObjectClassname() );
			localProvenance.put(new TaxonPair(subjectTaxon, objectTaxon), "Given");
			globalProvenance.put(new TaxonPair(subjectTaxon, objectTaxon), "Given");
		}
		localReasoner = new LocalReasoner();
		globalReasoner = new GlobalReasoner(taxonomyFileContents.getT1(), taxonomyFileContents.getT2());
	}

	public Map<TaxonPair, String> getArticulations(){return articulations;}
	public Taxonomy getT1(){return T1;}
	public Taxonomy getT2(){return T2;}

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
		boolean localFoundNew = localReasoner.runReasoner(articulations, localProvenance, T1, T2);
		boolean globalFoundNew = globalReasoner.runReasoner(articulations, globalProvenance);
		return localFoundNew || globalFoundNew;
	}

	public void printMIR(PrintStream output, int outputType, boolean isProvenance) throws IOException{
		cleanProvenance();
		TaxonomyInfo.printTaxonomies(output, outputType, T1, T2, articulations, localProvenance, globalProvenance, isProvenance);
	}

	public Set<SimpleRelation> getMIRRelations(){
		Set<SimpleRelation> MIRRelations = new LinkedHashSet<SimpleRelation>();
		for ( TaxonPair pair : articulations.keySet() )
			MIRRelations.add( new SimpleRelation(pair.getTaxon1().toString(), articulations.get(pair), pair.getTaxon2().toString()) );
		return MIRRelations;
	}

	private void cleanProvenance(){
		for(Map.Entry<TaxonPair, String> entry : localProvenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 2){
				if(value.substring(value.length() - 2).equals(", ")){
					value = value.substring(0, value.length() - 2);
					localProvenance.put(entry.getKey(), value);
				}
			}
		}
		for(Map.Entry<TaxonPair, String> entry : globalProvenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 2){
				if(value.substring(value.length() - 2).equals(", ")){
					value = value.substring(0, value.length() - 2);
					globalProvenance.put(entry.getKey(), value);
				}
			}
		}
	}

	public Map<TaxonPair, String> getLocalProvenance() { return localProvenance; }
	public Map<TaxonPair, String> getGlobalProvenance() { return globalProvenance; }
}

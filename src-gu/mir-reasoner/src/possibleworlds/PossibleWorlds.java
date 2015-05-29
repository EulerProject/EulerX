package possibleworlds;

import java.io.*;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Random;
import java.util.Iterator;
import common_classes.*;

public class PossibleWorlds{

	//The two taxonomies from the input file, which is the result
	//	of running the reasoner on a file.
	private Taxonomy inputT1, inputT2;
	//The relations from the input file.
	private List<SimpleRelation> inputRelations;
	//The input file as a TaxonomyInfo object
	private TaxonomyInfo inputResults;
	//A map of containing the index and relations of the nodes that
	//	have more than one deduced relation.
	//	The key is the index of the relations in the inputRelations list
	//	The value is an array of characters representing the multiple relations.
	private Map<Integer, char[]> multipleRelations;
	private int relationIndex;

	public PossibleWorlds(TaxonomyInfo input){
		inputResults = input;
		inputT1 = inputResults.getT1();
		inputT2 = inputResults.getT2();
		inputRelations = inputResults.getInterrelations();
		multipleRelations = setPossibleWorldsList();
		Random rn = new Random();
		if(multipleRelations.size() >= 1){
			//relationIndex = rn.nextInt(multipleRelations.size());
			relationIndex = 0;
			//relationIndex = findLongestRelation();
			//relationIndex = findMiddleIndex();
		}

	}

	//Creates the map containing the indices of multiple relations
	//	as well as the associated multiple relations
	private Map<Integer, char[]> setPossibleWorldsList(){
		Map<Integer, char[]> returnMap = new LinkedHashMap<Integer, char[]>();
		ArrayList<Integer> multRelationsIndices = findMultipleRelations(inputRelations);
		for(Integer i : multRelationsIndices){
			returnMap.put(i, inputRelations.get(i).getPredicate().toCharArray());
		}
		return returnMap;
	}

	//Searches through a list of relations and returns the indices that contain more than
	//	one relation.
	private ArrayList<Integer> findMultipleRelations(List<SimpleRelation> relations){
		ArrayList<Integer> multRelationsIndices = new ArrayList<Integer>();
		for(int i = 0; i < relations.size(); i++){
			if(relations.get(i).getPredicate().length() > 1){
				multRelationsIndices.add(i);
			}
		}
		return multRelationsIndices;
	}

	//Creates new relations for the new input file based on the chosen multiple relation.
	private List<SimpleRelation> createRelations(){
		char[] firstMultRel = multipleRelations.values().iterator().next();
		Iterator<char[]> multRelIterator = multipleRelations.values().iterator();
		Iterator<Integer> multRelKeyIterator = multipleRelations.keySet().iterator();
		for(int j = 0; j < relationIndex; j++){
			multRelIterator.next();
			multRelKeyIterator.next();
		}
		char[] chosenMultRel = multRelIterator.next();
		int index = multRelKeyIterator.next();
		List<SimpleRelation> relations = new ArrayList<SimpleRelation>();
		Taxon subjectTaxon = inputResults.getT1().getTaxon(inputRelations.get(index).getSubjectClassname());
		Taxon objectTaxon = inputResults.getT2().getTaxon(inputRelations.get(index).getObjectClassname());
		for(int i = 0; i < chosenMultRel.length; i++){
			relations.add(new SimpleRelation(subjectTaxon.toString(), chosenMultRel[i]+"", objectTaxon.toString()));
		}
		return relations;
	}

	//Creates a new input file to be run through the reasoner
	private TaxonomyInfo createNewWorld(SimpleRelation relation, TaxonomyInfo originalTI){
		List<SimpleRelation> newRelations = new ArrayList<SimpleRelation>(originalTI.getInterrelations());
		newRelations.add(relation);
		return (new TaxonomyInfo(inputT1, inputT2, newRelations));
	}

	//Creates all possible worlds.
	public ArrayList<TaxonomyInfo> createAllWorlds(TaxonomyInfo originalTI){
		ArrayList<TaxonomyInfo> allWorlds = new ArrayList<TaxonomyInfo>();
		List<SimpleRelation> newRelations = createRelations();
		for(SimpleRelation relation : newRelations){
			allWorlds.add(createNewWorld(relation, originalTI));

		}
		return allWorlds;
	}

	public long getNumWorlds(){
		long num = 1;
		for(Map.Entry<Integer, char[]> entry : multipleRelations.entrySet()){
			num *= entry.getValue().length;
		}
		return num;
	}

	public Map<TaxonPair, String> createArticulations(TaxonomyInfo input){
		LinkedHashMap<TaxonPair, String> newArticulation = new LinkedHashMap<TaxonPair, String>();
		Taxon subjectTaxon, objectTaxon;
		for(SimpleRelation s : inputRelations){
			subjectTaxon = input.getT1().getTaxon(s.getSubjectClassname());
			objectTaxon = input.getT2().getTaxon(s.getObjectClassname());
			newArticulation.put(new TaxonPair(subjectTaxon, objectTaxon), s.getPredicate());
		}
		return newArticulation;
	}

	@Override
	public String toString(){
		return inputRelations.toString();
	}

	private int findLongestRelation(){
		int index = 0;
		char[] curEntry = multipleRelations.values().iterator().next();
		int counter = 0;
		for(Map.Entry<Integer, char[]> entry : multipleRelations.entrySet()){
			if(entry.getValue().length > curEntry.length){
				index = counter;
				curEntry = entry.getValue();
			}
			counter++;
		}
		return index;
	}

	private int findMiddleIndex(){
		return (int) (multipleRelations.size() / 2);
	}
}
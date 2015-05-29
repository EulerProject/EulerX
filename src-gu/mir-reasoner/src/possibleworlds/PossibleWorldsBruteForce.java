package possibleworlds;

import java.io.*;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;

import common_classes.*;

public class PossibleWorldsBruteForce{

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

	public PossibleWorldsBruteForce(TaxonomyInfo input){
		inputResults = input;
		inputT1 = inputResults.getT1();
		inputT2 = inputResults.getT2();
		inputRelations = inputResults.getInterrelations();
		multipleRelations = setPossibleWorldsList();
	}

	//Creates the map containing the indices of multiple relations
	//	as well as the associated multiple relations
	public Map<Integer, char[]> setPossibleWorldsList(){
		Map<Integer, char[]> returnMap = new LinkedHashMap<Integer, char[]>();
		ArrayList<Integer> multRelationsIndices = findMultipleRelations(inputRelations);
		for(Integer i : multRelationsIndices){
			returnMap.put(i, inputRelations.get(i).getPredicate().toCharArray());
		}
		return returnMap;
	}

	//Searches through a list of relations and returns the indices that contain more than
	//	one relation.
	public ArrayList<Integer> findMultipleRelations(List<SimpleRelation> relations){
		ArrayList<Integer> multRelationsIndices = new ArrayList<Integer>();
		for(int i = 0; i < relations.size(); i++){
			if(relations.get(i).getPredicate().length() > 1){
				multRelationsIndices.add(i);
			}
		}
		return multRelationsIndices;
	}

	//Takes in one possible world combination and creates a new articulation based on it
	private LinkedHashMap<TaxonPair, String> createNewArticulation(Map<Integer, Character> currentCombo){
		LinkedHashMap<TaxonPair, String> newArticulation = new LinkedHashMap<TaxonPair, String>();
		Taxon subjectTaxon, objectTaxon;
		for(int i = 0; i < inputRelations.size(); i++){
			subjectTaxon = inputResults.getT1().getTaxon(inputRelations.get(i).getSubjectClassname());
			objectTaxon = inputResults.getT2().getTaxon(inputRelations.get(i).getObjectClassname());
			String predicate;
			if(currentCombo.containsKey(i)){
				predicate = currentCombo.get(i) + "";
			}
			else{
				predicate = inputRelations.get(i).getPredicate();
			}
			newArticulation.put(new TaxonPair(subjectTaxon, objectTaxon), predicate);
		}
		return newArticulation;
	}

	//Creates a new TaxonomyInfo object based on one of the possible combos
	private TaxonomyInfo createNewWorld(Map<Integer, Character> currentCombo){
		Map<TaxonPair, String> newArticulation = createNewArticulation(currentCombo);
		List<SimpleRelation> interrelations = new ArrayList<SimpleRelation>();
		for(Map.Entry<TaxonPair, String> entry : newArticulation.entrySet()){
			interrelations.add(new SimpleRelation(entry.getKey().getTaxon1().toString(), entry.getValue(), entry.getKey().getTaxon2().toString()));
		}
		return (new TaxonomyInfo(inputT1, inputT2, interrelations));
	}

	//Finds all combinations of possible worlds
	//	Creates a map with the index as the key and a relation as the value
	//	Returns a collection of all possible maps
	private Collection<Map<Integer, Character>> findAllCombos(){
		int[] counters = new int[multipleRelations.size()];
		char[][] set = createSet();
		Collection<Map<Integer, Character>> returnArray = new HashSet<Map<Integer, Character>>();
		int[] index = new int[multipleRelations.size()];
		int j = 0;
		for(Integer key : multipleRelations.keySet()){
			index[j++] = key;
		}
		do{
			returnArray.add(getCombinationMapEntry(counters, set, index));
		}
		while(increment(counters, set));
		return returnArray;
	}

	//Finds one combination of possible worlds
	//Returns a map with the index as the key and relation as the value.
	private Map<Integer, Character> getCombinationMapEntry(int[] counters, char[][] sets, int[] index){
		Map<Integer, Character> returnMap = new LinkedHashMap<Integer, Character>();
		for(int i = 0; i < counters.length; i++){
			returnMap.put(index[i], sets[i][counters[i]]);
		}
		return returnMap;
	}

	//Takes all multiple relation arrays and combines them into one 2D character array
	private char[][] createSet(){
		char[][] returnArray = new char[multipleRelations.size()][];
		int i = 0;
		for(Map.Entry<Integer, char[]> entry : multipleRelations.entrySet()){
			returnArray[i++] = entry.getValue();
		}
		return returnArray;
	}

	private char[][] createSet2(){
		char[][] returnArray = new char[2][];
		for(int i = 0; i < 2; i++){
			returnArray[i] = multipleRelations.entrySet().iterator().next().getValue();
		}
		return returnArray;
	}

	//Helper function to increment through all possible combinations of the set
	//	created by the createSet() function.
	private boolean increment(int[] counters, char[][] sets){
		for(int i = counters.length-1; i >= 0; i--){
			if(counters[i] < sets[i].length-1){
				counters[i]++;
				return true;
			}
			else{
				counters[i] = 0;
			}
		}
		return false;
	}

	//Creates all possible worlds and corresponding files.
	public ArrayList<TaxonomyInfo> createAllWorlds(){
		Collection<Map<Integer, Character>> worldCombinations = findAllCombos();
		//Collection<Map<Integer, Character>> worldCombinations = findCombosBetweenFirstTwo();
		ArrayList<TaxonomyInfo> allWorlds = new ArrayList<TaxonomyInfo>();
		int worldNumber = 0;
		for(Map<Integer, Character> elem : worldCombinations){
			allWorlds.add(createNewWorld(elem));
		}
		return allWorlds;
	}
}
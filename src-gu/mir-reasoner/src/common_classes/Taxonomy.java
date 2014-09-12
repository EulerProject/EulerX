package common_classes;

import java.io.PrintStream;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * The object, used by the seeder, containing all the internal information of one taxonomy. 
 * @author cbryan2
 */
public class Taxonomy {
				/* Class fields */

	// the namespace of the taxonomy
	private String namespace;
	// list containing the intra-taxonomical relations for this taxonomy 
	private List<SimpleRelation> intrarelations = new LinkedList<SimpleRelation>();
	// the Taxon object containing the root of the taxonomy
	private Taxon root;
	// map mapping a taxon's name to its Taxon object
	private Map<String,Taxon> taxonMap;
	// the size of the taxonomy
	private int size = 0;
	// the height of the taxonomy
	private int height = 0;


				/* Class methods */

	/** Builds the taxonomy based on the list of intrarelations.
	 * @return True if the build was successful, else false.	*/
	public Taxonomy(String namespace, List<SimpleRelation> intrarelations, String rootName){
		this.namespace = namespace;
		this.intrarelations = intrarelations;

		// if the set of intrarelations is empty, it has only one taxon
		// and the calling function should use the one-arg version of buildTaxonomy instead
		if ( intrarelations.isEmpty() )
			buildTaxonomy(rootName, namespace);

		root = buildSubtree(rootName, intrarelations);
		taxonMap = new LinkedHashMap<String,Taxon>(size+1, 1.0f);
		buildMap(root);
		setHeightAndTaxonNumbers();
	}

	/** @return True is the Taxonomy object is empty, else false.	*/
	public boolean isEmpty() { return root == null; }

	/** Returns the decomposition of this taxonomy into a binary tree.
	 *  Note: contains the intrarelations and size of the original tree. */
	public Taxonomy decompose(){
		return new Taxonomy(root.decompose(), intrarelations, size);
	}

	/** Returns the taxa which have no children. */
	public List<Taxon> getLeaves(){
		List<Taxon> leaves = new LinkedList<Taxon>();
		for (Taxon t : getAllTaxa())
			if (t.getChildren().isEmpty())
				leaves.add(t);
		return leaves;
	}

	public void printTaxonomy(PrintStream output){ // TODO for testing
		root.printTaxon(output);
	}


				/* Helper functions */

	private Taxonomy(Taxon root, List<SimpleRelation> intrarelations, int size){
		this.namespace = root.getNamespace();
		this.intrarelations = intrarelations;
		this.root = root;
		this.size = size;
		taxonMap = new LinkedHashMap<String,Taxon>();
		buildMap(root);
		setHeightAndTaxonNumbers();
	}

	/** Builds a taxonomy which has only one taxon.
	 * @param rootName The name of the root.	*/
	private void buildTaxonomy(String rootName, String namespace){
		this.namespace = namespace;
		root = new Taxon(namespace, rootName);
		size = 1;
		taxonMap.put(rootName, root);
	}

	/** Recursively builds a subtree in the taxonomy using the list of intrarelations.
	 * @param rootName The classname of the subtree's root taxon.
	 * @param intrarelations The list of the taxonomies internal relations.
	 * @return The root of the subtree, now containing the subtree's information.	*/
	private Taxon buildSubtree(String rootName, List<SimpleRelation> intrarelations){
		Taxon root = new Taxon(namespace, rootName);
		// for each internal relation
		for (SimpleRelation rel : intrarelations)
			// if the current taxon is the parent in the relation, add the subject as its child
			if ( root.getClassname().equals( rel.getObjectClassname() ) ){
				Taxon child = buildSubtree(rel.getSubjectClassname(), intrarelations);
				child.setParent(root);
				root.addChild(child);
			}
		size++;
		// return the root of the subtree
		return root;
	}

	/** Builds the taxonMap object.
	 * @param t The taxon which, along with its children, will be added to the map.	*/
	private void buildMap(Taxon t){
		if (t == null)
			return;
		taxonMap.put(t.getClassname(), t);
		for ( Taxon child : t.getChildren() )
			buildMap(child);
	}

	private void setHeightAndTaxonNumbers(){
		List<Taxon> rootList = new LinkedList<Taxon>();
		rootList.add(root);
		height = 0;
		setHeightHelper(rootList, 0);
	}

	// recursive helper function to discover the height of the tree and 
	private void setHeightHelper(List<Taxon> taxa, int level){
		if (taxa.isEmpty()){
			height = level;
			return;
		}

		List<Taxon> nextTaxa = new LinkedList<Taxon>();
		for (Taxon taxon : taxa){
			taxon.setLevel(level);
			nextTaxa.addAll(taxon.getChildren());
		}
		setHeightHelper(nextTaxa, level+1);
	}


				/* Getters and setters */

	// getter for the namespace
	public String getNamespace() { return namespace; }

	// getter for the intrarelations
	public List<SimpleRelation> getIntrarelations() { return intrarelations; }

	// getter for the individual Taxon objects
	public Taxon getTaxon(String taxonName) { return taxonMap.get(taxonName); }

	// getter for all the Taxon objects in the Taxonomy
	public List<Taxon> getAllTaxa() {
		List<Taxon> allTaxa = new LinkedList<Taxon>();
		for ( String taxonName : taxonMap.keySet() )
			allTaxa.add( taxonMap.get(taxonName) );
		return allTaxa;
	}

	// getter for the size
	public int getSize() { return size; }

	// getter for the height
	public int getHeight() { return height; }
}
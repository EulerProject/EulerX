package common_classes;

import java.io.PrintStream;
import java.util.LinkedList;
import java.util.List;

/**
 * The object, used by the Taxonomy class, containing all the information of one taxon.
 * @author cbryan2
 */
public class Taxon {
				/* Class fields */

	// the namespace and classname of the taxon
	private String namespace, classname;
	// the parent of the taxon
	private Taxon parent;
	// the children of the taxon
	private List<Taxon> children;
	// the level of the taxon in the taxonomy
	private int level = -1;
	// the flag telling whether the taxon is false
	private boolean type;

	// the variable used for the numbering system in decompose()
	private static int falseNodeNumber;


				/* Class methods */

	/** The constructor for the Taxon object.
	 * @param namespace The namespace of the taxon.
	 * @param classname The classname of the taxon.	*/
	public Taxon(String namespace, String classname){
		this.namespace = namespace;
		this.classname = classname;
		type = true;
		children = new LinkedList<Taxon>();
	}

	/** The constructor for the Taxon object.
	 * @param namespace The namespace of the taxon.
	 * @param classname The classname of the taxon.	*/
	public Taxon(String namespace, String classname, boolean type){
		this.namespace = namespace;
		this.classname = classname;
		this.type = type;
		children = new LinkedList<Taxon>();
	}

	/** Adds a child to the Taxon object's list of children.
	 * @param child The child to be added.	*/
	public void addChild(Taxon child){
		children.add(child);
	}

	/** Decomposes this Taxon object into a binary tree.
	 * @return A Taxon object which uses false nodes to become a binary tree.	*/
	public Taxon decompose(){
		falseNodeNumber = 0;
		return decomposeTaxon(null, this);
	}

	/** Prints the full taxonomy contained in this Taxon object. 
	 * @param T The Taxon object to be printed.	*/
	public void printTaxon(PrintStream output){ // TODO for testing
		String msg = toString() + " -> ";

		if (children.isEmpty()){
			output.println(msg);
			return;
		}

		else{
			msg += '(';
			for (Taxon a : children)
				msg += a + ", ";
			msg = msg.substring(0, msg.length()-2);
			output.println(msg + ')');

			for (Taxon c : children)
				c.printTaxon(output);
		}
	}


				/* Helper functions */

	private static Taxon decomposeTaxon(Taxon parent, Taxon T){
		// create the decomposed node and set its parent
		Taxon _T = new Taxon(T.getNamespace(), T.getClassname());
		_T.setParent(parent);

		// pull the children of T
		List<Taxon> children = new LinkedList<Taxon>();
		children.addAll( T.getChildren() );
		if (children.size() < 3){
			for (Taxon child : T.getChildren())
				_T.addChild(decomposeTaxon(_T, child));
			return _T;
		}

		// start with the last child in the list
		Taxon cur, last, f;
		String falseNodeName;
		int indexOfLast = children.size()-1;
		cur = children.remove(indexOfLast--);

		// while A has more than one child left
		while (children.size() > 1){
			// pull the last child in the list
			last = children.remove(indexOfLast--);
			// create a false node
			falseNodeName = "F" + falseNodeNumber + '_' + last.hashCode();
			f = new Taxon(T.getNamespace(), falseNodeName, false);
			falseNodeNumber++;
			// make last and cur the children of the false node
			f.addChild(decomposeTaxon(_T, last));
			f.addChild(cur);
			// move the false node into cur
			cur = f;
		}
		// pull the last child in the list
		last = children.get(indexOfLast);
		// add last and cur as the children of the decomposed node
		_T.addChild(decomposeTaxon(_T, last)); 
		_T.addChild(cur);

		// return the decomposed node
		return _T;
	}


				/* Getters and setters */

	// getters for the namespace and the classname
	public String getNamespace() { return namespace; }
	public String getClassname() { return classname; }

	// getter and setter for the parent
	public Taxon getParent() { return parent; };
	public void setParent(Taxon par) { parent = par; }

	// getter for the list of children
	public List<Taxon> getChildren() { return children; }

	// getter and setter for the level
	public int getLevel() { return level; }
	public void setLevel(int level) { this.level = level; }

	// getter for the isFalse flag
	public boolean isFalse() { return !type; }


				/* Redefinitions of methods inherited from Object */

	/** Returns a string containing the Taxon object's information.
	 * @return The namespace and classname of the taxon, separated by a pound sign.
	 *   Ex.: "T1#canis_lupus"	*/
	public String toString() { return namespace + '#' + classname; }

	/** Determines whether two Taxon objects are equal, based on toString().
	 * @param rhs The object with which this object is compared.
	 * @return True if toString() produces an identical string for both objects, else false.	*/
	public boolean equals(Object o) {
		if (o == null)
			return false;
		else if ( !(o instanceof Taxon) )
			return false;

		return this.toString().equals( o.toString() );
	} 

	/** Returns the hashcode of this Taxon object.
	 * @return This Taxon object's hashcode.	*/
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result
				+ ((classname == null) ? 0 : classname.hashCode());
		result = prime * result
				+ ((namespace == null) ? 0 : namespace.hashCode());
		return result;
	}
}
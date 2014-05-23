package common_classes;

/**
 * Object created by the Seeder class containing the information of a relation between two taxa (in string representation).
 * @author cbryan2
 */
public class SimpleRelation {
				/* Class fields */

	// strings representing the subject, predicate, and object of the relation
	private String subj, pred, obj;


				/* Class methods */

	/** Creates a SimpleRelation object containing a subject, predicate and object. 
	 * @param subj The string representing the subject of the relation.
	 * @param pred The string representing the predicate of the relation.
	 * @param obj The string representing the object of the relation.	*/
	public SimpleRelation(String subj, String pred, String obj){
		this.subj = subj;
		this.pred = pred;
		this.obj = obj;
	}

	/** Returns a SimpleRelation object's reverse.
	 * @return The SimpleRelation object reversed. Ex.: "A#3 =o> B#4"  returns  "B#4 =o< A#3"	*/
	public SimpleRelation reverse(){
		// reverse the direction-sensitive relation characters, if any
		// cannot use replace(); must be done simultaneously
		char[] chars = pred.toCharArray();
		for (int i=0;  i < chars.length;  i++){
			if (chars[i] == '<')
				chars[i] = '>';
			else if (chars[i] == '>')
				chars[i] = '<';
		}

		return new SimpleRelation(obj, new String(chars), subj );
	}

	/** Returns true if the relation is internal ("isa").
	 * @return True if relation is internal, else false.	*/
	public boolean isInternal() { return pred.equals("isa"); }


				/* Getters and setters */

	// getters for the subject
	public String getSubject()          { return subj; }
	public String getSubjectNamespace() { return subj.split("#")[0]; }
	public String getSubjectClassname() { return subj.split("#")[1]; }

	// getter for the predicate
	public String getPredicate() { return pred; }

	// getters for the object
	public String getObject()          { return obj; }
	public String getObjectNamespace() { return obj.split("#")[0]; }
	public String getObjectClassname() { return obj.split("#")[1]; }


				/* Redefinitions of methods inherited from Object */

	/** Returns a string containing the SimpleRelation object's information.
	 * @return The subject namespace and classname separated by a pound sign,
	 *         followed by the predicate,
	 *         followed by the object namespace and classname separated by a pound sign.
	 *         Ex.: "A#2 isa A#1"	*/
	public String toString() { return subj + " " + pred + " " + obj; }

	/** Determines whether two SimpleRelation objects are equal.
	 * @param o The object with which this object is compared.
	 * @return True if the objects relate the same two classes, else false.	*/
	public boolean equals(Object o) {
		if (o == null)
			return false;
		else if ( !(o instanceof SimpleRelation) )
			return false;

		SimpleRelation r = (SimpleRelation)o;
		return ( subj.equals(r.getSubject()) &&  obj.equals(r.getObject())  ||
				 subj.equals(r.getObject())  &&  obj.equals(r.getSubject()) );
	}

	/** Returns the hashcode for this SimpleRelation object.
	 * @return This SimpleRelation object's hashcode.	*/
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ( ((obj == null) ? 0 : obj.hashCode()) + ((subj == null) ? 0 : subj.hashCode()) );
		return result;
	}
}
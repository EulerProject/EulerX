package common_classes;

/**
 * Object created by the Seeder class containing the information of a relation between two taxa (in string representation).
 * @author cbryan2
 */
public class SimpleRelation {
				/* Class fields */

	// strings representing the subject, predicate, and object of the relation
	private String subj, subj2, subj3, pred, obj, obj2, obj3;


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

	public SimpleRelation(String subj, String subj2, String pred, String obj){
		this.subj = subj;
		this.subj2 = subj2;
		this.pred = pred;
		this.obj = obj;
	}

	public SimpleRelation(String subj, String pred, String obj, String obj2, boolean isRSum){
		this.subj = subj;
		this.pred = pred;
		this.obj = obj;
		this.obj2 = obj2;
	}

	public SimpleRelation(String subj, String subj2, String subj3, String pred, String obj){
		this.subj = subj;
		this.subj2 = subj2;
		this.subj3 = subj3;
		this.pred = pred;
		this.obj = obj;
	}

	public SimpleRelation(String subj, String pred, String obj, String obj2, String obj3, boolean isRSum){
		this.subj = subj;
		this.pred = pred;
		this.obj = obj;
		this.obj2 = obj2;
		this.obj3 = obj3;
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
	public boolean isSum() { return isLeftSum() || isRightSum(); }
	public boolean isLeftSum() { return pred.equals("l"); }
	public boolean isRightSum() { return pred.equals("r"); }
	public boolean isLeftSum3() { return pred.equals("l3"); }
	public boolean isRightSum3() { return pred.equals("r3"); }


				/* Getters and setters */

	// getters for the subject
	public String getSubject()          { return subj; }
	public String getSubjectNamespace() { return subj.split("#")[0]; }
	public String getSubjectClassname() { return subj.split("#")[1]; }
	public String getSubject2(){
		if(subj2 != null && !subj2.isEmpty())
			return subj2;
		else
			return "";
	}
	public String getSubject2Namespace(){
		if(subj2 != null && !subj2.isEmpty())
			return subj2.split("#")[0];
		else
			return "";
	}
	public String getSubject2Classname(){
		if(subj2 != null && !subj2.isEmpty())
			return subj2.split("#")[1];
		else
			return "";
	}
	public String getSubject3(){
		if(subj3 != null && !subj3.isEmpty())
			return subj3;
		else
			return "";
	}
	public String getSubject3Namespace(){
		if(subj3 != null && !subj3.isEmpty())
			return subj3.split("#")[0];
		else
			return "";
	}
	public String getSubject3Classname(){
		if(subj3 != null && !subj3.isEmpty())
			return subj3.split("#")[1];
		else
			return "";
	}

	// getter for the predicate
	public String getPredicate() { return pred; }

	// getters for the object
	public String getObject()          { return obj; }
	public String getObjectNamespace() { return obj.split("#")[0]; }
	public String getObjectClassname() { return obj.split("#")[1]; }
	public String getObject2(){
		if(obj2 != null && !obj2.isEmpty())
			return obj2;
		else
			return "";
	}
	public String getObject2Namespace(){
		if(obj2 != null && !obj2.isEmpty())
			return obj2.split("#")[0];
		else
			return "";
	}
	public String getObject2Classname(){
		if(obj2 != null && !obj2.isEmpty())
			return obj2.split("#")[1];
		else
			return "";
	}
	public String getObject3(){
		if(obj3 != null && !obj3.isEmpty())
			return obj3;
		else
			return "";
	}
	public String getObject3Namespace(){
		if(obj3 != null && !obj3.isEmpty())
			return obj3.split("#")[0];
		else
			return "";
	}
	public String getObject3Classname(){
		if(obj3 != null && !obj3.isEmpty())
			return obj3.split("#")[1];
		else
			return "";
	}


				/* Redefinitions of methods inherited from Object */

	/** Returns a string containing the SimpleRelation object's information.
	 * @return The subject namespace and classname separated by a pound sign,
	 *         followed by the predicate,
	 *         followed by the object namespace and classname separated by a pound sign.
	 *         Ex.: "A#2 isa A#1"	*/
	public String toString() {
		if(subj2 != null && !subj2.isEmpty() && subj3 == null){
			return subj + " " + subj2 + " " + pred + " " + obj;
		}
		else if(subj3 != null && !subj3.isEmpty()){
			return subj + " " + subj2 + " " + subj3 + " " + pred + " " + obj;
		}
		else if(obj2 != null && !obj2.isEmpty() && obj3 == null){
			return subj + " " + pred + " " + obj + " " + obj2;
		}
		else if(obj3 != null && !obj3.isEmpty()){
			return subj + " " + pred + " " + obj + " " + obj2 + " " + obj3;
		}
		else
			return subj + " " + pred + " " + obj;
	}

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
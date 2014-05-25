package common_classes;

public class Articulations{
	/**
	 * A string containing all valid RCC5 relation characters.
	 */
	private static final String RCC5_RELATION_CHARS = "<>=!o";

	/**
	 * @param articulation1
	 * @param articulation2
	 * @return True if the articulations contain the same RCC-5 relation characters, else false.
	 */
	public static boolean areEqual(String articulation1, String articulation2){
		if (articulation1 == null  &&  articulation2 == null)
			return true;
		else if (articulation1 == null  ||  articulation2 == null)
			return false;

		if (articulation1.length() != articulation2.length())
			return false;

		for (char r : RCC5_RELATION_CHARS.toCharArray()){
			String relation = r+"";
			if (articulation1.contains(relation) && !articulation2.contains(relation))
				return false;
			if (articulation2.contains(relation) && !articulation1.contains(relation))
				return false;
		}

		return true;
	}

	/**
	 * @param articulation1
	 * @param articulation2
	 * @return A string containing all RCC-5 relation characters which are in either articulation1 or articulation2. 
	 */
	public static String union(String articulation1, String articulation2){
		if (articulation1 == null && articulation2 == null)
			return "";
		else if (articulation1 == null)
			return articulation2;
		else if (articulation2 == null)
			return articulation1;

		String newArticulation = "";
		for (char relation : RCC5_RELATION_CHARS.toCharArray())
			if ( articulation1.contains(relation+"") || articulation2.contains(relation+"") )
				newArticulation += relation;

		return newArticulation;
	}

	/**
	 * @param articulation1
	 * @param articulation2
	 * @return A string containing all RCC-5 relation characters which are in both articulation1 and articulation2. 
	 */
	public static String intersect(String articulation1, String articulation2){
		if (articulation1 == null || articulation2 == null ||
				articulation1.isEmpty() || articulation2.isEmpty())
			return "";

		String newArticulation = "";
		for (char relation : RCC5_RELATION_CHARS.toCharArray())
			if ( articulation1.contains(relation+"") && articulation2.contains(relation+"") )
				newArticulation += relation;

		return newArticulation;
	}
}

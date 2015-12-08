package reasoner;

import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;

import common_classes.*;

public class ParentToChildrenPatterns {
	// a map which, when given the relations A_to_b1 and A_to_b2, yields the relation for A_to_B
	private static final Map<String, String> FROM_RELATIONS_TO_R = build_ToR();
	// a map which, when given the relation R, yields the relations A_to_b1 and A_to_b2
	private static final Map<String, Set<String>> FROM_R_TO_RELATIONS = build_FromR();

	// yields R from the parent-to-children relations
	public static String getRFromRelations(String A_to_b1, String A_to_b2){
		String R = "";
		for ( char r1 : A_to_b1.toCharArray() )
			for ( char r2 : A_to_b2.toCharArray() )
				R = Articulations.union(R, FROM_RELATIONS_TO_R.get(""+r1+r2));
		return R;
	}

	// yields the parent-to-children relations from R
	public static String[] getRelationsFromR(String R, String A_to_b1, String A_to_b2){
		Set<String> possiblePatterns = new HashSet<String>(25, 1.0f);
		Set<String> consistentPatterns = new HashSet<String>(25, 1.0f);
		String[] newRelations = new String[2];

		for (char relation : R.toCharArray())
			possiblePatterns.addAll(FROM_R_TO_RELATIONS.get(""+relation));

		boolean matchesPattern;
		for (String pattern : possiblePatterns){
			matchesPattern =
					A_to_b1.contains(""+pattern.charAt(0)) &&
					A_to_b2.contains(""+pattern.charAt(1));
			if (matchesPattern)
				consistentPatterns.add(pattern);
		}

		String new_A_to_b1 = "";
		String new_A_to_b2 = "";
		for (String pattern : consistentPatterns){
			new_A_to_b1 += Articulations.union(new_A_to_b1, ""+pattern.charAt(0));
			new_A_to_b2 += Articulations.union(new_A_to_b2, ""+pattern.charAt(1));
		}

		newRelations[0] = new_A_to_b1;
		newRelations[1] = new_A_to_b2;

		return newRelations;
	}

	// builds the map FROM_RELATIONS_TO_R
	private static Map<String, String> build_ToR(){
		Map<String, String> to_R = new HashMap<String, String>(25, 1.0f);
		to_R.put("<<", "");   // (<,<) ->  inconsistent
		to_R.put("<>", "");   // (<,>) ->  inconsistent
		to_R.put("<=", "");   // (<,=) ->  inconsistent
		to_R.put("<!", "<");  // (<,!) ->  <
		to_R.put("<o", "");   // (<,o) ->  inconsistent
		to_R.put("><", "");   // (>,<) ->  inconsistent
		to_R.put(">>", ">="); // (>,>) ->  >=
		to_R.put(">=", "");   // (>,=) ->  inconsistent
		to_R.put(">!", "o");  // (>,!) ->  o
		to_R.put(">o", "<o"); // (>,o) ->  <o
		to_R.put("=<", "");   // (=,<) ->  inconsistent
		to_R.put("=>", "");   // (=,>) ->  inconsistent
		to_R.put("==", "");   // (=,=) ->  inconsistent
		to_R.put("=!", "<");  // (=,!) ->  <
		to_R.put("=o", "");   // (=,o) ->  inconsistent
		to_R.put("!<", "<");  // (!,<) ->  <
		to_R.put("!>", "o");  // (!,>) ->  o
		to_R.put("!=", "<");  // (!,=) ->  <
		to_R.put("!!", "!");  // (!,!) ->  !
		to_R.put("!o", "o");  // (!,o) ->  o
		to_R.put("o<", "");   // (o,<) ->  inconsistent
		to_R.put("o>", "<o"); // (o,>) ->  <o
		to_R.put("o=", "");   // (o,=) ->  inconsistent
		to_R.put("o!", "o");  // (o,!) ->  o
		to_R.put("oo", "<o"); // (o,o) ->  <o
		return to_R;
	}

	// builds the map FROM_R_TO_RELATIONS
	private static Map<String, Set<String>> build_FromR(){
		Map<String, Set<String>> fromR = new HashMap<String, Set<String>>(5, 1.0f);
		fromR.put("<", getProperPartPatterns());
		fromR.put(">", getInverseProperPartPatterns());
		fromR.put("=", getEqualsPatterns());
		fromR.put("!", getDisjointPatterns());
		fromR.put("o", getOverlapsPatterns());
		return fromR;
	}

	private static Set<String> getProperPartPatterns(){
		Set<String> properPartPatterns = new HashSet<String>(7, 1.0f);
		properPartPatterns.add("<!");
		properPartPatterns.add(">o");
		properPartPatterns.add("=!");
		properPartPatterns.add("!<");
		properPartPatterns.add("!=");
		properPartPatterns.add("o>");
		properPartPatterns.add("oo");
		return properPartPatterns;
	}

	private static Set<String> getInverseProperPartPatterns(){
		Set<String> inverseProperPartPatterns = new HashSet<String>(1, 1.0f);
		inverseProperPartPatterns.add(">>");
		return inverseProperPartPatterns;
	}

	private static Set<String> getEqualsPatterns(){
		Set<String> equalsPatterns = new HashSet<String>(1, 1.0f);
		equalsPatterns.add(">>");
		return equalsPatterns;
	}

	private static Set<String> getDisjointPatterns(){
		Set<String> disjointPatterns = new HashSet<String>(1, 1.0f);
		disjointPatterns.add("!!");
		return disjointPatterns;
	}

	private static Set<String> getOverlapsPatterns(){
		Set<String> overlapsPatterns = new HashSet<String>(7, 1.0f);
		overlapsPatterns.add(">!");
		overlapsPatterns.add(">o");
		overlapsPatterns.add("!o");
		overlapsPatterns.add("!>");
		overlapsPatterns.add("o>");
		overlapsPatterns.add("o!");
		overlapsPatterns.add("oo");
		return overlapsPatterns;
	}
}

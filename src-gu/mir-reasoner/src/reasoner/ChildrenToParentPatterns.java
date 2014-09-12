package reasoner;

import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;

import common_classes.*;

public class ChildrenToParentPatterns {
	// a map which, when given the relations a1_to_B and a2_to_B, yields the relation for A_to_B
	private static final Map<String, String> FROM_RELATIONS_TO_R = build_ToR();
	// a map which, when given the relation R, yields the relations a1_to_B and a2_to_B
	private static final Map<String, Set<String>> FROM_R_TO_RELATIONS = build_FromR();

	// yields R from the children-to-parent relations
	public static String getRFromRelations(String a1_to_B, String a2_to_B){
		String R = "";
		for ( char r1 : a1_to_B.toCharArray() )
			for ( char r2 : a2_to_B.toCharArray() )
				R = Articulations.union(R, FROM_RELATIONS_TO_R.get(""+r1+r2));
		return R;
	}

	// yields the children-to-parent relations from R
	public static String[] getRelationsFromR(String R, String a1_to_B, String a2_to_B){
		Set<String> possiblePatterns = new HashSet<String>(25, 1.0f);
		Set<String> consistentPatterns = new HashSet<String>(25, 1.0f);
		String[] newRelations = new String[2];

		for (char relation : R.toCharArray())
			possiblePatterns.addAll(FROM_R_TO_RELATIONS.get(""+relation));

		boolean matchesPattern;
		for (String pattern : possiblePatterns){
			matchesPattern =
					a1_to_B.contains(""+pattern.charAt(0)) &&
					a2_to_B.contains(""+pattern.charAt(1));
			if (matchesPattern)
				consistentPatterns.add(pattern);			
		}

		String new_a1_to_B = "";
		String new_a2_to_B = "";
		for (String pattern : consistentPatterns){
			new_a1_to_B += Articulations.union(new_a1_to_B, ""+pattern.charAt(0));
			new_a2_to_B += Articulations.union(new_a2_to_B, ""+pattern.charAt(1));
		}

		newRelations[0] = new_a1_to_B;
		newRelations[1] = new_a2_to_B;

		return newRelations;
	}

	// builds the map FROM_RELATIONS_TO_R
	private static Map<String, String> build_ToR(){
		Map<String, String> to_R = new HashMap<String, String>(25, 1.0f);
		to_R.put("<<","<=");  // (<,<) ->  <=
		to_R.put("<>", "");   // (<,>) ->  inconsistent
		to_R.put("<=", "");   // (<,=) ->  inconsistent
		to_R.put("<!", "o");  // (<,!) ->  o
		to_R.put("<o", ">o"); // (<,o) ->  >o
		to_R.put("><", "");   // (>,<) ->  inconsistent
		to_R.put(">>", "");   // (>,>) ->  inconsistent
		to_R.put(">=", "");   // (>,=) ->  inconsistent
		to_R.put(">!", ">");  // (>,!) ->  >
		to_R.put(">o", "");   // (>,o) ->  inconsistent
		to_R.put("=<", "");   // (=,<) ->  inconsistent
		to_R.put("=>", "");   // (=,>) ->  inconsistent
		to_R.put("==", "");   // (=,=) ->  inconsistent
		to_R.put("=!", ">");  // (=,!) ->  >
		to_R.put("=o", "");   // (=,o) ->  inconsistent
		to_R.put("!<", "o");  // (!,<) ->  o
		to_R.put("!>", ">");  // (!,>) ->  >
		to_R.put("!=", ">");  // (!,=) ->  >
		to_R.put("!!", "!");  // (!,!) ->  !
		to_R.put("!o", "o");  // (!,o) ->  o
		to_R.put("o<", ">o"); // (o,<) ->  >o
		to_R.put("o>", "");   // (o,>) ->  inconsistent
		to_R.put("o=", "");   // (o,=) ->  inconsistent
		to_R.put("o!", "o");  // (o,!) ->  o
		to_R.put("oo", ">o"); // (o,o) ->  >o
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
		Set<String> properPartPatterns = new HashSet<String>(1, 1.0f);
		properPartPatterns.add("<<");
		return properPartPatterns;
	}

	private static Set<String> getInverseProperPartPatterns(){
		Set<String> inverseProperPartPatterns = new HashSet<String>(7, 1.0f);
		inverseProperPartPatterns.add("<o");
		inverseProperPartPatterns.add(">!");
		inverseProperPartPatterns.add("=!");
		inverseProperPartPatterns.add("!>");
		inverseProperPartPatterns.add("!=");
		inverseProperPartPatterns.add("o<");
		inverseProperPartPatterns.add("oo");
		return inverseProperPartPatterns;
	}

	private static Set<String> getEqualsPatterns(){
		Set<String> equalsPatterns = new HashSet<String>(1, 1.0f);
		equalsPatterns.add("<<");
		return equalsPatterns;
	}

	private static Set<String> getDisjointPatterns(){
		Set<String> disjointPatterns = new HashSet<String>(1, 1.0f);
		disjointPatterns.add("!!");
		return disjointPatterns;
	}

	private static Set<String> getOverlapsPatterns(){
		Set<String> overlapsPatterns = new HashSet<String>(7, 1.0f);
		overlapsPatterns.add("<!");
		overlapsPatterns.add("<o");
		overlapsPatterns.add("!<");
		overlapsPatterns.add("!o");
		overlapsPatterns.add("o<");
		overlapsPatterns.add("o!");
		overlapsPatterns.add("oo");
		return overlapsPatterns;
	}
}

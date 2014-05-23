package common_classes;

import java.io.PrintStream;
import java.util.List;
import java.util.Map;

public class TaxonomyInfo {
				/* Class fields */

	// the two taxonomies
	private Taxonomy T1;
	private Taxonomy T2;

	// list of the inter-taxonomical relations
	private List<SimpleRelation> interrelations;


				/* Class methods */
	
	public TaxonomyInfo(Taxonomy T1, Taxonomy T2, List<SimpleRelation> interrelations){
		this.T1 = T1;
		this.T2 = T2;
		this.interrelations = interrelations;
	}


				/* Getters */

	// getters for the taxonomies
	public Taxonomy getT1() { return T1; }
	public Taxonomy getT2() { return T2; }

	// getter for the interrelations
	public List<SimpleRelation> getInterrelations() { return interrelations; }

	/** Prints the taxonomies and their interrelations to the given output with the given formatting. */
	public static void printTaxonomies(PrintStream output, int outputType, Taxonomy T1, Taxonomy T2, Map<TaxonPair, String> articulations){
		if (outputType == Parser.SPECIAL)
			printSpecialFormat(output, T1, T2, articulations);
		else if (outputType == Parser.STANDARD)
			printStandardFormat(output, T1, T2, articulations);
		else
			System.out.println("Invalid output type.");
	}

	private static void printSpecialFormat(PrintStream output, Taxonomy T1, Taxonomy T2, Map<TaxonPair, String> articulations){
		// write out the first taxonomy
		for (SimpleRelation intrarelation : T1.getIntrarelations()){
			output.println(intrarelation);
			output.flush();
		}
		output.println();

		// write out the second taxonomy
		for (SimpleRelation intrarelation : T2.getIntrarelations()){
			output.println(intrarelation);
			output.flush();
		}
		output.println();

		// write out the interrelations
		String relation;
		for (TaxonPair taxonPair : articulations.keySet()){
			String articulation = articulations.get(taxonPair);
			if (Articulations.areEqual(articulation, "<>=!o"))
				continue;

			relation = taxonPair.getTaxon1() + " ";
			relation += formatSpecialArticulation(articulation);
			relation += " " + taxonPair.getTaxon2();

			output.print(relation);
			output.println();
			output.flush();
		}

	}

	private static void printStandardFormat(PrintStream output, Taxonomy T1, Taxonomy T2,  Map<TaxonPair, String> articulations){
		output.println("taxonomy " + T1.getNamespace() + " " + T1.getNamespace());
		List<Taxon> t1Children;
		String line;
		for (Taxon t1 : T1.getAllTaxa()){
			line = "";
			t1Children = t1.getChildren();
			if (t1Children.isEmpty())
				continue;
			else{
				line += "(" + t1.getClassname() + " ";
				for (Taxon t1Child : t1Children)
					line += t1Child.getClassname() + " ";
				line = line.substring(0, line.length()-1);
				line += ')';
			}
			output.println(line);
		}
		output.println();

		output.println("taxonomy " + T2.getNamespace() + " " + T2.getNamespace());
		List<Taxon> t2Children;
		for (Taxon t2 : T2.getAllTaxa()){
			line = "";
			t2Children = t2.getChildren();
			if (t2Children.isEmpty())
				continue;
			else{
				line += "(" + t2.getClassname() + " ";
				for (Taxon t2Child : t2Children)
					line += t2Child.getClassname() + " ";
				line = line.substring(0, line.length()-1);
				line += ')';
			}
			output.println(line);
		}
		output.println();

		output.println("articulation " +
				T1.getNamespace() + T2.getNamespace() + " " +
				T1.getNamespace() + T2.getNamespace());
		String subject, articulation, object;
		for (TaxonPair pair : articulations.keySet()){
			articulation = articulations.get(pair);
			if (Articulations.areEqual(articulation, "<>=!o"))
				continue;

			subject = '[' + pair.getTaxon1().toString().replace('#', '.');
			object =  pair.getTaxon2().toString().replace('#', '.') + ']';
			articulation = formatStandardArticulation(articulation);
			output.println(subject + " " + articulation + " " + object);
		}
	}

	private static String formatSpecialArticulation(String articulation){
		String formattedArticulation = "{";
		for (char r : articulation.toCharArray())
			formattedArticulation += r + ",";
		formattedArticulation = formattedArticulation.substring(0, formattedArticulation.length()-1);
		formattedArticulation += '}';
		return formattedArticulation;
	}

	private static String formatStandardArticulation(String articulation){
		String formattedArticulation = "";

		if (articulation.contains("<"))
			formattedArticulation += "is_included_in ";
		if (articulation.contains(">"))
			formattedArticulation += "includes ";
		if (articulation.contains("="))
			formattedArticulation += "equals ";
		if (articulation.contains("!"))
			formattedArticulation += "disjoint ";
		if (articulation.contains("o"))
			formattedArticulation += "overlaps ";

		formattedArticulation = formattedArticulation.substring(0, formattedArticulation.length()-1);
		if (articulation.length() > 1)
			return '{' + formattedArticulation + '}';
		else
			return formattedArticulation;
	}
}

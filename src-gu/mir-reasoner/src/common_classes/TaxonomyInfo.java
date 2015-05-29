package common_classes;

import java.io.PrintStream;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

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
		handleSums();
	}


				/* Getters */

	// getters for the taxonomies
	public Taxonomy getT1() { return T1; }
	public Taxonomy getT2() { return T2; }

	// getter for the interrelations
	public List<SimpleRelation> getInterrelations() { return interrelations; }

	private void handleSums(){
		for(int i = 0; i < interrelations.size(); i++){
			SimpleRelation sr = interrelations.get(i);
			if(!sr.getSubject2().isEmpty() && sr.getSubject3().isEmpty()){
				handleLeftSum(sr);
				interrelations.remove(i--);
			}
			else if(!sr.getObject2().isEmpty() && sr.getObject3().isEmpty()){
				handleRightSum(sr);
				interrelations.remove(i--);
			}
			else if(!sr.getSubject3().isEmpty()){
				handleLeftSum3(sr);
				interrelations.remove(i--);
			}
			else if(!sr.getObject3().isEmpty()){
				handleRightSum3(sr);
				interrelations.remove(i--);
			}
		}
	}

	private void handleLeftSum(SimpleRelation sr){
		interrelations.add(new SimpleRelation(sr.getSubject() + "_" + sr.getSubject2Classname(), "=", sr.getObject()));
	}

	private void handleLeftSum3(SimpleRelation sr){
		interrelations.add(new SimpleRelation(sr.getSubject() + "_" + sr.getSubject2Classname() + "_" + sr.getSubject3Classname(), "=", sr.getObject()));
	}

	private void handleRightSum(SimpleRelation sr){
		interrelations.add(new SimpleRelation(sr.getSubject(), "=", sr.getObject() + "_" + sr.getObject2Classname()));
	}

	private void handleRightSum3(SimpleRelation sr){
		interrelations.add(new SimpleRelation(sr.getSubject(), "=", sr.getObject() + "_" + sr.getObject2Classname() + "_" + sr.getObject3Classname()));
	}

	/** Prints the taxonomies and their interrelations to the given output with the given formatting. */
	public static void printTaxonomies(PrintStream output, int outputType, Taxonomy T1, Taxonomy T2, Map<TaxonPair, String> articulations, Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance, boolean isProvenance){
		if (outputType == Parser.SPECIAL)
			printSpecialFormat(output, T1, T2, articulations, localProvenance, globalProvenance, false, isProvenance);
		else if (outputType == Parser.STANDARD)
			printStandardFormat(output, T1, T2, articulations, localProvenance, globalProvenance, false, isProvenance);
		else
			System.out.println("Invalid output type.");
	}

	/** Prints the interrelations of possible worlds to the given output with the given formatting. */
	public static void printTaxonomiesPW(PrintStream output, int outputType, Taxonomy T1, Taxonomy T2, Map<TaxonPair, String> articulations,  Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance, int worldNum, boolean isProvenance){
		cleanProvenance(localProvenance, globalProvenance);
		if (outputType == Parser.SPECIAL){
			output.println("\nPossible World " + worldNum + "\n");
			printSpecialFormat(output, T1, T2, articulations, localProvenance, globalProvenance, true, isProvenance);
		}
		else if (outputType == Parser.STANDARD){
			output.println("\nPossible World " + worldNum + "\n");
			printStandardFormat(output, T1, T2, articulations, localProvenance, globalProvenance, true, isProvenance);
		}
		else
			System.out.println("Invalid output type.");
	}

	private static void printSpecialFormat(PrintStream output, Taxonomy T1, Taxonomy T2, Map<TaxonPair, String> articulations,  Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance, boolean isPW, boolean isProvenance){
		if(!isPW){
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
		}

		// write out the interrelations
		String relation;
		for (TaxonPair taxonPair : articulations.keySet()){
			String articulation = articulations.get(taxonPair);
			if (Articulations.areEqual(articulation, "<>=!o"))
				continue;

			relation = taxonPair.getTaxon1() + " ";
			relation += formatSpecialArticulation(articulation);
			relation += " " + taxonPair.getTaxon2();

			if(isProvenance)
				output.printf("%-40s", relation);
			else
				output.print(relation);
			if(isProvenance){
				String provenance = getProvenance(taxonPair, localProvenance, true);
				provenance += " " + getProvenance(taxonPair, globalProvenance, false);
				output.printf("%s%n", provenance);
			}
			else
				output.printf("%n");
			output.flush();
		}

	}

	private static void printStandardFormat(PrintStream output, Taxonomy T1, Taxonomy T2,  Map<TaxonPair, String> articulations,  Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance, boolean isPW, boolean isProvenance){
		if(!isPW){
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
		}

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
			String relation = subject + " " + articulation + " " + object;
			if(isProvenance)
				output.printf("%-40s", relation);
			else
				output.print(relation);
			if(isProvenance){
				String provenance = getProvenance(pair, localProvenance, true);
				provenance += " " + getProvenance(pair, globalProvenance, false);
				output.printf("%s%n", provenance);
			}
			else
				output.printf("%n");
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

	private static String getProvenance(TaxonPair tp, Map<TaxonPair, String> provenance, boolean isLocal){
		String returnString = new String();
		if(provenance.containsKey(tp)){
			if(isLocal)
				returnString = "Local: ";
			else
				returnString = "Global: ";
			returnString += provenance.get(tp);
			return returnString;
		}
		else
			return "";
	}

	private static void cleanProvenance(Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance){
		for(Map.Entry<TaxonPair, String> entry : localProvenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 2){
				if(value.substring(value.length() - 2).equals(", ")){
					value = value.substring(0, value.length() - 2);
					localProvenance.put(entry.getKey(), value);
				}
			}
		}
		for(Map.Entry<TaxonPair, String> entry : globalProvenance.entrySet()){
			String value = entry.getValue();
			if(value.length() > 2){
				if(value.substring(value.length() - 2).equals(", ")){
					value = value.substring(0, value.length() - 2);
					globalProvenance.put(entry.getKey(), value);
				}
			}
		}
	}
}

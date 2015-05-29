package reasoner;

import java.io.*;

import common_classes.*;
import possibleworlds.*;
import java.util.ArrayList;
import java.util.Map;
import java.util.List;

public class ApplyMIRReasonerPW {

	private static int worldNum = 1;
	private static int cons = 1;
	private static long maxWorlds;
	private static boolean isProvenance;

	//Applies the MIRReasoner to the possible worlds problem using recursion
	public static void main(String[] args) {
		if (args.length != 5){
			System.out.println("USAGE ERROR: ApplyMIRReasonerPW input_filename input_type output_filename output_type provenance_flag");
			return;
		}

		else if (!isFormatType(args[1])){
			System.out.println("Usage Error: input type must be either \"special\" or \"standard.\"");
			return;
		}

		else if (args.length == 5 && !isFormatType(args[3])){
			System.out.println("Usage Error: output type must be either \"special\" or \"standard.\"");
			return;
		}
		//if(args.length == 6){
		//	maxWorlds = Integer.parseInt(args[5]);
		//}
		isProvenance = Boolean.valueOf(args[4]);
		try{
			Parser parser = new Parser(args[0], getFormatType(args[1]));
			TaxonomyInfo original = parser.getTaxonomyContents();
			MIRReasoner reasoner = new MIRReasoner(original);
			boolean isConsistent;

			if (!reasoner.runReasoner()){
				isConsistent = false;
				System.out.println("Inconsistent");
			}
			else{
				isConsistent = true;
				System.out.println("Consistent");
			}
			if (args.length == 5 || args.length == 6){
				reasoner.printMIR(new PrintStream(args[2]), getFormatType(args[3]), isProvenance);
				if(isConsistent){
					Parser outputParser = new Parser(args[2], getFormatType(args[3]));
					PossibleWorlds pw = new PossibleWorlds(outputParser.getTaxonomyContents());
					long numWorlds = pw.getNumWorlds();
					maxWorlds = numWorlds;
					if(numWorlds != 1){
						ArrayList<TaxonomyInfo> worlds = pw.createAllWorlds(original);
						FileOutputStream fos = new FileOutputStream(args[2], true);
						PrintStream output = new PrintStream(fos);
						for(TaxonomyInfo ti : worlds){
							MIRReasoner reasonerPW = new MIRReasoner(ti);
							if(!reasonerPW.runReasoner()){}
							else{
								runPW(ti, createTaxonomyInfo(reasonerPW.getArticulations(), reasoner.getT1(), reasoner.getT2()), output, args[3], reasonerPW.getLocalProvenance(), reasonerPW.getGlobalProvenance());
							}
						}
					}
				}
			}
		}
		catch(IOException ex1){
			System.out.println("Error: failed to access one of the given files.");
			System.out.println(ex1.getMessage());
		}
		catch(InvalidTokenException ex2){
			System.out.println("Error: file contains incorrect syntax.");
			System.out.println(ex2.getMessage());
		}
	}

	private static boolean isFormatType(String formatType){
		return formatType.equals("special") || formatType.equals("standard");
	}

	private static int getFormatType(String formatType){
		if (formatType.equals("special"))
			return Parser.SPECIAL;
		else
			return Parser.STANDARD;
	}

	//Recursive function to find all possible worlds
	private static void runPW(TaxonomyInfo original, TaxonomyInfo input, PrintStream output, String outputType, Map<TaxonPair, String> localProvenance, Map<TaxonPair, String> globalProvenance) throws IOException{
		MIRReasoner reasoner = new MIRReasoner(true);
		PossibleWorlds pw = new PossibleWorlds(input);
		long numWorlds = pw.getNumWorlds();
		//if(numWorlds != 1 && maxWorlds > 0){
		if(numWorlds != 1){
			ArrayList<TaxonomyInfo> worlds = pw.createAllWorlds(input);
			for(TaxonomyInfo ti : worlds){
				reasoner.setEverythingPW(original, ti, localProvenance, globalProvenance);
				if(!reasoner.runReasoner()){}
				else{
					runPW(original, createTaxonomyInfo(reasoner.getArticulations(), reasoner.getT1(), reasoner.getT2()), output, outputType, reasoner.getLocalProvenance(), reasoner.getGlobalProvenance());
				}
			}
		}
		else{
			//if(maxWorlds > 0)
				input.printTaxonomiesPW(output, getFormatType(outputType), input.getT1(), input.getT2(), pw.createArticulations(input), localProvenance, globalProvenance, worldNum++, isProvenance);
			//maxWorlds--;
		}
	}

	//Creates a new "input file" to run through the reasoner.
	//This new input file contains a new articulation and is meant to reason down to the most deduced it can be.
	private static TaxonomyInfo createTaxonomyInfo(Map<TaxonPair, String> articulations, Taxonomy inputT1, Taxonomy inputT2){
		List<SimpleRelation> interrelations = new ArrayList<SimpleRelation>();
		for(Map.Entry<TaxonPair, String> entry : articulations.entrySet()){
			interrelations.add(new SimpleRelation(entry.getKey().getTaxon1().toString(), entry.getValue(), entry.getKey().getTaxon2().toString()));
		}
		return (new TaxonomyInfo(inputT1, inputT2, interrelations));
	}
}

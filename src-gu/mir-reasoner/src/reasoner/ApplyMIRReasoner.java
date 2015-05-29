package reasoner;

import java.io.IOException;
import java.io.PrintStream;

import common_classes.*;

public class ApplyMIRReasoner {

    public static void main(String[] args) {
		if(args.length != 2 && args.length != 3 && args.length != 4){
		    System.out.println("USAGE: ApplyMIRReasoner input_filename input_type [output_filename] provenance_flag");
		    return;
		}
		else if(!isInputType(args[1])) {
		    System.out.println("USAGE: output type must be either \"special\" or \"standard.\"");
		    return;
		}
		
		try{
		    Parser parser = new Parser(args[0], getInputType(args[1]));
		    MIRReasoner reasoner = new MIRReasoner(parser.getTaxonomyContents());
		    
		    if (!reasoner.runReasoner())
				System.out.println("Inconsistent");
		    else
				System.out.println("Consistent");

		    if (args.length == 4)
			// reasoner.printMIR(args[2]);
			reasoner.printMIR(new PrintStream(args[2]), getInputType(args[1]), Boolean.valueOf(args[3]));
		} catch(IOException ex1){
		    System.out.println("ERROR: failed to access one of the given files.");
		    System.out.println(ex1.getMessage());
		} catch(InvalidTokenException ex2){
		    System.out.println("ERROR: file contains incorrect syntax.");
		    System.out.println(ex2.getMessage());
		}
    }

    private static boolean isInputType(String inputType){
		return inputType.equals("special") || inputType.equals("standard");
    }

    private static int getInputType(String inputType){
		if (inputType.equals("special"))
		    return Parser.SPECIAL;
		else
		    return Parser.STANDARD;
    }
}

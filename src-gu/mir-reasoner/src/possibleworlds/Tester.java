package possibleworlds;

import java.io.PrintStream;
import java.io.IOException;

import common_classes.*;

public class Tester{

	//arguments: input_file output_file
	public static void main(String[] args){
		try{
			Parser parser = new Parser(args[0], Parser.STANDARD);
			TaxonomyInfo original = parser.getTaxonomyContents();
			PossibleWorlds pw = new PossibleWorlds(original);
			PrintStream out = new PrintStream(args[1]);
			pw.createAllWorlds(original);
		}
		catch(IOException e){
			System.out.println("Failed on file operation");
			System.out.println(e.getMessage());
		}
		catch(InvalidTokenException e){
			System.out.println("Invalid Syntax");
			System.out.println(e.getMessage());
		}
	}
}
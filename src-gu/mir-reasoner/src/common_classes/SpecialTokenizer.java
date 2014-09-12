package common_classes;

import java.io.*;
import java.util.List;
import java.util.LinkedList;
import java.util.Scanner;

/** Tokenizer is used to convert an input file into a series of Tokens, 
 * which can then be parsed and evaluated
 */
class SpecialTokenizer{
	private int lineNumber;
	private List<Token> tokenStream = new LinkedList<Token>();



	public void tokenize(File in) throws IOException, InvalidTokenException{
		lineNumber = 1;
		Scanner input = new Scanner(in); // TODO change to BufferedReader

		while ( input.hasNextLine() )
			addLineToTokenStream( input.nextLine().split("[ ]+") );

		input.close();
	}


				/* Helper functions */

	/** Tokenizes and adds a given line of input to the token stream as tokens
	 * @param line The line of the input file to tokenize and add
	 */
	private void addLineToTokenStream(String[] line) throws InvalidTokenException{
		boolean foundSubjectCandidate = false;
		boolean foundPredicateCandidate = false;
		boolean foundObjectCandidate = false;

		for (int i=0;  i < line.length;  i++){
			// renamed for the purpose of readability
			String curToken = line[i];
			// remove whitespace (spaces and newlines have already been handled)
			curToken = curToken.replace("\t","");

			if ( curToken.isEmpty() )
				continue;
			
			else if (!foundSubjectCandidate){
				foundSubjectCandidate = true;
				if ( isClassToken(curToken) )
					tokenStream.add(new ClassToken(lineNumber, curToken));
				else
					throw new InvalidTokenException("Invalid Subject", lineNumber, curToken);
			}

			else if (!foundPredicateCandidate){
				foundPredicateCandidate = true;
				if ( isRelationToken(curToken) )
					tokenStream.add(new RelationToken(lineNumber, curToken));
				else
					throw new InvalidTokenException("Invalid Predicate", lineNumber, curToken);
			}

			else if (!foundObjectCandidate){
				foundObjectCandidate = true;
				if ( isClassToken(curToken) )
					tokenStream.add(new ClassToken(lineNumber, curToken));
				else
					throw new InvalidTokenException("Invalid Object", lineNumber, curToken);
			}

			else
				throw new InvalidTokenException("Too many tokens: ", lineNumber, curToken);
		}
		
		if (foundSubjectCandidate && !foundObjectCandidate)
			throw new InvalidTokenException("Too few tokens: ", lineNumber, " beginning with " + line[0]);

		lineNumber++;
	}

	/** Returns true if the given string represents a relation token,
	 *  otherwise returns false.
	 * @param value The string being tested
	 * @return true if value represents a relation token, else false
	 */
	private static boolean isRelationToken(String value){
		// a relation token must be three or more characters
		if (value.length() < 3)
			return false;

		// special case of isA
		if ( value.toLowerCase().equals("isa") )
			return true;

		char[] valueArray = value.toCharArray();

		// a relation token (which is not isA) must begin and end with brackets
		if (valueArray[0] != '{')
			return false;
		
		else if (valueArray[valueArray.length - 1] != '}')
			return false;

		// relation tokens must have valid characters,
		// at most one of each relation,
		// and commas separating the relations
		String validRelationChars = "<>=!o";
		for (int i=1;  i < valueArray.length-1;  i++){
			if ( validRelationChars.contains("" + valueArray[i]) ){
				validRelationChars = validRelationChars.replace("" + valueArray[i], "");
				i++;
				if (valueArray[i] == '}')
					return true;
				else if (valueArray[i] != ',')
					return false;
			}
			else
				return false;
		}
		
		return true;
	}

	/** Returns true if the given string represents a class token,
	 *  otherwise returns false.
	 * @param value The string being tested
	 * @return true if value represents a class token, else false
	 */
	private static boolean isClassToken(String value){
		// a class token must have one nonempty namespace and one nonempty class name
		// separated by one pound sign
		String [] namespaceAndClassname = value.split("#");
		if (namespaceAndClassname.length != 2 ||
			namespaceAndClassname[0].isEmpty() ||
			namespaceAndClassname[1].isEmpty())
			return false;

		// each character in the namespace and class name must be valid
		char[] valueArray = value.toCharArray();		
		for (char c : valueArray){
			if ( !isValidClassChar(c) )
				return false;
		}

		return true;
	}

	/** Tests whether a character is valid for namespace names and class names.  
	 * @param ch The character tested for validity.
	 * @return true if character is valid for namespace and class names, else false
	 */
	private static boolean isValidClassChar(char ch){
		return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_#".contains("" + ch);
	}


				/* Getters */

	public List<Token> getTokenList() { return tokenStream; }
}
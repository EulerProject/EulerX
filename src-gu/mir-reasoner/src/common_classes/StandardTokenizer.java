package common_classes;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

class StandardTokenizer {
	private int lineNumber;
	private List<Token> tokenStream = new LinkedList<Token>();
	private String T1Namespace, T2Namespace;
	private String T1Citation, T2Citation;
	private String currentNamespace;

	public void tokenize(File inputFile) throws IOException, InvalidTokenException{
		lineNumber = 1;
		BufferedReader inputReader = new BufferedReader(new FileReader(inputFile));

		T1Namespace = T2Namespace = "";
		while (inputReader.ready()){
			addLineToTokenStream(inputReader.readLine());
			lineNumber++;
		}

		inputReader.close();
	}

	private void addLineToTokenStream(String line) throws InvalidTokenException{
		line = line.trim();
		String firstToken = line.split("[ ]+")[0];
		if (firstToken.isEmpty())
			return;
		else if (firstToken.equals("taxonomy"))
			processTaxonomyHeader(line);
		else if (firstToken.equals("articulation"))
			processArticulationHeader(line);
		else if (line.charAt(0) == '(')
			processIntrarelation(line);
		else if (line.charAt(0) == '[')
			processInterrelation(line);
		else
			throw new InvalidTokenException("Invalid syntax", lineNumber, line);
	}

	private void processTaxonomyHeader(String line) throws InvalidTokenException{
		String[] tokens = line.split("[ ]+");

		if (tokens.length < 3)
			throw new InvalidTokenException("Missing taxonomy names", lineNumber, line);
		else if (tokens.length > 3)
			throw new InvalidTokenException("Too many taxonomy names", lineNumber, line);

		currentNamespace = tokens[1];

		if (T1Namespace.isEmpty()){
			T1Namespace = tokens[1];
			T1Citation = tokens[2];
		}
		else if (T2Namespace.isEmpty()){
			T2Namespace = tokens[1];
			T2Citation = tokens[2];
		}
		else
			throw new InvalidTokenException("File contains more than two taxonomies", lineNumber, line); 
	}

	private void processArticulationHeader(String line) throws InvalidTokenException{
		String[] tokens = line.split("[ ]+");

		if (tokens.length < 3)
			throw new InvalidTokenException("Missing articulation identifiers", lineNumber, line);
		else if (tokens.length > 3)
			throw new InvalidTokenException("Too many articulation identifiers", lineNumber, line);

		String articulationIdentifier = tokens[1];
		if (!articulationIdentifier.equals(T1Namespace + T2Namespace) &&
		    !articulationIdentifier.equals(T2Namespace + T1Namespace) )
		    throw new InvalidTokenException("Articulation identifier references nonexistent taxonomies", lineNumber, line);

		String articulationCitation = tokens[2];
		if (!articulationCitation.equals(T1Citation + T2Citation) &&
			!articulationCitation.equals(T2Citation + T1Citation) )
			throw new InvalidTokenException("Articulation citation references nonexistent taxonomies", lineNumber, line);
	}

	private void processIntrarelation(String line) throws InvalidTokenException{
		if (line.charAt(0) != '(' || line.charAt(line.length()-1) != ')')
			throw new InvalidTokenException("Intrarelation not enclosed in parentheses", lineNumber, line);

		String tokenString = line.substring(1, line.length()-1);
		String[] tokens = tokenString.split("[ ]+");

		if (tokens.length < 2)
			throw new InvalidTokenException("Too few taxa given for the intrarelation", lineNumber, line);

		try{
			for (String token : tokens)
				Integer.parseInt(token);

			ClassToken parent = new ClassToken(lineNumber, currentNamespace + "#" + tokens[0]);
			ClassToken child;
			String token;
			for (int i=1; i < tokens.length; i++){
				token = tokens[i];
				child = new ClassToken(lineNumber, currentNamespace + "#" + token);
				tokenStream.add(child);
				tokenStream.add(new RelationToken(lineNumber, "isa"));
				tokenStream.add(parent);
			}
		} catch(NumberFormatException ex){
			throw new InvalidTokenException("Invalid taxon token (must be an integer)", lineNumber, line);
		}
	}

	private void processInterrelation(String line) throws InvalidTokenException{
		if (line.charAt(0) != '[' || line.charAt(line.length()-1) != ']')
			throw new InvalidTokenException("Intrarelation not enclosed in brackets", lineNumber, line);

		String tokenString = line.substring(1, line.length()-1);
		tokenString = tokenString.replace("{", "").replace("}", "");
		String[] tokens = tokenString.split("[ ]+");

		String subjectName = tokens[0];
		String objectName = tokens[tokens.length-1];

		if (isValidTaxonToken(subjectName))
			throw new InvalidTokenException("Invalid subject", lineNumber, line);
		else if (isValidTaxonToken(objectName))
			throw new InvalidTokenException("Invalid object", lineNumber, line);

		String relations = "";
		for (int i=1; i < tokens.length-1; i++)
			relations += getRelation(tokens[i], line);

		ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
		RelationToken articulation = new RelationToken(lineNumber, relations);
		ClassToken object =  new ClassToken(lineNumber, objectName.replace('.', '#'));

		tokenStream.add(subject);
		tokenStream.add(articulation);
		tokenStream.add(object);
	}

	private boolean isValidTaxonToken(String token){
		String[] tokenParts = token.split(".");

		if (tokenParts.length != 2)
			return false;

		String namespace = tokenParts[0];
		String classname = tokenParts[1];

		if (!namespace.equals(T1Namespace) && !namespace.equals(T2Namespace))
			return false;

		try{
			Integer.parseInt(classname);
		} catch(NumberFormatException ex){
			return false;
		}

		return true;
	}

	private char getRelation(String relationName, String line) throws InvalidTokenException{
		if (relationName.equals("is_included_in")) return '<';
		else if (relationName.equals("includes"))  return '>';
		else if (relationName.equals("equals"))    return '=';
		else if (relationName.equals("disjoint"))  return '!';
		else if (relationName.equals("overlaps"))  return 'o';
		else
			throw new InvalidTokenException("Invalid articulation", lineNumber, line);
	}

	public List<Token> getTokenList() {
		return tokenStream;
	}
}

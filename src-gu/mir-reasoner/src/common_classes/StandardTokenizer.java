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
		    String line = inputReader.readLine();
		    int endIndex = line.indexOf(']');
		    if(endIndex == -1){
		    	if(!line.startsWith("#"))
					addLineToTokenStream(line);
		    }
		    else{
		    	String subline = line.substring(0, endIndex+1);
		    	if(!subline.startsWith("#"))
					addLineToTokenStream(subline);
			}
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
			//for (String token : tokens)
			//	Integer.parseInt(token);

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
		String subject2Name, subject3Name;
		String possibleLSum = tokens[2];
		String possibleLSum3 = new String();
		if(tokens.length >= 4)
			possibleLSum3 = tokens[3];
		String possibleRSum = tokens[1];
		String possibleRSum3 = tokens[1];
		String objectName = tokens[tokens.length-1];
		String object2Name, object3Name;
		boolean isLSum = false;
		boolean isLSum3 = false;
		boolean isRSum = false;
		boolean isRSum3 = false;

		if (isValidTaxonToken(subjectName))
			throw new InvalidTokenException("Invalid subject", lineNumber, line);
		else if (isValidTaxonToken(objectName))
			throw new InvalidTokenException("Invalid object", lineNumber, line);

		String relations = "";
		if(possibleLSum.equals("lsum")){
			relations += getRelation("lsum", line);
			isLSum = true;
		}
		else if(possibleLSum3.equals("l3sum")){
			relations += getRelationString("l3sum", line);
			isLSum3 = true;
		}
		else if(possibleRSum.equals("rsum")){
			relations += getRelation("rsum", line);
			isRSum = true;
		}
		else if(possibleRSum3.equals("r3sum")){
			relations += getRelationString("r3sum", line);
			isRSum3 = true;
		}
		else{
			for (int i=1; i < tokens.length-1; i++)
				relations += getRelation(tokens[i], line);
		}

		if (isLSum){
			subject2Name = tokens[1];
			ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
			ClassToken subject2 = new ClassToken(lineNumber, subject2Name.replace('.', '#'));
			RelationToken articulation = new RelationToken(lineNumber, relations);
			ClassToken object = new ClassToken(lineNumber, objectName.replace('.', '#'));
			tokenStream.add(subject);
			tokenStream.add(subject2);
			tokenStream.add(articulation);
			tokenStream.add(object);
		}
		else if(isLSum3){
			subject2Name = tokens[1];
			subject3Name = tokens[2];
			ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
			ClassToken subject2 = new ClassToken(lineNumber, subject2Name.replace('.', '#'));
			ClassToken subject3 = new ClassToken(lineNumber, subject3Name.replace('.', '#'));
			RelationToken articulation = new RelationToken(lineNumber, relations);
			ClassToken object = new ClassToken(lineNumber, objectName.replace('.', '#'));
			tokenStream.add(subject);
			tokenStream.add(subject2);
			tokenStream.add(subject3);
			tokenStream.add(articulation);
			tokenStream.add(object);
		}
		else if(isRSum){
			objectName = tokens[tokens.length-2];
			object2Name = tokens[tokens.length-1];
			ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
			RelationToken articulation = new RelationToken(lineNumber, relations);
			ClassToken object = new ClassToken(lineNumber, objectName.replace('.', '#'));
			ClassToken object2 = new ClassToken(lineNumber, object2Name.replace('.', '#'));
			tokenStream.add(subject);
			tokenStream.add(articulation);
			tokenStream.add(object);
			tokenStream.add(object2);
		}
		else if(isRSum3){
			objectName = tokens[tokens.length-3];
			object2Name = tokens[tokens.length-2];
			object3Name = tokens[tokens.length-1];
			ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
			RelationToken articulation = new RelationToken(lineNumber, relations);
			ClassToken object = new ClassToken(lineNumber, objectName.replace('.', '#'));
			ClassToken object2 = new ClassToken(lineNumber, object2Name.replace('.', '#'));
			ClassToken object3 = new ClassToken(lineNumber, object3Name.replace('.', '#'));
			tokenStream.add(subject);
			tokenStream.add(articulation);
			tokenStream.add(object);
			tokenStream.add(object2);
			tokenStream.add(object3);
		}
		else{
			ClassToken subject = new ClassToken(lineNumber, subjectName.replace('.', '#'));
			RelationToken articulation = new RelationToken(lineNumber, relations);
			ClassToken object =  new ClassToken(lineNumber, objectName.replace('.', '#'));

			tokenStream.add(subject);
			tokenStream.add(articulation);
			tokenStream.add(object);
		}
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
		else if (relationName.equals("lsum"))      return 'l';
		else if (relationName.equals("rsum"))      return 'r';
		else
			throw new InvalidTokenException("Invalid articulation", lineNumber, line);
	}

	private String getRelationString(String relationName, String line) throws InvalidTokenException{
		if(relationName.equals("l3sum"))		return "l3";
		else if(relationName.equals("r3sum"))	return "r3";
		else
			throw new InvalidTokenException("Invalid articulation", lineNumber, line);
	}

	public List<Token> getTokenList() {
		return tokenStream;
	}
}

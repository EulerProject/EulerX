package common_classes;

import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import converter.SeederInitializer;

/** A class used to convert a list of tokens into a list of parts. 
 *  Acts as intermediary between tokenization and conversion.
 */
public class Parser{
				/* Class fields */

	// object containing all the relevant information from the input file
	private TaxonomyInfo taxonomyInformation;

	private SeederInitializer seederInitializer;

	public static final int STANDARD = 0;
	public static final int SPECIAL = 1;


				/* Class methods */

	// TODO make this a static method which returns a TaxonomyInfo object
	public Parser(String fileName, int inputType) throws IOException, InvalidTokenException{
		File in = new File(fileName);

		if (inputType == SPECIAL){
			SpecialTokenizer specialTokenizer = new SpecialTokenizer();
			specialTokenizer.tokenize(in);
			parse(specialTokenizer.getTokenList(), SPECIAL);
		}
		else if (inputType == STANDARD){
			StandardTokenizer standardTokenizer = new StandardTokenizer();
			standardTokenizer.tokenize(in);
			parse(standardTokenizer.getTokenList(), STANDARD);
		}
		else{
			System.out.println("Incorrect input type parameter.");
		}
	}


	/** Converts a list of Tokens into a list of Parts, and saves list of 
	 *  Parts to parts variable
	 * @param tokenStream the list of Tokens to evaluate
	 * @return true if the list of Tokens is evaluated successfully, 
	 *   otherwise false
	 */
	private boolean parse(List<Token> tokenStream, int inputType){
		// list of all relations
		Set<SimpleRelation> allRelations = new LinkedHashSet<SimpleRelation>();
		// list of the inter-taxonomical relations
		List<SimpleRelation> interrelations = new LinkedList<SimpleRelation>();

		// list of the first taxonomy's intra-taxonomical relations
		List<SimpleRelation> T1intrarelations = new LinkedList<SimpleRelation>();
		// list of the second taxonomy's intra-taxonomical relations
		List<SimpleRelation> T2intrarelations = new LinkedList<SimpleRelation>();
		List<SimpleRelation> T1sums = new LinkedList<SimpleRelation>();
		List<SimpleRelation> T2sums = new LinkedList<SimpleRelation>();
		// taxonomy namespaces
		String Namespace1 = "";
		String Namespace2 = "";

		// children and parent sets used for error-checking
		Set<String> T1children = new HashSet<String>();
		Set<String> T2children = new HashSet<String>();
		Set<String> T1parentlessTaxa = new HashSet<String>();
		Set<String> T2parentlessTaxa = new HashSet<String>();

		// taxonomy objects to be constructed from the data collected
		Taxonomy T1;
		Taxonomy T2;
		String T1RootName, T2RootName;

		// Warning: input file is empty
		if ( tokenStream.isEmpty() )
			System.out.println("NOTE: The input file is empty.");

		try{

			for (int i = 0; i < tokenStream.size(); i+= 3){
				String subj = tokenStream.get(i).getContents();
				String subj2, subj3;
				String possibleLSum = tokenStream.get(i+2).getContents();
				String possibleL3Sum = new String();
				if(i + 4 <= tokenStream.size() - 1)
					possibleL3Sum = tokenStream.get(i+3).getContents();
				String pred = tokenStream.get(i+1).getContents();
				String obj;
				String obj2, obj3;
				SimpleRelation rel;

				if(possibleLSum.toLowerCase().equals("{l}") || possibleLSum.toLowerCase().equals("l")){
					pred = "l";
					subj2 = tokenStream.get(i+1).getContents();
					obj = tokenStream.get(i+3).getContents();
					rel = new SimpleRelation(subj, subj2, pred, obj);
					if(rel.getSubjectNamespace().equals(Namespace1))
						T1sums.add(rel);
					else
						T2sums.add(rel);
					i++;
				}
				else if(possibleL3Sum.toLowerCase().equals("{l3}") || possibleL3Sum.toLowerCase().equals("l3")){
					pred = "l3";
					subj2 = tokenStream.get(i+1).getContents();
					subj3 = tokenStream.get(i+2).getContents();
					obj = tokenStream.get(i+4).getContents();
					rel = new SimpleRelation(subj, subj2, subj3, pred, obj);
					if(rel.getSubjectNamespace().equals(Namespace1))
						T1sums.add(rel);
					else
						T2sums.add(rel);
					i += 2;
				}
				else if (pred.toLowerCase().equals("{r}") || pred.toLowerCase().equals("r")){
					pred = "r";
					obj = tokenStream.get(i+2).getContents();
					obj2 = tokenStream.get(i+3).getContents();
					rel = new SimpleRelation(subj, pred, obj, obj2, true);
					if(rel.getObjectNamespace().equals(Namespace2))
						T2sums.add(rel);
					else
						T1sums.add(rel);
					i++;
				}
				else if(pred.toLowerCase().equals("{r3}") || pred.toLowerCase().equals("r3")){
					pred = "r3";
					obj = tokenStream.get(i+2).getContents();
					obj2 = tokenStream.get(i+3).getContents();
					obj3 = tokenStream.get(i+4).getContents();
					rel = new SimpleRelation(subj, pred, obj, obj2, obj3, true);
					if(rel.getObjectNamespace().equals(Namespace2))
						T2sums.add(rel);
					else
						T1sums.add(rel);
					i += 2;
				}
				else if ( pred.toLowerCase().equals("isa") ){
					pred = "isa";
					rel = new SimpleRelation(
						tokenStream.get(i).getContents(),
						pred,
						tokenStream.get(i+2).getContents()
						);
				}
				else if (inputType == SPECIAL){
					pred = pred.substring(1, pred.length()-1).replace(",","");
					rel = new SimpleRelation(
						tokenStream.get(i).getContents(),
						pred,
						tokenStream.get(i+2).getContents()
						);
				}
				else{
					rel = new SimpleRelation(
						tokenStream.get(i).getContents(),
						pred,
						tokenStream.get(i+2).getContents()
						);
				}

				/** Errors with individual relations */
				// Error: intra-taxonomical relation ("isa") between taxa of different taxonomies
				if ( rel.getPredicate()       .equals("isa")  &&
				  !( rel.getSubjectNamespace().equals( rel.getObjectNamespace() ) ) )
					throw new InvalidTaxonomyException("Error, \"" + rel + 
						"\": intra-taxonomical relation (\"isa\") between taxa of different taxonomies."
					);
				// Error: inter-taxonomical relation between taxa of the same taxonomy
				else if ( !( rel.getPredicate()       .equals("isa") )  &&
						     rel.getSubjectNamespace().equals( rel.getObjectNamespace() ) )
					throw new InvalidTaxonomyException("Error, \"" + rel + 
						"\": inter-taxonomical relation (non-\"isa\") between taxa of the same taxonomy."
					);
				// Error: relation relates a taxon to itself
				else if ( rel.getSubject().equals( rel.getObject() ) )
					throw new InvalidTaxonomyException("Error: \"" +
						rel + "\" relates a taxon to itself."
					);
				// Error: relation overrides (relates the same two taxa as) a previous relation
				else if ( !allRelations.add(rel) )
					throw new InvalidTaxonomyException("Error: \""
						+ rel + "\" overrides (relates the same two taxa as) a previous relation."
					);


				/** Errors with the namespaces */
				// assign to Namespace1 the first namespace that appears
				if (i == 0)
					Namespace1 = rel.getSubjectNamespace();
				// assign to Namespace2 the second namespace that appears
				if ( Namespace2.isEmpty() ){
					if ( !( rel.getSubjectNamespace().equals(Namespace1) ) )
						Namespace2 = rel.getSubjectNamespace();
					else if ( !( rel.getSubject2Namespace().equals(Namespace1)))
						Namespace2 = rel.getSubject2Namespace();
					else if ( !( rel.getObjectNamespace().equals(Namespace1) ) )
						Namespace2 = rel.getObjectNamespace();
					else if ( !( rel.getObject2Namespace().equals(Namespace1)))
						Namespace2 = rel.getObject2Namespace();
				}

				// Error: input file declares more than two taxonomies
				else if ( !( rel.getSubjectNamespace().equals( Namespace1 ) )  &&
						  !( rel.getSubjectNamespace().equals( Namespace2 ) ) ){
					throw new InvalidTaxonomyException("Error, \"" +
						rel.getSubject() + "\": the input file declares more than two taxonomies."
					);
				}
				// Error: input file declares more than two taxonomies
				else if ( !( rel.getObjectNamespace().equals( Namespace1 ) )  &&  
						  !( rel.getObjectNamespace().equals( Namespace2 ) ) ){
					throw new InvalidTaxonomyException("Error, \"" +
						rel.getObject() + "\": the input file declares more than two taxonomies."
					);
				}

				/** Errors with individual taxa */
				// Error: taxon has more than one parent
				if ( rel.isInternal() ){
					if ( rel.getSubjectNamespace().equals(Namespace1) ){
						// the subject is always a child (no longer parentless)
						T1parentlessTaxa.remove( rel.getSubjectClassname() );
						// so add it to the set of children
						if ( !T1children.add( rel.getSubjectClassname() ) )
							// if the taxon was already in the set, then it already had a parent
							throw new InvalidTaxonomyException("Error: \"" +
								rel.getSubject() + "\" has been assigned more than one parent."
							);
						// if the object is not already a child, it is parentless
						if ( !( T1children.contains( rel.getObjectClassname() ) ) )
							T1parentlessTaxa.add( rel.getObjectClassname() );
						T1intrarelations.add(rel);
					}
					else{
						// the subject is always a child (no longer parentless)
						T2parentlessTaxa.remove( rel.getSubjectClassname() );
						// so add it to the set of children
						if ( !T2children.add( rel.getSubjectClassname() ) )
							// if the taxon was already in the set, then it already had a parent
							throw new InvalidTaxonomyException("Error: \"" +
								rel.getSubject() + "\" has been assigned more than one parent."
							);
						// if the object is not already a child, it is parentless
						if ( !( T2children.contains( rel.getObjectClassname() ) ) )
							T2parentlessTaxa.add( rel.getObjectClassname() );
						T2intrarelations.add(rel);
					}
				}
				else{
					// if the subject is in namespace one and is not a child
					if ( rel.getSubjectNamespace().equals(Namespace1)  &&
					   !( T1children.contains( rel.getSubjectClassname() ) ) )
						T1parentlessTaxa.add( rel.getSubjectClassname() );
					// else if the subject is in namespace two and is not a child
					else if ( rel.getSubjectNamespace().equals(Namespace2)  &&
							!( T2children.contains( rel.getSubjectClassname() ) ) )
						T2parentlessTaxa.add( rel.getSubjectClassname() );
					// if the object is in namespace one and not a child
					if ( rel.getObjectNamespace().equals(Namespace1)  &&
					   !( T1children.contains( rel.getObjectClassname() ) ) )
						T1parentlessTaxa.add( rel.getObjectClassname() );
					// else if the object is in namespace two and not a child
					else if ( rel.getObjectNamespace().equals(Namespace2)  &&
							!( T2children.contains( rel.getObjectClassname() ) ) )
						T2parentlessTaxa.add( rel.getObjectClassname() );

					// if the relation maps from T1 to T2, add it to the list of interrelations
					if ( rel.getSubjectNamespace().equals( Namespace1 ) )
						interrelations.add(rel);
					// if it maps from T2 to T1, reverse it before adding it
					else
						interrelations.add( rel.reverse() );
				} // end if
			} // end for


			/** Errors with individual taxa (cont.) */
			// Error: more than one parentless taxa
			if ( T1parentlessTaxa.size() > 1){
				String errorMsg = "Each of the following taxa has no parent:\n";
				for (String taxon : T1parentlessTaxa)
					errorMsg += '\t' + Namespace1 + '#' + taxon + '\n';
				errorMsg += "Error: each taxonomy must have exactly one parentless taxon (the root).";
				throw new InvalidTaxonomyException(errorMsg);
			}
			else if ( T2parentlessTaxa.size() > 1){
				String errorMsg = "Each of the following taxa has no parent:\n";
				for (String taxon : T2parentlessTaxa)
					errorMsg += '\t' + Namespace2 + '#' + taxon + '\n';
				errorMsg += "Error: each taxonomy must have exactly one parentless taxon (the root).";
				throw new InvalidTaxonomyException(errorMsg);
			}
			// Error: no parentless taxa (no valid root)
			else if ( tokenStream.size() > 0  &&  T1parentlessTaxa.isEmpty() )
				throw new InvalidTaxonomyException("Error: taxonomy \"" + Namespace1 + "\" has no valid root taxon.");
			else if ( tokenStream.size() > 0  &&  !Namespace2.isEmpty()  &&  T2parentlessTaxa.isEmpty() )
				throw new InvalidTaxonomyException("Error: taxonomy \"" + Namespace2 + "\" has no valid root taxon.");


			// Warning: input file contains only one taxonomy
			if ( tokenStream.size() > 0  &&  Namespace2.isEmpty() )
				System.out.println("NOTE: The input file has only one taxonomy.\n");

			// build the taxonomies
			T1RootName = T1parentlessTaxa.iterator().next();
			T2RootName = T2parentlessTaxa.iterator().next();
			T1 = new Taxonomy(Namespace1, T1intrarelations, T1RootName);
			for(SimpleRelation rel : T1sums){
				T1.handleSums(rel);
			}
			T2 = new Taxonomy(Namespace2, T2intrarelations, T2RootName);
			for(SimpleRelation rel : T2sums){
				T2.handleSums(rel);
			}
			
			// store the taxonomies and their interrelations
			taxonomyInformation = new TaxonomyInfo(T1, T2, interrelations);

			seederInitializer = new SeederInitializer(T1, T2, allRelations, interrelations);
		} catch (InvalidTaxonomyException ex) { System.out.println( ex.getMessage() ); return false; }
		// end try

		return true;
	}

	public SeederInitializer getSeederInitializer()  { return seederInitializer; }
	public TaxonomyInfo getTaxonomyContents()  { return taxonomyInformation; }
}

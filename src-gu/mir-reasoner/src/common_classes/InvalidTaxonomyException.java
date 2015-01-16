package common_classes;

/**
 * The exception to be thrown whenever the seeder encounters an invalid taxonomy.
 * @author cbryan2
 */
public class InvalidTaxonomyException extends Exception{
				/* Class fields */

	// serial version
	private static final long serialVersionUID = 6360528270183648203L;
	// the message of the error
	private String msg;


				/* Class methods */

	/** Creates an InvalidTaxonomyException object.
	 * @param msg The error message.	*/
	public InvalidTaxonomyException(String msg) { this.msg = msg; }


				/* Redefinitions of methods inherited from Exception */

	/** @return The error message.	*/
	public String getMessage() { return msg; }
}

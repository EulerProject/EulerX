package common_classes;

/** A class representing the smallest pieces of useful information as 
 *  read from an input file. To be used within Tokenizer
 */
public abstract class Token{	
	private int lineNumber;
	private String contents;
	
	/**Sets the lineNumber on which this token was found
	 * @param i The line number on which this token was found
	 */
	void setLineNumber(int i){
		lineNumber = i;
	}
	
	/**Gets the lineNumber on which this token was found
	 * @return The line number on which this token was found
	 */ 
	int getLineNumber(){
		return lineNumber;
	}
	
	/**Sets the contents of this token
	 * @param contents The string to which this token's contents will be set
	 */
	void setContents(String contents){
		this.contents = contents;
	}
	
	/** Returns the contents of this token
	 * @return The contents of this token
	 */
	String getContents(){
		return contents;
	}
}

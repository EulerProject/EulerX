package common_classes;

/** A token which represents the OWL Class in an axiom assertion */
class ClassToken extends Token{
	/**Constructor for a new ClassToken*
	 * @param lineNumber the line number on which this token was found
	 * @param contents the contents of this token
	 */
	ClassToken(int lineNumber, String contents){
		this.setLineNumber(lineNumber);
		this.setContents(contents);
	}
}
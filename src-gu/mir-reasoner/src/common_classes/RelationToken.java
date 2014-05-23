package common_classes;

/** A Token which represents the relation between two OWL Classes in
 *  an axiom assertion
 */
class RelationToken extends Token{
	/**Constructor for a new RelationToken
	 * @param lineNumber the line on which this token was encountered
	 * @param contents The contents of this token
	 */
	RelationToken(int lineNumber, String contents){
		this.setLineNumber(lineNumber);
		this.setContents(contents);
	}
}

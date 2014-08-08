package common_classes;

/** An exception generated which an invalid token is evaluated*/
public class InvalidTokenException extends Exception{
	private static final long serialVersionUID = 1552199438102205956L;

	private String msg;
	private int lineNumber;
	private String contents;
	
	/** Creates a new InvalidTokenException
	 * @param msg The message for this exception
	 * @param lineNumber the line number on which this exception was found
	 * @param contents the Contents of the token that caused this exception
	 */
	InvalidTokenException(String msg, int lineNumber, String contents){
		this.msg = msg;
		this.lineNumber = lineNumber;
		this.contents = contents;
	}
	
	/** Returns the message, line number, and contents of this exception
	 * @return the message, line number, and contents of this exception
	 */
	public String getMessage(){
		return msg + ": Line " + lineNumber + ", \"" + contents + '"';
	}
}
package common_classes;

/**
 * The class representing an inter-taxonomical pair of taxa.
 * @author cbryan2
 */
public class TaxonPair{
	private Taxon t1, t2;

	public TaxonPair(Taxon t1, Taxon t2){
		this.t1 = t1;
		this.t2 = t2;
	}

	public boolean isFalse(){
		return (t1.isFalse() || t2.isFalse());
	}

	public Taxon getTaxon1() { return t1; }
	public Taxon getTaxon2() { return t2; }

	@Override
	public String toString() {
		return "(" + t1 + "," + t2 + ")";
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((t1 == null) ? 0 : t1.hashCode());
		result = prime * result + ((t2 == null) ? 0 : t2.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;

		if (obj == null  ||  getClass() != obj.getClass())
			return false;

		TaxonPair other = (TaxonPair) obj;
		if ( (t1 == null  &&  other.t1 != null)  ||  !t1.equals(other.t1) ||
			 (t2 == null  &&  other.t2 != null)  ||  !t2.equals(other.t2) )
			return false;

		return true;
	}
}
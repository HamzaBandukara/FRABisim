package DataStructures;

import org.javatuples.Quintet;
import org.javatuples.Triplet;

public final class HardQuintet<A, B, C, D, E> {

    public Quintet<A, B, C, D, E> triplet;
    public int hash;

    public HardQuintet(Quintet<A, B, C, D, E> triplet){
        this.triplet = triplet;
        this.hash = triplet.hashCode();
    }

    public int hashCode(){
        return this.hash;
    }
}

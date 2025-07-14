package DataStructures;

import org.javatuples.Quintet;
import org.javatuples.Triplet;

import java.util.Objects;

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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        HardQuintet<?, ?, ?, ?, ?> that = (HardQuintet<?, ?, ?, ?, ?>) o;
        return Objects.equals(triplet, that.triplet);
    }
}

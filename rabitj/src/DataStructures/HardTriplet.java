package DataStructures;



import org.antlr.v4.runtime.misc.Triple;

import java.util.Objects;

public final class HardTriplet<A, B, C> {

    public Triple<A, B, C> triplet;
    public int hash;

    public HardTriplet(A a, B b, C c){
        this.triplet = new Triple<>(a,b,c);
        this.hash = Objects.hash(a,b,c);
//        this.hash = triplet.hashCode();
    }

    public int hashCode(){
        return this.hash;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        HardTriplet<?, ?, ?> that = (HardTriplet<?, ?, ?>) o;
        return (triplet.a.equals(that.triplet.a)&& triplet.b.equals(that.triplet.b) && triplet.c.equals(that.triplet.c));
    }
}

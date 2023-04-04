package DataStructures;

import org.javatuples.Triplet;

import java.util.Objects;

public final class HardTriplet<A, B, C> {

    public Triplet<A, B, C> triplet;
    public int hash;

    public HardTriplet(A a, B b, C c){
        this.triplet = new Triplet<>(a,b,c);
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
        return (this.triplet.getValue0().equals(that.triplet.getValue0())) && (this.triplet.getValue1().equals(that.triplet.getValue1())) && (this.triplet.getValue2().equals(that.triplet.getValue2()));
    }
}

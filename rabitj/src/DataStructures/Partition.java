package DataStructures;

import java.util.*;

public class Partition {
    public String qc;
    public Set<Integer> xc;
    public Map<String, PartialPermutation> rays;
    public SetPermutationGroup group;
    private int hash;

    // For initial use;
    public Partition(String q, Set<Integer> x, Map<String, PartialPermutation> sigmas) {
        qc = q;
        xc = x;
        rays = sigmas;
        Map<Integer, Integer> map = new HashMap<>();
        int degree = 0;
        for(PartialPermutation val: sigmas.values()){
            degree = val.degree;
            break;
        }
        for(int i: xc)
            map.put(i, i);
        HashSet<PartialPermutation> perms = new HashSet<>();
        perms.add(PartialPermutation.generatePartialPermutation(map, degree));
        group = new SetPermutationGroup(perms);
        hash = Objects.hash(qc, xc, rays, group);
    }

    public Partition(String q, Set<Integer> x, Map<String, PartialPermutation> sigmas, Set<PartialPermutation> gc) {
        qc = q;
        xc = x;
        rays = sigmas;
        group = new SetPermutationGroup(gc);
        hash = Objects.hash(qc, xc, rays, group);
    }

    public String toString(){
        return qc + " " + xc + " -> " + rays +" >> "+ group;
    }
    //

    @Override
    public Partition clone(){
        Map<String, PartialPermutation> newrays = new HashMap<>(rays);
        return new Partition(qc, xc, newrays, new HashSet<>(group.gc));
    }

    public void addPermutation(PartialPermutation toPermutation) {
        group.addGenerator(toPermutation);
        hash = Objects.hash(qc, xc, rays, group);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Partition partition = (Partition) o;
        return Objects.equals(qc, partition.qc) && Objects.equals(xc, partition.xc) && Objects.equals(rays, partition.rays) && Objects.equals(group, partition.group);
    }

    @Override
    public int hashCode() {
        return hash;
    }
}

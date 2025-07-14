package DataStructures;

import java.util.*;

public class Partition {
    public String qc;
    public Set<Integer> xc;
    public Map<String, PartialPermutation> rays;
    public SetPermutationGroup group;
    private final int hash;
    public int id;
    private static int counter;

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
        id = counter;
        counter ++;
        hash = id;
//        hash = Objects.hash(qc, xc, rays, group);
    }

    public Partition(String q, Set<Integer> x, Map<String, PartialPermutation> sigmas, SetPermutationGroup g) {
        qc = q;
        xc = x;
        rays = sigmas;
//        group = new SetPermutationGroup(g.getGc());
        group = new SetPermutationGroup(g);
        id = counter;
        counter ++;
        hash = id;
//        hash = Objects.hash(qc, xc, rays, group);
    }

    public String toString(){
        return qc + " " + xc + " -> " + rays +" >> "+ group;
    }
    //

    @Override
    public Partition clone(){
        Map<String, PartialPermutation> newrays = new HashMap<>(rays);
        return new Partition(qc, xc, newrays, group);
    }

    public void addPermutation(PartialPermutation toPermutation) {
        group.addGenerator(toPermutation);
//        hash = Objects.hash(qc, xc, rays, group);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        Partition p = (Partition) o;
        return p.id == id;
//        if (o == null || getClass() != o.getClass()) return false;
//        Partition partition = (Partition) o;
//        return Objects.equals(qc, partition.qc) && Objects.equals(xc, partition.xc) && Objects.equals(rays, partition.rays) && Objects.equals(group, partition.group);
    }

    @Override
    public int hashCode() {
        return hash;
    }
}

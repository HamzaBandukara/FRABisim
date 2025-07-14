package DataStructures;

import cc.redberry.core.groups.permutations.Permutation;
import cc.redberry.core.groups.permutations.PermutationGroup;

import java.util.*;

public class SetPermutationGroup {
    private Set<PartialPermutation> gc;
    public PermutationGroup group;
    public static Map<Set<PartialPermutation>, PermutationGroup> memo;
    public Set<PartialPermutation> members;
    public List<Integer> sortedDomain;
    private int degree;

    public SetPermutationGroup(Set<PartialPermutation> generators){
        gc = generators;
        List<Permutation> gens = new ArrayList<>();
        for(PartialPermutation p: gc) {
            gens.add(p.toPermutation());
            if(sortedDomain == null)
                sortedDomain = p.sortedDomain;
            degree = p.degree;
        }
        group = PermutationGroup.createPermutationGroup(gens);
        members = new HashSet<>(gc);
    }

    public SetPermutationGroup(SetPermutationGroup g) {
        group = g.group;
        members = new HashSet<>(g.members);
        gc = g.gc;
        sortedDomain = g.sortedDomain;
        degree = g.degree;
    }

    public PartialPermutation getRandom(){
        Permutation p = group.randomElement();
        Map<Integer, Integer> mp = new HashMap<>();
        for(int key: sortedDomain) {
            mp.put(key, sortedDomain.get(p.imageOf(key)));
        }
        return PartialPermutation.generatePartialPermutation(mp, degree);
    }

    public void addGenerator(PartialPermutation g){
        if(members.contains(g)) return;
        gc = null;
        group = group.union(g.toPermutation());
    }

    public boolean isMember(PartialPermutation p){
        if(members.contains(p)) return true;
//        if(memo == null) memo = new HashMap<>();
//        if(group == null) {
//            if(memo.get(gc) != null) group = memo.get(gc);
//            else{
//                List<Permutation> generators = new ArrayList<>();
//                for(PartialPermutation g: gc)
//                    generators.add(g.toPermutation());
//                group = PermutationGroup.createPermutationGroup(generators);
//                memo.put(new HashSet<>(gc), group);
//            }
//        }
        boolean res = group.membershipTest(p.toPermutation());
        if(res) members.add(p);
        return res;
    }

    public void setGroup(Set<PartialPermutation> p){
        List<Permutation> l = new ArrayList<>();
        for(PartialPermutation x: p)
            l.add(x.toPermutation());
        group = PermutationGroup.createPermutationGroup(l);
        gc = p;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SetPermutationGroup that = (SetPermutationGroup) o;
        return Objects.equals(gc, that.gc);
    }

    @Override
    public int hashCode() {
        return Objects.hash(gc);
    }

    @Override
    public String toString(){
        return gc.toString();
    }

    public Set<PartialPermutation> getGc(){
        if(gc == null){
            gc = new HashSet<>();
            for(Permutation p: group.generators()){
                Map<Integer, Integer> mp = new HashMap<>();
                for(int key: sortedDomain) {
                    try {
                        mp.put(key, sortedDomain.get(p.imageOf(key)));
                    } catch(Exception e){
                        System.out.println(sortedDomain);
                        System.out.println(p.imageOf(key));
                        System.out.println(Arrays.toString(p.oneLine()));
                        System.exit(5);
                    }
                }
                gc.add(PartialPermutation.generatePartialPermutation(mp, degree));
            }
        }
        return gc;
    }

}

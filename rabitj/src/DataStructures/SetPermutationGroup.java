package DataStructures;

import cc.redberry.core.groups.permutations.Permutation;
import cc.redberry.core.groups.permutations.PermutationGroup;

import java.util.*;

public class SetPermutationGroup {
    public Set<PartialPermutation> gc;
    public PermutationGroup group;
    public static Map<Set<PartialPermutation>, PermutationGroup> memo;
    public Set<PartialPermutation> members;

    public SetPermutationGroup(Set<PartialPermutation> generators){
        gc = generators;
        members = new HashSet<>(gc);
    }

    public void addGenerator(PartialPermutation g){
        if(members.contains(g)) return;
        gc.add(g);
        members.add(g);
        group = null;
    }

    public boolean isMember(PartialPermutation p){
        if(members.contains(p)) return true;
        if(memo == null) memo = new HashMap<>();
        if(group == null) {
            if(memo.get(gc) != null) group = memo.get(gc);
            else{
                List<Permutation> generators = new ArrayList<>();
                for(PartialPermutation g: gc)
                    generators.add(g.toPermutation());
                group = PermutationGroup.createPermutationGroup(generators);
                memo.put(new HashSet<>(gc), group);
            }
        }
        boolean res = group.membershipTest(p.toPermutation());
        if(res) members.add(p);
        return res;
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

}

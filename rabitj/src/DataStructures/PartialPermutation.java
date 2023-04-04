package DataStructures;

import cc.redberry.core.groups.permutations.Permutation;
import cc.redberry.core.groups.permutations.Permutations;
import org.antlr.v4.runtime.misc.Pair;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class PartialPermutation {

    public Permutation p;
    public Set<Integer> domain;
    public Set<Integer> range;
    int[] perm;
    public Map<Integer, Integer> sortedDomainInverse;
    public Map<Integer, Integer> map;
    public Map<Integer, Integer> inverse;
    public static Map<HardMap<Integer, Integer>, PartialPermutation> memo;
    public Map<PartialPermutation, PartialPermutation> multmemo;
    int degree;
    private Map<Set<Integer>, PartialPermutation> res1memo;
    private List<Integer> sortedDomain;
    private Map<Set<Integer>, Map<Set<Integer>, PartialPermutation>> res2memo;
    private PartialPermutation inverted;
    public Map<Pair<Integer, Integer>, PartialPermutation> addMemo;
    private int id;

    private PartialPermutation(Map<Integer, Integer> x, int degree){
        // [3] => [3, 1, 2, 0]
        multmemo = new HashMap<>();
        domain = x.keySet();
        range = new HashSet<>(x.values());
        this.degree = degree;
        sortedDomain = new ArrayList<>(domain);
        Collections.sort(sortedDomain);
        sortedDomainInverse = new HashMap<>();
        perm = new int[sortedDomain.size()];
        for(int c = 0; c < sortedDomain.size(); c++)
//            perm[c] = x.get(sortedDomain.get(c));
            sortedDomainInverse.put(sortedDomain.get(c), c);
        map = Collections.unmodifiableMap(x);
        inverse = map.entrySet()
                .stream()
                .collect(Collectors.toMap(Map.Entry::getValue, Map.Entry::getKey));
        res1memo = new HashMap<>();
        res2memo = new HashMap<>();
        addMemo = new HashMap<>();
        id = memo.size();
    }

    public static PartialPermutation generatePartialPermutation(Map<Integer, Integer> x, int degree){
        if(memo == null) memo = new HashMap<>();
        HardMap<Integer, Integer> m = new HardMap<Integer, Integer>(x);
        PartialPermutation result = memo.get(m);
        if(result == null) {
            result = new PartialPermutation(x, degree);
            memo.put(m, result);
        }
        return result;
    }

    public PartialPermutation add(int key, int value){
        Pair<Integer, Integer> p = new Pair<>(key, value);
        PartialPermutation result = addMemo.get(p);
        if(result == null){
            if(map.get(key) != null)
                if(map.get(key) == value) {
                    addMemo.put(p, this);
                    return this;
                }
            Map<Integer, Integer> newMap = new HashMap<>(map);
            if(inverse.get(value) != null){
                newMap.remove(inverse.get(value));
            }
            newMap.remove(key);
            newMap.put(key, value);
            result = generatePartialPermutation(newMap, degree);
            addMemo.put(p, result);
        }
        return result;
    }

    public Permutation toPermutation(){ // [2,3] => [3,2] => (1,0)
        if(p == null){
            int[] x = new int[sortedDomain.size()];
            for(int i = 0; i<x.length; i++)
                x[i] = sortedDomainInverse.get(apply(sortedDomain.get(i)));
            p = Permutations.createPermutation(x);
        }
        return p;
    }


    public PartialPermutation multiply(PartialPermutation other){
        PartialPermutation result = multmemo.get(other);
        if(result==null){
            Map<Integer, Integer> newmap = new HashMap<>();
            for(Integer d: domain)
            {
                Integer val = other.map.get(map.get(d));
                if(val != null)
                    newmap.put(d, val);
            }
            result = generatePartialPermutation(newmap, degree);
            multmemo.put(other, result);
        }
        return result;
    }

    public PartialPermutation inverse(){
        if(inverted == null)
            inverted = generatePartialPermutation(inverse, degree);
        return inverted;
    }

    public Integer apply(int key){
        return map.get(key);
    }

    public PartialPermutation restrict(Set<Integer> res){
        PartialPermutation result = res1memo.get(res);
        if(result == null){
            Map<Integer, Integer> newmap = new HashMap<>(map);
            newmap.keySet().retainAll(res);
            result = generatePartialPermutation(newmap, degree);
            res1memo.put(res, result);
        }
        return result;
    }

    public PartialPermutation restrict(Set<Integer> res1, Set<Integer> res2){
        res2memo.computeIfAbsent(res1, k -> new HashMap<>());
        PartialPermutation result = res2memo.get(res1).get(res2);
        if(result == null){
            Map<Integer, Integer> newmap = new HashMap<>();
            for(Map.Entry<Integer, Integer> entry: map.entrySet()){
                Integer key = entry.getKey();
                Integer val = entry.getValue();
                if(res2.contains(val) && res1.contains(key))
                    newmap.put(key, val);
            }
            result = generatePartialPermutation(newmap, degree);
            res2memo.get(res1).put(res2, result);
        }
        return result;
    }

    @Override
    public boolean equals(Object o) {
        return this == o;
//        if (this == o) return true;
//        System.out.println(this + " " + o + " => " + " | " + hashCode() + " <> " + o.hashCode());
//        if (o == null || getClass() != o.getClass()) return false;
//        PartialPermutation that = (PartialPermutation) o;
//        return this == that;
    }

    public int hashCode(){
        return id;
    }

    public String toString(){
        return map.toString();
    }
}
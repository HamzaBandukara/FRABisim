package DataStructures;

import cc.redberry.core.groups.permutations.Permutation;
import cc.redberry.core.groups.permutations.Permutations;
import org.antlr.v4.runtime.misc.Pair;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;
import java.util.stream.Collectors;

public class PartialPermutation {

    public Permutation p;
    public Set<Integer> domain;
    public Set<Integer> range;
//    public Map<Integer, Integer> reUse;
    int[] perm;
    public Map<Integer, Integer> sortedDomainInverse;
    public Map<Integer, Integer> map;
    public Map<Integer, Integer> inverse;
    public static Map<HardMap<Integer, Integer>, PartialPermutation> memo;
    public Map<PartialPermutation, PartialPermutation> multmemo;
    int degree;
    private Map<Set<Integer>, PartialPermutation> res1memo;
    public List<Integer> sortedDomain;
    private PartialPermutation inverted;
    public Map<HardPair<Integer, Integer>, PartialPermutation> addMemo;
    private int id;
    public static int counter;
    private Boolean domimgsame;
    private Map<Set<Integer>, PartialPermutation> resValMemo;


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
            sortedDomainInverse.put(sortedDomain.get(c), c);
        map = x;
//        map = Collections.unmodifiableMap(x);
        inverse = new HashMap<>(map.size() + 1);
        for(Map.Entry<Integer, Integer> e: x.entrySet())
            inverse.put(e.getValue(), e.getKey());
//        inverse = map.entrySet()
//                .stream()
//                .collect(Collectors.toMap(Map.Entry::getValue, Map.Entry::getKey));
        res1memo = new HashMap<>();
        resValMemo = new HashMap<>();
        addMemo = new HashMap<>();
//        id = Objects.hash(x);
        id = memo.size();
//        reUse = new HashMap<>(map.size());
    }

    public boolean xc_check(){
        if(domimgsame == null){
            domimgsame = domain.equals(range);
        }
        return domimgsame;
    }

//    public static PartialPermutation generatePartialPermutation(Map<Integer, Integer> x, int degree) {
//        if (memo == null) {
//            memo = new HashMap<>();
//        }
//        return memo.computeIfAbsent(new HardMap<>(x), k -> new PartialPermutation(x, degree));
//    }
    public static PartialPermutation generatePartialPermutation(Map<Integer, Integer> x, int degree){
        if(memo == null) {
            memo = new HashMap<>();
            counter = 0;
        }

        HardMap<Integer, Integer> m = new HardMap<>(x);
        PartialPermutation result = memo.get(m);
        if(result == null) {
            result = new PartialPermutation(x, degree);
            memo.put(m, result);
        } else{
            counter ++;
        }
        return result;
    }

    public PartialPermutation add(int key, int value){
        HardPair<Integer, Integer> p = new HardPair<>(key, value);
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

    public static PartialPermutation bigMultiply(PartialPermutation p1, PartialPermutation p2, PartialPermutation p3){
        if(p2.multmemo.containsKey(p3)){
            return p1.multiply((p2.multiply(p3)));
        }
        return (p1.multiply(p2)).multiply(p3);
    }

//    public static PartialPermutation bigMultiply(PartialPermutation p1, PartialPermutation p2, PartialPermutation p3){
//        HardTriplet<PartialPermutation, PartialPermutation, PartialPermutation> t = new HardTriplet<>(p1, p2, p3);
//        PartialPermutation result = bigMultMemo.get(t);
//        if(result == null){
//            Map<Integer, Integer> newMap = new HashMap<>(p1.domain.size() + 1, 1.0f);
//            for(Integer d: p1.domain){
//                Integer val = p2.apply(p1.apply(d));
//                if(val != null){
//                    val = p3.apply(val);
//                    if(val != null)
//                        newMap.put(d, val);
//                }
//            }
//            result = generatePartialPermutation(newMap, p1.degree);
//            bigMultMemo.put(t, result);
//        }
//        return result;
//    }

    public PartialPermutation multiply(PartialPermutation other){
        PartialPermutation result = multmemo.get(other);
        if(result==null){
            Map<Integer, Integer> newmap = new HashMap<>(domain.size() +1 , 1.0f);
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
            Map<Integer, Integer> newmap = new HashMap<>();
            for(Map.Entry<Integer, Integer> e: map.entrySet())
                if(res.contains(e.getKey()))
                    newmap.put(e.getKey(), e.getValue());
//            newmap.keySet().retainAll(res);
            result = generatePartialPermutation(newmap, degree);
            res1memo.put(res, result);
        }
        return result;
    }

    public PartialPermutation restrict(Set<Integer> res1, Set<Integer> res2){
            PartialPermutation first = restrict(res1);
            first = first.restrictValues(res2);
            return first;
    }

    private PartialPermutation restrictValues(Set<Integer> res) {
        PartialPermutation result = resValMemo.get(res);
        if(result == null){
            Map<Integer, Integer> newmap = new HashMap<>();
            for(Map.Entry<Integer, Integer> e: map.entrySet())
                if(res.contains(e.getValue()))
                    newmap.put(e.getKey(), e.getValue());
            result = generatePartialPermutation(newmap, degree);
            resValMemo.put(res, result);
        }
        return result;
    }

//    public PartialPermutation restrict(Set<Integer> res1, Set<Integer> res2){
//        HardPair<Set<Integer>, Set<Integer>> pair = new HardPair<>(res1, res2);
//        PartialPermutation result = res2memo.get(pair);
//        if(result == null){
//            Map<Integer, Integer> newmap = new HashMap<>();
//            for(Map.Entry<Integer, Integer> e : map.entrySet()){
//                if(res1.contains(e.getKey()) && res2.contains(e.getValue())){
//                    newmap.put(e.getKey(), e.getValue());
//                }
//            }
//            result = generatePartialPermutation(newmap, degree);
//            res2memo.put(pair, result);
//        }
//        return result;
//    }

    @Override
    public boolean equals(Object o) {
        return this.id == ((PartialPermutation) o).id;
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
package DataStructures;

import com.google.common.collect.ImmutableMap;
import org.javatuples.Pair;
import org.javatuples.Quintet;

import java.util.*;

public class GeneratingSystem {

    //    public List<Integer> domain;
    public Partition[] partitionMap;
//    public Map<String, Partition> partitionMap;
    private Map<String, Integer> stateMap;
    public static Map<HardTriplet<Integer, PartialPermutation, Integer>, Partition> partitionMemo;
//    public static Map<HardQuintet<Partition, Partition, String, PartialPermutation, String>, Partition> partitionMemo;
    public static List<Integer> domain;
    public static Map<Set<PartialPermutation>, Set<Integer>> bimemo;
    public static Map<HardTriplet<Set<Integer>, Set<Integer>, Map<Integer, Set<Integer>>>, Set<Integer>> bfsMemo;
    private static Map<Integer, Map<String, Partition>> fStateMemo;
    private static Map<Map<String, Partition>, Pair<Integer, Integer>> bStateMemo;
    public static int counter;


    public GeneratingSystem(List<Partition> R, int stateCount){
        if(fStateMemo == null) {
            fStateMemo = new HashMap<>();
            bStateMemo = new HashMap<>();
            counter = 0;
            partitionMemo = new HashMap<>();
        }
        stateMap = new HashMap<>(stateCount + 1, 1.0f);
        partitionMap = new Partition[stateCount];
//        partitionMap = new HashMap<>();
        for(Partition p: R)
            for(String state: p.rays.keySet()) {
                stateMap.put(state, stateMap.size());
                partitionMap[stateMap.get(state)] = p;
            }
    }
    public Partition[] getState(){
        Partition[] copy = new Partition[partitionMap.length];
        System.arraycopy(partitionMap, 0, copy, 0, partitionMap.length);
        return copy;
//        return Arrays.copyOf(partitionMap, partitionMap.length);
    }
//    public Integer getState(){
//        Map<String, Partition> mp = ImmutableMap.copyOf(partitionMap);
//        Pair<Integer, Integer> x = bStateMemo.get(mp);
//        if(x == null){
//            x = new Pair<>(counter, 1);
//            bStateMemo.put(mp, x);
//            fStateMemo.put(counter, mp);
//            counter ++;
//            return x.getValue0();
//        }
//        bStateMemo.put(mp, x.setAt1(x.getValue1() + 1));
//        return x.getValue0();
//    }

//    public Map<String, Partition> getState(){
//        return partitionMap;
//    }
//    public Map<String, Partition> getState(){
//        return Collections.unmodifiableMap(partitionMap);
//    }

    public void setState(Partition[] state){
        partitionMap = state;
    }

//    public void setState(Integer ticket){
//        Map<String, Partition> mp = fStateMemo.get(ticket);
//        Pair<Integer, Integer> x = bStateMemo.get(mp);
////        System.out.println(x + " => " + bStateMemo.values());
//        if(x.getValue1() == 1){
//            bStateMemo.remove(mp);
//            fStateMemo.remove(ticket);
//        }
//        else{
//            bStateMemo.put(mp, x.setAt1(x.getValue1() - 1));
//        }
//        partitionMap = new HashMap<>(mp);
//    }
//    public void setState(Map<String, Partition> state){
//        partitionMap = new HashMap<>(state);
//    }

    public boolean isMember(String q1, PartialPermutation sigma, String q2){
        Partition p1 = partitionMap[stateMap.get(q1)];
        Partition p2 = partitionMap[stateMap.get(q2)];
        if(p1 != p2) return false;
        PartialPermutation s1 = p1.rays.get(q1);
        PartialPermutation s2 = p2.rays.get(q2);
        PartialPermutation sigma_hat = PartialPermutation.bigMultiply(s1, sigma, s2.inverse());
//        PartialPermutation sigma_hat = s1.multiply(sigma).multiply(s2.inverse());
        if(sigma_hat.xc_check()){
            if(sigma_hat.domain.equals(p1.xc))
//        if(sigma_hat.domain.equals(p1.xc) && sigma_hat.range.equals(p1.xc)){
            return p1.group.isMember(sigma_hat);
        }
        return false;
    }

    public void update(String q1, PartialPermutation sigma, String q2) {
//        if(isMember(q1, sigma, q2)) return;
        Partition p1 = partitionMap[stateMap.get(q1)];
        Partition p2 = partitionMap[stateMap.get(q2)];
        PartialPermutation sigma_q1 = p1.rays.get(q1);
        PartialPermutation sigma_q2 = p2.rays.get(q2);
        PartialPermutation sigma_hat = PartialPermutation.bigMultiply(sigma_q1, sigma, sigma_q2.inverse());
        HardTriplet<Integer, PartialPermutation, Integer> q = new HardTriplet<>(p1.id, sigma_hat, p2.id);
//        HardQuintet<Partition, Partition, String, PartialPermutation, String> q = new HardQuintet<>(new Quintet<>(p1, p2, q1, sigma, q2));
        Partition ptmp = partitionMemo.get(q);
        if(ptmp != null){
            for(String state: ptmp.rays.keySet())
                partitionMap[stateMap.get(state)] = ptmp;
            return;
        }
        Partition part = p1.clone();
        partitionMemo.put(q, part);
//        partitionMemo.put(new HardTriplet<>(p2.id, sigma_hat.inverse(), p1.id), part);
        for(String state: p1.rays.keySet())
            partitionMap[stateMap.get(state)] = part;
//        PartialPermutation sigma_hat = sigma_q1.multiply(sigma).multiply(sigma_q2.inverse());
        Set<PartialPermutation> I;
        if(p1 == p2){
            if(sigma_hat.domain.equals(part.xc)){
                part.addPermutation(sigma);
                return;
            }
            I = part.group.getGc();
            I.add(sigma_hat);
        }
        else{
            for(String key: p2.rays.keySet()) {
                part.rays.put(key, sigma_hat.multiply(p2.rays.get(key)));
                partitionMap[stateMap.get(key)] = part;
            }
            I = part.group.getGc();
            PartialPermutation sigma_hat_inverse = sigma_hat.inverse();
            boolean empty = true;
            for(PartialPermutation p: p2.group.getGc()){
                PartialPermutation tauHat = PartialPermutation.bigMultiply(sigma_hat, p, sigma_hat_inverse);
//                PartialPermutation tauHat = sigma_hat.multiply(p).multiply(sigma_hat_inverse);
                    if(!part.group.isMember(tauHat)) {
                        empty = false;
                        I.add(tauHat);
                    }
            }
            if(empty){
                return;
            }
        }
        Set<Integer> B_I = generate_BI(I, sigma_hat.degree);
        part.xc = B_I;
        part.rays.replaceAll((k, v) -> v.restrict(B_I));
        part.group = new SetPermutationGroup(I);
//        if(merge)
//            for(String key: p2.rays.keySet()){
////                part.rays.put(key, sigma_hat.multiply(p2.rays.get(key)));
//                partitionMap[stateMap.get(key)] = part;
//            }
    }

    private Set<Integer> generate_BI(Set<PartialPermutation> I, int degree) {
        if(domain == null)
        {
            domain = new ArrayList<>();
            for(int j = 1; j<degree+1; j++) domain.add(j);
        }
        if(bimemo == null) bimemo = new HashMap<>();
        Set<Integer> res = bimemo.get(I);
        if(res == null){
            Map<Integer, Set<Integer>> edges = new HashMap<>();
            HashSet<Integer> endangered = new HashSet<>();
            Set<Integer> domset = new HashSet<>(domain);
            for(PartialPermutation sigma: I){
                for(int key: sigma.domain){
                    int val = sigma.apply(key);
                    edges.computeIfAbsent(key, k -> new HashSet<>());
                    edges.computeIfAbsent(val, v -> new HashSet<>());
                    edges.get(key).add(val);
                    edges.get(val).add(key);
                }
                HashSet<Integer> total = new HashSet<>(domset);
                HashSet<Integer> intersection = new HashSet<>(sigma.domain);
                intersection.retainAll(sigma.range);
                total.removeAll(intersection);
                endangered.addAll(total);
            }
            domset.removeAll(endangered);
            res = bfs(domset, endangered, edges);
            bimemo.put(I,res);
        }
        return res;
    }

    private Set<Integer> bfs(Set<Integer> good, Set<Integer> bad, Map<Integer, Set<Integer>> edges) {
        if(bfsMemo == null) bfsMemo = new HashMap<>();
        HardTriplet<Set<Integer>, Set<Integer>, Map<Integer, Set<Integer>>> t = new HardTriplet<>(good, bad, edges);
        Set<Integer> res = bfsMemo.get(t);
        if(res == null) {
            counter ++;
            var badQ = new LinkedList<>(bad);
//            var visited = new HashSet<Integer>();
            while (badQ.size() > 0) {
                Integer current = badQ.pop();
//                bad.add(current);
//                visited.add(current);
                if (edges.get(current) == null) continue;
                for (int v : edges.get(current))
                    if (!bad.contains(v)) {
//                    if (!visited.contains(v) && !bad.contains(v)) {
                        bad.add(v);
                        good.remove(v);
                        badQ.add(v);
                    }
            }
            bfsMemo.put(t, good);
            return good;
        }
        return res;
    }

    @Override
    public String toString(){
        String s = "Generating System with:\n";
        HashSet<String> checked = new HashSet<>();
        for(Partition p: partitionMap){
            if(checked.contains(p.qc)){
                continue;
            }
            checked.addAll(p.rays.keySet());
            s = s + "\t- " + p + "\n";
        }
        return s;
    }

}



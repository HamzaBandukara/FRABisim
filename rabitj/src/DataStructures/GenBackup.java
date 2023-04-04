//package DataStructures;
//
//import org.javatuples.Pair;
//import org.javatuples.Triplet;
//import org.javatuples.Quintet;
//
//import com.google.common.collect.ImmutableSet;
//
//import java.util.*;
//
//public class GeneratingSystem {
//
//    //    public List<Integer> domain;
//    public Map<String, Partition> partitionMap;
//    public static Map<Quintet<Partition, Partition, String, PartialPermutation, String>, Partition> partitionMemo;
//    public static List<Integer> domain;
//    public static Map<Set<PartialPermutation>, Set<Integer>> bimemo;
//    public static Map<Triplet<Set<Integer>, Set<Integer>, Map<Integer, Set<Integer>>>, Set<Integer>> bfsMemo;
//
//    public GeneratingSystem(List<Partition> R){
//        partitionMap = new HashMap<>();
//        for(Partition p: R)
//            for(String state: p.rays.keySet())
//                partitionMap.put(state, p);
//    }
//
//    public Map<String, Partition> getState(){
//        return partitionMap;
//    }
//
//    public void setState(Map<String, Partition> state){
//        partitionMap = state;
//    }
//
//    public boolean isMember(String q1, PartialPermutation sigma, String q2){
//        Partition p1 = partitionMap.get(q1);
//        Partition p2 = partitionMap.get(q2);
//        if(p1 != p2) return false;
//        PartialPermutation s1 = p1.rays.get(q1);
//        PartialPermutation s2 = p2.rays.get(q2);
//        PartialPermutation sigma_hat = s1.multiply(sigma).multiply(s2.inverse());
//        HashSet<Integer> xc = new HashSet<>(p1.xc);
//        if(sigma_hat.domain.equals(xc) && sigma_hat.range.equals(xc)){
//            return p1.group.isMember(sigma_hat);
//        }
//        return false;
//    }
//
//    public void update(String q1, PartialPermutation sigma, String q2) {
//        if(isMember(q1, sigma, q2)) return;
//        partitionMap = new HashMap<>(partitionMap);
//        if(partitionMemo==null) partitionMemo = new HashMap<>();
//        Partition p1 = partitionMap.get(q1);
//        Partition p2 = partitionMap.get(q2);
//        Quintet<Partition, Partition, String, PartialPermutation, String> q = new Quintet<>(p1, p2, q1, sigma, q2);
//        if(partitionMemo.get(q) != null){
//            Partition part = partitionMemo.get(q);
//            for(String state: part.rays.keySet())
//                partitionMap.put(state, part);
//            return;
//        }
//        Partition part = p1.clone();
//        partitionMemo.put(q, part);
//        boolean merge = false;
//        for(String state: p1.rays.keySet())
//            partitionMap.put(state, part);
//        PartialPermutation sigma_q1 = part.rays.get(q1);
//        PartialPermutation sigma_q2 = p2.rays.get(q2);
//        PartialPermutation sigma_hat = sigma_q1.multiply(sigma).multiply(sigma_q2.inverse());
//        Set<PartialPermutation> I;
//        if(p1 == p2){
//            if(sigma_hat.domain.equals(new HashSet<>(part.xc))){
//                part.addPermutation(sigma);
//                return;
//            }
//            I = new HashSet<>(part.group.gc);
//            I.add(sigma_hat);
//        }
//        else{
//            merge = true;
//            for(String key: p2.rays.keySet())
//                part.rays.put(key, p2.rays.get(key));
//            I = new HashSet<>(part.group.gc);
//            PartialPermutation sigma_hat_inverse = sigma_hat.inverse();
//            for(PartialPermutation p: p2.rays.values()){
//                PartialPermutation tauHat = sigma_hat.multiply(p).multiply(sigma_hat_inverse);
//                I.add(tauHat);
//            }
//        }
//        Set<Integer> B_I = generate_BI(I, sigma_hat.degree);
//        part.xc = B_I;
//        part.rays.replaceAll((k, v) -> part.rays.get(k).restrict(B_I));
//        if(merge)
//            for(String key: p2.rays.keySet()){
//                part.rays.put(key, sigma_hat.multiply(p2.rays.get(key)));
//                partitionMap.put(key, part);
//            }
//    }
//
//    private Set<Integer> generate_BI(Set<PartialPermutation> I, int degree) {
//        if(domain == null)
//        {
//            domain = new ArrayList<>();
//            for(int j = 1; j<degree+1; j++) domain.add(j);
//        }
//        if(bimemo == null) bimemo = new HashMap<>();
//        Set<Integer> res = bimemo.get(I);
//        if(res == null){
//            Map<Integer, Set<Integer>> edges = new HashMap<>();
//            HashSet<Integer> endangered = new HashSet<>();
//            Set<Integer> domset = new HashSet<>(domain);
//            for(PartialPermutation sigma: I){
//                for(int key: sigma.domain){
//                    int val = sigma.apply(key);
//                    edges.computeIfAbsent(key, k -> new HashSet<>());
//                    edges.computeIfAbsent(val, v -> new HashSet<>());
//                    edges.get(key).add(val);
//                    edges.get(val).add(key);
//                }
//                HashSet<Integer> total = new HashSet<>(domset);
//                HashSet<Integer> toremove = new HashSet<>(sigma.domain);
//                toremove.removeAll(sigma.range);
//                total.removeAll(toremove);
//                endangered.addAll(total);
//            }
//            domset.removeAll(endangered);
//            res = bfs(domset, endangered, edges);
//            bimemo.put(I,res);
//        }
//        return res;
//    }
//
//    private Set<Integer> bfs(Set<Integer> good, Set<Integer> bad, Map<Integer, Set<Integer>> edges) {
//        if(bfsMemo == null) bfsMemo = new HashMap<>();
//        Triplet<Set<Integer>, Set<Integer>, Map<Integer, Set<Integer>>> t = new Triplet<>(good, bad, edges);
//        Set<Integer> res = bfsMemo.get(t);
//        if(res == null) {
//            var badQ = new LinkedList<>(bad);
//            var visited = new HashSet<Integer>();
//            while (badQ.size() > 0) {
//                int current = badQ.pop();
//                visited.add(current);
//                if (edges.get(current) == null) continue;
//                for (int v : edges.get(current))
//                    if (!visited.contains(v) && !bad.contains(v)) {
//                        bad.add(v);
//                        good.remove(v);
//                        badQ.add(v);
//                    }
//            }
//            bfsMemo.put(t, good);
//            return good;
//        }
//        return res;
//    }
//
//}
//
//

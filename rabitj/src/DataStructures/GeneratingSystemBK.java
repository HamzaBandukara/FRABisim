package DataStructures;

import org.javatuples.Quintet;

import java.util.*;

public class GeneratingSystemBK {

    //    public List<Integer> domain;
    public PartitionList partitionMap;
    public static Map<HardQuintet<Partition, Partition, String, PartialPermutation, String>, Partition> partitionMemo;
    public static List<Integer> domain;
    public static Map<Set<PartialPermutation>, Set<Integer>> bimemo;
    public static Map<HardTriplet<Set<Integer>, Set<Integer>, Map<Integer, Set<Integer>>>, Set<Integer>> bfsMemo;

    public GeneratingSystemBK(List<Partition> R){
        partitionMap = null;
        for(Partition p: R)
            partitionMap = new PartitionList(p, partitionMap);
    }

    public PartitionList getState(){
        return partitionMap;
    }

    public void setState(PartitionList state){
        partitionMap = state;
    }

    public boolean isMember(String q1, PartialPermutation sigma, String q2){
        Partition p1 = partitionMap.getPartition(q1);
        Partition p2 = partitionMap.getPartition(q2);
        if(p1 != p2) return false;
        PartialPermutation s1 = p1.rays.get(q1);
        PartialPermutation s2 = p2.rays.get(q2);
        PartialPermutation sigma_hat = s1.multiply(sigma).multiply(s2.inverse());
        HashSet<Integer> xc = new HashSet<>(p1.xc);
        if(sigma_hat.domain.equals(xc) && sigma_hat.range.equals(xc)){
            return p1.group.isMember(sigma_hat);
        }
        return false;
    }

    public void update(String q1, PartialPermutation sigma, String q2) {
        if(isMember(q1, sigma, q2)) return;
        if(partitionMemo==null) partitionMemo = new HashMap<>();
        Partition p1 = partitionMap.getPartition(q1);
        Partition p2 = partitionMap.getPartition(q2);
        HardQuintet<Partition, Partition, String, PartialPermutation, String> q = new HardQuintet<>(new Quintet<>(p1, p2, q1, sigma, q2));
        Partition ptmp = partitionMemo.get(q);
        if(ptmp != null){
            partitionMap = new PartitionList(ptmp, partitionMap);
            return;
        }
        Partition part = p1.clone();
        partitionMemo.put(q, part);
        partitionMap = new PartitionList(part, partitionMap);
        boolean merge = false;
        PartialPermutation sigma_q1 = part.rays.get(q1);
        PartialPermutation sigma_q2 = p2.rays.get(q2);
        PartialPermutation sigma_hat = sigma_q1.multiply(sigma).multiply(sigma_q2.inverse());
//        System.out.println(sigma_hat + " " + sigma_q1 + " " + sigma + " " + sigma_q2);
        Set<PartialPermutation> I;
        if(p1 == p2){
            if(sigma_hat.domain.equals(new HashSet<>(part.xc))){
                part.addPermutation(sigma);
                return;
            }
            I = new HashSet<>(part.group.gc);
            I.add(sigma_hat);
        }
        else{
            merge = true;
            for(String key: p2.rays.keySet())
                part.rays.put(key, p2.rays.get(key));
            I = new HashSet<>(part.group.gc);
            PartialPermutation sigma_hat_inverse = sigma_hat.inverse();
            for(PartialPermutation p: p2.rays.values()){
                PartialPermutation tauHat = sigma_hat.multiply(p).multiply(sigma_hat_inverse);
                I.add(tauHat);
            }
        }
        Set<Integer> B_I = generate_BI(I, sigma_hat.degree);
//        System.out.println("BI: " + B_I + " > " + I);
        part.xc = B_I;
        part.rays.replaceAll((k, v) -> part.rays.get(k).restrict(B_I));
        if(merge)
            for(String key: p2.rays.keySet()){
                part.rays.put(key, sigma_hat.multiply(p2.rays.get(key)));
            }
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
            var badQ = new LinkedList<>(bad);
            var visited = new HashSet<Integer>();
            while (badQ.size() > 0) {
                Integer current = badQ.pop();
                visited.add(current);
                if (edges.get(current) == null) continue;
                for (int v : edges.get(current))
                    if (!visited.contains(v) && !bad.contains(v)) {
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
        PartitionList p = partitionMap;
        HashSet<String> checked = new HashSet<>();
        while(p!=null){
            if(checked.contains(p.value.qc)){
                p = p.next;
                continue;
            }
            checked.addAll(p.value.rays.keySet());
            s = s + "\t- " + p.value + "\n";
            p = p.next;
        }
        return s;
    }

}



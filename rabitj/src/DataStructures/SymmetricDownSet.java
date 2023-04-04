package DataStructures;

import ProcessElement.Par;
import org.javatuples.Triplet;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class SymmetricDownSet {

    public Map<String, Map<String, Set<PartialPermutation>>> partitionMap;
    public int size;
    public Set<HardTriplet<String, PartialPermutation, String>> members;

    public SymmetricDownSet(){
        partitionMap = new HashMap<>();
        size = 0;
        members = new HashSet<>();
    }

    public boolean isMember(String q1, PartialPermutation ray, String q2){
        HardTriplet<String, PartialPermutation, String> t = new HardTriplet<>(q1, ray, q2);
        if(members.contains(t)) {
            return true;
        }
        Map<String, Set<PartialPermutation>> tmp = partitionMap.get(q1);
        if(tmp == null) return false;
        Set<PartialPermutation> tmp2 = tmp.get(q2);
        if(tmp2 == null) return false;
        for(PartialPermutation sigma: tmp2){
            if(sigma.map.entrySet().containsAll(ray.map.entrySet())){
                members.add(t);
                members.add(new HardTriplet<>(q2, ray.inverse(), q1));
                return true;
            }
        }
        return false;
    }

    public void update(String q1, PartialPermutation ray, String q2){
        members.add(new HardTriplet<>(q1, ray, q2));
        members.add(new HardTriplet<>(q2, ray.inverse(), q1));
        partitionMap.computeIfAbsent(q1, k -> new HashMap<>());
        partitionMap.get(q1).computeIfAbsent(q2, k -> new HashSet<>());
        partitionMap.computeIfAbsent(q2, k -> new HashMap<>());
        partitionMap.get(q2).computeIfAbsent(q1, k -> new HashSet<>());
        Set<PartialPermutation> q1set = partitionMap.get(q1).get(q2);
        Set<PartialPermutation> q2set = partitionMap.get(q2).get(q1);
        HashSet<PartialPermutation> set = new HashSet<>(q1set);
        for(PartialPermutation s: set){
            if(ray.map.entrySet().containsAll(s.map.entrySet())) return;
            if(s.map.entrySet().containsAll(ray.map.entrySet())){
                q1set.remove(s);
                q2set.remove(s.inverse());
                size -= 2;
            }
        }
        q1set.add(ray);
        q2set.add(ray.inverse());
        size += 2;
    }
}

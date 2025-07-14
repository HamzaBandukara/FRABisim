import DataStructures.*;

import java.util.*;

public class Fwd {

    public static int callcntr;
    public static int bkcntr;

    public static boolean forward(RA ra, String q1, Map<Integer, Integer> set, String q2){
        PartialPermutation sigma = PartialPermutation.generatePartialPermutation(set, ra.degree);
        Map<HardTriplet<String, PartialPermutation, String>, Integer> visited = new HashMap<>();
        Set<Integer> assumed = new HashSet<>();
        Set<HardTriplet<String, PartialPermutation, String>> bad = new HashSet<>();
        Set<Integer> deleted = new HashSet<>();
        GlobalCounter counter = new GlobalCounter();
        callcntr = 0;
        bkcntr = 0;
        boolean result = bisimOK(q1, sigma, q2, ra, visited, assumed, bad, counter, deleted);
//        System.out.println("Calls: " + callcntr);
//        System.out.println("Backtracks: " + bkcntr);
        return result;
    }

    private static boolean checkTags(RA ra, String q1, String q2){
        return ra.getTags(q1).equals(ra.getTags(q2));
    }

    private static boolean bisimOK(String q1, PartialPermutation sigma, String q2, RA ra, Map<HardTriplet<String, PartialPermutation, String>, Integer> visited, Set<Integer> assumed, Set<HardTriplet<String, PartialPermutation, String>> bad, GlobalCounter counter, Set<Integer> deleted) {
        callcntr ++;
        HardTriplet<String, PartialPermutation, String> current = new HardTriplet<>(q1, sigma, q2);
        if(bad.contains(current)) {
            return false;
        }
        Integer tmp = visited.get(current);
        if(tmp != null){
            if(!deleted.contains(tmp)){
                assumed.add(tmp);
                return true;
            }
        }
        HardTriplet<String, PartialPermutation, String> inverse = new HardTriplet<>(q2, sigma.inverse(), q1);
        if(!checkTags(ra, q1, q2)){
            bad.add(current);
            bad.add(inverse);
            return false;
        }
        counter.increment();
        int currentCounter = counter.getValue();
        visited.put(current, currentCounter);
        visited.put(inverse, currentCounter);
        if(simulate(q1, sigma, q2, ra, visited, assumed, bad, counter, deleted))
            if(simulate(q2, sigma.inverse(), q1, ra, visited, assumed, bad, counter, deleted)){
                return true;
            }
        bad.add(current);
        bad.add(inverse);
        if(assumed.contains(currentCounter)){
            for(int i = currentCounter; i<counter.getValue() + 1; i++){
                deleted.add(i);
                assumed.remove(i);
            }
        }
        bkcntr ++;
        return false;
    }

    private static boolean simulate(String q1, PartialPermutation sigma, String q2, RA ra, Map<HardTriplet<String, PartialPermutation, String>, Integer> visited, Set<Integer> assumed, Set<HardTriplet<String, PartialPermutation, String>> bad, GlobalCounter counter, Set<Integer> deleted) {
        for(String tag: ra.getTags(q1)){
            Map<String, Map<Integer, Set<String>>> alltrans1 = ra.transitions.get(q1).get(tag);
            Map<String, Map<Integer, Set<String>>> alltrans2 = ra.transitions.get(q2).get(tag);
            for(String type1: alltrans1.keySet())
                for(int reg1: alltrans1.get(type1).keySet()) {
                    if (tag.equals("TAU")) {
                        for (String nextq1 : ra.getTargets(q1, tag, type1, reg1)) {
                            boolean found = false;
                            for (String nextq2 : ra.getTargets(q2, tag, type1, reg1)) {
                                PartialPermutation nsigma = sigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                if (bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)) {
                                    found = true;
                                    break;
                                }
                            }
                            if (!found) return false;
                        }
                    }
                    else if(type1.equals("K")){
                        if(sigma.domain.contains(reg1)){
                            int reg2 = sigma.apply(reg1);
                            for(String nextq1: ra.getTargets(q1, tag, type1, reg1)){
                                boolean found = false;
                                for(String nextq2: ra.getTargets(q2, tag, type1, reg2)){
                                    PartialPermutation nsigma = sigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)){
                                        found = true;
                                        break;
                                    }
                                }
                                if(!found) return false;
                            }
                        }
                        else{
                            for(String nextq1: ra.getTargets(q1, tag, type1, reg1)){
                                boolean found = false;
                                for(int reg2: alltrans2.get("L").keySet()) {
                                    PartialPermutation newsigma = sigma.add(reg1, reg2);
                                    for(String nextq2:ra.getTargets(q2, tag, "L", reg2)) {
                                        PartialPermutation nsigma = newsigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                        if(bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)){
                                            found = true;
                                            break;
                                        }
                                    }
                                    if(found) break;
                                }
                                if(!found) return false;
                            }
                        }
                    }
                    else if(type1.equals("L")){
                        for(String nextq1: ra.getTargets(q1, tag, type1, reg1)){
                            boolean found = false;
                            for(int reg2: alltrans2.get("L").keySet()){
                                PartialPermutation newsigma = sigma.add(reg1, reg2);
                                for(String nextq2: ra.getTargets(q2, tag, type1, reg2)){
                                    PartialPermutation nsigma = newsigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)){
                                        found = true;
                                        break;
                                    }
                                }
                                if(found) break;
                            }
                            if(!found) return false;
                        }
                        Set<Integer> sub = new HashSet<>(ra.s_map.get(q2));
                        sub.removeAll(sigma.range);
                        for(int x: sub){
                            PartialPermutation newsigma = sigma.add(reg1, x);
                            for(String nextq1: ra.getTargets(q1, tag, type1, reg1)){
                                boolean found = false;
                                for(String nextq2: ra.getTargets(q2, tag, "K", x)){
                                    PartialPermutation nsigma = newsigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)){
                                        found = true;
                                        break;
                                    }
                                }
                                if(!found) return false;
                            }
                        }

                    }
                    else if(type1.equals("G")){
                        for(String nextq1: ra.getTargets(q1, tag, type1, reg1)){
                            boolean found = false;
                            for(int reg2: ra.transitions.get(q2).get(tag).get(type1).keySet()){
                                PartialPermutation newsigma = sigma.add(reg1, reg2);
                                for(String nextq2: ra.getTargets(q2, tag, type1, reg2)){
                                    PartialPermutation nsigma = newsigma.restrict(ra.s_map.get(nextq1), ra.s_map.get(nextq2));
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, visited, assumed, bad, counter, deleted)){
                                        found = true;
                                        break;
                                    }
                                }
                                if(found) break;
                            }
                            if(!found) return false;
                        }
                    }

                }
        }
        return true;
    }
}
import DataStructures.*;

import java.util.*;

public class FwdGen{

    public static int callcnt;
    public static int bkcnt;

    public static boolean forward(RA ra, String q1, Map<Integer, Integer> set, String q2){
        PartialPermutation sigma = PartialPermutation.generatePartialPermutation(set, ra.degree);
        List<Partition> partitions = new ArrayList<>();
        for(String q: ra.s_map.keySet()){
            HashMap<String, PartialPermutation> rays = new HashMap<>();
            HashMap<Integer, Integer> ray = new HashMap<>();
            for(int x: ra.s_map.get(q)) ray.put(x, x);
            rays.put(q, PartialPermutation.generatePartialPermutation(ray, ra.degree));
            partitions.add(new Partition(q, new HashSet<>(ra.s_map.get(q)), rays));
        }
        GeneratingSystem G;
        G = new GeneratingSystem(partitions, ra.s_map.size());
        SymmetricDownSet notBisim = new SymmetricDownSet();
        callcnt = 0;
        bkcnt = 0;
        boolean result = bisimOK(q1, sigma, q2, ra, G, notBisim);
//        System.out.println("Calls: " + callcnt);
//        System.out.println("Backtracks: " + bkcnt);
//        System.out.println("BFS: " + GeneratingSystem.counter);
//        System.out.println("Saved Permutation Calls: " + PartialPermutation.counter);
        return result;
    }

    private static boolean checkTags(RA ra, String q1, String q2){
        return ra.getTags(q1).equals(ra.getTags(q2));
    }

    private static boolean bisimOK(String q1, PartialPermutation sigma, String q2, RA ra, GeneratingSystem G, SymmetricDownSet notBisim) {
        callcnt ++;
        if(notBisim.isMember(q1, sigma, q2)) {
            return false;
        }
        if(G.isMember(q1, sigma, q2)) {
            return true;
        }
        if(!checkTags(ra, q1, q2)){
            notBisim.update(q1, sigma, q2);
            return false;
        }
        Partition[] state = G.getState();
        G.update(q1, sigma, q2);
        if(simulate(q1, sigma, q2, ra, G, notBisim))
            if(simulate(q2, sigma.inverse(), q1, ra, G, notBisim)){
                return true;
            }
        bkcnt ++;
        G.setState(state);
//        System.out.println("Bad: " + q1 + " " + q2 + " " + sigma);
        notBisim.update(q1, sigma, q2);
        return false;
    }

    private static boolean simulate(String q1, PartialPermutation sigma, String q2, RA ra, GeneratingSystem g, SymmetricDownSet notBisim) {
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
                                if (bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)) {
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
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)){
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
                                        if(bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)){
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
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)){
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
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)){
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
                                    if(bisimOK(nextq1, nsigma, nextq2, ra, g, notBisim)){
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
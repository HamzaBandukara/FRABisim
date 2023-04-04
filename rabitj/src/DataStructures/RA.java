package DataStructures;

import ProcessElement.Definition;
import ProcessElement.Process;
import ProcessElement.RawProcess;
import ProcessElement.Transition;
import org.antlr.v4.runtime.misc.Pair;
import ParserPi.Antlr;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.util.*;

public class RA{

    public Map<String, Set<Integer>> s_map;
    public Map<String, Map<String, Map<String, Map<Integer, Set<String>>>>> transitions;
    public int degree;
    public boolean deterministic;
    public Process currentProcess1;
    public Process currentProcess2;
    private Set<Process> seen;
    private Map<Process, HashSet<Transition>> memo;
    private Map<String, HashSet<Transition>> memoStrict;
    private Map<Process, String> pmap;
    public int transitionCounter;

    public RA(){
        s_map = new HashMap<>();
        transitions = new HashMap<>();
        degree = 0;
        deterministic = false;
        seen = new HashSet<>();
        memo = new HashMap<>();
        memoStrict = new HashMap<>();
        pmap =new HashMap<>();
        transitionCounter = 0;
    }

    public void completeSetup(){
        s_map.replaceAll((k, v) -> Collections.unmodifiableSet(s_map.get(k)));
    }

    public Set<String> getTargets(String src, String tag, String type, int reg){
        Set<String> targets = transitions.get(src).get(tag).get(type).get(reg);
        if(targets != null)
            return targets;
        return new HashSet<>();
    }


    public void AddTransition(String src, String tag, int reg, String type, String tgt){
        if(!transitions.containsKey(src))
            transitions.put(src, new HashMap<>());
        if(!transitions.get(src).containsKey(tag)) {
            transitions.get(src).put(tag, new HashMap<>());
            transitions.get(src).get(tag).put("K", new HashMap<>());
            transitions.get(src).get(tag).put("L", new HashMap<>());
            transitions.get(src).get(tag).put("G", new HashMap<>());
        }
        if(!transitions.get(src).get(tag).get(type).containsKey(reg))
            transitions.get(src).get(tag).get(type).put(reg, new HashSet<>());
        if (!transitions.get(src).get(tag).get(type).get(reg).contains(tgt)) transitionCounter++;
        transitions.get(src).get(tag).get(type).get(reg).add(tgt);
        if(transitions.get(src).get(tag).get(type).get(reg).size() > 1){ deterministic = false; }
        if(reg > degree) degree = reg;
    }

    public String getPmap(Process p){
        if(pmap.get(p) == null)
            pmap.put(p, "q" + pmap.size());
        return pmap.get(p);
    }

    public void PiOTF(String fileName, String letter) throws Exception{
        Pair<RawProcess, Map<String, Definition>> x = Antlr.run(fileName);
        Process.defined = x.b;
        Map<Integer, Integer> nmap = new HashMap<>();
        for(int i: x.a.support)
            nmap.put(i, i*-1);
        Process tmp = new Process(x.a, nmap);
        tmp.rehash();
        List<Transition> stp = new ArrayList<>(tmp.Step(true, seen, memo, memoStrict));
        currentProcess1 = stp.get(0).tgt;
        currentProcess2 = stp.get(stp.size() - 1).tgt;
    }

    public void PiProcess(String fileName, String letter) throws Exception {
        Pair<RawProcess, Map<String, Definition>> x = Antlr.run(fileName);
        Process.defined = x.b;
        LinkedHashSet<Transition> transitions = Process.Reduce(x.a);
        HashMap<String, String> statemap = new HashMap<>();
        String state;
        String state2;
        for(Transition t: transitions){
//            System.out.println( " - " + t);
            if(!statemap.containsKey(t.src.uid))
                statemap.put(t.src.uid, letter + statemap.size());
            state = statemap.get(t.src.uid);
            if(!this.s_map.containsKey(state)) s_map.put(state, new HashSet<>(t.src.nameMap.values()));
            if(!statemap.containsKey(t.tgt.uid)) statemap.put(t.tgt.uid, letter + statemap.size());
            if(!this.s_map.containsKey(statemap.get(t.tgt.uid))) s_map.put(statemap.get(t.tgt.uid), new HashSet<>(t.tgt.nameMap.values()));
            switch(t.type.substring(0, 3)){
                case "TAU":
                    state2 = statemap.get(t.tgt.uid);
                    AddTransition(state, "TAU", -1, "K", state2);
                    break;
                case "inp":
                    state2 = state + "inp" + t.reg1;
                    if(!this.s_map.containsKey(state2))
                        this.s_map.put(state2, this.s_map.get(state));
                    AddTransition(state, "inp", t.reg1, "K", state2);
                    if(t.type.charAt(3) == 'F') {
                        AddTransition(state2, "inp2", t.reg2, "L", statemap.get(t.tgt.uid));
                    }
                    else {
                        AddTransition(state2, "inp2", t.reg2, "K", statemap.get(t.tgt.uid));
                    }
                    break;
                case "out":
                    state2 = state + "out" + t.reg1;
                    this.s_map.put(state2, this.s_map.get(state));
                    AddTransition(state, "out", t.reg1, "K", state2);
                    if(t.type.charAt(3) == 'F') {
                        AddTransition(state2, "out2", t.reg2, "G", statemap.get(t.tgt.uid));
                    }
                    else {
                        AddTransition(state2, "out2", t.reg2, "K", statemap.get(t.tgt.uid));
                    }
                default:
                    break;
            }
        }
//        for(Map.Entry<String, String> e: statemap.entrySet())
//            System.out.println(e.getKey() + " ===> " + e.getValue());
        completeSetup();
    }

    public void PiProcessWeak(String fileName, String letter) throws Exception {
        Pair<RawProcess, Map<String, Definition>> x = Antlr.run(fileName);
        Process.defined = x.b;
        LinkedHashSet<Transition> trans = Process.Reduce(x.a);
        HashMap<String, String> statemap = new HashMap<>();
        String state;
        String state2;
        Map<String, Set<String>> tauMap = new HashMap<>();
        for(Transition t: trans){
            if(!statemap.containsKey(t.src.uid))
                statemap.put(t.src.uid, letter + statemap.size());
            state = statemap.get(t.src.uid);
            tauMap.computeIfAbsent(state, k -> new HashSet<>());
            tauMap.get(state).add(state);
            if(!this.s_map.containsKey(state)) s_map.put(state, new HashSet<>(t.src.nameMap.values()));
            if(!statemap.containsKey(t.tgt.uid)) statemap.put(t.tgt.uid, letter + statemap.size());
            if(!this.s_map.containsKey(statemap.get(t.tgt.uid))) s_map.put(statemap.get(t.tgt.uid), new HashSet<>(t.tgt.nameMap.values()));
            tauMap.computeIfAbsent(statemap.get(t.tgt.uid), k -> new HashSet<>());
            tauMap.get(statemap.get(t.tgt.uid)).add(statemap.get(t.tgt.uid));
            switch(t.type.substring(0, 3)){
                case "TAU":
                    state2 = statemap.get(t.tgt.uid);
                    AddTransition(state, "TAU", -1, "K", state2);
                    tauMap.get(state).add(state2);
                    break;
                case "inp":
                    state2 = state + "inp" + t.reg1;
                    if(!this.s_map.containsKey(state2))
                        this.s_map.put(state2, this.s_map.get(state));
                    tauMap.computeIfAbsent(state2, k -> new HashSet<>());
                    tauMap.get(state2).add(state2);
                    AddTransition(state, "inp", t.reg1, "K", state2);
                    if(t.type.charAt(3) == 'F') {
                        AddTransition(state2, "inp2", t.reg2, "L", statemap.get(t.tgt.uid));
                    }
                    else {
                        AddTransition(state2, "inp2", t.reg2, "K", statemap.get(t.tgt.uid));
                    }
                    break;
                case "out":
                    state2 = state + "out" + t.reg1;
                    this.s_map.put(state2, this.s_map.get(state));
                    tauMap.computeIfAbsent(state2, k -> new HashSet<>());
                    tauMap.get(state2).add(state2);
                    AddTransition(state, "out", t.reg1, "K", state2);
                    if(t.type.charAt(3) == 'F') {
                        AddTransition(state2, "out2", t.reg2, "G", statemap.get(t.tgt.uid));
                    }
                    else {
                        AddTransition(state2, "out2", t.reg2, "K", statemap.get(t.tgt.uid));
                    }
                default:
                    break;
            }
        }

        Map<String, Set<String>> tauStar = new HashMap<>();
        for(String key: tauMap.keySet())
            tauStar.put(key, new HashSet<>(tauMap.get(key)));
        for(String key: tauStar.keySet()) {
            Set<String> examined = new HashSet<>(tauStar.get(key));
            LinkedList<String> queue = new LinkedList<>(tauStar.get(key));
            while (queue.size() > 0) {
                String current = queue.pop();
                if (tauMap.get(current) != null)
                    for (String item : tauMap.get(current)) {
                        tauStar.get(key).add(item);
                        if (!examined.contains(item)) {
                            queue.add(item);
                            examined.add(item);
                        }
                    }
            }
        }
        Map<String, Map<String, Map<String, Map<Integer, Set<String>>>>> delta1 = new HashMap<>(); // delta1 = tau*; delta
        for(String q: tauStar.keySet()){
            delta1.computeIfAbsent(q, k -> new HashMap<>());
            for(String q1: tauStar.get(q))
                if(this.transitions.get(q1) != null){
                    for(String tag: transitions.get(q1).keySet()){
                        if(!delta1.get(q).containsKey(tag)) {
                            delta1.get(q).put(tag, new HashMap<>());
                            delta1.get(q).get(tag).put("K", new HashMap<>());
                            delta1.get(q).get(tag).put("L", new HashMap<>());
                            delta1.get(q).get(tag).put("G", new HashMap<>());
                        }
                        for(String type: transitions.get(q1).get(tag).keySet()){
                            for(int reg: transitions.get(q1).get(tag).get(type).keySet()){
                                delta1.get(q).get(tag).get(type).computeIfAbsent(reg, k -> new HashSet<>());
                                for(String tgt: transitions.get(q1).get(tag).get(type).get(reg))
                                    delta1.get(q).get(tag).get(type).get(reg).add(tgt);
                            }

                        }
                    }
                }

        }
        Map<String, Map<String, Map<String, Map<Integer, Set<String>>>>> delta2 = new HashMap<>(); // delta2 = delta1; tau*
        for(String src: delta1.keySet())
            for(String tag: delta1.get(src).keySet())
                for(String type: delta1.get(src).get(tag).keySet())
                    for(int reg: delta1.get(src).get(tag).get(type).keySet())
                        for(String tgt: delta1.get(src).get(tag).get(type).get(reg))
                            for(String q2: tauStar.get(tgt)) {
                                delta2.computeIfAbsent(src, k -> new HashMap<>());
                                delta2.get(src).computeIfAbsent(tag, k -> new HashMap<>());
                                delta2.get(src).get(tag).computeIfAbsent(type, k -> new HashMap<>());
                                delta2.get(src).get(tag).get(type).computeIfAbsent(reg, k -> new HashSet<>());
                                delta2.get(src).get(tag).get(type).get(reg).add(q2);
                            }
        this.transitions = delta2;
        completeSetup();
//        System.out.println(this);
    }

    public String toString(){
        String s = (new HashSet<>(s_map.keySet())).toString().replace("[", "{").replace("]", "}");
        s = s + "{q0}{";
        for(String key: s_map.keySet()){
            s = s + "(" + key;
            for(int reg: s_map.get(key))
                s = s + "," + reg;
            s = s + ")";
        }
        s = s + "}{";
        for(String src: transitions.keySet())
            for(String tag: transitions.get(src).keySet())
                for(String type: transitions.get(src).get(tag).keySet())
                    for(int reg: transitions.get(src).get(tag).get(type).keySet())
                        for(String tgt: transitions.get(src).get(tag).get(type).get(reg))
                            s = s + String.format("(%s,%s,%d,%s,%s)", src, tag, reg, type, tgt);
        s = s + "{}}";
        return s;
    }

    public String raDebug(){
        String s = "DET: " + this.deterministic + "\nTransitions: ";
        ArrayList<String> trans = new ArrayList<>();
        for(String src: transitions.keySet())
            for(String tag: transitions.get(src).keySet())
                for(String type: transitions.get(src).get(tag).keySet())
                    for(int reg: transitions.get(src).get(tag).get(type).keySet())
                        for(String tgt: transitions.get(src).get(tag).get(type).get(reg))
                            trans.add(String.format("(%s,%s,%d,%s,%s)", src, tag, reg, type, tgt));
        Collections.sort(trans);
        for(String t: trans)
            s = s + "\n - " + t;
        return s;

    }

    public Set<String> getTags(String q) {
        if(transitions.get(q) != null)
            return transitions.get(q).keySet();
        return new HashSet<>();
    }
}

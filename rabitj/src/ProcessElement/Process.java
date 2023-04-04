package ProcessElement;

import java.util.*;
import java.util.regex.Pattern;


public class Process {

    public Map<Integer, Integer> nameMap;
    public RawProcess process;
    public static Map<String, Definition> defined;
    private int hash;
    public String uid;
    public HashMap<Integer, Integer> mp;
    public Set<Integer> iset;
    public Set<Integer> otherNames;

    public Process(RawProcess rp, Map<Integer, Integer> nmap){
        nameMap = nmap;
        process = rp;
        otherNames = new HashSet<>();
    }

    public Process duplicate(RawProcess newprocess){
        HashMap<Integer, Integer> map = new HashMap<>(nameMap);
        Process p = new Process(newprocess, map);
        p.otherNames = this.otherNames;
        p.rehash();
        return p;
    }

    public int findKey(int val){
        for(int key: nameMap.keySet()){
            if(nameMap.get(key) == val) return key;
        }
        return 0;
    }


    public static LinkedHashSet<Transition> Reduce(RawProcess a){
        Map<Integer, Integer> nmap = new HashMap<>();
        Process p = new Process(a, nmap);
        for(int val: a.support)
            nmap.put(val, val*-1);
//        p.ReFix();
        p.rehash();
        LinkedHashSet<Transition> transitions = new LinkedHashSet<>();
        HashSet<Process> seen = new HashSet<>();
        HashMap<Process, HashSet<Transition>> memo = new HashMap<>();
        HashMap<String, HashSet<Transition>> memoStrict = new HashMap<>();
        Process t;
        Set<Transition> tmp;
        Set<Process> examined = new HashSet<>();
        LinkedList<Process> queue = new LinkedList<>();
        tmp = p.Step(true, seen, memo, memoStrict);
        for(Transition x: tmp){
            transitions.add(x);
            queue.add(x.tgt);
        }
        while(queue.size() > 0){
            t = queue.pop();
            examined.add(t);
            if(seen.contains(t)) continue;
            tmp = t.Step(true, seen, memo, memoStrict);
            for(Transition x: tmp){
                x.tgt.otherNames = new HashSet<>();
                if(!examined.contains(x.tgt)){
                    queue.add(x.tgt);
                }
                transitions.add(x);
            }
        }
        return transitions;
    }

    public HashSet<Transition> Step(boolean strict, Set<Process> seen, Map<Process, HashSet<Transition>> memo, Map<String, HashSet<Transition>> memoStrict){
        HashSet<Transition> nextTrans = new HashSet<>();
        if(strict)
            if(memoStrict.containsKey(uid)){
                return memoStrict.get(uid);
            }
        else
            if(memo.containsKey(this)){
                return memo.get(this);
            }
        seen.add(this);
        if(process instanceof Terminal) {
            if(strict){
                this.nameMap = new HashMap<>();
                this.rehash();
            }
            return nextTrans;
        }
        if(process instanceof Tau) {
            Process pNext = duplicate(process.childProcess[0]);
            Transition t = new Transition(this, -1, -1, "TAU", pNext);
            nextTrans.add(t);
        }
        if(process instanceof Par par){
            Process pLeft = duplicate(par.childProcess[0]);
            pLeft.otherNames.addAll(par.childProcess[1].names);
            Process pRight = duplicate(par.childProcess[1]);
            pRight.otherNames.addAll(par.childProcess[0].names);
            pLeft.rehash();
            pRight.rehash();
            boolean removeLeft = !seen.contains(pLeft);
            boolean removeRight = !seen.contains(pRight);
            HashSet<Transition> accL = pLeft.Step(false, seen, memo, memoStrict);
            if(removeLeft)
                seen.remove(pLeft);
            HashSet<Transition> accR = pRight.Step(false, seen, memo, memoStrict);
            if(removeRight)
                seen.remove(pRight);
            HashSet<Transition> accLP = new HashSet<>();
            HashSet<Transition> accRP = new HashSet<>();
            for(Transition t: accL){
                int i = -1;
                t = t.duplicate();
                for(int n: t.tgt.process.getSupport())
                    if(pRight.process.getNames().contains(n)){
                        if(strict)
                            while(t.tgt.process.getNames().contains(i) || t.tgt.process.getSupport().contains(i) || pRight.process.getSupport().contains(i) || pRight.process.getNames().contains(i))
                                i--;
                        else
                            while(t.tgt.process.getNames().contains(i) || t.tgt.process.getSupport().contains(i) || pRight.process.getSupport().contains(i) || pRight.process.getNames().contains(i) || t.tgt.nameMap.get(i) != null)
                                i--;

                        t.tgt.process = t.tgt.process.rewrite(n, i);
                        t.tgt.nameMap.put(i, t.tgt.nameMap.get(n));
                        t.tgt.nameMap.remove(n);
                    }
                accLP.add(t);
            }
            for(Transition t: accR){
                int i = -1;
                t = t.duplicate();
                for(int n: t.tgt.process.getSupport())
                    if(pLeft.process.getNames().contains(n)){
                        if(strict)
                            while(t.tgt.process.getNames().contains(i) || t.tgt.process.getSupport().contains(i) || pLeft.process.getSupport().contains(i) || pLeft.process.getNames().contains(i))
                                i--;
                        else
                            while(t.tgt.process.getNames().contains(i) || t.tgt.process.getSupport().contains(i) || pLeft.process.getSupport().contains(i) || pLeft.process.getNames().contains(i) || t.tgt.nameMap.get(i) != null)
                                i--;
                        t.tgt.process = t.tgt.process.rewrite(n, i);
                        t.tgt.nameMap.put(i, t.tgt.nameMap.get(n));
                        t.tgt.nameMap.remove(n);
                    }
                accRP.add(t);
            }
            boolean first = true;
            HashSet<Transition> accNew;
            HashSet<Transition> lOutK = new HashSet<>();
            HashSet<Transition> lInpK = new HashSet<>();
            HashSet<Transition> lOutF = new HashSet<>();
            HashSet<Transition> lInpF = new HashSet<>();
            HashSet<Transition> lpOutK = new HashSet<>();
            HashSet<Transition> lpInpK = new HashSet<>();
            HashSet<Transition> lpOutF = new HashSet<>();
            HashSet<Transition> lpInpF = new HashSet<>();
            HashSet<Transition> rOutK = new HashSet<>();
            HashSet<Transition> rInpK = new HashSet<>();
            HashSet<Transition> rOutF = new HashSet<>();
            HashSet<Transition> rInpF = new HashSet<>();
            HashSet<Transition> rpOutK = new HashSet<>();
            HashSet<Transition> rpInpK = new HashSet<>();
            HashSet<Transition> rpOutF = new HashSet<>();
            HashSet<Transition> rpInpF = new HashSet<>();
            extract(accL, lOutK, lInpK, lOutF, lInpF, new HashSet<>());
            extract(accLP, lpOutK, lpInpK, lpOutF, lpInpF, nextTrans);
            extract(accR, rOutK, rInpK, rOutF, rInpF, new HashSet<>());
            extract(accRP, rpOutK, rpInpK, rpOutF, rpInpF, nextTrans);
            for(int qwert = 0; qwert < 2; qwert ++){
                if(first){
                    accNew = accLP;
                }
                else{
                    accNew = accRP;
                }
                for(Transition e: accNew){
                    Transition elem = e.duplicate();
                    elem.src = this;
                    elem.src.rehash();
                    Process pNext = duplicate(new Par(par));

                    pNext.nameMap = elem.tgt.nameMap;
                    if(first) {
                        pNext.process.childProcess[0] = elem.tgt.process;
                    }
                    else {
                        pNext.process.childProcess[1] = elem.tgt.process;
                        // make a copy of child 1
                        // IF THERE IS A CLASH
                    }
//                    for(int key: nameMap.keySet())
//                        if(pNext.nameMap.containsKey(key))
//                            pNext.nameMap.put(key, nameMap.get(key));
                    elem.tgt = pNext;
                    elem.tgt.process.names = new HashSet<>();
                    elem.tgt.process.support = new HashSet<>();
                    elem.tgt.process.SetUpRP();
                    pNext.rehash();
                    if(!(elem.type.equals("TAU") || elem.type.equals("outK") || elem.type.equals("inpK"))) {
                        int n2 = pNext.findKey(elem.reg2);
                        pNext.nameMap.remove(n2);
                        int i = pNext.minFree();
                        if (n2 != 0) {
                            pNext.nameMap.put(n2, i);
                        }
                    }
                    if(strict){
                        Set<Integer> keys = new HashSet<>(pNext.nameMap.keySet());
                        for(int k: keys)
                            if(pNext.process.childProcess[0].getSupport().contains(k)||pNext.process.childProcess[1].getSupport().contains(k)) {
                            }
                            else
                                pNext.nameMap.remove(k);
                   }
                    pNext.rehash();
                    nextTrans.add(elem);
                }
                first = false;
            }
            close(nextTrans, rInpF, lOutF, true);
            close(nextTrans, lInpF, rOutF, false);
            comm(nextTrans, rpInpK, lOutK, true);
            comm(nextTrans, lpInpK, rOutK, false);
        }
        if(process instanceof Input inp){
            int n1 = inp.receiver;
            int n2 = inp.received;
            boolean n1free = inNext(n1, 0);
            int n1i = 0;
            try{
                n1i = nameMap.get(n1);
            } catch(Exception e){
                e.printStackTrace();
                System.exit(1);
            }
            for(int i : nameMap.values()){
                Process pNext = duplicate(process.childProcess[0]);
                pNext.substitute(i, n2);
                if(strict && !n1free){
                    pNext.removeFromMap(n1);
                }
                pNext.rehash();

                Transition t = new Transition(this, n1i, i, "inpK", pNext);
                nextTrans.add(t);
//                nextTrans.addAll(pNext.Step(strict, seen, memo));
            }
            Process pNext = duplicate(process.childProcess[0]);
            if(strict && !n1free)
                pNext.removeFromMap(n1);
            int i = pNext.minFree();
            pNext.substitute(i, n2);
            pNext.rehash();
            Transition t = new Transition(this, n1i, i, "inpF", pNext);
            nextTrans.add(t);

//            nextTrans.addAll(pNext.Step(strict, seen, memo));
        }
        if(process instanceof Output out){
            int n1 = out.receiver;
            int n2 = out.received;
            boolean n1free = inNext(n1, 0);
            boolean n2free = inNext(n2, 0);
            int n1i = nameMap.get(n1);
            int n2i = nameMap.get(n2);
            Process pNext = duplicate(process.childProcess[0]);
            if(strict && !(n1free && n2free)){
                if(!n1free)
                    pNext.nameMap.remove(n1);
                if((n1 != n2) && !n2free)
                    pNext.nameMap.remove(n2);
            }
            pNext.rehash();
            Transition t = new Transition(this, n1i, n2i, "outK", pNext);
            nextTrans.add(t);
//            nextTrans.addAll(pNext.Step(strict, seen, memo));
        }
        if(process instanceof Neq neq){
            int n1 = neq.n1;
            int n2 = neq.n2;
            if(nameMap.get(n1).equals(nameMap.get(n2))) return nextTrans;
            boolean n1free = inNext(n1, 0);
            boolean n2free = inNext(n2, 0);
            Process pNext = duplicate(process.childProcess[0]);
            if(strict && !(n1free && n2free)){
                if(!n1free)
                    pNext.nameMap.remove(n1);
                if((n1 != n2) && !n2free)
                    pNext.nameMap.remove(n2);
            }
            pNext.rehash();
            HashSet<Transition> acc = pNext.Step(strict, seen, memo, memoStrict);
            for(Transition t: acc) {
                t = t.duplicate();
                t.src = this;
                nextTrans.add(t);
            }
        }
        if(process instanceof Eq eq){
            int n1 = eq.n1;
            int n2 = eq.n2;
            if(!nameMap.get(n1).equals(nameMap.get(n2))) return nextTrans;
            boolean n1free = inNext(n1, 0);
            boolean n2free = inNext(n2, 0);
            Process pNext = duplicate(process.childProcess[0]);
            if(strict && !(n1free && n2free)){
                if(!n1free)
                    pNext.nameMap.remove(n1);
                if((n1 != n2) && !n2free)
                    pNext.nameMap.remove(n2);
            }
            pNext.rehash();
            HashSet<Transition> acc = pNext.Step(strict, seen, memo, memoStrict);
            for(Transition t: acc) {
                t = t.duplicate();
                t.src = this;
                nextTrans.add(t);
            }
        }
        if(process instanceof Nu nu){
            int n1 = nu.channel;
            Process pNext = duplicate(process.childProcess[0]);
            if(!pNext.process.getSupport().contains(n1)){
                pNext.rehash();
                nextTrans.addAll(pNext.Step(strict, seen, memo, memoStrict));
            }
            else{
                int i = pNext.minFree();
                pNext.nameMap.put(n1, i);
                pNext.rehash();
                boolean preSeen = seen.contains(pNext);
                HashSet<Transition> acc = pNext.Step(strict, seen, memo, memoStrict);
                if(!preSeen) seen.remove(pNext);
                for(Transition t: acc){
                    t = t.duplicate();
                    t.src = this;
                    boolean notTau = !t.type.equals("TAU");
                    if(notTau && t.reg1 == i) continue;
                    if(notTau && t.type.equals("inpK") && t.reg2 == i) continue;
                    if(notTau && t.type.equals("outK") && t.reg2 == i) nextTrans.add(new Transition(this, t.reg1, i, "outF", t.tgt));
                    else{
                        pNext = t.tgt.duplicate(t.tgt.process);
                        if(pNext.nameMap.containsKey(n1)){
                            int n1i = pNext.nameMap.get(n1);
                            Set<Integer> keys = new HashSet<>(pNext.nameMap.keySet());
                            for(int key: keys){
                                if(key == n1) continue;
                                if(pNext.nameMap.get(key) == n1i){
                                    pNext.process = pNext.process.rewrite(key, n1);
                                    pNext.nameMap.remove(key);
                                }
                            }
                            if(pNext.nameMap.containsKey(n1)){
                                pNext.nameMap.remove(n1);
                                if(notTau && (t.type.equals("inpF") || t.type.equals("outF"))){
                                    if(pNext.nameMap.containsValue(t.reg2)){
                                        int key = 0;
                                        for(int k: pNext.nameMap.keySet())
                                            if(pNext.nameMap.get(k) == t.reg2) {
                                                key = k;
                                                break;
                                            }
                                        pNext.nameMap.put(key, n1i);
//                                        pNext.removeFromMap(key);
                                    }
                                    t.reg2 = n1i;
                                }
                                if(!(pNext.process instanceof Terminal)){
                                    pNext.process = new Nu(nu.channel, pNext.process);
                                }
                            }
                        }
                        pNext.rehash();
                        t.tgt = pNext;
                        nextTrans.add(t);
                    }
                }
            }
        }
        if(process instanceof Sum sum){
            HashSet<Transition> acc = new HashSet<>();
            for(int i = 0; i<2; i++){
                Process pNext = duplicate(sum.childProcess[i]);
                pNext.rehash();
                boolean preSeen = seen.contains(pNext);
                acc.addAll(pNext.Step(strict, seen, memo, memoStrict));
                if(!preSeen) seen.remove(pNext);
            }
            for(Transition t: acc) {
                t = t.duplicate();
                t.src = this;
                nextTrans.add(t);
            }
        }
        if(process instanceof  Defined def){
            HashMap<Integer, Integer> mp = new HashMap<>(nameMap);
            if(strict) {
                Set<Integer> argSet = new HashSet<>();
                for(int x: def.args)
                    argSet.add(x);
                for (int key : nameMap.keySet())
                    if (!argSet.contains(key)) mp.remove(key);
            }
            Map<Integer, Integer> copyMap = new HashMap<>(mp);
            RawProcess rp = defined.get(def.name).childProcess[0];
            int i = -1;
            for(int x: defined.get(def.name).names) {
                if (mp.containsKey(x)) {
                    while (mp.containsKey(i) || rp.names.contains(i) || rp.support.contains(i) || defined.get(def.name).getNames().contains(i) || defined.get(def.name).getSupport().contains(i) || otherNames.contains(i))
//                    while(mp.containsKey(i) || rp.names.contains(i) || defined.get(def.name).getNames().contains(i)|| defined.get(def.name).getSupport().contains(i))
                        i--;
                    rp = rp.rewrite(x, i);
                }
            }
            Map<Integer, Integer> rwmap = new HashMap<>();
            for(i = 0; i<def.args.length; i++){
//            for(i = def.args.length - 1; i>=0; i--){
                if(defined.get(def.name).args[i] != def.args[i]) {
                    rwmap.put(defined.get(def.name).args[i], def.args[i]);
//                    rp = rp.rewrite(defined.get(def.name).args[i], def.args[i]);

                }
                mp.put(def.args[i], copyMap.get(def.args[i]));
//                mp.put(defined.get(def.name).args[i], nameMap.get(def.args[i]));
            }
            if(rwmap.size()!=0)
                rp = rp.ReFix(rwmap);
            Process pNext = duplicate(rp);
            pNext.nameMap = mp;
            pNext.rehash();
            boolean removeFromSeen = !seen.contains(pNext);
            Set<Transition> tmp = pNext.Step(strict, seen, memo, memoStrict);
            for(Transition t: tmp){
                t = t.duplicate();
                t.src = this;
                nextTrans.add(t);
            }
            if(removeFromSeen)
                seen.remove(pNext);
        }
        if(strict){
            memoStrict.put(uid, nextTrans);
        }
        else
            memo.put(this, nextTrans);
        return nextTrans;
    }

    private void extract(HashSet<Transition> accL, HashSet<Transition> lOutK, HashSet<Transition> lInpK, HashSet<Transition> lOutF, HashSet<Transition> lInpF, HashSet<Transition> next) {
        for(Transition t: accL)
            switch (t.type) {
                case "inpK" -> lInpK.add(t);
                case "outK" -> lOutK.add(t);
                case "inpF" -> lInpF.add(t);
                case "outF" -> lOutF.add(t);
                default -> {
                    //                    next.add(t);
                }
            }
    }


    private void close(HashSet<Transition> acc, HashSet<Transition> lInpF, HashSet<Transition> rOutF, boolean bool) {
        for(Transition t1i: rOutF)
            for(Transition t2i: lInpF)
                if(t1i.reg1 == t2i.reg1 && t1i.reg2 == t2i.reg2){
                    Transition t1 = t1i.duplicate();
                    Transition t2 = t2i.duplicate();
                    int n1 = 0;
                    for(int key: t1.tgt.nameMap.keySet())
                            if (t1.tgt.nameMap.get(key) == t2.reg2) {
                                n1 = key;
                                break;
                            }
                    int n2 = 0;
                    for(int key: t2.tgt.nameMap.keySet())
                        if (t2.tgt.nameMap.get(key) == t2.reg2) {
                            n2 = key;
                            break;
                        }
                    Par pr;
                    if(bool)
                        pr = new Par(t1.tgt.process, t2.tgt.process.rewrite(n2, n1));
                    else
                        pr = new Par(t2.tgt.process.rewrite(n2, n1), t1.tgt.process);
                    Process pNext;
//                    if(t1.tgt.process.getSupport().contains(n1) || t2.tgt.process.getSupport().contains(n1) ){
                    if(pr.childProcess[0].getSupport().contains(n1) || pr.childProcess[1].getSupport().contains(n1) ){
                        pNext = duplicate(new Nu(n1, pr));
                    }
                    else{
                        pNext = duplicate(pr);
                    }
                    pNext.nameMap.remove(n1);
                    pNext.rehash();
                    Transition t = new Transition(this, -1, -1, "TAU", pNext);
                    acc.add(t);
                }
    }

    private void comm(HashSet<Transition> acc, HashSet<Transition> lInpK, HashSet<Transition> rOutK, boolean bool) {
        for(Transition t1: rOutK)
            for(Transition t2: lInpK)
                if(t1.reg1 == t2.reg1 && t1.reg2 == t2.reg2){
                    Process pNext;
                    if(bool)
                        pNext = duplicate(new Par(t1.tgt.process, t2.tgt.process));
                    else
                        pNext = duplicate(new Par(t2.tgt.process, t1.tgt.process));
                    pNext.nameMap = t2.tgt.nameMap;
                    pNext.rehash();
                    Transition t = new Transition(this, -1, -1, "TAU", pNext);
                    // inpK, outK, inpF, outF, TAU
                    acc.add(t);
                }
    }

    public void rehash() {
//        System.out.println("Proc > " + process.toString() + " => " + nameMap);
        uid = process.strBuilder(nameMap);
//        System.out.println("UID > " + uid);
//        uid = process.toString();
//        fix(nameMap);
        iset = new HashSet<>();
        for(int key: nameMap.keySet())
            if(!process.support.contains(key))
                iset.add(nameMap.get(key));
//        hash = this.toString().hashCode();
//        hash = Objects.hash(uid);
        hash = Objects.hash(uid, iset);
    }

    private void fix(Map<Integer, Integer> map) {
        try{
            for(Map.Entry<Integer, Integer> entry: nameMap.entrySet()){
                uid = uid.replace("'" + entry.getKey() + "'", entry.getValue().toString());
            }
        } catch(Exception e){
            System.out.println("FIX ERROR");
            System.out.println(this + " => " + map);
            e.printStackTrace();
            System.exit(1);
        }
    }

    private void removeFromMap(int n1) {
        nameMap.remove(n1);
    }

    private void substitute(int i, int n2) {
        if(nameMap.containsKey(n2)){
            System.out.println("SUBSTITUTION ERROR");
            try{
                throw new Exception();
            } catch (Exception e) {
                System.out.println(i + " => " + n2 + " => " + nameMap);
                System.out.println("\t => " + this);
                e.printStackTrace();
            }
            System.exit(-11);
        }
        if(process.support.contains(n2))
            nameMap.put(n2, i);
    }

    private int minFree() {
        int x = 1;
        while(nameMap.containsValue(x)) x++;
        return x;
    }

    private int minAlpha() {
        int x = -1;
        while(nameMap.containsValue(x)) x--;
        return x;
    }

    public boolean inNext(int val, int index){
        return process.childProcess[index].support.contains(val);
    }

    public String toString(){
//        return "" + nameMap + " |- " + process;
        return uid;
    }

    @Override
    public boolean equals(Object o) {
        if (o == this) return true;
        if(o instanceof Process p){
            return this.uid.equals(p.uid) && this.nameMap.equals(p.nameMap);
        }
        return false;
    }

    @Override
    public int hashCode(){
        return hash;
    }

    public static boolean containsArg(int[] args, int key){
        for(int x: args)
            if(x == key) return true;
        return false;
    }

}


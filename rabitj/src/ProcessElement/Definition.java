package ProcessElement;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Definition extends RawProcess {

    public String name;
    public int[] args;
    public Map<String, Integer> namemap;

    public Definition(String name, String[] args, Map<String, Integer> nmap){
        super();
        this.name = name;
        this.args = new int[args.length];
        children = 1;
        int i = -1;
        for(String n: args){
            nmap.put(n,i);
            this.args[(i * -1) -1] = i;
            i --;
        }
        for(int k : this.args)
            support.add(k);
        namemap = nmap;
    }

    @Override
    public Set<Integer> getNames(){ return new HashSet<Integer>(); }

    @Override
    public String toString() {
        String[] arg = new String[args.length];
        for(int i = 0; i<args.length; i++)
            arg[i] = "'" + args[i] + "'";
        return name + Arrays.toString(arg) + " = " + childProcess[0] + " |- " + names;
    }

    public RawProcess ReFix(Map<Integer, Integer> nameMap, Map<Integer, Integer> newMap){
        return this.childProcess[0].ReFix(nameMap);
    }
}

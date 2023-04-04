package ProcessElement;

import java.util.Arrays;
import java.util.Map;
import java.util.Set;

public class Defined extends RawProcess {
    public String name;
    public int[] args;

    public Defined(String name, String[] args, Map<String, Integer> nmap){
        super();
        children = 0;
        this.name = name;
        this.args = new int[args.length];
        for(int i = 0; i<args.length; i++)
            this.args[i] = nmap.get(args[i]);
        for(int i : this.args){
            support.add(i);
        }
        childProcess = new RawProcess[0];
    }

    public Defined(String name, int[] args){
        super();
        this.name = name;
        this.args = args;
        for(int i : this.args)
            support.add(i);
    }

    @Override
    public Set<Integer> getNames(){return names;}

//    @Override
//    public Set<Integer> getSupport(){return Process.defined.get(name).support;}

    public String strBuilder(Map<Integer, Integer> nameMap) {
        String[] arg = new String[args.length];
        for(int i = 0; i<args.length; i++)
            arg[i] = nameMap.get(args[i]) == null ? "'" + args[i] + "'" : nameMap.get(args[i]).toString();
        return name + Arrays.toString(arg);
    }

    @Override
    protected void setUpStrForm() {
        String[] arg = new String[args.length];
        for(int i = 0; i<args.length; i++)
            arg[i] = "'" + args[i] + "'";
        strForm = name + Arrays.toString(arg);
    }

    public RawProcess rewrite(int key, int n1){
        for(int i = 0; i < args.length; i++)
            if(args[i] == key){
                int[] newArgs = args.clone();
                newArgs[i] = n1;
                return new Defined(name, newArgs);
            }
        return this;
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        int[] newArgs = args.clone();
        for(int i = 0; i < newArgs.length; i++){
            if(nameMap.containsKey(args[i])){
                newArgs[i] = nameMap.get(args[i]);
            }
        }
        return new Defined(name, newArgs);
    }

}

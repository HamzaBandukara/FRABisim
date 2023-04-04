package ProcessElement;

import java.util.Map;

public class Neq extends RawProcess {
    public int n1;
    public int n2;

    public Neq(String n1, String n2, Map<String, Integer> nmap){
        super();
        children = 1;
        this.n1 = nmap.get(n1);
        this.n2 = nmap.get(n2);
        support.add(this.n1);support.add(this.n2);
    }

    public Neq(int n1, int n2, RawProcess child){
        super();
        children = 1;
        this.n1 = n1;
        this.n2 = n2;
        support.add(this.n1);support.add(this.n2);
        childProcess = new RawProcess[1];
        childProcess[0] = child;
        SetUpRP();
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        String first = nameMap.get(n1) == null ? "'" + n1 + "'" : nameMap.get(n1).toString();
        String second = nameMap.get(n2) == null ? "'" + n2 + "'" : nameMap.get(n2).toString();
        return "[" + first + "#" + second + "]" + childProcess[0].strBuilder(nameMap);
    }

    protected void setUpStrForm(){
        strForm = "['" + n1 + "'#'" + n2 + "']" + childProcess[0];
    }

    public RawProcess rewrite(int key, int new1) {
        int first = n1;
        int second = n2;
        if(n1 == key)
            first = new1;
        if(n2 == key)
            second = new1;
        return new Neq(first, second, childProcess[0].rewrite(key, new1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        int first = n1;
        int second = n2;
        if(nameMap.containsKey(first))
            first = nameMap.get(first);
        if(nameMap.containsKey(second))
            second = nameMap.get(second);
        return new Neq(first, second, childProcess[0].ReFix(nameMap));
    }
}

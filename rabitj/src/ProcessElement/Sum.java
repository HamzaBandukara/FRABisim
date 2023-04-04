package ProcessElement;

import java.util.Map;

public class Sum extends RawProcess {

    public Map<String, Integer> nmap;

    public Sum(){
        super();
        children = 2;
    }

    @Override
    protected void setUpStrForm() {
        strForm = "(" + childProcess[0] + "+" + childProcess[1] + ")";
    }

    public Sum(RawProcess p1, RawProcess p2){
        children = 2;
        childProcess = new RawProcess[2];
        childProcess[0] = p1;
        childProcess[1] = p2;
        SetUpRP();
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        return "(" + childProcess[0].strBuilder(nameMap) + "+" + childProcess[1].strBuilder(nameMap) + ")";
    }

    @Override
    public RawProcess rewrite(int key, int n1){
        return new Sum(childProcess[0].rewrite(key, n1), childProcess[1].rewrite(key, n1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        return new Sum(childProcess[0].ReFix(nameMap), childProcess[1].ReFix(nameMap));
    }
}

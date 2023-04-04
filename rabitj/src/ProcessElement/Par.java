package ProcessElement;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Par extends RawProcess {

    public Par(){
        super();
        children = 2;
        support = new HashSet<>();
    }

    public Par(Par p){
        super();
        children = 2;
        childProcess = new RawProcess[2];
        childProcess[0] = p.childProcess[0];
        childProcess[1] = p.childProcess[1];
        SetUpRP();
    }

    public Par(RawProcess p1, RawProcess p2){
        super();
        children = 2;
        childProcess = new RawProcess[2];
        childProcess[0] = p1;
        childProcess[1] = p2;
        SetUpRP();
    }

    @Override
    protected void setUpStrForm() {
        strForm = "(" + childProcess[0] + "|" + childProcess[1] + ")";
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        return "(" + childProcess[0].strBuilder(nameMap) + "|" + childProcess[1].strBuilder(nameMap) + ")";
    }

    @Override
    public RawProcess rewrite(int key, int n1){
        return new Par(childProcess[0].rewrite(key, n1), childProcess[1].rewrite(key, n1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        return new Par(childProcess[0].ReFix(nameMap), childProcess[1].ReFix(nameMap));
    }
}

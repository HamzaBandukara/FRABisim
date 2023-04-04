package ProcessElement;

import java.util.Map;

public class Tau extends RawProcess {

    public Tau(){
        super();
        children = 1;
    }

    public Tau(RawProcess child){
        super();
        children = 1;
        childProcess = new RawProcess[1];
        childProcess[0] = child;
        SetUpRP();
    }

    @Override
    public void SetUpRP(){
        support.addAll(childProcess[0].support);
        names.addAll(childProcess[0].names);
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        return "_t." + childProcess[0].strBuilder(nameMap);
    }

    protected void setUpStrForm(){
        strForm = "_t." + childProcess[0];
    }

    @Override
    public RawProcess rewrite(int key, int n1){
        return new Tau(childProcess[0].rewrite(key, n1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        return new Tau(childProcess[0].ReFix(nameMap));
    }
}


package ProcessElement;

import java.util.Map;

public class Terminal extends RawProcess {

    public Terminal(Map<String, Integer> nmap){
        super();
        children = 0;
        childProcess = new RawProcess[0];
        strForm = "0";
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        return "0";
    }

//    @Override
//    public String toString(){
//        return "0";
//    }

    @Override
    public RawProcess rewrite(int key, int n1){
        return this;
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap){ return this; }
}


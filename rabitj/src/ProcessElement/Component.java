package ProcessElement;

import java.util.HashSet;

public class Component extends RawProcess {
    public Component(){
        children = 1;
        support = new HashSet<>();
    }

    @Override
    public String toString(){ return "(" + childProcess[0] + ")"; }
}

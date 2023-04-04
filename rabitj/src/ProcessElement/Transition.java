package ProcessElement;

public class Transition {
    public Process src;
    public int reg1;
    public int reg2;
    public String type;
    public Process tgt;

    public Transition(Process p1, int r1, int r2, String t, Process p2){
        src = p1;
        reg1 = r1;
        reg2 = r2;
        type = t;
        tgt = p2;
    }

    public Transition duplicate(){
        return new Transition(
                src.duplicate(src.process),
                reg1,
                reg2,
                type,
                tgt.duplicate(tgt.process)
        );
    }

    public String toString(){
        if(type.equals("TAU")){
            return src + " - (TAU) -> " + tgt;
        }
        return src +
                " - (" +
                reg1 +
                " " +
                reg2 +
                type +
                ") -> " +
                tgt;
    }

    @Override
    public boolean equals(Object o){
        if(o instanceof Transition)
            return o.toString().equals(this.toString());
        return false;
    }


    @Override
    public int hashCode(){
        return toString().hashCode();
    }
}

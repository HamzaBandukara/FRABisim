package DataStructures;

public class GlobalCounter {

    private int value;

    public GlobalCounter(){
        value = 0;
    }

    public int getValue(){
        return value;
    }

    public void increment(){
        value ++;
    }
}

package ProcessElement;

import java.util.HashSet;
import java.util.Map;

public class Input extends RawProcess {

    public int receiver;
    public int received;

    public Input(String n1, String n2, Map<String, Integer> nmap){
        super();
        children = 1;
        if(nmap.containsKey(n1))
            receiver = nmap.get(n1);
        else{
            receiver = -1;
            while(nmap.containsValue(receiver))
                receiver --;
            nmap.put(n1, receiver);
        }
        received = -1;
        while(nmap.containsValue(received))
            received --;
        nmap.put(n2, received);
    }

    @Override
    public void SetUpRP(){
        support = new HashSet<>();
        support.add(receiver);
        support.addAll(childProcess[0].support);
        support.remove(received);
        names = new HashSet<>();
        names.add(received);
        names.addAll(childProcess[0].names);
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        String first = nameMap.get(receiver) == null ? "'" + receiver + "'" : nameMap.get(receiver).toString();
        String second = nameMap.get(received) == null ? "'" + received + "'" : nameMap.get(received).toString();
        return first + "(" + second + ")." + this.childProcess[0].strBuilder(nameMap);
    }

    @Override
    protected void setUpStrForm() {
        strForm = "'" + this.receiver + "'('" + this.received + "')." + this.childProcess[0];
    }

    public Input(int n1, int n2, RawProcess child){
        children = 1;
        receiver = n1;
        received = n2;
        childProcess = new RawProcess[1];
        childProcess[0] = child;
        SetUpRP();
    }

    public RawProcess rewrite(int key, int new1) {
            int first = receiver;
            int second = received;
            if(receiver == key)
                first = new1;
            if(received == key)
                second = new1;
            return new Input(first, second, childProcess[0].rewrite(key, new1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        int i = -1;
        int first = receiver;
        int second = received;
        if(nameMap.containsKey(first))
            first = nameMap.get(first);
        if(nameMap.containsKey(second))
            second = nameMap.get(second);
        return new Input(first, second, childProcess[0].ReFix(nameMap));
    }
}

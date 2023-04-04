package ProcessElement;

import java.util.Map;

public class Nu extends RawProcess {

    public int channel;

    public Nu(String n1, Map<String, Integer> nmap){
        super();
        children = 1;
        channel = -1;
        while(nmap.containsValue(channel))
            channel --;
        nmap.put(n1, channel);
        names.add(channel);
    }

    public Nu(int n1, RawProcess child){
        super();
        children = 1;
        channel = n1;
        childProcess = new RawProcess[1];
        childProcess[0] = child;
        names.add(n1);
        SetUpRP();
        support.remove(n1);
    }

    public String strBuilder(Map<Integer, Integer> nameMap) {
        String first = nameMap.get(channel) == null ? "'" + channel + "'" : nameMap.get(channel).toString();
        return "$" + first + ".(" + childProcess[0].strBuilder(nameMap) + ")";
    }

    @Override
    public void SetUpRP(){
        support.addAll(childProcess[0].support);
        names.addAll(childProcess[0].names);
        support.remove(channel);
        names.add(channel);
    }

    protected void setUpStrForm(){
        strForm = "$'" + channel + "'.(" + childProcess[0] + ")";
    }

    @Override
    public RawProcess rewrite(int key, int n1){
        int first = channel;
        if(channel == key){
            first = n1;
        }
        return new Nu(first, childProcess[0].rewrite(key, n1));
    }

    @Override
    public RawProcess ReFix(Map<Integer, Integer> nameMap) {
        int first = channel;
        if(nameMap.containsKey(first))
            first = nameMap.get(first);
        return new Nu(first, childProcess[0].ReFix(nameMap));
    }
}


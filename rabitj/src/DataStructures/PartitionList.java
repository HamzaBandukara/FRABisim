package DataStructures;

import java.util.HashMap;

public class PartitionList {

    public Partition value;
    public PartitionList next;
    private final HashMap<String, Partition> memo;

    public PartitionList(Partition value, PartitionList next) {
        this.value = value;
        this.next = next;
        memo = new HashMap<>();
    }

    public Partition getPartition(String state) {
        Partition res = memo.get(state);
        if(res ==  null){
            PartitionList ptr = this;
            while (!ptr.value.rays.containsKey(state)){
                res = ptr.memo.get(state);
                if(res != null){
                    memo.put(state, res);
                    return res;
                }
                ptr = ptr.next;
            }
            res = ptr.value;
            memo.put(state, res);
        }
        return res;
    }
}

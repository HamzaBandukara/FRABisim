package DataStructures;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class HardMap<A,B>{

    public Map<A, B> map;
    public int hash;

    public HardMap(Map<A, B> map){
        this.map = map;
        hash = 0;
        for(Map.Entry<A, B> entry: map.entrySet()){
            int multiplier = 1000003;
            int x = 345678;
            int y = entry.getKey().hashCode();
            x = (x ^ y) * multiplier;
            multiplier = multiplier + (82524);
            x = x + 97531;
            y = entry.getValue().hashCode();
            x = (x ^ y) * multiplier + (82522);
            x = x + 97531;
            hash = hash + x;
        }
    }
    // HashMap memo;
    // Number of hashes = 218
    // Number of keys = 288000

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        HardMap<?, ?> hardMap = (HardMap<?, ?>) o;
        return Objects.equals(map, hardMap.map);
    }

    @Override
    public int hashCode() {
        return hash;
    }
}

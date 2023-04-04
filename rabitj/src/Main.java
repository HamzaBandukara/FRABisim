import DataStructures.RA;
import ParserRA.RAParser;
import org.javatuples.Triplet;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Main {

    public static void main(String[] args) throws Exception {
        if(args[0].equals("-pi"))
//            piOTF(args[1]);
            piCalculusBisim(args[1], false);
        else if(args[0].equals("-piw"))
            piCalculusBisim(args[1], true);
        else if(args[0].equals("-g") || args[0].equals("-b")){
            boolean isGen = args[0].equals("-g");
            ThreadMXBean bean = ManagementFactory.getThreadMXBean();
            RA ra = new RA();
            Map<String, String> m1 = RAParser.parseXML(args[1], "q", ra);
            Map<String, String> m2 = RAParser.parseXML(args[2], "p", ra);
            ra.completeSetup();
            Triplet<String, HashMap<Integer, Integer>, String> triple = getTriple(args[3]);
//            long startTime = System.nanoTime();
            boolean result;
            long time = bean.getCurrentThreadCpuTime();
            if(isGen)
                result = FwdGen.forward(ra, m1.get(triple.getValue0()), triple.getValue1(), m2.get(triple.getValue2()));
            else
                result = Fwd.forward(ra, m1.get(triple.getValue0()), triple.getValue1(), m2.get(triple.getValue2()));
            time = bean.getCurrentThreadCpuTime() - time;
            float timetaken = ((float) time) / 1000000;
            System.out.println(result + " " + timetaken);
//            System.out.println(result + " " + ((float)(System.nanoTime() - startTime))/1000000);
        }
    }

    private static Triplet<String, HashMap<Integer, Integer>, String> getTriple(String arg) {
        HashMap<Integer, Integer> map = new HashMap<>();
        String removedBraces = arg.substring(1, arg.length()-1);
        String[] split1 = removedBraces.split("[{]");
        String[] split2 = split1[1].split("[}]");
        String first = split1[0];
        first = first.replace(",", "");
        String second = split2[1];
        second = second.replace(",", "");
        String x = split2[0];
        Matcher m = Pattern.compile("\\((.*?)\\)").matcher(x);
        while(m.find()){
            String current = m.group(1);
            String[] split = current.split(",");
            map.put(Integer.parseInt(split[0]), Integer.parseInt(split[1]));
        }
        return new Triplet<>(first, map, second);
    }

    public static void piOTF(String filename) throws Exception{
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        boolean result;
        RA ra = new RA();
        long time = bean.getCurrentThreadCpuTime();
        ra.PiOTF(filename, "q");
    }

    public static void piCalculusBisim(String filename, boolean weak) throws Exception {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        boolean result;
        RA ra = new RA();
        long time = bean.getCurrentThreadCpuTime();
        if(weak)
            ra.PiProcessWeak(filename, "q");
        else
            ra.PiProcess(filename, "q");
        List<String> q = new ArrayList<>(ra.getTargets("q0out0", "out2", "K", 0));
        if(q.size() == 1) result = true;
        else{
            Map<Integer, Integer> map = new HashMap<>();
            for(int x: ra.s_map.get(q.get(0)))
                if(ra.s_map.get(q.get(1)).contains(x))
                    map.put(x, x);
            result = FwdGen.forward(ra, q.get(0), map, q.get(1));
        }
        time = bean.getCurrentThreadCpuTime() - time;
        float timetaken = ((float) time) / 1000000;
        System.out.println(result + " " + timetaken);
    }
}

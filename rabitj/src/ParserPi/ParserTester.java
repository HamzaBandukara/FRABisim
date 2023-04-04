package ParserPi;

import ProcessElement.Definition;
import ProcessElement.RawProcess;
import org.antlr.v4.runtime.misc.Pair;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.util.Map;

public class ParserTester {
    public static void main(String[] args) throws Exception{
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long time = bean.getCurrentThreadCpuTime();
        Pair<RawProcess, Map<String, Definition>> result = Antlr.run("./src/ParserPi/test.pi");
        float endtime = ((float) bean.getCurrentThreadCpuTime() - time) / 1000000;
        System.out.println("TEST TIME: " + endtime);
    }

}

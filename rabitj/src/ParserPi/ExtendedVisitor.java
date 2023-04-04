package ParserPi;

import ProcessElement.*;
import org.antlr.v4.runtime.misc.Pair;

import java.util.*;

public class ExtendedVisitor extends PiBaseVisitor {

        public Map<String, Integer> nmap;
        public Map<String, Definition> defined;
        public ArrayList<RawProcess> sequence;
        public int counter;
        private final boolean debug;

        private void dbprint(Object ... objects){
                if(debug)
                        System.out.println("DB: " + Arrays.toString(objects));
        }

        public ExtendedVisitor(){
                super();
                nmap = new HashMap<>();
                defined = new HashMap<>();
                sequence = new ArrayList<>();
                counter = -1;
                debug = false;
        }

        @Override
        public RawProcess visitRoot(PiParser.RootContext ctx){
                RawProcess root1 = null;
                RawProcess root2 = null;
                for(int i = 0; i < ctx.getChildCount(); i++){
                        if(ctx.getChild(i) instanceof PiParser.LineContext) {
                                this.visitLine((PiParser.LineContext) ctx.getChild(i));
                        }
                        else if(Objects.equals(ctx.getChild(i).getText(), "TEST")){
                                nmap = new HashMap<>();
//                                Map<String, Integer> namemap = new HashMap<>();
                                i = i + 1;
                                String text = ctx.getChild(i).getText().substring(0, ctx.getChild(i).getText().length()-1);
                                String[] text2 = text.split("[(]");
                                if(text2.length == 2)
                                        for(String x: text2[1].split(","))
                                                if(!nmap.containsKey(x))
                                                        nmap.put(x, (nmap.size() + 1) * -1);
                                root1 = visitAprocess((PiParser.AprocessContext) ctx.getChild(i));
                                i = i + 2;
                                String text3 = ctx.getChild(i).getText().substring(0, ctx.getChild(i).getText().length()-1);
                                String[] text4 = text3.split("[(]");
                                if(text4.length==2)
                                        for(String x: text4[1].split(","))
                                                if(!nmap.containsKey(x))
                                                        nmap.put(x, (nmap.size() + 1) * -1);
                                root2 = visitAprocess((PiParser.AprocessContext) ctx.getChild(i));
                                root1 = new Output(0, 0, root1);
                                root2 = new Output(0, 0, root2);
                                return new Sum(root1, root2);
                        }
                }
                return null;
        }

        @Override
        public RawProcess visitLine(PiParser.LineContext ctx){
                return visitDefinition((PiParser.DefinitionContext) ctx.getChild(0));
        }

        @Override
        public RawProcess visitDefinition(PiParser.DefinitionContext ctx){
                this.nmap = new HashMap<>();
                Definition nextProcess;
                String[] parts = ctx.getText().split("=");
                String p1 = parts[0].substring(0, parts[0].length() - 1);
                parts = p1.split("[(]");
                String[] args;
                if(parts.length == 2)
                        args = parts[1].split(",");
                else
                        args = new String[0];
                nextProcess = new Definition(parts[0], args, nmap);
                defined.put(parts[0], nextProcess);
                try{
                        RawProcess p = visitAprocess((PiParser.AprocessContext) ctx.getChild(ctx.getChildCount() - 1));
                        nextProcess.setChildren(new RawProcess[]{p});
                        counter = -1;
                } catch(Exception e){
                        e.printStackTrace();
                        System.exit(-5);
                }
                nextProcess.SetUpRP();
                return nextProcess;
        }

        @Override
        public RawProcess visitAprocess(PiParser.AprocessContext ctx){
                RawProcess t = visitBprocess((PiParser.BprocessContext) ctx.getChild(0));
                for(int i = 2; i < ctx.getChildCount(); i = i + 2){
                        t = new Sum(t, visitBprocess((PiParser.BprocessContext) ctx.getChild(i)));
                        t.SetUpRP();
                }
                return t;
        }

        @Override
        public RawProcess visitBprocess(PiParser.BprocessContext ctx){
                RawProcess t = visitProcess((PiParser.ProcessContext) ctx.getChild(0));
                for(int i = 2; i < ctx.getChildCount(); i = i + 2){
                        t = new Par(t, visitProcess((PiParser.ProcessContext) ctx.getChild(i)));
                }
                return t;
        }


        @Override
        public RawProcess visitProcess(PiParser.ProcessContext ctx) {
                dbprint("VISITING:", ctx.getText());
                RawProcess t;
                boolean hasChild = true;
                if (ctx.getChild(0).getText().equals("(")) {
                        t = visitAprocess((PiParser.AprocessContext) ctx.getChild(1));
                        hasChild = false;
                }
                else if (ctx.getChild(0).getText().equals("[")) {
                        if (ctx.getChild(2).getText().equals("="))
                                t = new Eq(ctx.getChild(1).getText(), ctx.getChild(3).getText(), nmap);
                        else
                                t = new Neq(ctx.getChild(1).getText(), ctx.getChild(3).getText(), nmap);

                } else if (ctx.getChild(0).getText().equals("$"))
                        t = new Nu(ctx.getChild(1).getText(), nmap);
                else if (ctx.getChild(0).getText().equals("_t"))
                        t = new Tau();
                else if (ctx.PROCESSNAME() != null) {
                        dbprint("CASE DEF");
                        String proc = ctx.getText().substring(0, ctx.getText().length() - 1);
                        String[] parts = proc.split("[(]");
                        String[] args;
                        if (parts.length == 2)
                                args = parts[1].split(",");
                        else
                                args = new String[0];
                        t = new Defined(parts[0], args, nmap);
                        dbprint("RESULT", ctx.getText()," => ", t);
                        return t;
                }
                else if (ctx.getChildCount() == 1){
                        t = new Terminal(nmap);
                        hasChild = false;
                }
                else {
                        if (ctx.getChild(1).getText().equals("<"))
                                t = new Output(ctx.getChild(0).getText(), ctx.getChild(2).getText(), nmap);
                        else
                                t = new Input(ctx.getChild(0).getText(), ctx.getChild(2).getText(), nmap);
                }
                if (hasChild) {
                        try {
                                t.setChildren(new RawProcess[]{visitProcess((PiParser.ProcessContext) ctx.getChild(ctx.getChildCount() - 1))});
                        } catch (Exception e) {
                                System.out.println("Error Setting Children for: " + t);
                                System.exit(8);
                        }
                }
                t.SetUpRP();
                dbprint("RESULT", ctx.getText()," => ", t);
                return t;
        }


        @Override
        public Pair<RawProcess, String> visitProcessmid(PiParser.ProcessmidContext ctx){
                dbprint("VISITING MID:", ctx.getText());
                RawProcess t = visitProcess(ctx.process());
//                if(ctx.processmid().getChildCount() != 0){
//                        Pair<RawProcess, String> res = visitProcessmid(ctx.processmid());
//                        if(res.b.equals("PAR"))
//                                t = new Par(t, res.a);
//                        else
//                                t = new Sum(t, res.a);
//                        t.SetUpRP();
//                }
                dbprint("Result: ", ctx.getText(), "=>", t);
                if(ctx.PAR() != null)
                        return new Pair<>(t, "PAR");
                return new Pair<>(t, "SUM");
        }
}

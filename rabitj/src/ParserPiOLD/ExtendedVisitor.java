package ParserPiOLD;

import ProcessElement.*;

import java.util.*;

public class ExtendedVisitor extends PiBaseVisitor{

        public Map<String, Integer> nmap;
        public Map<String, Definition> defined;
        public ArrayList<RawProcess> sequence;
        public int counter;

        public ExtendedVisitor(){
                super();
                nmap = new HashMap<>();
                defined = new HashMap<>();
                sequence = new ArrayList<>();
                counter = -1;
        }

        @Override
        public RawProcess visitRoot(PiParser.RootContext ctx){
                RawProcess root1 = null;
                RawProcess root2 = null;
                for(int i = 0; i < ctx.getChildCount(); i++){
                        if(ctx.getChild(i) instanceof PiParser.LineContext) {
//                                if(root == null)
//                                        root = this.visitLine((PiParser.LineContext) ctx.getChild(i));
//                                else
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
                                root1 = visitProcess((PiParser.ProcessContext) ctx.getChild(i));
                                i = i + 2;
                                String text3 = ctx.getChild(i).getText().substring(0, ctx.getChild(i).getText().length()-1);
                                String[] text4 = text3.split("[(]");
                                if(text4.length==2)
                                        for(String x: text4[1].split(","))
                                                if(!nmap.containsKey(x))
                                                        nmap.put(x, (nmap.size() + 1) * -1);
                                root2 = visitProcess((PiParser.ProcessContext) ctx.getChild(i));
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
                        RawProcess p = visitProcess((PiParser.ProcessContext) ctx.getChild(ctx.getChildCount() - 1));
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
        public RawProcess visitProcess(PiParser.ProcessContext ctx){
                RawProcess t;
                if(ctx.PAR()!= null || ctx.SUM() != null){
                        if(ctx.PAR() != null)
                                t = new Par();
                        else
                                t = new Sum();
//                        Map<String, Integer> copy = new HashMap<>(nmap);
                        RawProcess p1 = visitProc((PiParser.ProcContext) ctx.getChild(0));
//                        nmap = copy;
                        RawProcess p2 =visitProc((PiParser.ProcContext) ctx.getChild(2));
                        try{
                                t.setChildren(new RawProcess[]{p1, p2});
                        } catch(Exception e){
                                System.exit(-9);
                        }
                }
                else if(ctx.getChildCount() == 1){;
                        t = visitProc((PiParser.ProcContext) ctx.getChild(0));
                }
                else{
                        t = visitProcess((PiParser.ProcessContext) ctx.getChild(1));
                }
                t.SetUpRP();
                return t;
        }

        @Override
        public RawProcess visitProc(PiParser.ProcContext ctx){
                RawProcess nextProcess = null;
                PiParser.ProcessContext next = null;
                if(ctx.getChild(0).getText().equals("(")){
                        return visitProcess((PiParser.ProcessContext) ctx.getChild(1));
                }
                if(ctx.zero() != null){
                        nextProcess = new Terminal(this.nmap);
                        return nextProcess;
                }
                else if(ctx.read() != null){
                        String n1 = ctx.read().getChild(0).getText();
                        String n2 = ctx.read().getChild(2).getText();
                        nextProcess = new Input(n1, n2, nmap);
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(4);

                }
                else if(ctx.write() != null) {
                        String n1 = ctx.write().getChild(0).getText();
                        String n2 = ctx.write().getChild(2).getText();
                        nextProcess = new Output(n1, n2, nmap);
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(4);
                }
                else if(ctx.tau() != null){
                        nextProcess = new Tau();
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(1);
                }
                else if(ctx.nu() != null){
                        String n1 = ctx.nu().getChild(1).getText();
                        nextProcess = new Nu(n1, nmap);
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(3);
                }
                else if(ctx.eq() != null){
                        String n1 = ctx.eq().getChild(1).getText();
                        String n2 = ctx.eq().getChild(3).getText();
                        nextProcess = new Eq(n1, n2, nmap);
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(5);
                }
                else if(ctx.neq() != null){
                        String n1 = ctx.neq().getChild(1).getText();
                        String n2 = ctx.neq().getChild(3).getText();
                        nextProcess = new Neq(n1, n2, nmap);
                        next = (PiParser.ProcessContext) ctx.getChild(0).getChild(5);
                }
                else if(ctx.defined() != null){
                        String proc = ctx.defined().getText().substring(0,ctx.defined().getText().length()-1);
                        String[] parts = proc.split("[(]");
                        String[] args;
                        if(parts.length == 2)
                                args = parts[1].split(",");
                        else
                                args = new String[0];
                        nextProcess = new Defined(parts[0], args, nmap);
                        return nextProcess;
                }
                else {
                        System.exit(-2);
                }
                RawProcess p = visitProcess(next);
                try{
                        nextProcess.setChildren(new RawProcess[]{p});
                } catch(Exception e){
                        System.exit(-8);
                }
                nextProcess.SetUpRP();
                return nextProcess;
        }
}

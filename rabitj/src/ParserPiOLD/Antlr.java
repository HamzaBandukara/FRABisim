package ParserPiOLD;

import ProcessElement.Definition;
import ProcessElement.RawProcess;
import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.misc.Pair;
import org.antlr.v4.runtime.tree.ParseTree;

import java.util.Map;

public class Antlr{
    public static Pair<RawProcess, Map<String, Definition>> run(String filename) throws Exception{
        PiLexer lexer = new PiLexer(new ANTLRFileStream(filename));
        PiParser parser = new PiParser(new CommonTokenStream(lexer));
        ParseTree tree = parser.root();
        ExtendedVisitor visitor = new ExtendedVisitor();
        return new Pair<RawProcess, Map<String, Definition>>((RawProcess) visitor.visit(tree), visitor.defined);
    }
}

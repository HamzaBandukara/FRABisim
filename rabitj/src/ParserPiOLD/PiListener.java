package ParserPiOLD;// Generated from Pi.g4 by ANTLR 4.9.3
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PiParser}.
 */
public interface PiListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PiParser#root}.
	 * @param ctx the parse tree
	 */
	void enterRoot(PiParser.RootContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#root}.
	 * @param ctx the parse tree
	 */
	void exitRoot(PiParser.RootContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#line}.
	 * @param ctx the parse tree
	 */
	void enterLine(PiParser.LineContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#line}.
	 * @param ctx the parse tree
	 */
	void exitLine(PiParser.LineContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#definition}.
	 * @param ctx the parse tree
	 */
	void enterDefinition(PiParser.DefinitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#definition}.
	 * @param ctx the parse tree
	 */
	void exitDefinition(PiParser.DefinitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#process}.
	 * @param ctx the parse tree
	 */
	void enterProcess(PiParser.ProcessContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#process}.
	 * @param ctx the parse tree
	 */
	void exitProcess(PiParser.ProcessContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#proc}.
	 * @param ctx the parse tree
	 */
	void enterProc(PiParser.ProcContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#proc}.
	 * @param ctx the parse tree
	 */
	void exitProc(PiParser.ProcContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#zero}.
	 * @param ctx the parse tree
	 */
	void enterZero(PiParser.ZeroContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#zero}.
	 * @param ctx the parse tree
	 */
	void exitZero(PiParser.ZeroContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#write}.
	 * @param ctx the parse tree
	 */
	void enterWrite(PiParser.WriteContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#write}.
	 * @param ctx the parse tree
	 */
	void exitWrite(PiParser.WriteContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#read}.
	 * @param ctx the parse tree
	 */
	void enterRead(PiParser.ReadContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#read}.
	 * @param ctx the parse tree
	 */
	void exitRead(PiParser.ReadContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#nu}.
	 * @param ctx the parse tree
	 */
	void enterNu(PiParser.NuContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#nu}.
	 * @param ctx the parse tree
	 */
	void exitNu(PiParser.NuContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#eq}.
	 * @param ctx the parse tree
	 */
	void enterEq(PiParser.EqContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#eq}.
	 * @param ctx the parse tree
	 */
	void exitEq(PiParser.EqContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#neq}.
	 * @param ctx the parse tree
	 */
	void enterNeq(PiParser.NeqContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#neq}.
	 * @param ctx the parse tree
	 */
	void exitNeq(PiParser.NeqContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#tau}.
	 * @param ctx the parse tree
	 */
	void enterTau(PiParser.TauContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#tau}.
	 * @param ctx the parse tree
	 */
	void exitTau(PiParser.TauContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#defined}.
	 * @param ctx the parse tree
	 */
	void enterDefined(PiParser.DefinedContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#defined}.
	 * @param ctx the parse tree
	 */
	void exitDefined(PiParser.DefinedContext ctx);
}
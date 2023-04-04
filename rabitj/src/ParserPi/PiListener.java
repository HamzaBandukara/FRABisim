// Generated from Pi.g4 by ANTLR 4.9.3

    package ParserPi;

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
	 * Enter a parse tree produced by {@link PiParser#aprocess}.
	 * @param ctx the parse tree
	 */
	void enterAprocess(PiParser.AprocessContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#aprocess}.
	 * @param ctx the parse tree
	 */
	void exitAprocess(PiParser.AprocessContext ctx);
	/**
	 * Enter a parse tree produced by {@link PiParser#bprocess}.
	 * @param ctx the parse tree
	 */
	void enterBprocess(PiParser.BprocessContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#bprocess}.
	 * @param ctx the parse tree
	 */
	void exitBprocess(PiParser.BprocessContext ctx);
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
	 * Enter a parse tree produced by {@link PiParser#processmid}.
	 * @param ctx the parse tree
	 */
	void enterProcessmid(PiParser.ProcessmidContext ctx);
	/**
	 * Exit a parse tree produced by {@link PiParser#processmid}.
	 * @param ctx the parse tree
	 */
	void exitProcessmid(PiParser.ProcessmidContext ctx);
}
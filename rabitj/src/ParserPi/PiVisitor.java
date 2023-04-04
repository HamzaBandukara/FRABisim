// Generated from Pi.g4 by ANTLR 4.9.3

    package ParserPi;

import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link PiParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface PiVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link PiParser#root}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRoot(PiParser.RootContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#line}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLine(PiParser.LineContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDefinition(PiParser.DefinitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#aprocess}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAprocess(PiParser.AprocessContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#bprocess}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBprocess(PiParser.BprocessContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#process}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess(PiParser.ProcessContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#processmid}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcessmid(PiParser.ProcessmidContext ctx);
}
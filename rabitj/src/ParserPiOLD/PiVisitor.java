package ParserPiOLD;
// Generated from Pi.g4 by ANTLR 4.9.3
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
	 * Visit a parse tree produced by {@link PiParser#process}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess(PiParser.ProcessContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#proc}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProc(PiParser.ProcContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#zero}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZero(PiParser.ZeroContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#write}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWrite(PiParser.WriteContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#read}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRead(PiParser.ReadContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#nu}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNu(PiParser.NuContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#eq}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEq(PiParser.EqContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#neq}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNeq(PiParser.NeqContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#tau}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTau(PiParser.TauContext ctx);
	/**
	 * Visit a parse tree produced by {@link PiParser#defined}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDefined(PiParser.DefinedContext ctx);
}
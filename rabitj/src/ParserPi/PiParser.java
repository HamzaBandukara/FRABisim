// Generated from Pi.g4 by ANTLR 4.9.3

    package ParserPi;

import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class PiParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, CHANNEL=16, 
		PROCESSNAME=17, WHITESPACE=18, NEWLINE=19, PAR=20, SUM=21;
	public static final int
		RULE_root = 0, RULE_line = 1, RULE_definition = 2, RULE_aprocess = 3, 
		RULE_bprocess = 4, RULE_process = 5, RULE_processmid = 6;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "line", "definition", "aprocess", "bprocess", "process", "processmid"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'TEST'", "'WITH'", "'('", "','", "')'", "'='", "'<'", "'>'", "'.'", 
			"'['", "'#'", "']'", "'$'", "'_t.'", "'0'", null, null, "' '", null, 
			"'|'", "'+'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, "CHANNEL", "PROCESSNAME", "WHITESPACE", "NEWLINE", 
			"PAR", "SUM"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "Pi.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public PiParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class RootContext extends ParserRuleContext {
		public List<AprocessContext> aprocess() {
			return getRuleContexts(AprocessContext.class);
		}
		public AprocessContext aprocess(int i) {
			return getRuleContext(AprocessContext.class,i);
		}
		public TerminalNode EOF() { return getToken(PiParser.EOF, 0); }
		public List<LineContext> line() {
			return getRuleContexts(LineContext.class);
		}
		public LineContext line(int i) {
			return getRuleContext(LineContext.class,i);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(PiParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(PiParser.NEWLINE, i);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterRoot(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitRoot(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitRoot(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_root);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(17); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(14);
				line();
				setState(15);
				match(NEWLINE);
				}
				}
				setState(19); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__2) | (1L << T__9) | (1L << T__12) | (1L << T__13) | (1L << T__14) | (1L << CHANNEL) | (1L << PROCESSNAME) | (1L << NEWLINE))) != 0) );
			setState(21);
			match(T__0);
			setState(22);
			aprocess();
			setState(23);
			match(T__1);
			setState(24);
			aprocess();
			setState(28);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==NEWLINE) {
				{
				{
				setState(25);
				match(NEWLINE);
				}
				}
				setState(30);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(31);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LineContext extends ParserRuleContext {
		public AprocessContext aprocess() {
			return getRuleContext(AprocessContext.class,0);
		}
		public DefinitionContext definition() {
			return getRuleContext(DefinitionContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(PiParser.NEWLINE, 0); }
		public LineContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_line; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterLine(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitLine(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitLine(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LineContext line() throws RecognitionException {
		LineContext _localctx = new LineContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_line);
		try {
			setState(36);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(33);
				aprocess();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(34);
				definition();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(35);
				match(NEWLINE);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DefinitionContext extends ParserRuleContext {
		public TerminalNode PROCESSNAME() { return getToken(PiParser.PROCESSNAME, 0); }
		public AprocessContext aprocess() {
			return getRuleContext(AprocessContext.class,0);
		}
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public DefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_definition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DefinitionContext definition() throws RecognitionException {
		DefinitionContext _localctx = new DefinitionContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_definition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(38);
			match(PROCESSNAME);
			setState(39);
			match(T__2);
			setState(41);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CHANNEL) {
				{
				setState(40);
				match(CHANNEL);
				}
			}

			setState(47);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(43);
				match(T__3);
				setState(44);
				match(CHANNEL);
				}
				}
				setState(49);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(50);
			match(T__4);
			setState(51);
			match(T__5);
			setState(52);
			aprocess();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AprocessContext extends ParserRuleContext {
		public List<BprocessContext> bprocess() {
			return getRuleContexts(BprocessContext.class);
		}
		public BprocessContext bprocess(int i) {
			return getRuleContext(BprocessContext.class,i);
		}
		public List<TerminalNode> SUM() { return getTokens(PiParser.SUM); }
		public TerminalNode SUM(int i) {
			return getToken(PiParser.SUM, i);
		}
		public AprocessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_aprocess; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterAprocess(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitAprocess(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitAprocess(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AprocessContext aprocess() throws RecognitionException {
		AprocessContext _localctx = new AprocessContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_aprocess);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(54);
			bprocess();
			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==SUM) {
				{
				{
				setState(55);
				match(SUM);
				setState(56);
				bprocess();
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BprocessContext extends ParserRuleContext {
		public List<ProcessContext> process() {
			return getRuleContexts(ProcessContext.class);
		}
		public ProcessContext process(int i) {
			return getRuleContext(ProcessContext.class,i);
		}
		public List<TerminalNode> PAR() { return getTokens(PiParser.PAR); }
		public TerminalNode PAR(int i) {
			return getToken(PiParser.PAR, i);
		}
		public BprocessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bprocess; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterBprocess(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitBprocess(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitBprocess(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BprocessContext bprocess() throws RecognitionException {
		BprocessContext _localctx = new BprocessContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_bprocess);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(62);
			process();
			setState(67);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==PAR) {
				{
				{
				setState(63);
				match(PAR);
				setState(64);
				process();
				}
				}
				setState(69);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ProcessContext extends ParserRuleContext {
		public AprocessContext aprocess() {
			return getRuleContext(AprocessContext.class,0);
		}
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public TerminalNode PROCESSNAME() { return getToken(PiParser.PROCESSNAME, 0); }
		public ProcessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_process; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterProcess(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitProcess(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitProcess(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProcessContext process() throws RecognitionException {
		ProcessContext _localctx = new ProcessContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_process);
		int _la;
		try {
			setState(111);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__2:
				enterOuterAlt(_localctx, 1);
				{
				setState(70);
				match(T__2);
				setState(71);
				aprocess();
				setState(72);
				match(T__4);
				}
				break;
			case CHANNEL:
				enterOuterAlt(_localctx, 2);
				{
				setState(74);
				match(CHANNEL);
				setState(81);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__6:
					{
					setState(75);
					match(T__6);
					setState(76);
					match(CHANNEL);
					setState(77);
					match(T__7);
					}
					break;
				case T__2:
					{
					setState(78);
					match(T__2);
					setState(79);
					match(CHANNEL);
					setState(80);
					match(T__4);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(83);
				match(T__8);
				setState(84);
				process();
				}
				break;
			case T__9:
				enterOuterAlt(_localctx, 3);
				{
				setState(85);
				match(T__9);
				setState(86);
				match(CHANNEL);
				setState(87);
				_la = _input.LA(1);
				if ( !(_la==T__5 || _la==T__10) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(88);
				match(CHANNEL);
				setState(89);
				match(T__11);
				setState(90);
				process();
				}
				break;
			case T__12:
				enterOuterAlt(_localctx, 4);
				{
				setState(91);
				match(T__12);
				setState(92);
				match(CHANNEL);
				setState(93);
				match(T__8);
				setState(94);
				process();
				}
				break;
			case T__13:
				enterOuterAlt(_localctx, 5);
				{
				setState(95);
				match(T__13);
				setState(96);
				process();
				}
				break;
			case PROCESSNAME:
				enterOuterAlt(_localctx, 6);
				{
				setState(97);
				match(PROCESSNAME);
				setState(98);
				match(T__2);
				setState(100);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==CHANNEL) {
					{
					setState(99);
					match(CHANNEL);
					}
				}

				setState(106);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(102);
					match(T__3);
					setState(103);
					match(CHANNEL);
					}
					}
					setState(108);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(109);
				match(T__4);
				}
				break;
			case T__14:
				enterOuterAlt(_localctx, 7);
				{
				setState(110);
				match(T__14);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ProcessmidContext extends ParserRuleContext {
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public TerminalNode PAR() { return getToken(PiParser.PAR, 0); }
		public TerminalNode SUM() { return getToken(PiParser.SUM, 0); }
		public ProcessmidContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_processmid; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterProcessmid(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitProcessmid(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitProcessmid(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProcessmidContext processmid() throws RecognitionException {
		ProcessmidContext _localctx = new ProcessmidContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_processmid);
		int _la;
		try {
			setState(116);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case PAR:
			case SUM:
				enterOuterAlt(_localctx, 1);
				{
				setState(113);
				_la = _input.LA(1);
				if ( !(_la==PAR || _la==SUM) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(114);
				process();
				}
				break;
			case EOF:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\27y\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\3\2\3\2\3\2\6\2\24\n\2\r\2"+
		"\16\2\25\3\2\3\2\3\2\3\2\3\2\7\2\35\n\2\f\2\16\2 \13\2\3\2\3\2\3\3\3\3"+
		"\3\3\5\3\'\n\3\3\4\3\4\3\4\5\4,\n\4\3\4\3\4\7\4\60\n\4\f\4\16\4\63\13"+
		"\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\7\5<\n\5\f\5\16\5?\13\5\3\6\3\6\3\6\7\6"+
		"D\n\6\f\6\16\6G\13\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7T"+
		"\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3"+
		"\7\5\7g\n\7\3\7\3\7\7\7k\n\7\f\7\16\7n\13\7\3\7\3\7\5\7r\n\7\3\b\3\b\3"+
		"\b\5\bw\n\b\3\b\2\2\t\2\4\6\b\n\f\16\2\4\4\2\b\b\r\r\3\2\26\27\2\u0083"+
		"\2\23\3\2\2\2\4&\3\2\2\2\6(\3\2\2\2\b8\3\2\2\2\n@\3\2\2\2\fq\3\2\2\2\16"+
		"v\3\2\2\2\20\21\5\4\3\2\21\22\7\25\2\2\22\24\3\2\2\2\23\20\3\2\2\2\24"+
		"\25\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2\26\27\3\2\2\2\27\30\7\3\2\2\30"+
		"\31\5\b\5\2\31\32\7\4\2\2\32\36\5\b\5\2\33\35\7\25\2\2\34\33\3\2\2\2\35"+
		" \3\2\2\2\36\34\3\2\2\2\36\37\3\2\2\2\37!\3\2\2\2 \36\3\2\2\2!\"\7\2\2"+
		"\3\"\3\3\2\2\2#\'\5\b\5\2$\'\5\6\4\2%\'\7\25\2\2&#\3\2\2\2&$\3\2\2\2&"+
		"%\3\2\2\2\'\5\3\2\2\2()\7\23\2\2)+\7\5\2\2*,\7\22\2\2+*\3\2\2\2+,\3\2"+
		"\2\2,\61\3\2\2\2-.\7\6\2\2.\60\7\22\2\2/-\3\2\2\2\60\63\3\2\2\2\61/\3"+
		"\2\2\2\61\62\3\2\2\2\62\64\3\2\2\2\63\61\3\2\2\2\64\65\7\7\2\2\65\66\7"+
		"\b\2\2\66\67\5\b\5\2\67\7\3\2\2\28=\5\n\6\29:\7\27\2\2:<\5\n\6\2;9\3\2"+
		"\2\2<?\3\2\2\2=;\3\2\2\2=>\3\2\2\2>\t\3\2\2\2?=\3\2\2\2@E\5\f\7\2AB\7"+
		"\26\2\2BD\5\f\7\2CA\3\2\2\2DG\3\2\2\2EC\3\2\2\2EF\3\2\2\2F\13\3\2\2\2"+
		"GE\3\2\2\2HI\7\5\2\2IJ\5\b\5\2JK\7\7\2\2Kr\3\2\2\2LS\7\22\2\2MN\7\t\2"+
		"\2NO\7\22\2\2OT\7\n\2\2PQ\7\5\2\2QR\7\22\2\2RT\7\7\2\2SM\3\2\2\2SP\3\2"+
		"\2\2TU\3\2\2\2UV\7\13\2\2Vr\5\f\7\2WX\7\f\2\2XY\7\22\2\2YZ\t\2\2\2Z[\7"+
		"\22\2\2[\\\7\16\2\2\\r\5\f\7\2]^\7\17\2\2^_\7\22\2\2_`\7\13\2\2`r\5\f"+
		"\7\2ab\7\20\2\2br\5\f\7\2cd\7\23\2\2df\7\5\2\2eg\7\22\2\2fe\3\2\2\2fg"+
		"\3\2\2\2gl\3\2\2\2hi\7\6\2\2ik\7\22\2\2jh\3\2\2\2kn\3\2\2\2lj\3\2\2\2"+
		"lm\3\2\2\2mo\3\2\2\2nl\3\2\2\2or\7\7\2\2pr\7\21\2\2qH\3\2\2\2qL\3\2\2"+
		"\2qW\3\2\2\2q]\3\2\2\2qa\3\2\2\2qc\3\2\2\2qp\3\2\2\2r\r\3\2\2\2st\t\3"+
		"\2\2tw\5\f\7\2uw\3\2\2\2vs\3\2\2\2vu\3\2\2\2w\17\3\2\2\2\16\25\36&+\61"+
		"=ESflqv";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
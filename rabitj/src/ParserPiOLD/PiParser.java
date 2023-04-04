package ParserPiOLD;
// Generated from Pi.g4 by ANTLR 4.9.3
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class PiParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, CHANNEL=17, 
		PROCESSNAME=18, WHITESPACE=19, NEWLINE=20, PAR=21, SUM=22;
	public static final int
		RULE_root = 0, RULE_line = 1, RULE_definition = 2, RULE_process = 3, RULE_proc = 4, 
		RULE_zero = 5, RULE_write = 6, RULE_read = 7, RULE_nu = 8, RULE_eq = 9, 
		RULE_neq = 10, RULE_tau = 11, RULE_defined = 12;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "line", "definition", "process", "proc", "zero", "write", "read", 
			"nu", "eq", "neq", "tau", "defined"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'TEST'", "'WITH'", "'('", "','", "')'", "'='", "'0'", "'<'", "'>.'", 
			"').'", "'$'", "'.'", "'['", "']'", "'#'", "'_t.'", null, null, "' '", 
			null, "'|'", "'+'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, "CHANNEL", "PROCESSNAME", "WHITESPACE", 
			"NEWLINE", "PAR", "SUM"
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
		public List<ProcessContext> process() {
			return getRuleContexts(ProcessContext.class);
		}
		public ProcessContext process(int i) {
			return getRuleContext(ProcessContext.class,i);
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
			setState(29); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(26);
				line();
				setState(27);
				match(NEWLINE);
				}
				}
				setState(31); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__2) | (1L << T__6) | (1L << T__10) | (1L << T__12) | (1L << T__15) | (1L << CHANNEL) | (1L << PROCESSNAME) | (1L << NEWLINE))) != 0) );
			setState(33);
			match(T__0);
			setState(34);
			process();
			setState(35);
			match(T__1);
			setState(36);
			process();
			setState(40);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==NEWLINE) {
				{
				{
				setState(37);
				match(NEWLINE);
				}
				}
				setState(42);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(43);
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
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
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
			setState(48);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(45);
				process();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(46);
				definition();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(47);
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
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
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
			setState(50);
			match(PROCESSNAME);
			setState(51);
			match(T__2);
			setState(53);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CHANNEL) {
				{
				setState(52);
				match(CHANNEL);
				}
			}

			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(55);
				match(T__3);
				setState(56);
				match(CHANNEL);
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(62);
			match(T__4);
			setState(63);
			match(T__5);
			setState(64);
			process();
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
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public List<ProcContext> proc() {
			return getRuleContexts(ProcContext.class);
		}
		public ProcContext proc(int i) {
			return getRuleContext(ProcContext.class,i);
		}
		public TerminalNode PAR() { return getToken(PiParser.PAR, 0); }
		public TerminalNode SUM() { return getToken(PiParser.SUM, 0); }
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
		enterRule(_localctx, 6, RULE_process);
		int _la;
		try {
			setState(75);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(66);
				match(T__2);
				setState(67);
				process();
				setState(68);
				match(T__4);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(70);
				proc();
				setState(71);
				_la = _input.LA(1);
				if ( !(_la==PAR || _la==SUM) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(72);
				proc();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(74);
				proc();
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

	public static class ProcContext extends ParserRuleContext {
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public ZeroContext zero() {
			return getRuleContext(ZeroContext.class,0);
		}
		public WriteContext write() {
			return getRuleContext(WriteContext.class,0);
		}
		public ReadContext read() {
			return getRuleContext(ReadContext.class,0);
		}
		public NuContext nu() {
			return getRuleContext(NuContext.class,0);
		}
		public EqContext eq() {
			return getRuleContext(EqContext.class,0);
		}
		public NeqContext neq() {
			return getRuleContext(NeqContext.class,0);
		}
		public DefinedContext defined() {
			return getRuleContext(DefinedContext.class,0);
		}
		public TauContext tau() {
			return getRuleContext(TauContext.class,0);
		}
		public ProcContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_proc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterProc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitProc(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitProc(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProcContext proc() throws RecognitionException {
		ProcContext _localctx = new ProcContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_proc);
		try {
			setState(89);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(77);
				match(T__2);
				setState(78);
				process();
				setState(79);
				match(T__4);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(81);
				zero();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(82);
				write();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(83);
				read();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(84);
				nu();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(85);
				eq();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(86);
				neq();
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(87);
				defined();
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(88);
				tau();
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

	public static class ZeroContext extends ParserRuleContext {
		public ZeroContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zero; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterZero(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitZero(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitZero(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ZeroContext zero() throws RecognitionException {
		ZeroContext _localctx = new ZeroContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_zero);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(91);
			match(T__6);
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

	public static class WriteContext extends ParserRuleContext {
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public WriteContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_write; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterWrite(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitWrite(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitWrite(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WriteContext write() throws RecognitionException {
		WriteContext _localctx = new WriteContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_write);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(93);
			match(CHANNEL);
			setState(94);
			match(T__7);
			setState(95);
			match(CHANNEL);
			setState(96);
			match(T__8);
			setState(97);
			process();
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

	public static class ReadContext extends ParserRuleContext {
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public ReadContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_read; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterRead(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitRead(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitRead(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ReadContext read() throws RecognitionException {
		ReadContext _localctx = new ReadContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_read);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99);
			match(CHANNEL);
			setState(100);
			match(T__2);
			setState(101);
			match(CHANNEL);
			setState(102);
			match(T__9);
			setState(103);
			process();
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

	public static class NuContext extends ParserRuleContext {
		public TerminalNode CHANNEL() { return getToken(PiParser.CHANNEL, 0); }
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public NuContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nu; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterNu(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitNu(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitNu(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NuContext nu() throws RecognitionException {
		NuContext _localctx = new NuContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_nu);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(105);
			match(T__10);
			setState(106);
			match(CHANNEL);
			setState(107);
			match(T__11);
			setState(108);
			process();
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

	public static class EqContext extends ParserRuleContext {
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public EqContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eq; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterEq(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitEq(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitEq(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EqContext eq() throws RecognitionException {
		EqContext _localctx = new EqContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_eq);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(110);
			match(T__12);
			setState(111);
			match(CHANNEL);
			setState(112);
			match(T__5);
			setState(113);
			match(CHANNEL);
			setState(114);
			match(T__13);
			setState(115);
			process();
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

	public static class NeqContext extends ParserRuleContext {
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public NeqContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_neq; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterNeq(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitNeq(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitNeq(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NeqContext neq() throws RecognitionException {
		NeqContext _localctx = new NeqContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_neq);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(117);
			match(T__12);
			setState(118);
			match(CHANNEL);
			setState(119);
			match(T__14);
			setState(120);
			match(CHANNEL);
			setState(121);
			match(T__13);
			setState(122);
			process();
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

	public static class TauContext extends ParserRuleContext {
		public ProcessContext process() {
			return getRuleContext(ProcessContext.class,0);
		}
		public TauContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tau; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterTau(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitTau(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitTau(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TauContext tau() throws RecognitionException {
		TauContext _localctx = new TauContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_tau);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(124);
			match(T__15);
			setState(125);
			process();
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

	public static class DefinedContext extends ParserRuleContext {
		public TerminalNode PROCESSNAME() { return getToken(PiParser.PROCESSNAME, 0); }
		public List<TerminalNode> CHANNEL() { return getTokens(PiParser.CHANNEL); }
		public TerminalNode CHANNEL(int i) {
			return getToken(PiParser.CHANNEL, i);
		}
		public DefinedContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_defined; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).enterDefined(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PiListener ) ((PiListener)listener).exitDefined(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PiVisitor ) return ((PiVisitor<? extends T>)visitor).visitDefined(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DefinedContext defined() throws RecognitionException {
		DefinedContext _localctx = new DefinedContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_defined);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(127);
			match(PROCESSNAME);
			setState(128);
			match(T__2);
			setState(130);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CHANNEL) {
				{
				setState(129);
				match(CHANNEL);
				}
			}

			setState(136);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(132);
				match(T__3);
				setState(133);
				match(CHANNEL);
				}
				}
				setState(138);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(139);
			match(T__4);
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\30\u0090\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\3\2\3\2\3\2\6\2 \n\2\r\2\16\2!\3\2\3\2"+
		"\3\2\3\2\3\2\7\2)\n\2\f\2\16\2,\13\2\3\2\3\2\3\3\3\3\3\3\5\3\63\n\3\3"+
		"\4\3\4\3\4\5\48\n\4\3\4\3\4\7\4<\n\4\f\4\16\4?\13\4\3\4\3\4\3\4\3\4\3"+
		"\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5N\n\5\3\6\3\6\3\6\3\6\3\6\3\6\3"+
		"\6\3\6\3\6\3\6\3\6\3\6\5\6\\\n\6\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3"+
		"\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3"+
		"\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\5\16\u0085"+
		"\n\16\3\16\3\16\7\16\u0089\n\16\f\16\16\16\u008c\13\16\3\16\3\16\3\16"+
		"\2\2\17\2\4\6\b\n\f\16\20\22\24\26\30\32\2\3\3\2\27\30\2\u0094\2\37\3"+
		"\2\2\2\4\62\3\2\2\2\6\64\3\2\2\2\bM\3\2\2\2\n[\3\2\2\2\f]\3\2\2\2\16_"+
		"\3\2\2\2\20e\3\2\2\2\22k\3\2\2\2\24p\3\2\2\2\26w\3\2\2\2\30~\3\2\2\2\32"+
		"\u0081\3\2\2\2\34\35\5\4\3\2\35\36\7\26\2\2\36 \3\2\2\2\37\34\3\2\2\2"+
		" !\3\2\2\2!\37\3\2\2\2!\"\3\2\2\2\"#\3\2\2\2#$\7\3\2\2$%\5\b\5\2%&\7\4"+
		"\2\2&*\5\b\5\2\')\7\26\2\2(\'\3\2\2\2),\3\2\2\2*(\3\2\2\2*+\3\2\2\2+-"+
		"\3\2\2\2,*\3\2\2\2-.\7\2\2\3.\3\3\2\2\2/\63\5\b\5\2\60\63\5\6\4\2\61\63"+
		"\7\26\2\2\62/\3\2\2\2\62\60\3\2\2\2\62\61\3\2\2\2\63\5\3\2\2\2\64\65\7"+
		"\24\2\2\65\67\7\5\2\2\668\7\23\2\2\67\66\3\2\2\2\678\3\2\2\28=\3\2\2\2"+
		"9:\7\6\2\2:<\7\23\2\2;9\3\2\2\2<?\3\2\2\2=;\3\2\2\2=>\3\2\2\2>@\3\2\2"+
		"\2?=\3\2\2\2@A\7\7\2\2AB\7\b\2\2BC\5\b\5\2C\7\3\2\2\2DE\7\5\2\2EF\5\b"+
		"\5\2FG\7\7\2\2GN\3\2\2\2HI\5\n\6\2IJ\t\2\2\2JK\5\n\6\2KN\3\2\2\2LN\5\n"+
		"\6\2MD\3\2\2\2MH\3\2\2\2ML\3\2\2\2N\t\3\2\2\2OP\7\5\2\2PQ\5\b\5\2QR\7"+
		"\7\2\2R\\\3\2\2\2S\\\5\f\7\2T\\\5\16\b\2U\\\5\20\t\2V\\\5\22\n\2W\\\5"+
		"\24\13\2X\\\5\26\f\2Y\\\5\32\16\2Z\\\5\30\r\2[O\3\2\2\2[S\3\2\2\2[T\3"+
		"\2\2\2[U\3\2\2\2[V\3\2\2\2[W\3\2\2\2[X\3\2\2\2[Y\3\2\2\2[Z\3\2\2\2\\\13"+
		"\3\2\2\2]^\7\t\2\2^\r\3\2\2\2_`\7\23\2\2`a\7\n\2\2ab\7\23\2\2bc\7\13\2"+
		"\2cd\5\b\5\2d\17\3\2\2\2ef\7\23\2\2fg\7\5\2\2gh\7\23\2\2hi\7\f\2\2ij\5"+
		"\b\5\2j\21\3\2\2\2kl\7\r\2\2lm\7\23\2\2mn\7\16\2\2no\5\b\5\2o\23\3\2\2"+
		"\2pq\7\17\2\2qr\7\23\2\2rs\7\b\2\2st\7\23\2\2tu\7\20\2\2uv\5\b\5\2v\25"+
		"\3\2\2\2wx\7\17\2\2xy\7\23\2\2yz\7\21\2\2z{\7\23\2\2{|\7\20\2\2|}\5\b"+
		"\5\2}\27\3\2\2\2~\177\7\22\2\2\177\u0080\5\b\5\2\u0080\31\3\2\2\2\u0081"+
		"\u0082\7\24\2\2\u0082\u0084\7\5\2\2\u0083\u0085\7\23\2\2\u0084\u0083\3"+
		"\2\2\2\u0084\u0085\3\2\2\2\u0085\u008a\3\2\2\2\u0086\u0087\7\6\2\2\u0087"+
		"\u0089\7\23\2\2\u0088\u0086\3\2\2\2\u0089\u008c\3\2\2\2\u008a\u0088\3"+
		"\2\2\2\u008a\u008b\3\2\2\2\u008b\u008d\3\2\2\2\u008c\u008a\3\2\2\2\u008d"+
		"\u008e\7\7\2\2\u008e\33\3\2\2\2\13!*\62\67=M[\u0084\u008a";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
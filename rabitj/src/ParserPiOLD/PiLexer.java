package ParserPiOLD;
// Generated from Pi.g4 by ANTLR 4.9.3
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class PiLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, CHANNEL=17, 
		PROCESSNAME=18, WHITESPACE=19, NEWLINE=20, PAR=21, SUM=22;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "CHANNEL", 
			"PROCESSNAME", "WHITESPACE", "NEWLINE", "PAR", "SUM"
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


	public PiLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Pi.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\30x\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\3\2\3\2\3\2\3\2\3\2"+
		"\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3"+
		"\n\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20"+
		"\3\21\3\21\3\21\3\21\3\22\3\22\7\22\\\n\22\f\22\16\22_\13\22\3\23\3\23"+
		"\7\23c\n\23\f\23\16\23f\13\23\3\24\3\24\3\24\3\24\3\25\5\25m\n\25\3\25"+
		"\3\25\6\25q\n\25\r\25\16\25r\3\26\3\26\3\27\3\27\2\2\30\3\3\5\4\7\5\t"+
		"\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23"+
		"%\24\'\25)\26+\27-\30\3\2\6\3\2c|\4\2\62;c|\3\2C\\\4\2\62;C\\\2|\2\3\3"+
		"\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2"+
		"\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3"+
		"\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2"+
		"%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\3/\3\2\2\2\5\64"+
		"\3\2\2\2\79\3\2\2\2\t;\3\2\2\2\13=\3\2\2\2\r?\3\2\2\2\17A\3\2\2\2\21C"+
		"\3\2\2\2\23E\3\2\2\2\25H\3\2\2\2\27K\3\2\2\2\31M\3\2\2\2\33O\3\2\2\2\35"+
		"Q\3\2\2\2\37S\3\2\2\2!U\3\2\2\2#Y\3\2\2\2%`\3\2\2\2\'g\3\2\2\2)p\3\2\2"+
		"\2+t\3\2\2\2-v\3\2\2\2/\60\7V\2\2\60\61\7G\2\2\61\62\7U\2\2\62\63\7V\2"+
		"\2\63\4\3\2\2\2\64\65\7Y\2\2\65\66\7K\2\2\66\67\7V\2\2\678\7J\2\28\6\3"+
		"\2\2\29:\7*\2\2:\b\3\2\2\2;<\7.\2\2<\n\3\2\2\2=>\7+\2\2>\f\3\2\2\2?@\7"+
		"?\2\2@\16\3\2\2\2AB\7\62\2\2B\20\3\2\2\2CD\7>\2\2D\22\3\2\2\2EF\7@\2\2"+
		"FG\7\60\2\2G\24\3\2\2\2HI\7+\2\2IJ\7\60\2\2J\26\3\2\2\2KL\7&\2\2L\30\3"+
		"\2\2\2MN\7\60\2\2N\32\3\2\2\2OP\7]\2\2P\34\3\2\2\2QR\7_\2\2R\36\3\2\2"+
		"\2ST\7%\2\2T \3\2\2\2UV\7a\2\2VW\7v\2\2WX\7\60\2\2X\"\3\2\2\2Y]\t\2\2"+
		"\2Z\\\t\3\2\2[Z\3\2\2\2\\_\3\2\2\2][\3\2\2\2]^\3\2\2\2^$\3\2\2\2_]\3\2"+
		"\2\2`d\t\4\2\2ac\t\5\2\2ba\3\2\2\2cf\3\2\2\2db\3\2\2\2de\3\2\2\2e&\3\2"+
		"\2\2fd\3\2\2\2gh\7\"\2\2hi\3\2\2\2ij\b\24\2\2j(\3\2\2\2km\7\17\2\2lk\3"+
		"\2\2\2lm\3\2\2\2mn\3\2\2\2nq\7\f\2\2oq\7\17\2\2pl\3\2\2\2po\3\2\2\2qr"+
		"\3\2\2\2rp\3\2\2\2rs\3\2\2\2s*\3\2\2\2tu\7~\2\2u,\3\2\2\2vw\7-\2\2w.\3"+
		"\2\2\2\n\2[]bdlpr\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
// Generated from Pi.g4 by ANTLR 4.9.3

    package ParserPi;

import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class PiLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, CHANNEL=16, 
		PROCESSNAME=17, WHITESPACE=18, NEWLINE=19, PAR=20, SUM=21;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "CHANNEL", "PROCESSNAME", 
			"WHITESPACE", "NEWLINE", "PAR", "SUM"
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\27r\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3"+
		"\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13"+
		"\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\17\3\17\3\20\3\20\3\21\3\21"+
		"\7\21V\n\21\f\21\16\21Y\13\21\3\22\3\22\7\22]\n\22\f\22\16\22`\13\22\3"+
		"\23\3\23\3\23\3\23\3\24\5\24g\n\24\3\24\3\24\6\24k\n\24\r\24\16\24l\3"+
		"\25\3\25\3\26\3\26\2\2\27\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25"+
		"\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27\3\2\6\3\2c|\4"+
		"\2\62;c|\3\2C\\\4\2\62;C\\\2v\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t"+
		"\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2"+
		"\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2"+
		"\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2"+
		"+\3\2\2\2\3-\3\2\2\2\5\62\3\2\2\2\7\67\3\2\2\2\t9\3\2\2\2\13;\3\2\2\2"+
		"\r=\3\2\2\2\17?\3\2\2\2\21A\3\2\2\2\23C\3\2\2\2\25E\3\2\2\2\27G\3\2\2"+
		"\2\31I\3\2\2\2\33K\3\2\2\2\35M\3\2\2\2\37Q\3\2\2\2!S\3\2\2\2#Z\3\2\2\2"+
		"%a\3\2\2\2\'j\3\2\2\2)n\3\2\2\2+p\3\2\2\2-.\7V\2\2./\7G\2\2/\60\7U\2\2"+
		"\60\61\7V\2\2\61\4\3\2\2\2\62\63\7Y\2\2\63\64\7K\2\2\64\65\7V\2\2\65\66"+
		"\7J\2\2\66\6\3\2\2\2\678\7*\2\28\b\3\2\2\29:\7.\2\2:\n\3\2\2\2;<\7+\2"+
		"\2<\f\3\2\2\2=>\7?\2\2>\16\3\2\2\2?@\7>\2\2@\20\3\2\2\2AB\7@\2\2B\22\3"+
		"\2\2\2CD\7\60\2\2D\24\3\2\2\2EF\7]\2\2F\26\3\2\2\2GH\7%\2\2H\30\3\2\2"+
		"\2IJ\7_\2\2J\32\3\2\2\2KL\7&\2\2L\34\3\2\2\2MN\7a\2\2NO\7v\2\2OP\7\60"+
		"\2\2P\36\3\2\2\2QR\7\62\2\2R \3\2\2\2SW\t\2\2\2TV\t\3\2\2UT\3\2\2\2VY"+
		"\3\2\2\2WU\3\2\2\2WX\3\2\2\2X\"\3\2\2\2YW\3\2\2\2Z^\t\4\2\2[]\t\5\2\2"+
		"\\[\3\2\2\2]`\3\2\2\2^\\\3\2\2\2^_\3\2\2\2_$\3\2\2\2`^\3\2\2\2ab\7\"\2"+
		"\2bc\3\2\2\2cd\b\23\2\2d&\3\2\2\2eg\7\17\2\2fe\3\2\2\2fg\3\2\2\2gh\3\2"+
		"\2\2hk\7\f\2\2ik\7\17\2\2jf\3\2\2\2ji\3\2\2\2kl\3\2\2\2lj\3\2\2\2lm\3"+
		"\2\2\2m(\3\2\2\2no\7~\2\2o*\3\2\2\2pq\7-\2\2q,\3\2\2\2\n\2UW\\^fjl\3\b"+
		"\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
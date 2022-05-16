# Generated from Pi.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\25")
        buf.write("`\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7")
        buf.write("\3\7\3\b\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f")
        buf.write("\3\r\3\r\3\16\3\16\3\17\6\17G\n\17\r\17\16\17H\3\20\6")
        buf.write("\20L\n\20\r\20\16\20M\3\21\3\21\3\21\3\21\3\22\5\22U\n")
        buf.write("\22\3\22\3\22\6\22Y\n\22\r\22\16\22Z\3\23\3\23\3\24\3")
        buf.write("\24\2\2\25\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write("\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25\3\2\4")
        buf.write("\3\2c|\4\2\62;C\\\2d\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2")
        buf.write("\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2")
        buf.write("\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31")
        buf.write("\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2")
        buf.write("\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\3)\3\2\2\2\5+\3")
        buf.write("\2\2\2\7-\3\2\2\2\t/\3\2\2\2\13\61\3\2\2\2\r\63\3\2\2")
        buf.write("\2\17\65\3\2\2\2\218\3\2\2\2\23;\3\2\2\2\25=\3\2\2\2\27")
        buf.write("?\3\2\2\2\31A\3\2\2\2\33C\3\2\2\2\35F\3\2\2\2\37K\3\2")
        buf.write("\2\2!O\3\2\2\2#X\3\2\2\2%\\\3\2\2\2\'^\3\2\2\2)*\7*\2")
        buf.write("\2*\4\3\2\2\2+,\7.\2\2,\6\3\2\2\2-.\7+\2\2.\b\3\2\2\2")
        buf.write("/\60\7?\2\2\60\n\3\2\2\2\61\62\7\62\2\2\62\f\3\2\2\2\63")
        buf.write("\64\7>\2\2\64\16\3\2\2\2\65\66\7@\2\2\66\67\7\60\2\2\67")
        buf.write("\20\3\2\2\289\7+\2\29:\7\60\2\2:\22\3\2\2\2;<\7&\2\2<")
        buf.write("\24\3\2\2\2=>\7\60\2\2>\26\3\2\2\2?@\7]\2\2@\30\3\2\2")
        buf.write("\2AB\7_\2\2B\32\3\2\2\2CD\7%\2\2D\34\3\2\2\2EG\t\2\2\2")
        buf.write("FE\3\2\2\2GH\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\36\3\2\2\2J")
        buf.write("L\t\3\2\2KJ\3\2\2\2LM\3\2\2\2MK\3\2\2\2MN\3\2\2\2N \3")
        buf.write("\2\2\2OP\7\"\2\2PQ\3\2\2\2QR\b\21\2\2R\"\3\2\2\2SU\7\17")
        buf.write("\2\2TS\3\2\2\2TU\3\2\2\2UV\3\2\2\2VY\7\f\2\2WY\7\17\2")
        buf.write("\2XT\3\2\2\2XW\3\2\2\2YZ\3\2\2\2ZX\3\2\2\2Z[\3\2\2\2[")
        buf.write("$\3\2\2\2\\]\7~\2\2]&\3\2\2\2^_\7-\2\2_(\3\2\2\2\t\2H")
        buf.write("KMTXZ\3\b\2\2")
        return buf.getvalue()


class PiLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    CHANNEL = 14
    PROCESSNAME = 15
    WHITESPACE = 16
    NEWLINE = 17
    PAR = 18
    SUM = 19

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "','", "')'", "'='", "'0'", "'<'", "'>.'", "').'", "'$'", 
            "'.'", "'['", "']'", "'#'", "' '", "'|'", "'+'" ]

    symbolicNames = [ "<INVALID>",
            "CHANNEL", "PROCESSNAME", "WHITESPACE", "NEWLINE", "PAR", "SUM" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "CHANNEL", 
                  "PROCESSNAME", "WHITESPACE", "NEWLINE", "PAR", "SUM" ]

    grammarFileName = "Pi.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None



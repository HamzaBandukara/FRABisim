from Element import *
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'PAR',
    'COMP',
    'SUM',
    'RES',
    'EQ',
    'NEQ',
    'INP',
    'OUT',
    'CHANNEL',
    'PRD',
    'TML',
    'LPAR',
    'RPAR',
    'TAU',

    'newline'
)

literals = "."


def t_COMP(t):
    r'\((.*)+\)'
    return t

def t_PAR(t):
    r'(.*)+\|(.*)'

def t_SUM(t):
    r'(.*)+\|(.*)'


def t_INP(t):
    r'\w+\(\w+\)'
    return t


def t_OUT(t):
    r'\w+\<\w+\>'
    return t

def t_EQ(t):
    r'\[\w+\=\w+\]'
    return t

def t_NEQ(t):
    r'\[\w+\#\w+\]'
    return t

def t_RES(t):
    r'\$\w+'
    return t

# Regular expression rules for simple tokens

def t_PRD(t):
    r'\.'
    return t

# A regular expression rule with some action code


def t_TML(t):
    r'0'
    t.value = "0"
    return t

def t_TAU(t):
    r'_TAU'
    t.value = "TAU"
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
# Test it out
# data = "(a<b>|b<a>)"
data = "($a.[a=b]a(b)._TAU.[c#d]c<d>.(a(b).b<c>.0|a(b).b<c>.0))"
# data = "((a<b>.0|b<a>.0)+(a<b>.0|b<a>.0))"
# data = "($a.[a=b]a(b)._TAU.[c#d]c<d>.(a(b).b<c>.0|a(b).b<c>.0))"
# ($a.[a=b]a(b)._TAU.[c#d]c<d>.(a(b)+b<c>).(a(b)|b<c>).0)

# Give the lexer some input
lexer.input(data)
channels = []

# Tokenize
def raiseException():
    raise Exception("Lexer error!")


def recursive_lexer(lexer):
    tok = lexer.token()
    if not tok:
        return
    print(tok)
    match tok.type:
        case "COMP":
            lexer = lex.lex()
            lexer.input(tok.value[1:-1])
            return recursive_lexer(lexer)

recursive_lexer(lexer)
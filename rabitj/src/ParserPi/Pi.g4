grammar Pi;

@header {
    package ParserPi;
}

/*
 * Parser Rules
 */

root
    : (line NEWLINE)+ 'TEST' aprocess 'WITH' aprocess NEWLINE* EOF
    ;

line
    : aprocess
    | definition
    | NEWLINE
    ;

definition
    : PROCESSNAME '(' CHANNEL? (',' CHANNEL)* ')' '=' aprocess
    ;

aprocess
    : bprocess (SUM bprocess)*
    ;

bprocess
    : process (PAR process)*
    ;

process
    :  '(' aprocess ')'
    | CHANNEL ( '<' CHANNEL '>' | '(' CHANNEL ')') '.' process
    | '[' CHANNEL ('#' | '=') CHANNEL ']' process
    | '$' CHANNEL '.' process
    | '_t.' process
    | PROCESSNAME '(' CHANNEL? (',' CHANNEL)* ')'
    | '0'
    ;

processmid
    : (PAR | SUM) process
    |
    ;

/*
 * Lexer Rules
 */

CHANNEL     : [a-z] ([a-z] | [0-9])* ;
PROCESSNAME : [A-Z] ([A-Z] | [0-9])* ;
WHITESPACE  : ' ' -> skip ;
NEWLINE     : ('\r'? '\n' | '\r')+ ;
PAR         : '|'  ;
SUM         : '+'  ;

grammar Pi;

/*
 * Parser Rules
 */

root
    : (line NEWLINE)+ 'TEST' process 'WITH' process NEWLINE* EOF
    ;

line
    : process
    | definition
    | NEWLINE
    ;

definition
    : PROCESSNAME '(' CHANNEL? (',' CHANNEL)* ')' '=' process
    ;

process
    :  '(' process ')'
    | proc (PAR | SUM) proc
    | proc
    ;

proc : '(' process ')' | zero | read | write | nu | eq | neq | defined | tau;
zero    : '0'  ;
write   : CHANNEL '<' CHANNEL '>.' process ;
read  : CHANNEL '(' CHANNEL ').' process;
nu      : '$' CHANNEL '.' process ;
eq      : '[' CHANNEL '=' CHANNEL ']' process ;
neq     : '[' CHANNEL '#' CHANNEL ']' process ;
tau     : '_t.' process;
defined     : PROCESSNAME '(' CHANNEL? (',' CHANNEL)* ')';




/*
 * Lexer Rules
 */

CHANNEL     : [a-z] ([a-z] | [0-9])* ;
PROCESSNAME : [A-Z] ([A-Z] | [0-9])* ;
WHITESPACE  : ' ' -> skip ;
NEWLINE     : ('\r'? '\n' | '\r')+ ;
PAR         : '|'  ;
SUM         : '+'  ;

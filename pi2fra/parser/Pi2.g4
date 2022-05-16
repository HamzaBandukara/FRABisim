grammar Pi2;

/*
 * Parser Rules
 */

root
    : line+ EOF  ;
line
    :  process NEWLINE
    | process
    | definition NEWLINE
    | definition
    ;
definition
    : PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')' '=' process
    ;
process
    :   '(' process ')'
    | process ('|' | '+') process
    | '0'
    | CHANNEL '<' CHANNEL '>.' process
    ;

/*
 * Lexer Rules
 */

CHANNEL
    : [a-z]+
    ;
PROCESSNAME
    : ([A-Z] | [0-9])+
    ;
WHITESPACE
    : ' ' -> skip
    ;
NEWLINE
    : ('\r'? '\n' | '\r')+
    ;
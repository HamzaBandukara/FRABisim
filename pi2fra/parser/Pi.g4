grammar Pi;

/*
 * Parser Rules
 */

root    : line+ EOF  ;
line    : process NEWLINE | process | definition NEWLINE | definition ;
definition: PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')' '=' process  ;
process :   '(' process ')' | process PAR process | process SUM process | zero | write | read | nu | eq | neq | defined;
zero    : '0'  ;
write   : CHANNEL '<' CHANNEL '>.' process ;
read  : CHANNEL '(' CHANNEL ').' process;
nu      : '$' CHANNEL '.' process ;
eq      : '[' CHANNEL '=' CHANNEL ']' process ;
neq     : '[' CHANNEL '#' CHANNEL ']' process ;
defined     : PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')';




/*
 * Lexer Rules
 */

CHANNEL     : [a-z]+ ;
PROCESSNAME : ([A-Z] | [0-9])+ ;
WHITESPACE  : ' ' -> skip ;
NEWLINE     : ('\r'? '\n' | '\r')+ ;
PAR         : '|'  ;
SUM         : '+'  ;

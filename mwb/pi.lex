structure Tokens = Tokens

type pos = int
type svalue = Tokens.svalue
type ('a,'b) token = ('a,'b) Tokens.token
type lexresult= (svalue,pos) token
type arg = int ref * int ref

(*val lineNum = ref 0*)
(* val pcount = ref 0 *)
(* val pos = ref 0 *)
val error = fn (e,l : int,_) =>
              (TextIO.output(TextIO.stdOut,"line " ^ (Lib.mkstrint l) ^
                               ": " ^ e ^ "\n"))

fun eof (lno:int ref,pc:int ref) =
    (if !pc > 0 then print("EOF with unclosed parentheses\n")
     else ();
     Tokens.EOF(!lno,!lno))

structure KeyWord : sig
			val cvstringtoint : string -> 
				 int
	     		val find : string ->
				 (string * int * int -> (svalue,int) token) option
	  	    end =
  struct

	val cvstringtoint = fn str =>
	    let fun mkint (nil, s:int) = s
	          | mkint (c::Rest, s) =
	            mkint (Rest, ((ord c)-(ord #"0"))+10*s)
	    in
		mkint (explode str, 0)
	    end

	val TableSize = 21
	val HashFactor = 5

	val hash = fn s =>
	   Lib.fold (fn (c,v)=>(v*HashFactor+(ord c)) mod TableSize) (explode s) 0


	val HashTable = Array.array(TableSize,nil) :
		 (string * (string * int * int -> (svalue,int) token)) list array


	val add = fn (s,v) =>
	 let val i = hash s
	 in Array.update(HashTable,i,(s,v) :: (Array.sub(HashTable, i)))
	 end

        val find = fn s =>
	  let val i = hash s
	      fun f ((key,v)::r) = if s=key then SOME v else f r
	        | f nil = NONE
	  in  f (Array.sub(HashTable, i))
	  end
 
	val _ = 
	    (List.app add
	[("t",Tokens.TAU),

	 ("actions",Tokens.ACTIONS),
	 ("all",Tokens.ALL),
	 ("agent",Tokens.AGENT),
	 ("fagent",Tokens.FAGENT),
	 ("check",Tokens.CHECK),
         ("prove",Tokens.PROVE),
	 ("clear",Tokens.CLEAR),
	 ("deadlocks",Tokens.DEAD),
	 ("debug",Tokens.DEBUG),
	 ("env",Tokens.ENVIRONMENT),
	 ("feq",Tokens.FEQ),
	 ("fweq",Tokens.FWEQ),
	 ("eq",Tokens.EQ),
	 ("eqd",Tokens.EQD),
         ("formula",Tokens.FORMULA),
	 ("input",Tokens.INPUT),
	 ("print",Tokens.PRINT),
	 ("rewrite",Tokens.REWRITE),
	 ("remember",Tokens.REMEMBER),
	 ("set",Tokens.SET),
	 ("show",Tokens.SHOW),
	 ("step",Tokens.STEP),
	 ("ztep",Tokens.ZTEP),
	 ("size",Tokens.SIZE),
	 ("sort",Tokens.SORT),
	 ("tables",Tokens.TABLES),
	 ("threshold",Tokens.THRESHOLD),
	 ("hashdepth",Tokens.HASHDEPTH),
	 ("time",Tokens.TIME),
	 ("traces",Tokens.TRACES),
	 ("ftransitions",Tokens.FTRANS),
	 ("fwtransitions",Tokens.FWTRANS),
	 ("transitions",Tokens.TRANS),
	 ("version",Tokens.VERSION),
         ("verify",Tokens.VERIFY),
	 ("wtransitions",Tokens.WTRANS),
	 ("weq",Tokens.WEQ),
	 ("weqd",Tokens.WEQD),
	 ("help",Tokens.HELP),
	 ("quit",Tokens.QUIT),
	 ("true",Tokens.TRUE),
	 ("false",Tokens.FALSE),
	 ("on",Tokens.ON),
	 ("off",Tokens.OFF),

	 ("TT",Tokens.TT),
	 ("FF",Tokens.FF),
	 ("Sigma",Tokens.SIGMA),
	 ("Bsigma",Tokens.BSIGMA),
	 ("Pi",Tokens.PI),
	 ("exists",Tokens.EXISTS),
         ("some",Tokens.SOME2),
	 ("not",Tokens.NOT),
	 ("nu",Tokens.NU),
	 ("mu",Tokens.MU),
         ("min",Tokens.MIN),
         ("max",Tokens.MAX)
	])
   end
   open KeyWord

%%
%header (functor PILexFun(structure Tokens: PI_TOKENS));
%arg (lineNo:int ref,pCount:int ref);
%s COMM;

loweralpha=[a-z~];
upperalpha=[A-Z];
any=[A-Za-z\_\$\'0-9];
digit=[0-9];
ws = [\ \t];
%%
<INITIAL>"\\\n"       => (Lib.inc lineNo; continue());
<INITIAL>\n       => (Lib.inc lineNo; if !pCount > 0 then continue()
			       else Tokens.EOL(!lineNo,!lineNo));
<INITIAL>{ws}+    => (continue());
<INITIAL>0	  => (Tokens.NIL(!lineNo,!lineNo));
<INITIAL>1	  => (Tokens.ONE(!lineNo,!lineNo));
<INITIAL>{digit}+ => (Tokens.NUM (cvstringtoint yytext, !lineNo, !lineNo));
<INITIAL>{loweralpha}{any}* => (case find yytext of SOME v => v(yytext,!lineNo,!lineNo)
			       | _ => Tokens.ACT(yytext,!lineNo,!lineNo));
<INITIAL>{upperalpha}{any}* => (case find yytext of SOME v => v(yytext,!lineNo,!lineNo)
			       | _ => Tokens.ID(yytext,!lineNo,!lineNo));
<INITIAL>"="      => (Tokens.EQUALS(!lineNo,!lineNo));
<INITIAL>"("      => (Lib.inc pCount; Tokens.LPAR(!lineNo,!lineNo));
<INITIAL>")"      => (Lib.dec pCount; Tokens.RPAR(!lineNo,!lineNo));
<INITIAL>"["      => (Tokens.LBRACK(!lineNo,!lineNo));
<INITIAL>"]"      => (Tokens.RBRACK(!lineNo,!lineNo));
<INITIAL>"{"      => (Tokens.LBRACE(!lineNo,!lineNo));
<INITIAL>"}"      => (Tokens.RBRACE(!lineNo,!lineNo));
<INITIAL>"<"	  => (Tokens.LESSTHAN(!lineNo,!lineNo));
<INITIAL>">"	  => (Tokens.GREATERTHAN(!lineNo,!lineNo));
<INITIAL>"+"      => (Tokens.PLUS(!lineNo,!lineNo));
<INITIAL>"|"      => (Tokens.PAR(!lineNo,!lineNo));
<INITIAL>"\."     => (Tokens.DOT(!lineNo,!lineNo));
<INITIAL>","      => (Tokens.COMMA(!lineNo,!lineNo));
<INITIAL>";"      => (Tokens.SEMICOLON(!lineNo,!lineNo));
<INITIAL>"!"      => (Tokens.BANG(!lineNo,!lineNo));
<INITIAL>"?"      => (Tokens.QUERY(!lineNo,!lineNo));
<INITIAL>"/"      => (Tokens.SLASH(!lineNo,!lineNo));
<INITIAL>"\\"     => (Tokens.BACKSLASH(!lineNo,!lineNo));
<INITIAL>'	  => (Tokens.QUOTE(!lineNo,!lineNo));
<INITIAL>\^	  => (Tokens.HAT(!lineNo,!lineNo));
<INITIAL>"#"	  => (Tokens.SHARP(!lineNo,!lineNo));
<INITIAL>"&"	  => (Tokens.AMPERSAND(!lineNo,!lineNo));
<INITIAL>.      => (error ("ignoring bad character "^yytext,!lineNo,!lineNo);
	             continue());
<INITIAL>\".*\"	=> (Tokens.STRING(substring(yytext,1,(size yytext)-2),!lineNo,!lineNo));
<INITIAL>"(*"     => (YYBEGIN COMM; continue());
<COMM>"\n" 	  => (Lib.inc lineNo; continue());
<COMM>"*)" 	  => (YYBEGIN INITIAL; continue());
<COMM>.    	  => (continue());

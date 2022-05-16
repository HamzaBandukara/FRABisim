functor PILexFun(structure Tokens: PI_TOKENS)=
   struct
    structure UserDeclarations =
      struct
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

end (* end of user routines *)
exception LexError (* raised if illegal leaf action tried *)
structure Internal =
	struct

datatype yyfinstate = N of int
type statedata = {fin : yyfinstate list, trans: string}
(* transition & final state table *)
val tab = let
val s = [ 
 (0, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
 (1, 
"\005\005\005\005\005\005\005\005\005\041\043\005\005\005\005\005\
\\005\005\005\005\005\005\005\005\005\005\005\005\005\005\005\005\
\\041\040\037\036\005\005\035\034\032\031\005\030\029\005\028\027\
\\026\025\023\023\023\023\023\023\023\023\005\022\021\020\019\018\
\\005\016\016\016\016\016\016\016\016\016\016\016\016\016\016\016\
\\016\016\016\016\016\016\016\016\016\016\016\015\013\012\011\005\
\\005\006\006\006\006\006\006\006\006\006\006\006\006\006\006\006\
\\006\006\006\006\006\006\006\006\006\006\006\010\009\008\006\005\
\\005"
),
 (3, 
"\044\044\044\044\044\044\044\044\044\044\047\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\045\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\044\
\\044"
),
 (6, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\007\000\000\007\000\000\000\000\000\000\000\000\
\\007\007\007\007\007\007\007\007\007\007\000\000\000\000\000\000\
\\000\007\007\007\007\007\007\007\007\007\007\007\007\007\007\007\
\\007\007\007\007\007\007\007\007\007\007\007\000\000\000\000\007\
\\000\007\007\007\007\007\007\007\007\007\007\007\007\007\007\007\
\\007\007\007\007\007\007\007\007\007\007\007\000\000\000\000\000\
\\000"
),
 (13, 
"\000\000\000\000\000\000\000\000\000\000\014\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
 (16, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\017\000\000\017\000\000\000\000\000\000\000\000\
\\017\017\017\017\017\017\017\017\017\017\000\000\000\000\000\000\
\\000\017\017\017\017\017\017\017\017\017\017\017\017\017\017\017\
\\017\017\017\017\017\017\017\017\017\017\017\000\000\000\000\017\
\\000\017\017\017\017\017\017\017\017\017\017\017\017\017\017\017\
\\017\017\017\017\017\017\017\017\017\017\017\000\000\000\000\000\
\\000"
),
 (23, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\024\024\024\024\024\024\024\024\024\024\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
 (32, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\033\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
 (37, 
"\038\038\038\038\038\038\038\038\038\038\000\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\039\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\038\
\\038"
),
 (41, 
"\000\000\000\000\000\000\000\000\000\042\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\042\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
 (45, 
"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\046\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\\000"
),
(0, "")]
fun f x = x 
val s = map f (rev (tl (rev s))) 
exception LexHackingError 
fun look ((j,x)::r, i) = if i = j then x else look(r, i) 
  | look ([], i) = raise LexHackingError
fun g {fin=x, trans=i} = {fin=x, trans=look(s,i)} 
in Vector.fromList(map g 
[{fin = [], trans = 0},
{fin = [], trans = 1},
{fin = [], trans = 1},
{fin = [], trans = 3},
{fin = [], trans = 3},
{fin = [(N 66)], trans = 0},
{fin = [(N 17),(N 66)], trans = 6},
{fin = [(N 17)], trans = 6},
{fin = [(N 34),(N 66)], trans = 0},
{fin = [(N 42),(N 66)], trans = 0},
{fin = [(N 32),(N 66)], trans = 0},
{fin = [(N 60),(N 66)], trans = 0},
{fin = [(N 30),(N 66)], trans = 0},
{fin = [(N 56),(N 66)], trans = 13},
{fin = [(N 2)], trans = 0},
{fin = [(N 28),(N 66)], trans = 0},
{fin = [(N 20),(N 66)], trans = 16},
{fin = [(N 20)], trans = 16},
{fin = [(N 52),(N 66)], trans = 0},
{fin = [(N 38),(N 66)], trans = 0},
{fin = [(N 22),(N 66)], trans = 0},
{fin = [(N 36),(N 66)], trans = 0},
{fin = [(N 48),(N 66)], trans = 0},
{fin = [(N 14),(N 66)], trans = 23},
{fin = [(N 14)], trans = 23},
{fin = [(N 11),(N 14),(N 66)], trans = 23},
{fin = [(N 9),(N 14),(N 66)], trans = 23},
{fin = [(N 54),(N 66)], trans = 0},
{fin = [(N 44),(N 66)], trans = 0},
{fin = [(N 46),(N 66)], trans = 0},
{fin = [(N 40),(N 66)], trans = 0},
{fin = [(N 26),(N 66)], trans = 0},
{fin = [(N 24),(N 66)], trans = 32},
{fin = [(N 73)], trans = 0},
{fin = [(N 58),(N 66)], trans = 0},
{fin = [(N 64),(N 66)], trans = 0},
{fin = [(N 62),(N 66)], trans = 0},
{fin = [(N 66)], trans = 37},
{fin = [], trans = 37},
{fin = [(N 70)], trans = 37},
{fin = [(N 50),(N 66)], trans = 0},
{fin = [(N 7),(N 66)], trans = 41},
{fin = [(N 7)], trans = 41},
{fin = [(N 4)], trans = 0},
{fin = [(N 80)], trans = 0},
{fin = [(N 80)], trans = 45},
{fin = [(N 78)], trans = 0},
{fin = [(N 75)], trans = 0}])
end
structure StartStates =
	struct
	datatype yystartstate = STARTSTATE of int

(* start state definitions *)

val COMM = STARTSTATE 3;
val INITIAL = STARTSTATE 1;

end
type result = UserDeclarations.lexresult
	exception LexerError (* raised if illegal leaf action tried *)
end

fun makeLexer yyinput =
let	val yygone0=1
	val yyb = ref "\n" 		(* buffer *)
	val yybl = ref 1		(*buffer length *)
	val yybufpos = ref 1		(* location of next character to use *)
	val yygone = ref yygone0	(* position in file of beginning of buffer *)
	val yydone = ref false		(* eof found yet? *)
	val yybegin = ref 1		(*Current 'start state' for lexer *)

	val YYBEGIN = fn (Internal.StartStates.STARTSTATE x) =>
		 yybegin := x

fun lex (yyarg as (lineNo:int ref,pCount:int ref)) =
let fun continue() : Internal.result = 
  let fun scan (s,AcceptingLeaves : Internal.yyfinstate list list,l,i0) =
	let fun action (i,nil) = raise LexError
	| action (i,nil::l) = action (i-1,l)
	| action (i,(node::acts)::l) =
		case node of
		    Internal.N yyk => 
			(let val yytext = substring(!yyb,i0,i-i0)
			     val yypos = i0+ !yygone
			open UserDeclarations Internal.StartStates
 in (yybufpos := i; case yyk of 

			(* Application actions *)

  11 => (Tokens.ONE(!lineNo,!lineNo))
| 14 => (Tokens.NUM (cvstringtoint yytext, !lineNo, !lineNo))
| 17 => (case find yytext of SOME v => v(yytext,!lineNo,!lineNo)
			       | _ => Tokens.ACT(yytext,!lineNo,!lineNo))
| 2 => (Lib.inc lineNo; continue())
| 20 => (case find yytext of SOME v => v(yytext,!lineNo,!lineNo)
			       | _ => Tokens.ID(yytext,!lineNo,!lineNo))
| 22 => (Tokens.EQUALS(!lineNo,!lineNo))
| 24 => (Lib.inc pCount; Tokens.LPAR(!lineNo,!lineNo))
| 26 => (Lib.dec pCount; Tokens.RPAR(!lineNo,!lineNo))
| 28 => (Tokens.LBRACK(!lineNo,!lineNo))
| 30 => (Tokens.RBRACK(!lineNo,!lineNo))
| 32 => (Tokens.LBRACE(!lineNo,!lineNo))
| 34 => (Tokens.RBRACE(!lineNo,!lineNo))
| 36 => (Tokens.LESSTHAN(!lineNo,!lineNo))
| 38 => (Tokens.GREATERTHAN(!lineNo,!lineNo))
| 4 => (Lib.inc lineNo; if !pCount > 0 then continue()
			       else Tokens.EOL(!lineNo,!lineNo))
| 40 => (Tokens.PLUS(!lineNo,!lineNo))
| 42 => (Tokens.PAR(!lineNo,!lineNo))
| 44 => (Tokens.DOT(!lineNo,!lineNo))
| 46 => (Tokens.COMMA(!lineNo,!lineNo))
| 48 => (Tokens.SEMICOLON(!lineNo,!lineNo))
| 50 => (Tokens.BANG(!lineNo,!lineNo))
| 52 => (Tokens.QUERY(!lineNo,!lineNo))
| 54 => (Tokens.SLASH(!lineNo,!lineNo))
| 56 => (Tokens.BACKSLASH(!lineNo,!lineNo))
| 58 => (Tokens.QUOTE(!lineNo,!lineNo))
| 60 => (Tokens.HAT(!lineNo,!lineNo))
| 62 => (Tokens.SHARP(!lineNo,!lineNo))
| 64 => (Tokens.AMPERSAND(!lineNo,!lineNo))
| 66 => (error ("ignoring bad character "^yytext,!lineNo,!lineNo);
	             continue())
| 7 => (continue())
| 70 => (Tokens.STRING(substring(yytext,1,(size yytext)-2),!lineNo,!lineNo))
| 73 => (YYBEGIN COMM; continue())
| 75 => (Lib.inc lineNo; continue())
| 78 => (YYBEGIN INITIAL; continue())
| 80 => (continue())
| 9 => (Tokens.NIL(!lineNo,!lineNo))
| _ => raise Internal.LexerError

		) end )

	val {fin,trans} = Vector.sub(Internal.tab, s)
	val NewAcceptingLeaves = fin::AcceptingLeaves
	in if l = !yybl then
	     if trans = #trans(Vector.sub(Internal.tab,0))
	       then action(l,NewAcceptingLeaves
) else	    let val newchars= if !yydone then "" else yyinput 1024
	    in if (size newchars)=0
		  then (yydone := true;
		        if (l=i0) then UserDeclarations.eof yyarg
		                  else action(l,NewAcceptingLeaves))
		  else (if i0=l then yyb := newchars
		     else yyb := substring(!yyb,i0,l-i0)^newchars;
		     yygone := !yygone+i0;
		     yybl := size (!yyb);
		     scan (s,AcceptingLeaves,l-i0,0))
	    end
	  else let val NewChar = Char.ord(String.sub(!yyb,l))
		val NewState = if NewChar<128 then Char.ord(String.sub(trans,NewChar)) else Char.ord(String.sub(trans,128))
		in if NewState=0 then action(l,NewAcceptingLeaves)
		else scan(NewState,NewAcceptingLeaves,l+1,i0)
	end
	end
(*
	val start= if substring(!yyb,!yybufpos-1,1)="\n"
then !yybegin+1 else !yybegin
*)
	in scan(!yybegin (* start *),nil,!yybufpos,!yybufpos)
    end
in continue end
  in lex
  end
end

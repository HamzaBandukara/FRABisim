(* Ported to NJ/SML 110 by Bjorn Victor *)
structure Lib =
struct

(* Old stuff for handling user interrupts in SML/NJ (added by John Reppy) *)
(*    exception Interrupt *)  (* not present in SML/NJ 0.59-0.65 *)
(*    fun capturetopcont () = *)
(*        Unsafe.topLevelCont := *)
(*        SMLofNJ.Cont.callcc (fn k => *)
(* 			    (SMLofNJ.Cont.callcc (fn k' => *)
(* 						  (SMLofNJ.Cont.throw k k')); *)
(* 				raise Interrupt)) *)
(* end of old interrupt handling *)
(* This is from CWB 7.1 *)
   (* I don't pretend to understand this: I got it from Steven Bradley, who *)
   (* says he got it from MLyacc, he thinks. *)

   exception Interrupt;
   fun handleInterrupt (operation : unit -> 'a) =
       let exception Done of 'a
	   val old'handler = Signals.inqHandler(Signals.sigINT)
	   fun reset'handler () =
	       Signals.setHandler(Signals.sigINT, old'handler)
       in (SMLofNJ.Cont.callcc
	   (fn k (* a unit cont *) =>
	    (Signals.setHandler(Signals.sigINT, Signals.HANDLER(fn _ => k));
	     raise Done (operation ())) (* NOT returning unit *));
	   raise Interrupt)
	   handle (Done v) => (reset'handler (); v)
		| exn  => (reset'handler (); raise exn)
       end
   (* end of what I don't understand (ha!) *)
(* End of CWB 7.1 stuff *)


   fun timediff (a,b) =
       if Time.<(a,b) then Time.-(b,a) else Time.-(a,b)

   fun xorb(x,y) = Word.toInt(Word.xorb(Word.fromInt(x),Word.fromInt(y)))
   and andb(x,y) = Word.toInt(Word.andb(Word.fromInt(x),Word.fromInt(y)))
   and lshift(n,bits) =
       Word.toInt(Word.<<(Word.fromInt(n),Word.fromInt(bits)))
   and rshift(n,bits) =
       Word.toInt(Word.>>(Word.fromInt(n),Word.fromInt(bits)))

   exception AtoI
   fun atoi a =
       case Int.fromString a of
	   SOME(i) => i
	 | NONE => raise AtoI

   fun inc x = x := !x+1
   and dec x = x := !x-1
   and min (x,y) = if x < y then x else y

   fun fst (x,_) = x
   fun snd (_,x) = x

   val mkstrint  :  int -> string = Int.toString
   val mkstrbool : bool -> string = Bool.toString

(* needed to flush output to stdOut *)
   fun print (str,s) = (TextIO.output(str,s); TextIO.flushOut str)
   fun msg s = print(TextIO.stdOut,s)

   type 'a array = 'a Array.array
   val array = Array.array
   val Sub = Array.sub
   val update = Array.update

   exception Hd = List.Empty;
   exception Tl = List.Empty;
   exception disaster of string

   val hd = hd
   val tl = tl
   val length : 'a list -> int = length
   val nth = List.nth
   val nthtail = List.drop

   fun isnil [] = true
     | isnil (h::t) = false

   fun forall p l = let fun fall [] = true
                          | fall (h::t) = (p h) andalso (fall t)
                     in fall l
                    end

   fun exists p l = let fun ex [] = false
                          | ex (h::t) = (p h) orelse (ex t)
                     in ex l
                    end

   fun member eq (a,l) = exists (fn x => eq(x,a)) l

   fun rm eq (a,l) =
       let fun rma [] = []
             | rma (h::t) = if eq(h,a) then rma t else h::(rma t)
        in rma l
       end

   val map = map

   val app = app
   fun fold f l i = List.foldr f i l
   val foldr = fold
   fun foldl f l i = List.foldl f i l
   fun fold2 f L1 L2 x =
       let fun f2 [] [] x = x
	     | f2 (h1::t1) (h2::t2) x =
	       f (h1,h2,f2 t1 t2 x)
       in f2 L1 L2 x
       end

   fun flatten [] = []
     | flatten (h::t) = h@(flatten t)

   fun filter p =
       let fun filt [] = []
             | filt (h::t) = let val ftail = filt t
                              in if p h then h::ftail else ftail
                             end
        in filt
       end

   fun eq elt_eq =
       let fun equal ([],[]) = true
             | equal (a::s,b::t) = elt_eq(a,b) andalso equal(s,t)
             | equal _ = false
        in equal
       end

   fun le elt_le =
       let fun leq ([],_)        = true
             | leq (_,[])        = false
             | leq (h::t,h'::t') = elt_le(h,h') andalso
                                   (not (elt_le(h',h)) orelse leq(t,t'))
        in leq
       end

   fun del_dups eq =
       let fun dd m [] = m
             | dd m (h::t) = if member eq (h,m) then dd m t else dd (m@[h]) t
        in dd []
       end

   fun multiply prod l1 l2 =
       let fun mult [] l = []
             | mult (h::t) l =
               let fun m [] = []
                     | m (h'::t') = prod(h,h') :: (m t')
                in (m l)@(mult t l)
               end
        in mult l1 l2
       end

   fun mkstr mkstrelt sep []     = ""
     | mkstr mkstrelt sep [a]    = mkstrelt a
     | mkstr mkstrelt sep (h::t) = (mkstrelt h)^sep^(mkstr mkstrelt sep t)

   val ran = ref 123
   fun random ub = (ran := (1005 * !ran + 7473) mod 8192;
                    (!ran) div (8192 div ub + 1))

(* get_line ignores leading and trailing blanks,   *)
(* and allows for the continuation character "\".  *)

   fun get_line infile =
       let fun strip (#" "::t) = strip t
             | strip (#"\n"::t) = strip t
             | strip l = l
	   val line = case TextIO.inputLine infile of
			  SOME x  => x
			| NONE => ""	       
           val revline = strip(rev(strip(explode(line))))
        in if not(isnil revline) andalso hd revline = #"\\" then
              (implode(rev(strip(tl revline))))^" "^(get_line infile)
           else implode(rev revline)
       end

   (* From GNU Emacs: *)
   (* Apply ELT to each element of LIST, *)
   (* concatenating the results as strings, sticking in SEP between. *)
   (* Thus (mapconcat makestring [1,2,3] "+") => "1+2+3" *)
   fun mapconcat elt [] sep = ""
     | mapconcat elt [h] sep = elt h
     | mapconcat elt (h::t) sep = (elt h) ^ sep ^ (mapconcat elt t sep)


   (* From sortedlist.str, modulo duplicate removal *)
   fun sort le =
       let fun sr []  = []
             | sr [a] = [a]
             | sr (h::t) =
               let fun part [] pivot = ([],[],[])
                     | part (h::t) pivot =
                       let val (A,B,C) = part t pivot
                        in if le(h,pivot) then
                              if le(pivot,h) then (A,h::B,C) else (h::A,B,C)
                           else (A,B,h::C)
                       end
                   val (A,B,C) = part t h
	       in
		   (sr A)@(h::B)@(sr C)
               end
       in sr
       end

   fun mapcan f [] = []
     | mapcan f (h::t) = (f h)@(mapcan f t)

   fun mapunion eq f [] = []
     | mapunion eq f (h::t) =
       let val v = mapunion eq f t
	   val e = f h
	   fun umapp r [] = r
	     | umapp r (h::t) = if member eq (h,r)
				    then umapp r t
				else umapp (h::r) t
       in
	   umapp v e
       end

   fun max elt_le (h::t) =
       let fun mx (x,[]) = x
	     | mx (x,[h]) = if elt_le(x,h) then h else x
	     | mx (x,h::t) = mx(if elt_le(x,h) then h else x,t)
       in
	   mx (h,t)
       end

(*
   fun map2 _ [] _ = []
     | map2 _ _ [] = []
     | map2 f (h1::t1) (h2::t2) = (f(h1,h2))::(map2 f t1 t2)
*)

  (* debugging code *)
  val dbglvl = ref 0
  val dbglen = ref (80*4)		(* four lines? *)
  fun dprint(direction,str) =
      let fun indent(st,i) =
	  let fun mkp 0 = []
		| mkp i = #" "::(mkp (i-1))
	      val pfx = mkp i
	      fun ind n [] = []
		| ind 0 l = [#".",#".",#".",#"\n"]@(nextnewline l)
		| ind n [#"\n"] = [#"\n"]	(* always end with newline *)
		| ind n [c] = [c,#"\n"]
		| ind n (c::r) =
		  if c = #"\n"
		      then c::pfx@(ind (!dbglen) r)
		  else c::(ind (n-1) r)
	      and nextnewline [] = []
		| nextnewline (#"\n"::r) =
		  ind (!dbglen) r
		| nextnewline (c::r) = nextnewline r
	  in implode(ind (!dbglen) (explode str))
	  end
	  val _ = if direction > 0 then inc dbglvl else ()
      in
	  msg (* print *)
	  ((mkstrint (!dbglvl))^
	   (case direction of
		~1 => "<"
	      | 0  => "-"
	      | 1  => ">")^" "^
		(indent(str,3)));
	  if direction < 0 then dec dbglvl else ()
      end

end;

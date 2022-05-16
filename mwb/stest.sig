(* This is just for parsing, really *)
signature STEST =
    sig
	structure N: SNAME

	type test

	val mkstr   : test -> string
	val eq      : test * test -> bool

	val classes : test -> N.name list list
	    
	val True    : test
	val match   : N.name * N.name -> test
	val join    : test * test -> test
	val sigma   : test -> (N.name * N.name) list

    end

(* Equivalence relation - based on the test structure by Faron *)
signature EQUIV =
    sig
	structure N: NAME

	type equiv

	(* Constructors *)
	val EmptyE    : equiv
	val equate   : N.name * N.name -> equiv
	val join    : equiv * equiv -> equiv

	val inc : equiv -> equiv

	val is_empty : equiv -> bool
	val hashval : equiv -> int

	val representative : equiv * N.name -> N.name
	(* removes mention of a name *)
	val minus : equiv * N.name -> equiv
	val restrict_to : equiv * N.name list -> equiv
	(* remove eqrel e' from e *)
	val remove : equiv * equiv -> equiv
	(* Does one equiv cover another? *)
	val implies : equiv * equiv -> bool
	(* And please give me a substitution agreeing with this *)
	val sigma   : equiv -> (N.name * N.name) list

	(* substitute [a/b,c/d,...] in this equivalence *)
	val substitute : equiv * (N.name * N.name) list -> equiv

	(* Are two equivalences the same? *)
	val eq      : equiv * equiv -> bool
	(* What names are in it *)
	val names : equiv -> N.name list
	val domain : equiv -> N.name list
	(* What names are free, at a certain binding level? *)
	val free_names: equiv * int -> N.name list

	val beta_reduce : equiv -> (N.name list * int) -> equiv

	(* for printing *)
	val mkstr   : equiv -> string
	val makstr  : equiv * (string list) -> string

    end

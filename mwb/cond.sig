signature COND =
    sig
	structure N: NAME
	structure E: EQUIV

	type cond

	val True    : cond
	val False   : cond
	val is_true : cond -> bool
	val is_false: cond -> bool
	val match   : N.name * N.name -> cond
	val mismatch: N.name * N.name -> cond
	val equiv   : cond -> E.equiv
	val mk_equiv: E.equiv -> cond

	val inc : cond -> cond

	val join    : cond * cond -> cond
	(* ONLY use this in second arg of implies!! *)
	val disjunction : cond list -> cond

	val implies : cond * cond -> bool	(* M\rhd N *)
	val sigma   : cond -> (N.name * N.name) list

	(* C\upharpoonright nl *)
	val restrict_to : cond * N.name list -> cond

	val dminus  : cond * N.name -> cond
(* 	val eminus  : cond * E.equiv -> cond    *)

	val substitute : cond * (N.name * N.name) list -> cond

	val eq      : cond * cond -> bool
	val ceq     : cond -> cond * cond -> bool
	val names : cond -> N.name list
	val domain : cond -> N.name list
	val free_names: cond * int -> N.name list

	val mkstr   : cond -> string
	val makstr  : cond * (string list) -> string

(*	val substitute : N.name * N.name * cond -> cond *)

	val beta_reduce : cond -> (N.name list * int) -> cond

	val negate : cond -> cond

    end

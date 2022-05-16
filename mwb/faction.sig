signature FACTION =
sig
    structure N : NAME
    structure F : EQUIV			(* fusions *)

    type action

    val hashval : action -> int

    (* tests and constructors *)
    val is_fusion : action -> bool
    val is_one : action -> bool		(* shorthand *)
    val is_input : action -> bool
    val is_output : action -> bool
    val mk_fusion : N.name list * N.name list -> action	(* ~x=~y *)
    val mk_one : unit -> action		(* shorthand *)
    val mk_input : N.name -> action
    val mk_output : N.name -> action

    val subject : action -> N.name
    val fusion_repr : action * N.name -> N.name
    val fusion_minus : action * N.name -> action
    val fusion_eq_under : action * action * F.equiv -> bool
    val eeq : F.equiv -> action * action -> bool
    val fusion_equiv : action -> F.equiv (* equivalence of a fusion action *)
    val mk_fusion_equiv : F.equiv -> action (* reverse *)

    (* Names free at a certain binding level *)
    val free_names : action * int -> N.name list
    (* Names *)
    val names : action -> N.name list

    val mkstr : action -> string
    val makstr : action * (string list) -> string
    val eq : action * action -> bool

    val beta_reduce : action -> (N.name list * int) -> action
end

functor StringPropVar(structure Agt: SAGENT):SPROPVAR =
struct

  structure A = Agt

  datatype propvar = mk_propvar of string

  fun eq (mk_propvar n) (mk_propvar m) = n=m

  fun mkstr (mk_propvar n) = n

(*   fun next l =                                        *)
(*         mk_propvar((max (fn x => fn y => x<=y)        *)
(*              (map (fn (mk_propvar n) => n) l) 0) + 1) *)

end; (* PropVar *)


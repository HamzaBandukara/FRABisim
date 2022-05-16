signature SPROPVAR =
sig

  structure A: SAGENT

  type propvar

  val eq: propvar -> propvar -> bool
  val mk_propvar: string -> propvar
  val mkstr : propvar -> string
(*   val next: propvar list -> propvar *)

end

signature PROPVAR =
sig

  (*structure A: McAGENT
*)
  type propvar

  val mkstr : propvar -> string

  val eq: propvar -> propvar -> bool
  val mk_propvar: int -> propvar
  val next: propvar list -> propvar

end

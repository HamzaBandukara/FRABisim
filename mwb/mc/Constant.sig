signature CONSTANT =
sig

  type constant

  val mkstr : constant -> string

  val eq: constant -> constant -> bool
  val init: constant
  val next: constant -> constant

  val l_eq : constant -> constant -> bool

  val g_eq : constant -> constant -> bool

end

signature SoTEST =
sig
    structure N: SoNAME

    type test

    val mkstr   : test -> string
    val eq      : test * test -> bool

    val True    : test
    val match   : N.name * N.name -> test
    val mismatch: N.name * N.name -> test
    val join    : test * test -> test
(*    val sigma   : test -> (N.name * N.name) list *)

    val names : test -> N.name list
    val substitute : N.name * N.name * test -> test

end

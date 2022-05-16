signature SoACTION =
sig
    structure N : SoNAME

    type action

    val mkstr : action -> string
    val eq : action * action -> bool

    val mk_input : N.name -> action
    val mk_output : N.name -> action
    val mk_tau : unit -> action

    val substitute : N.name * N.name * action -> action

    val is_tau : action -> bool
    val is_input : action -> bool
    val is_output : action -> bool
    val name : action -> N.name
end

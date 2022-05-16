signature SoNAME =
sig
    type name

    val mkname : string -> name
    val mksortedname : string * string -> name
    val mkstr  : name -> string
    val eq     : name * name -> bool
    val le     : name * name -> bool

end

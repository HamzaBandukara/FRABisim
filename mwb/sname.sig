signature SNAME =
sig
    type name

    val mkname : string -> name
    val mkstr  : name -> string
    val eq     : name * name -> bool
    val le     : name * name -> bool

end

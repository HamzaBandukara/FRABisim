signature SFACTION =
sig
    structure N : SNAME

    datatype action = Fusion of (N.name * N.name) list
      		 | Input of N.name
		 | Output of N.name

    val free_names : action -> N.name list
    val mkstr : action -> string
    val eq : action * action -> bool

end

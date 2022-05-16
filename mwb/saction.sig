signature SACTION =
sig
    structure N : SNAME

    datatype action = Tau
      		 | Input of N.name
		 | Output of N.name

    val mkstr : action -> string
    val eq : action * action -> bool

end

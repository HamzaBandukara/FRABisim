signature SAGENT =
sig
   structure Act : SACTION


   datatype agent = Nil
     		  | Prefix of Act.action * agent
		  | Abs of Act.N.name * agent
		  | Conc of Act.N.name * agent
		  | Test of ((Act.N.name * Act.N.name) list * (Act.N.name * Act.N.name) list) * agent
                  | Sum of agent list
                  | Parallel of agent list
		  | Nu of Act.N.name * agent
                  | AgentRef of string
		  | Applic of agent * Act.N.name

   exception WrongArgs of string


   val mkstr : agent -> string
   val eq : agent * agent -> bool

end

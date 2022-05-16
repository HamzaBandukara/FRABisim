signature SFAGENT =
sig
   structure Act : SFACTION

   datatype agent = Nil
     		  | Prefix of Act.action * agent
		  | Conc of Act.N.name list * agent
		  | Match of ((Act.N.name * Act.N.name) list * (Act.N.name * Act.N.name) list) * agent
                  | Sum of agent list
                  | Parallel of agent list
		  | Scope of Act.N.name * agent
                  | AgentID of string
		  | Applic of agent * Act.N.name list

   exception WrongArgs of string

   val free_names : agent -> Act.N.name list
   val mkstr : agent -> string
   val eq : agent * agent -> bool

end

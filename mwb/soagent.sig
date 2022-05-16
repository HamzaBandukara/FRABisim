signature SoAGENT =
sig
   structure T : SoTEST
   structure Act : SoACTION


   type agent

   exception WrongArgs of string


   val mkstr : agent -> string
   val eq : agent * agent -> bool

   val is_nil : agent -> bool
   val is_prefix : agent -> bool
   val is_sum : agent -> bool
   val is_parallel : agent -> bool
   val is_restriction : agent -> bool
   val is_abstraction : agent -> bool
   val is_concretion : agent -> bool
   val is_match : agent -> bool
   val is_conditional : agent -> bool
   val is_application : agent -> bool
   val is_identifier : agent -> bool

   val mk_nil : unit -> agent
   val mk_prefix : Act.action * agent -> agent
   val mk_sum : agent list -> agent
   val mk_parallel : agent list -> agent
   val mk_restriction : T.N.name * agent -> agent
   val mk_abstraction : T.N.name * agent -> agent
   val mk_concretion : T.N.name * agent -> agent
   val mk_match : T.test * agent -> agent
   val mk_conditional : T.test * agent * agent -> agent
   val mk_application : agent * T.N.name -> agent
   val mk_identifier : string -> agent

   val prefix_agent : agent -> agent
   val prefix_act : agent -> Act.action
   val sum_summands : agent -> agent list
   val parallel_pars : agent -> agent list
   val restriction_name : agent -> T.N.name
   val restriction_agent : agent -> agent
   val abstraction_agent : agent -> agent
   val abstraction_name : agent -> T.N.name
   val concretion_agent : agent -> agent
   val concretion_name : agent -> T.N.name
   val match_test : agent -> T.test
   val match_positive : agent -> agent
   val conditional_positive : agent -> agent
   val conditional_negative : agent -> agent
   val application_arg : agent -> T.N.name
   val application_abstr : agent -> agent
   val identifier_name : agent -> string

   val instantiate : T.N.name * agent * T.N.name list -> (T.N.name * agent)
   val free_names : agent -> T.N.name list

end


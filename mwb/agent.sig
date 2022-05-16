signature AGENT =
sig
   structure T : TEST
   structure E : ENV
   structure Act : ACTION


   type agent

   exception SemanticsError of string * agent


   val mkstr : agent -> string
   val makstr : agent * (string list) -> string
   val eq : agent * agent -> bool
   val hashval : agent -> int
   val hashdepth : int ref
   val desctbls : unit -> unit
   val enabletbls : bool -> unit
   val cleartbls : unit -> unit

   val a_eq : agent * agent -> bool

   val mk_nil : unit -> agent
   val mk_prefix : Act.action * agent -> agent
   val mk_match : T.test * agent -> agent
   val mk_conditional : T.test * agent * agent -> agent
   val mk_sum : agent list -> agent
   val mk_parallel : agent list -> agent
   val mk_abstraction : Act.N.name * agent -> agent
   val mk_concretion : Act.N.name * agent -> agent
   val mk_restriction : Act.N.name * agent -> agent
   val mk_identifier : string -> agent
   val mk_application : agent * Act.N.name -> agent

   val is_nil : agent * agent E.env -> bool
   val is_prefix : agent * agent E.env -> bool
   val is_match : agent * agent E.env -> bool
   val is_conditional : agent * agent E.env -> bool
   val is_sum : agent * agent E.env -> bool
   val is_parallel : agent * agent E.env -> bool
   val is_restriction : agent * agent E.env -> bool
   val is_identifier : agent * agent E.env -> bool
   val is_application : agent * agent E.env -> bool
   val is_abstraction : agent * agent E.env -> bool (* arity >= 0 *)
   val is_concretion : agent * agent E.env -> bool (* arity <= 0 *)
   val is_process : agent * agent E.env -> bool	(* arity = 0 *)

   val prefix_act : agent * agent E.env -> Act.action
   val prefix_agent : agent * agent E.env -> agent
   val match_test : agent * agent E.env -> T.test
   val match_positive : agent * agent E.env -> agent
   val conditional_test : agent * agent E.env -> T.test
   val conditional_positive : agent * agent E.env -> agent
   val conditional_negative : agent * agent E.env -> agent
   val sum_summands : agent * agent E.env -> agent list
   val parallel_pars : agent * agent E.env -> agent list
   val application_arg : agent * agent E.env -> Act.N.name
   val application_args : agent * agent E.env -> Act.N.name list
   val application_abstr : agent * agent E.env -> agent
   val application_abstrs : agent * agent E.env -> agent (* innermost *)
   val restriction_agent : agent * agent E.env -> agent
   val restriction_right : agent * Act.N.name * agent E.env -> agent
   val abstraction_agent : agent * agent E.env -> agent
   val abstraction_right : agent * Act.N.name * agent E.env -> agent
   val concretion_name : agent * agent E.env -> Act.N.name
   val concretion_agent : agent * agent E.env -> agent

   val arity : agent * agent E.env -> int

   val pseudo_apply: agent * agent * agent E.env -> agent

   (* returns a list of the free names in an agent *)
   val free_names : agent -> T.N.name list
   val names : agent * agent E.env -> T.N.name list

   val apply : agent * (T.N.name list) * agent E.env -> agent
   val beta_reduce : agent -> (T.N.name list * int) -> agent
   val std_form : agent * agent E.env -> agent

   val substitute : (T.N.name * T.N.name) list * agent -> agent

   (* for debug? *)
   val abs_body : agent * int * agent E.env -> agent
   val abs_all : agent * agent E.env -> (int * agent)
   val conc_all : agent * agent E.env -> (int * T.N.name list * agent)

   val identifier_def : agent * agent E.env -> agent

   val ag1 : agent ref
   val ag2 : agent ref
   val e1 : agent E.env ref

end

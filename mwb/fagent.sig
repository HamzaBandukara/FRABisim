signature FAGENT =
sig
   structure T : COND
   structure E : ENV
   structure Act : FACTION


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

   val ceq : T.cond -> agent * agent -> bool

   val mk_nil : unit -> agent
   val mk_prefix : Act.action * agent -> agent
   val mk_match : T.cond * agent -> agent
   val mk_sum : agent list -> agent
   val mk_parallel : agent list -> agent
   val mk_concretion : Act.N.name list * agent -> agent
   val mk_scope : Act.N.name * agent -> agent
   val mk_identifier : string -> agent
   val mk_application : agent * Act.N.name list -> agent

   val is_nil : agent * (agent*int) E.env -> bool
   val is_prefix : agent * (agent*int) E.env -> bool
   val is_match : agent * (agent*int) E.env -> bool
   val is_sum : agent * (agent*int) E.env -> bool
   val is_parallel : agent * (agent*int) E.env -> bool
   val is_scope : agent * (agent*int) E.env -> bool
   val is_identifier : agent * (agent*int) E.env -> bool
   val is_application : agent * (agent*int) E.env -> bool
   val is_concretion : agent * (agent*int) E.env -> bool (* arity <> 0 *)
   val is_process : agent * (agent*int) E.env -> bool	(* arity = 0 *)

   val prefix_act : agent * (agent*int) E.env -> Act.action
   val prefix_agent : agent * (agent*int) E.env -> agent
   val match_cond : agent * (agent*int) E.env -> T.cond
   val match_clause : agent * (agent*int) E.env -> agent
   val sum_summands : agent * (agent*int) E.env -> agent list
   val parallel_pars : agent * (agent*int) E.env -> agent list
   val application_args : agent * (agent*int) E.env -> Act.N.name list
   val application_identifier : agent * (agent*int) E.env -> agent
   val scope_name : agent * (agent*int) E.env -> Act.N.name
   val scope_agent : agent * (agent*int) E.env -> agent
   val concretion_names : agent * (agent*int) E.env -> Act.N.name list
   val concretion_agent : agent * (agent*int) E.env -> agent

   val arity : agent * (agent*int) E.env -> int

   val pseudo_apply: agent * agent * (agent*int) E.env -> agent

   (* returns a list of the free names in an agent *)
   val free_names : agent -> Act.N.name list
   val names : agent * (agent*int) E.env -> Act.N.name list

   val apply : agent * (Act.N.name list) * (agent*int) E.env -> agent
   val beta_reduce : agent -> (Act.N.name list * int) -> agent
   val std_form : agent * (agent*int) E.env -> agent

   val substitute : (Act.N.name * Act.N.name) list * agent -> agent

   (* for debug? *)
(*    val abs_body : agent * int * (agent*int) E.env -> agent  *)
(*    val abs_all : agent * (agent*int) E.env -> (int * agent) *)
   val conc_all : agent * (agent*int) E.env -> (int * Act.N.name list * agent)

   val identifier_def : agent * (agent*int) E.env -> agent
   val identifier_arity : agent * (agent*int) E.env -> int

(*    val ag1 : agent ref            *)
(*    val ag2 : agent ref            *)
(*    val e1 : (agent*int) E.env ref *)

end

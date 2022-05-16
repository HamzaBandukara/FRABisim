signature McAGENT =
sig

  structure ACT : ACTION
  structure B : COND
  structure E : ENV

  type agent

  val ag1:agent ref
  val ag2:agent ref

  val mkstr : agent -> string
  (* constructors *)

  val mk_nil: agent

  val mk_sum: agent -> agent -> agent

  val mk_prefix: ACT.action -> agent -> agent

  (* Remember to extend mk_par to abstractions/concretions on *)
  (* either side                                              *)
  val mk_par: agent -> agent -> agent

  val mk_conditional: B.cond -> agent -> agent -> agent

  val mk_abstraction: ACT.N.name -> agent -> agent

  val mk_application: agent -> ACT.N.name -> agent

  val mk_restriction: ACT.N.name -> agent -> agent

  val mk_concretion: ACT.N.name -> agent -> agent

  val mk_bconcretion: ACT.N.name -> agent -> agent

  val mk_identifier: string -> agent

  (* equality *)  

  val eq: agent -> agent -> bool

  val a_eq : agent -> agent -> bool

  (* Testers *)

  val is_nil: agent -> agent E.env -> bool

  val is_sum: agent -> agent E.env -> bool

  val is_prefix: agent -> agent E.env -> bool

  val is_par: agent -> agent E.env -> bool

  val is_conditional: agent -> agent E.env -> bool

  val is_application: agent -> agent E.env -> bool

  val is_restriction: agent -> agent E.env -> bool

  val is_identifier: agent -> agent E.env -> bool

  val is_process: agent -> agent E.env -> bool

  val is_concretion: agent -> agent E.env -> bool

  val is_bconcretion: agent -> agent E.env -> bool

  val is_abstraction: agent -> agent E.env -> bool

  (* Selectors *)

  val free_names: agent -> ACT.N.name list

  val sum_left: agent -> agent E.env -> agent

  val sum_right: agent -> agent E.env -> agent

  val prefix_left: agent -> agent E.env -> ACT.action

  val prefix_right: agent -> agent E.env -> agent

  val par_left: agent -> agent E.env -> agent

  val par_right: agent -> agent E.env -> agent

  val get_boolean: agent -> agent E.env -> B.cond

  val cond_positive: agent -> agent E.env -> agent

  val cond_negative: agent -> agent E.env -> agent

  val appl_fun: agent -> agent E.env -> agent

  val appl_arg: agent -> agent E.env -> ACT.N.name

  val restriction_right: ACT.N.name -> agent -> agent E.env -> agent

  val restriction_agent: agent -> agent E.env -> agent

  val concretion_left: agent -> agent E.env -> ACT.N.name

  val concretion_right: agent -> agent E.env -> agent

  val bconcretion_right: ACT.N.name -> agent -> agent E.env -> agent

  val abstraction_right: ACT.N.name -> agent -> agent E.env -> agent

  val abstraction_agent: agent -> agent E.env -> agent

  (* manipulators *)

  val substitute: (ACT.N.name * ACT.N.name) list -> agent -> agent

  val pseudo_appl: agent -> agent -> agent E.env -> agent

  val identifier_def: agent -> agent E.env -> agent

  val apply : agent * (ACT.N.name list) * agent E.env -> agent
end

signature MODELCHECKER =
sig

  structure S : SEQUENT

  structure V : VISITEDTABLE

  structure AS : AGENTSUBSEM

  exception cannot_happen
  exception not_closed_formula

  val mccount : int ref

  val mc2 : V.visited_table -> S.C.NS.name_subst -> S.D.def_list -> S.A.agent -> S.F.formula -> S.A.agent S.A.E.env -> bool
  val model_checker: V.visited_table -> S.sequent -> AS.A.agent AS.A.E.env -> bool
  val naked_model_checker : S.A.agent -> S.F.formula -> AS.A.agent AS.A.E.env -> bool

end

signature EQUIVALENCECHECKER =
sig

  structure MC : MODELCHECKER

  val characteristic_formula:
        MC.S.C.cond -> MC.S.A.agent -> MC.S.A.agent MC.S.A.E.env -> MC.S.F.formula

  val equivalence_checker:
        MC.S.C.cond -> MC.S.A.agent -> MC.S.A.agent -> MC.S.A.agent MC.S.A.E.env -> bool

end

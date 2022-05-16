signature AGENTSUBSEM =
sig

  structure A : McAGENT

  structure NS : NAMESUBSTITUTION

  exception name_substitution_too_small

  exception open_agent_encountered

  val normal_form: A.agent -> NS.name_subst -> A.agent A.E.env -> A.agent

  val commitments: NS.name_subst -> A.agent -> A.agent A.E.env -> (A.ACT.action * A.agent) list

end

signature PROVER =	
sig
	structure N   :  NAME
	structure S   :	 SEQ 
	structure A   :  McAGENT
	structure NE  :  NAMEEQUATION
	structure F   :  PFORMULA
	structure ACT :  ACTION
        structure B   :  COND
        structure E   :  ENV
        structure AS  : AGENTSUBSEM
        structure NS  : NAMESUBSTITUTION
        structure CST : CONSTANT
    
val prove : S.Sequent * A.agent E.env * NS.name_subst -> bool

val mccount : int ref

val naked_prover : A.agent -> F.formula -> A.agent E.env -> bool
end

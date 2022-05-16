signature SET = sig
		    datatype SetC = Debug of int
		      | Threshold of int
		      | Hashdepth of int
		      | Rewrite of bool
		      | Remember of bool
		      | PrintActions of bool
		      | Help
		end
signature SHOW = sig
		     datatype ShowC = Debug
		       | Threshold
		       | Hashdepth
		       | Rewrite
		       | Remember
		       | PrintActions
		       | Version
		       | Tables
		       | Help
		       | All
		 end
signature HELP = sig
		     datatype HelpC = All
		       | Agent | Check | Clear | Dead
		       | Form | Env | Eq | Eqd | Input | Prove
		       | Set | Show | Step | Ztep | Size | Sort
		       | Traces | Trans | Verify | Wtrans
		       | Weq | Weqd | Help | Quit | Time
		       | FAgent | Feq | FTransitions | Fweq | FWTransitions
		       | NULL
		 end

signature COMMANDS =
sig
    structure A : SAGENT
    structure F : SFORMULA
    structure FA : SFAGENT
    structure SetC : SET
    structure ShowC : SHOW
    structure HelpC : HELP
     datatype Command = Agent of (string * A.agent)
      		     | Check of A.agent * F.formula
      		     | Prove of A.agent * F.formula
		     | Clear of string
		     | Dead of A.agent
      		     | Environment of string
		     | Eq of A.agent * A.agent
		     | EqD of A.agent * A.agent * (A.Act.N.name list)
                     | Formula of (string * F.formula)
		     | Input of string
		     | Set of SetC.SetC
		     | Show of ShowC.ShowC
		     | Sort of A.agent
		     | Step of A.agent
		     | Ztep of A.agent
		     | Size of A.agent
		     | Traces of A.agent
	             | FTransitions of FA.agent
	             | FWTransitions of FA.agent
	             | Transitions of A.agent
                     | Verify of (int * bool * A.agent * F.formula)
	             | Wtransitions of A.agent
		     | Weq of A.agent * A.agent
		     | WeqD of A.agent * A.agent * (A.Act.N.name list)
		     | Help of HelpC.HelpC
		     | Quit
		     | NULL
		     | Time of Command
		     | FAgent of (string * A.Act.N.name list * FA.agent)
		     | Feq of FA.agent * FA.agent
		     | Fweq of FA.agent * FA.agent
    datatype Parse =   ParseCMD of Command
      		     | ParseAGENT of A.agent
		     | ParseFORMULA of F.formula
end

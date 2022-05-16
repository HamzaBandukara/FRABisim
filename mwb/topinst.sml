structure Top =
    struct
	structure Constant = Constant();
	structure SL = SL()
	structure V = Var()
	structure E = Env(structure V=V;
			  structure SL = SL)
	structure H = HashTable();

	(* String names are used for parsing *)
	structure SN = StringName();
	structure N = deBruijnName();

	(* fusion *)
	structure EQU = Equiv(structure N=N; structure SL=SL)
	structure FCond = Cond(structure N=N; structure SL=SL; structure E=EQU)
	structure FAct = Faction(structure N=N; structure F=EQU);
	structure FA = FAgent(structure SL=SL;
			      structure H=H;
			      structure Eq=EQU;
			      structure T=FCond;
			      structure Act=FAct;
			      structure E=E;
			      structure V=V)
	structure Fsem = FusionSem(structure A=FA; structure H=H)
	structure SFAct = StringFAction(structure N=SN; structure SL=SL)
	structure SFA = StringFAgent(structure Act=SFAct; structure SL=SL)
	(* end fusion *)

	(* and string tests... *)
	structure ST = StringTest(structure N=SN;
				  structure SL = SL)
	structure T = Test(structure N=N;
			   structure SL=SL)
	(* and string actions... *)
	structure SAct = StringAction(structure N=SN);
	structure Act = Action(structure N=N)
	(* and string agents... *)
	structure SA = StringAgent(structure T=ST;
				   structure Act=SAct;
				   structure SL=SL)

(* 	structure D = Distinction(structure T = T;      *)
(* 				  structure SL = SL)    *)
	structure A = OAgent(structure SL = SL;
				 structure H = H;
				 structure T=EQU;
				 structure C=FCond;
				 structure Act=Act;
				 structure E=E;
				 structure V=V)
	structure O = OpenSem(structure B=A;
				    structure C=FCond;
				    structure H=H)

	structure SP = StringPropVar(structure Agt=SA)
	structure SF = StringFormula(structure Act=SAct;
				     structure PropVar = SP)

	(* Model Checking stuff *)
(* 	structure Bool = Boolean(structure T=T; *)
(* 				 structure N=N) *)
	structure Bool = FCond
	structure BrA = A
	structure McAgent = McAgent(structure AG=BrA)
	structure PV = PropVar(McAgent)
	structure F = Formula(structure PropVar=PV;
			      structure Constant=Constant;
			      structure Action=Act)
	structure NS = NameSubstitution(structure Name=N;
					structure Boolean=Bool)
	structure ASS = AgentSubSem(structure Agent=McAgent;
				    structure NameSubstitution = NS;
				    structure Boolean= Bool)
	structure Cond = Condition(structure NameSubstitution = NS;
				   structure Formula = F)
	structure DF = DefList(structure Formula = F)
	structure SQ = Sequent(structure Formula = F;
			       structure Condition = Cond;
			       structure DefList = DF;
			       structure Agent = McAgent)
	structure MC = ModelChecker(structure Sequent = SQ;
				    structure AgentSubSem = ASS)
(*	structure EQ = EquivalenceChecker(structure ModelChecker = MC) *)
	(* end Model Checking Stuff *)


(* NEW MODEL PROVER STRUCTURES !!!! /FB 971208 *)

	structure NE = Nameequation(structure Name=N)
        structure PF = PFormula(structure PropVar=PV;
			      structure Constant=Constant;
			      structure Action=Act)
	structure SEQ = SubSequent(structure Agent = McAgent;
			    structure Name=N; 
			structure Constant=Constant;
			structure Formula=PF;
			structure Agsubsem=ASS;
			structure Ns=NS;				
			structure Nameeq=NE;				
			structure Action=Act;
			structure Env=E)
 structure PROVER = Prover(	structure Sequent=SEQ;
				structure Agent=McAgent;
				structure Formula=PF;
				structure Nameequation=NE;	
				structure Bool=FCond;
				structure Name=N;
				structure Env=E;
				structure AgentSubSemantics=ASS;
				structure NameSubstitution=NS;
				structure Act=Act;			
				structure Constant=Constant
								)

	(* **** sort checking *)
	structure SoN = SortName()
	structure SoAct = SortAction(structure N=SoN)
	structure SoT = SortTest(structure N=SoN;
				 structure SL=SL)
	structure SoA = SortAgent(structure T=SoT;
				  structure Act=SoAct;
				  structure SL=SL)
	structure EqR = Eqrel(structure SL=SL)
	structure SS = SSort(structure Name=SoN;
			     structure Agent=SoA;
			     structure Env=E;
			     structure Slist=SL;
			     structure Eqrel=EqR)

	(* **** end sort checking *)


	structure Cmd = Commands(structure A=SA;
				 structure F=SF;
				 structure FA=SFA)


(* 	structure PILrVals =                                          *)
(* 	    PILrValsFun(structure Token = LrParser.Token              *)
(* 			structure Agent = SA                          *)
(* 			structure Commands = Cmd                      *)
(* 			structure Prop = SP                           *)
(* 			structure F = SF)                             *)
(*                                                                    *)
(* 	structure PILex =                                             *)
(* 	    PILexFun(structure Tokens = PILrVals.Tokens)              *)
(*                                                                    *)
(* 	structure PIParser =                                          *)
(* 	    JoinWithArg(structure ParserData = PILrVals.ParserData    *)
(* 		 structure Lex = PILex                                *)
(* 		 structure LrParser = LrParser)                       *)

	structure TT = TopCode(
                structure Constant=Constant
		structure SL=SL
		structure V=V
		structure E=E
		structure SN=SN
		structure N=N
		structure ST=ST
		structure T=T
		structure SAct=SAct
		structure Act=Act
		structure SA=SA
(* 		structure D=D    *)
		structure A=A
		structure H=H
		structure O=O
		structure SP=SP
		structure SF=SF
		structure McAgent=McAgent
		structure PV=PV
		structure F=F
                structure PF=PF			       
		structure NS=NS
		structure ASS=ASS
		structure Cond=Cond
		structure DF=DF
		structure SQ=SQ
		structure MC=MC
	(*	structure EQ=EQ *);
		structure NE=NE
		structure SEQ=SEQ
		structure PROVER=PROVER
		structure SoN=SoN
		structure SoAct=SoAct
		structure SoT=SoT
		structure SoA=SoA
		structure EqR=EqR
		structure SS=SS
		structure Cmd=Cmd
(* 		structure PILrVals = PILrVals    *)
(* 		structure PILex = PILex          *)
(* 		structure PIParser = PIParser    *)
		(* fusion *)
		structure EQU=EQU
		structure FCond = FCond
		structure FAct = FAct
		structure FA = FA
		structure Fsem = Fsem
		structure SFAct = SFAct
		structure SFA = SFA
		    );

	val toplevel = TT.toplevel
	fun toptest() =
	    TT.cmdloop (fn _ => case TextIO.inputLine TextIO.stdIn of SOME x => x | NONE => "") (E.empty,E.empty,E.empty,E.empty)
    end

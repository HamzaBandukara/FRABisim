functor Prover( structure Sequent: SEQ
		structure Agent : McAGENT
			sharing Sequent.A = Agent
		structure Formula : PFORMULA	
			sharing Sequent.F = Formula
		structure Nameequation : NAMEEQUATION
			sharing Sequent.NE = Nameequation	
		structure Bool : COND    
			sharing Agent.B = Bool
		structure Name : NAME
			sharing Sequent.N = Name
			sharing Formula.ACT.N = Name
			sharing Nameequation.N = Name
			sharing Agent.ACT.N = Name
			sharing Bool.N  = Name
		structure Env : ENV
			sharing Agent.E = Env
			sharing Sequent.E = Env    
		structure AgentSubSemantics : AGENTSUBSEM
			sharing AgentSubSemantics.A = Agent
			sharing AgentSubSemantics.NS.N = Name
		structure NameSubstitution : NAMESUBSTITUTION
			sharing NameSubstitution.N = Name
                        sharing AgentSubSemantics.NS = NameSubstitution
		structure Act : ACTION
			sharing Act.N = Name                      
			sharing Agent.ACT = Act
			sharing Formula.ACT = Act
			sharing Sequent.ACT = Act			
		structure Constant : CONSTANT
			sharing Formula.CST = Constant
			sharing Sequent.CST = Constant
				): PROVER =

struct

structure S = Sequent
structure F = Formula
structure A = Agent
structure N = Name
structure NE = Nameequation
structure E = Env
structure AS = AgentSubSemantics
structure NS = NameSubstitution
structure B = Bool
structure ACT = Act
structure CST = Constant

exception cannot_happen
exception not_closed_formula

val mccount = ref 0

fun namsubst(A,F)=
(Lib.fold (fn (n,ns)=>NS.add_distinct n ns) (Lib.del_dups F.ACT.N.eq ((A.free_names A)@(F.free_names F))) NS.init)
fun compact_commits([])= []
  | compact_commits(commitments_list) = Lib.del_dups (S.commit_eq) (commitments_list)


(*#############################################*)
(*#####  M A I N  C O D E  P R O V E R   ######*)
(*#############################################*)

fun prove( S.Seq(ne, agent, f, daltlist, FPlist, i, dSusplist, dKlist),e, ns) =
let 

 val _ = mccount := !mccount + 1
 val ag = AS.normal_form agent ns e
 val _ = if not (Flags.trace()) then () else print ("Testing sequent-- "^(A.mkstr ag)^":"^(F.mkstr f)^"\n")
 val altlist = Lib.del_dups (S.alt_eq) daltlist
 val Klist = Lib.del_dups (S.conj_eq) dKlist
 val Susplist = Lib.del_dups (S.Susp_eq) dSusplist
(* output opportunities for debugging only *)
(* val _ = print("alternatives #:"^Lib.mkstrint(List.length(altlist))^"\n") 
 val _ = print("conjuncts: #:"^Lib.mkstrint(List.length(Klist))^"\n")
 val _ = print("visited fixpoints: #"^Lib.mkstrint(List.length(FPlist))^"\n")
 val _ = print("Suspendeds: #"^Lib.mkstrint(List.length(Susplist))^"\n") *)
in 
(*_______CONDITIONAL AGENTS_____*)
if A.is_conditional ag e then
let
   (* only defined for 2-name conditions e g { [x=y]Agent1, Agent2 } *)	
   val cond = B.names(A.get_boolean ag e)
   val name1 = hd(cond)
   val name2 = hd(tl(cond))
  in
	(*###  COND-AG1-rule ####*)
   if NE.eq_implies(name1, name2, ne) then
     prove(S.Seq(ne, A.cond_positive ag e, f, altlist, 
		FPlist, i, Susplist, Klist),e, ns)
	else 
	(*#### COND-AG2-rule ####*)
	if NE.ineq_implies(name1, name2, ne) then
	prove(S.Seq(ne, A.cond_negative ag e, f, altlist, 
		FPlist, i, Susplist, Klist), e, ns) 
	else
	let (*#### COND-AG3-rule ####*)
	  val ne1=NE.addEq(name1, name2, ne)
	  val ne2 = NE.addIneq(name1, name2, ne)	
	  val newSeq =S.mk_Sequent(ne2, A.cond_negative ag e, f, altlist, 
		FPlist, i, Susplist,[])
	   val newKlist = newSeq::Klist
	in
	    prove(S.Seq(ne1, A.cond_positive ag e, f, altlist, FPlist,
		i, Susplist, newKlist), e, ns) 
	end
end	
else
(* ____________AXIOMS & TERMINATION___________*)


 (*#####  S-TERM-rule   #####*)
if F.is_true(f) andalso (not(S.exists_conjunctive(Klist))) then true 
 else



 (* #####  F-TERM-rule   #####*)
if F.is_false(f) andalso (not(S.exists_alternative(altlist))) then false
 else



 (* ##### F-LIT-rule   #####*)
if F.is_false(f) andalso S.exists_alternative(altlist) then 
let
	val nextAlt = S.get_next_Alt(altlist)
	val nextag = S.nextAgent(nextAlt)
	val nextform = S.nextFormula(nextAlt)
	val nextalt = tl(nextAlt)
	val nextFP = S.nextFPlist(nextAlt)
	val nextSusp = S.nextSusplist(nextAlt)
        val _ = if not (Flags.trace()) then () else print ("Testing alternative-- "^(A.mkstr nextag)^":"^(F.mkstr nextform)^"\n")
in
  prove(S.Seq(ne, nextag, nextform, tl(altlist), nextFP, i, nextSusp, Klist), e, ns) 
end
else



 (*##### T-LIT-rule   #####*)
if F.is_true(f) andalso S.exists_conjunctive(Klist)
 then
let
  val _ = if not (Flags.trace()) then () else print("Testing Conjunct: ")
in
prove(S.Seq(S.newNeq(Klist), S.newAgent(Klist),
S.newFormula(Klist), S.newAlt(Klist), S.newFPlist(Klist),
S.newIndex(Klist), S.newSusplist(Klist), tl(Klist)), e, ns) 
end
else


(* _____________EQUALITY RULES________________*)

 (* ##### EQ1-rule  #####*)
if F.is_eq(f) andalso 
   N.is_name(F.eq_left(f)) andalso
   N.is_name(F.eq_right(f)) andalso 
   NE.ineq_implies(F.eq_left(f),F.eq_right(f), ne) then
let
 val new_f = F.mk_false
in
 prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, Susplist, Klist), e, ns) 
end
 else

 (* ###### EQ2-rule ##### *)
if F.is_eq(f) andalso 
   N.is_name(F.eq_left(f)) andalso
   N.is_name(F.eq_right(f)) andalso
((NE.eq_implies(F.eq_left(f), F.eq_right(f), ne)) 
	orelse N.eq(F.eq_left(f),F.eq_right(f)) ) then
let
 val  new_f = F.mk_true
in
 prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, Susplist, Klist), e, ns) 
end
else

 (* ##### EQ3a-rule  ##### *)
if F.is_eq(f) andalso 
   N.is_name(F.eq_left(f)) andalso 
   N.is_variable(F.eq_right(f)) andalso
   N.index_of(F.eq_left(f)) < N.index_of(F.eq_right(f)) then
 let
  val newName = F.eq_left(f)
  val oldVar  = F.eq_right(f)
  val newAltlist = S.replaceVarAlt(oldVar, newName, altlist)
  val newSusplist = S.replaceVarSus(oldVar, newName, Susplist)
  val newFPlist = S.replaceVarVF(oldVar, newName, FPlist)
  val newKlist = S.replaceVarSEQ(oldVar, newName, Klist)
  val new2Klist = S.get_activated_sequents(newName, newSusplist)@newKlist
  val new2Susplist = S.remove_activated_sequents(newName, newSusplist)
  val new_f = F.mk_true
  val _ = if not (Flags.trace()) then () else print("Unifying variable"^N.mkstr(oldVar)^" with name "^N.mkstr(newName)^" in structure \n")
 in
 prove(S.Seq(ne, ag, new_f, newAltlist, newFPlist, i, new2Susplist,
	new2Klist), e, ns)  
end
else

 (* ##### EQ3b-rule  ##### *)
if F.is_eq(f) andalso 
   N.is_variable(F.eq_left(f)) andalso 
   N.is_name(F.eq_right(f)) andalso
   N.index_of(F.eq_left(f)) > N.index_of(F.eq_right(f)) then
 let
  val newName = F.eq_right(f)
  val oldVar  = F.eq_left(f)
  val newAltlist = S.replaceVarAlt(oldVar, newName, altlist)
  val newSusplist = S.replaceVarSus(oldVar, newName, Susplist)
  val newFPlist = S.replaceVarVF(oldVar, newName, FPlist)
  val newKlist = S.replaceVarSEQ(oldVar, newName, Klist)
  val new2Klist = S.get_activated_sequents(newName, newSusplist)@newKlist
  val new2Susplist = S.remove_activated_sequents(newName, newSusplist)
  val new_f = F.mk_true
  val _ = if not (Flags.trace()) then () else print("Unifying variable"^N.mkstr(oldVar)^" with name "^N.mkstr(newName)^" in structure \n")
 in
 prove(S.Seq(ne, ag, new_f, newAltlist, newFPlist, i, new2Susplist,
	new2Klist), e, ns)  
end
else


(* ##### EQ4-rule ##### *)
if F.is_eq(f) andalso 
   N.is_name(F.eq_left(f)) andalso 
   N.is_name(F.eq_right(f)) andalso 
   not(NE.eq_implies(F.eq_left(f), F.eq_right(f), ne)) then
 let
   val newNE = NE.addIneq(F.eq_left(f), F.eq_right(f), ne)
   val newAlt = S.unbar(altlist)
   val new_f = F.mk_false 
in
  prove(S.Seq(newNE, ag, new_f, newAlt, FPlist, i, Susplist, Klist), e, ns) 
end
else



(* ##### INEQ1-rule #####*)
if F.is_neq(f) andalso
  N.is_name(F.eq_left(f)) andalso 
   N.is_name(F.eq_right(f)) andalso 
   not(NE.ineq_implies(F.eq_left(f), F.eq_right(f), ne)) then
 let
   val newNE = NE.addEq(F.eq_left(f), F.eq_right(f), ne)
   val newAlt = S.unbar(altlist)
   val new_f = F.mk_false
in
  prove(S.Seq(newNE, ag, new_f, newAlt, FPlist, i, Susplist, Klist), e, ns) 
end
else


(* ##### INEQ2a-rule #### *)
if F.is_neq(f) andalso N.is_variable(F.eq_left(f)) then
let
   val newSusp = S.addSuspSeq(Susplist, F.eq_left(f), ne, ag, f,
			altlist, FPlist, i)
   val new_f = F.mk_true
   val _ = if not (Flags.trace()) then () else print("Suspending...\n")
in
  prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, newSusp, Klist), e, ns) 
end
else

(* ##### INEQ2b-rule #### *)
if F.is_neq(f) andalso N.is_variable(F.eq_right(f)) then
let
   val newSusp = S.addSuspSeq(Susplist, F.eq_right(f), ne, ag, f,
			altlist, FPlist, i)
   val new_f = F.mk_true	
in
  prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, newSusp, Klist), e,ns) 
end
else

(*_____________LOGICAL CONNECTIVES_________*)

(* ##### OR-intro-rule  ##### *)
if F.is_or(f) then
let
   val disjunct1 = F.select_left(f)
   val disjunct2 = F.select_right(f)
   val newAlt = S.addAlt(altlist, ag, disjunct2, FPlist, Susplist)
	(* remove-duplicates i newAlt ? *)
in 
prove(S.Seq(ne, ag, disjunct1, newAlt, FPlist, i, Susplist, Klist), e,ns) 
end
else


(* ##### AND-intro-rule  #### *)
if F.is_and(f) then
let
   val conjunct = S.Seq(ne, ag, F.select_right(f), altlist, FPlist, i,
			Susplist, Klist) 
   val newKlist = conjunct::Klist
       
in
  prove(S.Seq(ne, ag, F.select_left(f), altlist, FPlist, i, Susplist, 
	newKlist), e,ns) 
end
else

(*________LOGICAL QUANTIFIERS________*)

(* ##### FORALL-intro-rule #### *)
if F.is_forall(f)  then 
  if not (A.is_concretion ag e)  then 
  let
    val j=i+1
    val names = S.names_in_sequent([S.Seq(ne, ag, f, altlist, FPlist, i,
		Susplist, [])])
    val newParameter = N.newNameNotin(names)
    val parameter = N.set_param(newParameter, j)
    val newag = A.apply(ag, [parameter], e) 
    val new_f = F.successor parameter f
    val new_ns = NS.restrict ns ((A.free_names ag)@(F.free_names f))
    val new2_ns = NS.add_distinct parameter new_ns 
 in
   prove(S.Seq(ne, newag, new_f, altlist, FPlist, j, Susplist, Klist), e, new2_ns) 
end
  else true 
else


(* ##### EXISTS- intro rule ##### *)
if F.is_exists(f)  andalso not (A.is_concretion ag e) then
let
   val names= S.names_in_sequent([S.Seq(ne, ag, f, altlist, FPlist, i,
		Susplist, Klist)])
   val newVariable = N.mkvariable(names)
   val newVar = N.set_param(newVariable,i)
   val newag = A.apply(ag, [newVar], e) 
   val new_f = F.successor newVar f
   val newAlt = S.addBar(altlist, ag, f, FPlist, Susplist)
   val new_ns = NS.add_distinct newVar ns
   
in
  prove(S.Seq(ne, newag, new_f, newAlt, FPlist, i, Susplist, Klist), e, ns) 
end
else


(*__________AGENT RULES_____________*)

(*##### SUM- rule ##### *)
if F.is_sigma(f) andalso not(A.is_abstraction ag e) andalso not (A.is_restriction ag e) then
let
   val concr_name = A.concretion_left ag e
   val newag = A.concretion_right ag e
   val new_f = F.successor concr_name f
   in
  prove(S.Seq(ne, newag, new_f, altlist, FPlist, i, Susplist, Klist), e, ns) 
end 
else


(* ###### NEW-rule ##### *)
if F.is_bsigma(f) andalso (A.is_bconcretion ag e) andalso not(A.is_process ag e)  then
let
   val j = i+1
   val names = S.names_in_sequent([S.Seq(ne, ag, f, altlist, FPlist,
		i, Susplist, Klist)])
   val newName = N.newNameNotin(names)
   val newag = A.bconcretion_right newName ag e 
   val new_f = F.successor newName f
   val new_ns = NS.add_distinct newName ns 
in  
  prove(S.Seq(ne, newag, new_f, altlist, FPlist, j, Susplist, Klist), e, new_ns) 
end
else


(*_____________MODAL RULES_______________*)
(* ##### DIAMOND1a -rule ##### *)
if (F.is_diamond_unbarred(f) andalso N.is_name(F.get_left(f)) andalso A.is_process ag e) then
let 
   val diamond_a = F.get_left(f)
   val new_f= F.select_right(f) 
   val commitments = compact_commits(AS.commitments ns ag e)
   val new_alt = S.add_unbarred_alt(diamond_a, commitments, new_f, 
			FPlist, Susplist) 
   val new2_f = F.mk_false
   val newAltlist = altlist@new_alt
   val _ = if not (Flags.trace()) then () else print ("Testing for diamond: action "^(N.pretty_name(F.get_left(f)))^", yielded" ^Lib.mkstrint( List.length(new_alt))^" alternatives\n")
in
  prove(S.Seq(ne, ag, new2_f, newAltlist, FPlist, i, Susplist, Klist), e,ns) 
end
else
(* ##### DIAMOND1b -rule ##### *)
if (F.is_diamond_barred(f)) andalso N.is_name(F.get_left(f)) andalso A.is_process ag e then
let 
   val diamond_a = F.get_left(f)
   val new_f= F.select_right(f) 
   val commitments = compact_commits(AS.commitments ns ag e)
   val new_alt = S.add_barred_alt(diamond_a, commitments, new_f, 
			FPlist, Susplist) 
   val new2_f = F.mk_false
   val newAltlist = altlist@new_alt
   val _ = if not (Flags.trace()) then () else print ("Testing for diamond: action "^(N.pretty_name(F.get_left(f)))^", yielded " ^Lib.mkstrint( List.length(new_alt))^" alternatives\n")
in
  prove(S.Seq(ne, ag, new2_f, newAltlist, FPlist, i, Susplist, Klist), e,ns) 
end
else
(* ##### DIAMOND2a-rule ##### *)
 if (F.is_diamond_barred(f)  andalso N.is_variable(F.get_left(f)) andalso A.is_process ag e)  then
let
   val dia_var = F.get_left(f)
   val next_f = F.select_right(f)
   val commitments = compact_commits(AS.commitments ns ag e)
   val new_alt = S.add_barred_alt_vars(dia_var, commitments, next_f, FPlist, Susplist)
   val new2f = F.mk_false
   val newAltlist = altlist@new_alt
   val _ = if not (Flags.trace()) then () else print ("diamond-variable: action "^(N.pretty_name(dia_var))^", yielded " ^Lib.mkstrint( List.length(new_alt))^"\n")
in
  unify_and_prove_one(dia_var, commitments, ne, f, newAltlist, FPlist, i, Susplist, Klist,e, ns)
end

else

(* ##### DIAMOND2b-rule ##### *)
 if F.is_diamond_unbarred(f) andalso N.is_variable(F.get_left(f)) andalso A.is_process ag e  then
let
   val dia_var = F.get_left(f)
   val next_f = F.select_right(f)
   val commitments = compact_commits(AS.commitments ns ag e)
   val new_alt = S.add_unbarred_alt_vars(dia_var, commitments, next_f, FPlist, Susplist)
   val new2f = F.mk_false
   val newAltlist = altlist@new_alt
 val _ = if not (Flags.trace()) then () else print ("diamond-variable: action "^(N.pretty_name(dia_var))^", yielded " ^Lib.mkstrint( List.length(new_alt))^"\n")
in
  unify_and_prove_one(dia_var, commitments,  ne, f, newAltlist, FPlist, i, Susplist, Klist,e, ns)
end

else

(* ##### DIAMOND3-rule ##### *)
if F.is_diamond_tau(f)  andalso A.is_process ag e then
let
   val new_f = F.select_right(f)  
   val all_commitments = compact_commits(AS.commitments ns ag e)
   val new_alt = S.add_tau_commit(all_commitments, new_f, 
			FPlist, Susplist) 
   val newAltlist = altlist@new_alt
  val new2_f = F.mk_false
val _ = if not (Flags.trace()) then () else print ("Testing for diamond: tau , yielded " ^Lib.mkstrint( List.length(new_alt))^"\n") 
in
  prove(S.Seq(ne, ag, new2_f, newAltlist, FPlist, i, Susplist, Klist), e, ns) 
end

else

(* ##### BOX1a-rule #### *)
if (F.is_box_unbarred(f)  andalso N.is_name(F.get_left(f))) then
   if (A.is_process ag e) then
   let
     val box_a = F.get_left(f)
     val new_f = F.select_right(f)
     val commitments = compact_commits(AS.commitments ns ag e)
     val newConjuncts = S.add_unbarred_Sequents(box_a, commitments, ne, new_f,
	altlist, FPlist, i, Susplist)
     val newKlist = Klist@newConjuncts
     val _ = if not (Flags.trace()) then () else print ("Testing for box action "^(N.pretty_name(box_a))^", yielded " ^Lib.mkstrint( List.length(newConjuncts))^" conjuncts\n")
     val new2_f = F.mk_true
   in
      prove(S.Seq(ne, ag, new2_f, altlist, FPlist, i, Susplist, newKlist), e, ns)  
   end
   else true
else

(* ##### BOX1b-rule #### *)
if F.is_box_barred(f)  andalso
	N.is_name(F.get_left(f)) then
   if  A.is_process ag e then
   let
     val box_a = F.get_left(f)
     val new_f = F.select_right(f)
     val commitments = compact_commits(AS.commitments ns ag e)
     val newConjuncts = S.add_barred_Sequents(box_a, commitments, ne, new_f,altlist, FPlist, i, Susplist)
     val newKlist = Klist@newConjuncts
     val _ = if not (Flags.trace()) then () else print ("Testing for box action "^(N.pretty_name(box_a))^", yielded " ^Lib.mkstrint( List.length(newConjuncts))^" conjuncts\n")
     val new2_f = F.mk_true
   in
     prove(S.Seq(ne, ag, new2_f, altlist, FPlist, i, Susplist, newKlist), e, ns)  
   end
   else true
else
(* ##### BOX2-rule #### *)
if F.is_box_barred(f) orelse F.is_box_unbarred(f)   andalso A.is_process ag e
	andalso N.is_variable(F.get_left(f))  then
let
   val Suspnew = S.addSuspSeq(Susplist, F.get_left(f), ne, ag, f,
	altlist, FPlist, i) 
   val _ = if not (Flags.trace()) then () else print("Testing for box: "^N.mkstr(F.get_left(f))^" ,  yielded"^Lib.mkstrint( List.length(Suspnew))^ " to suspend. \n")
   val new_f = F.mk_true
in
   prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, Suspnew, Klist), e, ns)  
end
else

(* ##### BOX3-rule #### *)
if F.is_box_tau(f) then
   if A.is_process ag e then
   let
     val new_f = F.select_right(f)
     val commitments = compact_commits(AS.commitments ns ag e)
     val newConjuncts = S.add_tau_Sequents(commitments, ne, new_f,
	altlist, FPlist, i, Susplist)
     val newKlist = Klist@newConjuncts
     val _ = if not (Flags.trace()) then () else print ("Testing for box: tau,  yielded" ^Lib.mkstrint(List.length(newConjuncts))^ "to conjuncts. \n")
     val new2_f = F.mk_true
   in
     prove(S.Seq(ne, ag, new2_f, altlist, FPlist, i, Susplist,newKlist), e, ns)  
   end
   else true
else

(*___________FIXPOINT RULES________*)
(*#### MINIMUM FIXPOINT Unfold-rule ####*)
if F.is_rooted_lfp(f) then
let
   val _ = if not (Flags.trace()) then () else print ("Unfold Minpoint...\n")
   val previous_constant = S.get_last_u(FPlist)
   val new_U = CST.next(previous_constant)
   val new_f = F.unfold new_U f
   val newFPlist = S.addMin(ne, ag, f, i, new_U)@FPlist
in
  prove(S.Seq(ne, ag, new_f, altlist, newFPlist, i, Susplist, Klist), e,ns)   
end

else

(*#### MAXIMUM FIXPOINT Unfold-rule ####*)
if F.is_rooted_gfp(f) then
let
   val _ = if not (Flags.trace()) then () else print ("Unfold maxpoint...\n")
   val previous_constant = S.get_last_u(FPlist)
   val new_U = CST.next(previous_constant)
   val new_f = F.unfold new_U f
   val newFPlist = S.addMax(ne, ag, f, i, new_U)@FPlist
in
  prove(S.Seq(ne, ag, new_f, altlist, newFPlist, i, Susplist, Klist), e,ns)   
end
else

(* #### LOOPCHECK (MINUMUM FIXPOINT FAILURE) ####*)
if F.is_rooted_con(f) andalso
   S.visitedMin(FPlist, F.constant f, ag, ne, f, i) then 
let
   val _ = if not (Flags.trace()) then () else print ("MinHit...\n")
   val new_f = F.mk_false
val new_Klist = S.remove_conjuncts(F.constant f, ag, S.get_formula(FPlist, F.constant f), Klist)

in
 prove(S.Seq(ne, ag, new_f, altlist, FPlist, i, Susplist, new_Klist), e,ns) 
end 
else

(*##### DISCHARGE (MAXIMUM FIXPOINT SUCCESS ) #####*)
if F.is_rooted_con(f) andalso
   S.visitedMax(FPlist, F.constant f, ag, ne, f, i) then
let
   val _ = if not (Flags.trace()) then () else print ("Discharge...\n")
   val new_f = F.mk_true
   val new_Klist = S.remove_conjuncts(F.constant f, ag, S.get_formula(FPlist, F.constant f), Klist)
in
 prove(S.Seq(ne, ag, new_f, altlist, FPlist, i , Susplist, new_Klist), e,ns) 
end
else

(* #### NO-HIT MIN/MAX FIXPOINTS (FOLD)###*)
if F.is_rooted_con(f) then
let
   val _ = if not (Flags.trace()) then () else print ("Fixpoint Folding...\n")
   val new_f = S.get_formula(FPlist, F.constant f)
   val new2f = F.unfold (F.constant f) new_f
  
in
 prove(S.Seq(ne, ag, new2f, altlist, FPlist, i, Susplist, Klist), e,ns) 
end

else if F.is_rooted_var(f) then raise not_closed_formula

else false

end

and

(* used by diamond2-rule when commitments like A>X.B or when dealing with <X>F formula, *)
(* where X is a variable. The variable is unified with names from the actions of the commitment relation and the *)
(* proof search continues. This is not possible for tau-actions since they do not contain a name. *)
    unify_and_prove_one(var, [], ne, f, alt, fp, i, susp, klist, e, ns)= false
  | unify_and_prove_one(var, (act, ag)::com_rest, ne, f, alt, fp, i, susp, klist,e, ns)=
    if N.eq(ACT.name(act), var) then (*same variable in commitment and formula. *) 
       let                             (* no unifying is necessary just continue search *)
          val new_f = F.select_right(f) 
          val sequent = S.mk_Sequent(ne, ag, new_f, alt, fp, i, susp, klist)
       in
         if prove(sequent,e, ns)
          then true
         else unify_and_prove_one(var, com_rest, ne, f, alt, fp, i, susp, klist, e, ns) 
       end
    else
    if (not(ACT.is_tau(act)) andalso N.is_name(ACT.name(act))) 
    then
       let     
          val n = ACT.name(act) (* commitment is a name and formula a variable *)
          val sequent = S.mk_Sequent(ne,  (* unify variable with name in sequent *)
                                    (A.substitute [(var,n)] ag), 
                                    (F.subst var n f), 
                                    (S.replaceVarAlt(var, n, alt)), 
                                    (S.replaceVarVF(var, n ,fp)), i, 
                                    (S.replaceVarSus(var, n, susp)), 
                                    (S.replaceVarSEQ(var, n, klist)))
           val _ = if not (Flags.trace()) then () else print("unifying "^ ACT.mkstr(act)^" with "^N.mkstr(n)^" in Sequent.\n")      
       in
         if prove(sequent, e, ns) 
         then true 
         else 
             unify_and_prove_one(var, com_rest, ne, f, alt, fp, i, susp, klist, e, ns)
       end
    else 
        if not(ACT.is_tau(act)) andalso N.is_variable(ACT.name(act))
        then 
            if N.index_of(ACT.name(act)) > N.index_of(var) 
            then     (* bind less restricted variable to more restricted (i e parameter index) *)
                let
                  val var2 = ACT.name(act) 
                  val sequent =  S.mk_Sequent(ne,(A.substitute [(var2, var)] ag), 
                                                 (F.subst var2 var f), 
                                                 (S.replaceVarAlt(var2, var, alt)), 
                                                 (S.replaceVarVF(var2, var, fp)), i, 
                                                 (S.replaceVarSus(var2, var, susp)), 
                                                 (S.replaceVarSEQ(var2, var, klist)))
                  val _ = if not (Flags.trace()) then () else print("unifying "^ ACT.mkstr(act)^" with "^N.mkstr(var)^" in Sequent.\n")      
                in 
                  if prove(sequent, e, ns) 
                  then true 
                  else
                      unify_and_prove_one(var, com_rest, ne, f, alt, fp, i, susp, klist, e, ns) 
                end
    else
        if not(ACT.is_tau(act)) andalso N.is_variable(ACT.name(act))
        then 
            if N.index_of(ACT.name(act)) <= N.index_of(var) 
            then  (* bind less restricted to more restricted *)
                let
                   val var2 = ACT.name(act) 
                   val sequent =  S.mk_Sequent(ne, (A.substitute [(var, var2)] ag),
                                                   (F.subst var var2 f), 
                                                   (S.replaceVarAlt(var, var2, alt)),                                                                         (S.replaceVarVF(var, var2, fp)), i, 
                                                   (S.replaceVarSus(var, var2, susp)), 
                                                   (S.replaceVarSEQ(var, var2, klist)))
		  val _ = if not (Flags.trace()) then () else print("unifying "^ ACT.mkstr(act)^" with "^N.mkstr(var)^" in Sequent.\n")      
                in 
                  if prove(sequent, e, ns) 
                  then true 
                  else
                      unify_and_prove_one(var, com_rest, ne, f, alt, fp, i, susp, klist, e, ns) 
                end
     else false
    else false            
   else false   
  

fun naked_prover agent formula env  = 
let 
        
	val ne = NE.mk_empty
	val altlist = S.mk_empty_delta
	val FPlist = S.mk_empty_FPlist
	val i = 0
	val Susplist = S.mk_empty_Susplist
	val Klist = S.mk_empty_Klist
        val ns = namsubst(agent, formula)
in
  
  prove(S.Seq(ne, agent, formula, altlist, FPlist, i, Susplist, Klist), env, ns)
end


end;





















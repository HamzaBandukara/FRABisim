functor SubSequent(	structure Name :NAME
			structure Agent : McAGENT
				sharing Agent.ACT.N = Name 
			structure Constant : CONSTANT
			structure Formula : PFORMULA
				sharing Formula.ACT.N = Name
				sharing Formula.CST = Constant
			structure Agsubsem : AGENTSUBSEM
				sharing Agsubsem.A = Agent
				sharing Agsubsem.NS.N = Name
			structure Ns : NAMESUBSTITUTION
				sharing Ns.N = Name
				sharing Ns = Agsubsem.NS				
			structure Nameeq : NAMEEQUATION
				sharing Nameeq.N = Name						
			structure Action : ACTION
				sharing Action.N = Name
				sharing Action = Agent.ACT
				sharing Action = Formula.ACT
			structure Env : ENV
				sharing Env = Agent.E
							): SEQ =

struct

structure N = Name
structure F = Formula
structure A = Agent
structure NE = Nameeq
structure CST = Constant
structure AS = Agsubsem
structure ACT = Action
structure NS= Ns
structure E = Env

val e = E.empty

datatype VisFixpoint = Min of CST.constant * NE.nameequation * 
			A.agent * F.formula * int
                      |Max of CST.constant * NE.nameequation * 
			A.agent * F.formula * int

	and

Delta = Alt of A.agent * F.formula * VisFixpoint list * SuspSequent list  
       |Bar of A.agent * F.formula * VisFixpoint list * SuspSequent list
	and

SuspSequent = SuspSeq of N.name * Sequent

	and
 
Sequent = Seq of NE.nameequation * A.agent * F.formula * 
			Delta list * VisFixpoint list * int *
			SuspSequent list * Sequent list 



val mk_empty_delta = nil

val mk_empty_FPlist = nil

val mk_empty_Susplist = nil

val mk_empty_Klist = nil

(* Predicates for existence testing *)
fun exists_alternative(Alt(_,_,_,_)::rest) = true 
  | exists_alternative(Bar(_,_,_,_)::rest) = exists_alternative(rest)
  | exists_alternative([]) = false

fun exists_conjunctive(Seq(_,_,_,_,_,_,_,_)::rest) = true
  | exists_conjunctive([]) = false
 
(* adding an alternative to current sequent *)
fun addAlt(d, ag, form, fplist, susplist)=
Alt(ag, form, fplist, susplist)::d

fun mk_Alt(ag, f, fpl, spl)= Alt(ag, f, fpl, spl)

fun mk_Sequent(nameequation, agent, formula, delta, FPlist, i,Susplist, Klist)=
Seq(nameequation, agent, formula, delta, FPlist, i, Susplist, Klist)

(* adding an alternative as a result of a contraction *)
fun addBar(d, ag, form, fplist, susplist)=
Bar(ag, form, fplist, susplist)::d

(* remove bar-status from alternatives in alternative list *)
fun unbar([])=[]
  | unbar(Alt(a, f, fplist, susplist)::rest)=
	  Alt(a, f, fplist, susplist)::unbar(rest)
  | unbar(Bar(a, f, fplist, susplist)::rest)=
          Alt(a, f, fplist, susplist)::unbar(rest)

(* instansiating an variable for a name *)

fun replaceVarAlt(var, name, [])=[]
  | replaceVarAlt(var, name, Alt(a, f, fplist, susplist)::rest)=
    Alt( A.substitute[(var,name)] a, F.subst var name f,
       replaceVarVF(var, name, fplist), replaceVarSus(var, name,
	susplist))::replaceVarAlt(var, name, rest)	
   | replaceVarAlt(var, name, (Bar(a, f, fplist, susplist))::rest)=
     Bar(A.substitute[(var,name)] a, F.subst var name f,
       replaceVarVF(var, name, fplist), replaceVarSus(var, name,
	susplist))::replaceVarAlt(var, name, rest)	 

and
 
 replaceVarVF(var, name, [])=[] 
|replaceVarVF(var, name, Min(c, ne, a, f, i)::rest)=
 Min(c, ne, A.substitute[(var, name)] a, F.subst var name f,
i)::replaceVarVF(var, name, rest)  
|replaceVarVF(var, name, Max(c, ne, a, f, i)::rest)=
 Max(c, ne, A.substitute[(var, name)] a, F.subst var name f,
 i)::replaceVarVF(var, name, rest)


and

 replaceVarSus(var, name, [])=[]
|replaceVarSus(var, name, SuspSeq(queVar,Seq(ne, a, f, alts, fplist,
i, susps,seqlist))::rest)=
SuspSeq(if N.eq(queVar, var) then name else queVar,Seq(ne, 
A.substitute[(var, name)] a, F.subst var name f, 
replaceVarAlt(var, name, alts),
replaceVarVF(var, name, fplist), i, replaceVarSus(var, name, susps),
replaceVarSEQ(var, name, seqlist)))::replaceVarSus(var, name, rest)

and

 replaceVarSEQ(var, name, [])=[]
|replaceVarSEQ(var, name, Seq(ne, a, f, dlist, fplist, i, susplist, seqlist)::rest)=
 Seq(ne, A.substitute[(var, name)] a, F.subst var name f,
replaceVarAlt(var, name, dlist), replaceVarVF(var, name, fplist), i,
replaceVarSus(var, name, susplist), replaceVarSEQ(var, name,seqlist))
::replaceVarSEQ(var, name, rest)


(* calculate ALL commitments for a certain agent, based on the
equality information of the name-equations *)
fun calc_all_commits(ne, agent) = 
let
	fun all_commits(ag, [])=[]        
	  | all_commits(ag, namehead::nametail)  = 
        (AS.commitments (NS.pack([namehead])) ag e)@all_commits(ag, nametail)
 
    in all_commits(agent, NE.get_all_eq_classes(ne))
end

(* add input alternatives as long as the commitments do not commit to tau *)
fun add_unbarred_alt(n, [], formula, FPlist, Susplist) = []
  | add_unbarred_alt(n, (action, agent)::rest, formula, FPlist, Susplist)=
    if not(ACT.is_tau(action)) andalso N.eq(n, ACT.name(action)) 
           andalso ACT.is_input(action) 
	then mk_Alt(agent, formula, FPlist,
Susplist)::add_unbarred_alt(n, rest, formula, FPlist, Susplist)
	else add_unbarred_alt(n, rest, formula, FPlist, Susplist)

(* add output alternatives as long as the commitments do not commit to tau *)
fun add_barred_alt(n, [], formula, FPlist, Susplist) = []
  | add_barred_alt(n, (action, agent)::rest, formula, FPlist, Susplist)=
    if not(ACT.is_tau(action)) andalso N.eq(n, ACT.name(action)) 
           andalso ACT.is_output(action) 
	then mk_Alt(agent, formula, FPlist,
Susplist)::add_barred_alt(n, rest, formula, FPlist, Susplist)
	else add_barred_alt(n, rest, formula, FPlist, Susplist)

(* add input alternatives as long as the commitments do not commit to tau *)
(* regardless of name equality: this is for  variable commitments *)
fun add_unbarred_alt_vars(n, [], formula, FPlist, Susplist) = []
  | add_unbarred_alt_vars(n, (action, agent)::rest, formula, FPlist, Susplist)=
    if not(ACT.is_tau(action)) andalso ACT.is_input(action) 
	then mk_Alt(agent, formula, FPlist,
Susplist)::add_unbarred_alt_vars(n, rest, formula, FPlist, Susplist)
	else add_unbarred_alt_vars(n, rest, formula, FPlist, Susplist)

(* add output alternatives as long as the commitments do not commit to tau *)
fun add_barred_alt_vars(n, [], formula, FPlist, Susplist) = []
  | add_barred_alt_vars(n, (action, agent)::rest, formula, FPlist, Susplist)=
    if not(ACT.is_tau(action)) andalso ACT.is_output(action) 
	then mk_Alt(agent, formula, FPlist,
Susplist)::add_barred_alt_vars(n, rest, formula, FPlist, Susplist)
	else add_barred_alt_vars(n, rest, formula, FPlist, Susplist)

(* add only tau-commitments to alternative list *)
fun add_tau_commit([], formula, FPlist, Susplist) = []
  | add_tau_commit((action, agent)::rest, formula, FPlist, Susplist)=
    if ACT.is_tau(action) then 
	mk_Alt(agent, formula, FPlist, Susplist)
		::add_tau_commit(rest, formula, FPlist, Susplist)
    else
	add_tau_commit(rest, formula, FPlist, Susplist)

(* add sequents as long as they do not commit tau and are input actions*)
fun add_unbarred_Sequents(n, [], ne, f, al, FPlist, i, Sul)= []
  | add_unbarred_Sequents(n, (ac, ag)::rest, ne, f, al, FPlist, i, Sul) =
     if not(ACT.is_tau(ac)) andalso N.eq(n, ACT.name(ac)) andalso ACT.is_input(ac) 
then mk_Sequent(ne, ag, f, al, FPlist, i, Sul,[])::
			add_unbarred_Sequents(n, rest, ne,f, al, FPlist, i, Sul)
	else add_unbarred_Sequents(n, rest, ne, f, al, FPlist, i, Sul) 

(* add sequents as long as they do not commit tau and are output actions*)
fun add_barred_Sequents(n, [], ne, f, al, FPlist, i, Sul)= []
  | add_barred_Sequents(n, (ac, ag)::rest, ne, f, al, FPlist, i, Sul) =
     if not(ACT.is_tau(ac)) andalso N.eq(n, ACT.name(ac)) andalso ACT.is_output(ac) 
then mk_Sequent(ne, ag, f, al, FPlist, i, Sul,[])::
			add_barred_Sequents(n, rest, ne,f, al, FPlist, i, Sul)
	else add_barred_Sequents(n, rest, ne, f, al, FPlist, i, Sul) 

(* add sequents to conjunctives when they do commit tau *)
fun add_tau_Sequents([], ne, f, al, FPlist, i, Sul)= []
  | add_tau_Sequents((ac,ag)::rest, ne, f, al, FPlist, i, Sul) =
     if ACT.is_tau(ac) then
	mk_Sequent(ne, ag, f, al, FPlist, i, Sul,[])::
		add_tau_Sequents(rest, ne,f, al, FPlist, i, Sul)
     else add_tau_Sequents(rest, ne,f, al, FPlist, i, Sul)


fun names_in_alt([])=[]
  | names_in_alt(Alt(ag, form, FPlist, Susplist)::altrest)=
    A.free_names(ag)@
    F.free_names(form)@
    names_in_FP(FPlist)@
    names_in_Susp(Susplist)@
    names_in_alt(altrest)
  | names_in_alt(Bar(ag, form, FPlist, Susplist)::altrest)=
    A.free_names(ag)@
    F.free_names(form)@
    names_in_FP(FPlist)@
    names_in_Susp(Susplist)@
    names_in_alt(altrest)

and

 names_in_FP([])=[]
|names_in_FP(Min(c, ne, ag, f, i)::fprest) =
 A.free_names(ag)@
 F.free_names(f)@
 names_in_FP(fprest) 
|names_in_FP(Max(c, ne, ag, f, i)::fprest) =
 A.free_names(ag)@
 F.free_names(f)@
 names_in_FP(fprest) 

and

 names_in_Susp([])=[]
|names_in_Susp(SuspSeq(var, seq)::susprest) =
 names_in_sequent([seq])@
 names_in_Susp(susprest)

and

 names_in_sequent([])=[]
|names_in_sequent( (Seq(n, a, f, al, FPl, i, Sul, Sel))::rest ) =
	NE.names(n)@
	A.free_names(a)@
	F.free_names(f)@
	names_in_alt(al)@
	names_in_FP(FPl)@
	names_in_Susp(Sul)@
	names_in_sequent(Sel)@
	names_in_sequent(rest)

fun get_activated_sequents(_, []) = []
  | get_activated_sequents(name, SuspSeq(n, seq)::rest) = 
	if N.eq(name, n) then seq::get_activated_sequents(name, rest) else
		get_activated_sequents(name, rest)

fun remove_activated_sequents(_,[]) = []
  | remove_activated_sequents(name, SuspSeq(n, seq)::rest)=
    if N.eq(name, n) then remove_activated_sequents(name, rest) else
       SuspSeq(n, seq)::remove_activated_sequents(name, rest)

fun get_next_Alt([]) = []
  | get_next_Alt(Bar(_,_,_,_)::rest) =
	get_next_Alt(rest)
  | get_next_Alt(Alt(a,f,FP,S)::rest) = Alt(a,f,FP,S)::rest

fun nextAgent(Alt(a,f,FP,S)::rest)= a

fun nextFormula(Alt(a, f, FP, S)::rest) = f

fun nextFPlist(Alt(a, f, FP, S)::rest) = FP

fun nextSusplist(Alt(a,f,FP,S)::rest) = S

fun newNeq(Seq(ne, a, f, altlist, Fplist, i, Susplist, Klist)::rest) = ne
fun newAgent(Seq(ne, a, f, altlist, Fplist, i, Susplist, Klist)::rest)
= a

fun newFormula(Seq(ne, a, f, altlist, Fplist, i, Susplist,
Klist)::rest)= f

fun newAlt(Seq(ne, a, f, altlist, Fplist, i, Susplist, Klist)::rest)=
altlist

fun newFPlist(Seq(ne, a, f, altlist, Fplist, i, Susplist,
Klist)::rest)= Fplist

fun newIndex(Seq(ne, a, f, altlist, Fplist, i, Susplist, Klist)::rest)
= i

fun newSusplist(Seq(ne, a, f, altlist, Fplist, i, Susplist,
Klist)::rest) = Susplist


fun addSuspSeq(suspOld, name, ne, agent, formula, altlist, Fplist, index)=
SuspSeq(name, Seq(ne, agent, formula, altlist, Fplist, index, [], []))
::suspOld

fun addMax(ne, ag, form, index, constant)=
	[Max(constant, ne, ag, form, index)]

fun addMin(ne, ag, form, index, constant)=
	[Min(constant, ne, ag, form, index)]

fun visitedMin([], constant, agent, nameeq, form, index)= false
  | visitedMin(Max(_,_,_,_,_)::rest, constant, agent, nameeq, 
	form, index) = visitedMin(rest, constant, agent, nameeq, 
		form, index)
  | visitedMin(Min(cst, ne, a, f, i)::rest, constant, agent, nameeq, 
	form, index) = 
	if (CST.eq cst constant) andalso (A.eq agent a)  andalso
		NE.quiet(nameeq, ne) then true 
	else 
	visitedMin(rest, constant, agent, nameeq, form, index)


fun visitedMax([], constant, agt, nameeq, form, index)= false
  | visitedMax(Min(_,_,_,_,_)::rest, constant, agt, nameeq, 
	form, index) = visitedMax(rest, constant, agt, nameeq, 
		form, index)
  | visitedMax(Max(cst, ne, a, f, i)::rest, constant, agt, nameeq, 
	form, index) = 
               
	if (CST.eq cst constant) andalso (A.eq a agt)   andalso  
		NE.equation_implies(nameeq, ne)  then true
	else 
	visitedMax(rest, constant, agt, nameeq, form, index)



fun commit_eq((ac1, ag1), (ac2, ag2)) = ACT.eq(ac1, ac2) andalso (A.eq ag1 ag2)
(*   | commit_eq(_,_) = false  *)


 
fun alt_eqC (Alt(_,_,_,_)) (Bar(_,_,_,_)) = false
  | alt_eqC (Alt(a,f,fp,s)) (Alt(a1,f1,fp1, s1)) = (A.eq a a1) andalso F.eq (f,f1) andalso (McList.l_eq (FPeqC) fp fp1)
            andalso (McList.l_eq (Susp_eqC) s s1)
  | alt_eqC (Bar(_,_,_,_)) (Alt(_,_,_,_)) = false
  | alt_eqC (Bar(a,f,fp,s)) (Bar(a1,f1,fp1, s1)) = (A.eq a a1) andalso F.eq( f, f1) andalso (McList.l_eq (FPeqC) fp fp1)
            andalso (McList.l_eq (Susp_eqC) s s1)
(*   | alt_eqC _ _ = false *)

and 
    Susp_eqC (SuspSeq(n, seq)) (SuspSeq(m, seq1)) =  N.eq(n,m) andalso conj_eqC (seq)(seq1) 
(*    |Susp_eqC _ _ = false *)

and      
        
 conj_eqC (Seq(ne, a, f, altlist, Fplist, i, Susplist, clist)) (Seq(ne1, a1, f1, altlist1, Fplist1, i1, Susplist1, clist1))  = NE.eq(ne, ne1) andalso (A.eq a a1) andalso F.eq( f, f1) andalso (McList.l_eq (alt_eqC)(altlist)(altlist1)) andalso (McList.l_eq (FPeqC) Fplist Fplist1) andalso (i=i1) andalso (McList.l_eq (Susp_eqC) Susplist  Susplist1) andalso  (McList.l_eq (conj_eqC) clist clist1)
(*   | conj_eqC _ _ = false *)
and 

   FPeqC (Max(_,_,_,_,_)) (Min(_,_,_,_,_)) = false
 | FPeqC (Min(_,_,_,_,_)) (Max(_,_,_,_,_)) = false
 | FPeqC (Min(cst, ne, ag, f, i)) (Min(cst1, ne1, ag1, f1, i1)) = 
        (CST.eq cst cst1) andalso NE.eq(ne, ne1) andalso (A.eq ag ag1) andalso F.eq(f, f1) andalso (i=i1)
 | FPeqC (Max(cst, ne, ag, f, i)) (Max(cst1, ne1, ag1, f1, i1)) = 
        (CST.eq cst cst1) andalso NE.eq(ne, ne1) andalso (A.eq ag ag1) andalso F.eq( f, f1) andalso (i=i1)
(*  | FPeqC _ _ = false *)

fun alt_eq(alt1, alt2) = alt_eqC alt1 alt2

fun FPeq(m1, m2) = FPeqC m1 m2

fun conj_eq(s1, s2) = conj_eqC s1 s2

fun Susp_eq(su1, su2) = Susp_eqC su1 su2


  
fun get_last_u([]) = CST.init
  | get_last_u(Max(c,_,_,_,_)::rest) = c
  | get_last_u(Min(c,_,_,_,_)::rest) = c

fun get_formula([], cst) = F.mk_false
  | get_formula(Max(c, _, _, f,_)::rest, cst)= if (CST.eq cst c) 
	then f else get_formula(rest, cst)
  | get_formula(Min(c, _, _, f,_)::rest, cst) = if (CST.eq cst c)
	then f else get_formula(rest, cst)

fun f_s([],[]) = false
  | f_s(_,[]) = false
  | f_s([],_) = false
  | f_s(f1::rest1, f2_list) = McList.member (F.eq_curried) f1 f2_list orelse
                              f_s(rest1, f2_list)   
 

fun formula_subset(cst, f) = 
    let
       val const_list = F.f_constants(f)
    in
       if List.length(const_list)=1 then CST.eq (List.hd(const_list)) cst
       else
       McList.member (CST.eq) cst const_list andalso 
                      CST.eq (McList.max (CST.l_eq) const_list CST.init) cst
    end
    
fun remove_conjuncts(_,_,_,[]) = []
  | remove_conjuncts(cst,agent, form,  Seq(ne, a, f, altlist, Fplist, i, Susplist, clist)::rest) = 
      if formula_subset(cst, f)  andalso not(F.is_rooted_gfp(f) orelse F.is_rooted_lfp(f)) then remove_conjuncts(cst, agent, form, rest)
      else  
        Seq(ne, a, f, altlist, Fplist, i, Susplist, clist)::remove_conjuncts(cst, agent, form, rest)
    

end








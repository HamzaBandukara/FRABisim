signature SEQ  =
sig 
	structure NE : NAMEEQUATION
      structure A : McAGENT
      structure F : PFORMULA
	structure N : NAME	
    structure CST : CONSTANT
    structure ACT : ACTION
	structure E : ENV
     structure AS : AGENTSUBSEM
    structure NS  : NAMESUBSTITUTION
    

	datatype Delta = Alt of A.agent * F.formula * VisFixpoint list *
			SuspSequent list
		    | Bar of A.agent * F.formula * VisFixpoint list *
			SuspSequent list

	and

	SuspSequent = SuspSeq of N.name * Sequent
	
	and

	VisFixpoint = Min of CST.constant * NE.nameequation * 
			A.agent * F.formula * int 
	             |Max of CST.constant * NE.nameequation * 
			A.agent * F.formula * int
	and	
	
	Sequent = Seq of NE.nameequation * A.agent * F.formula * Delta
		list * VisFixpoint list * int * SuspSequent list *
		Sequent list


	val mk_empty_delta : Delta list

	val mk_empty_FPlist : VisFixpoint list

	val mk_empty_Susplist : SuspSequent list

	val mk_empty_Klist :  Sequent list

    	val addAlt      : Delta list * A.agent * F.formula *
                          VisFixpoint list * SuspSequent list  ->
			   Delta list
		
	val mk_Alt	: A.agent * F.formula * VisFixpoint list *
				SuspSequent list -> Delta 

	val mk_Sequent  : NE.nameequation * A.agent * F.formula *
				Delta list * VisFixpoint list *int *
				SuspSequent list * Sequent list -> Sequent

	val addBar	: Delta list * A.agent * F.formula *
			  VisFixpoint list * SuspSequent list ->
			  Delta list

	val unbar	: Delta list  -> Delta list


        val conj_eqC : Sequent -> Sequent -> bool

        val alt_eqC : Delta -> Delta -> bool

        val Susp_eqC : SuspSequent -> SuspSequent -> bool

        val conj_eq : Sequent *  Sequent -> bool

        val alt_eq : Delta * Delta -> bool

        val Susp_eq : SuspSequent * SuspSequent -> bool


        val commit_eq : (ACT.action * A.agent) * (ACT.action *
			A.agent) -> bool


	val exists_alternative : Delta list -> bool

        val exists_conjunctive : Sequent list -> bool

        val calc_all_commits : NE.nameequation * A.agent  -> 
			(ACT.action * A.agent) list

        val add_unbarred_alt : N.name * (ACT.action * A.agent ) list * F.formula *
		               VisFixpoint list * SuspSequent list -> Delta list 
  
        val add_barred_alt : N.name * (ACT.action * A.agent ) list * F.formula *
		               VisFixpoint list * SuspSequent list -> Delta list 

        val add_tau_commit : (ACT.action * A.agent ) list * F.formula *
			VisFixpoint list * SuspSequent list ->
			Delta list 

       val add_unbarred_alt_vars : N.name * (ACT.action * A.agent ) list * F.formula *
		               VisFixpoint list * SuspSequent list -> Delta list 
  
        val add_barred_alt_vars : N.name * (ACT.action * A.agent ) list * F.formula *
		               VisFixpoint list * SuspSequent list -> Delta list 

        val add_unbarred_Sequents : N.name * (ACT.action * A.agent) list * 
                                NE.nameequation *
			         F.formula * Delta list * VisFixpoint list
			         * int * SuspSequent list -> Sequent list

         val add_barred_Sequents   : N.name * (ACT.action * A.agent) list * 
                                     NE.nameequation *
			             F.formula * Delta list * VisFixpoint list
			             * int * SuspSequent list -> Sequent list

        val add_tau_Sequents : (ACT.action * A.agent) list * NE.nameequation *
			F.formula * Delta list * VisFixpoint list
			* int * SuspSequent list -> Sequent list

	(* structures for propagating variable instantiation into
		different subsequentss *)

	val replaceVarAlt  : N.name * N.name * Delta list -> Delta list
		
	val replaceVarSus : N.name * N.name * SuspSequent list ->
				SuspSequent list

	val replaceVarVF  : N.name * N.name * VisFixpoint list ->
				VisFixpoint list

	val replaceVarSEQ : N.name * N.name * Sequent list -> 
				Sequent list


	val names_in_alt  : Delta list -> N.name list

	val names_in_FP   : VisFixpoint list -> N.name list

	val names_in_Susp : SuspSequent list -> N.name list

	val names_in_sequent : Sequent list -> N.name list
 
	val get_activated_sequents : N.name * SuspSequent list ->
				Sequent list

	val remove_activated_sequents : N.name * SuspSequent list ->
				SuspSequent list

        val remove_conjuncts : CST.constant * A.agent * F.formula * Sequent list -> Sequent list

	(* brings out next alternative from Delta list *)
 	val nextAgent	 : Delta list -> A.agent 
	val nextFormula  : Delta list -> F.formula
        val nextFPlist   : Delta list -> VisFixpoint list
        val nextSusplist : Delta list -> SuspSequent list
	
	val get_next_Alt : Delta list -> Delta list
	
	val newNeq	 : Sequent list -> NE.nameequation
	val newAgent     : Sequent list -> A.agent
	val newFormula   : Sequent list -> F.formula
	val newAlt       : Sequent list -> Delta list
	val newFPlist    : Sequent list -> VisFixpoint list
	val newSusplist  : Sequent list -> SuspSequent list
	val newIndex     : Sequent list -> int
	
	(* function for adding a suspended sequent to its list  *)
	val addSuspSeq : SuspSequent list * N.name * NE.nameequation
	* A.agent * F.formula * Delta list * VisFixpoint list * int ->
			SuspSequent list

	(* functions for fixpoints list  *)	
	val get_last_u   : VisFixpoint list -> CST.constant

	
    	val addMax       : NE.nameequation * 
			    A.agent * F.formula * int * CST.constant
				-> VisFixpoint list

    	val addMin      : NE.nameequation * 
			    A.agent * F.formula * int * CST.constant
				-> VisFixpoint list

	(* predicates for testing a fixpoint *)
	val visitedMin : VisFixpoint list * CST.constant * 
		A.agent * NE.nameequation * F.formula * int -> bool

	val visitedMax  : VisFixpoint list * CST.constant * 
		A.agent * NE.nameequation * F.formula * int -> bool

	val get_formula : VisFixpoint list * CST.constant -> F.formula 
end






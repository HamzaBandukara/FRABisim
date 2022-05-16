signature NAMEEQUATION =
sig 
    	structure N : NAME

	type nameequation
	type eqclass

	val mk_empty : nameequation      
 
    	val addEq : N.name * N.name * nameequation -> nameequation
		(* Gamma':=Gamma U {x=y} *)

	val addIneq : N.name * N.name * nameequation -> nameequation
		(* Gamma':=Gamma U {x#y} *)

	val is_consistent : N.name * N.name * nameequation -> bool
		(* if Gamma':=Gamma U {x=y} makes Gamma' consistent *)

	val ineq_implies : N.name * N.name * nameequation -> bool
		(* if Gamma implies x=y *)

    	val eq_implies : N.name * N.name * nameequation -> bool
		(* if Gamma implies x#y *)

	val get_all_equals : N.name * nameequation -> N.name list
		(* returns all names equal to current name *)

	val get_all_eq_classes: nameequation -> N.name list list

	val quiet : nameequation * nameequation -> bool
		(* if Gamma is quiet w r t  Gamma' *)
	
	val equation_implies : nameequation * nameequation -> bool
		(* if Gamma implies Gamma' *)

	val names : nameequation -> N.name list
		(* returns all names in an nameequation *)

        val eq : nameequation * nameequation -> bool
end

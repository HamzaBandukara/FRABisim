signature PFORMULA =
sig

    structure CST : CONSTANT
    structure ACT : ACTION
    structure P : PROPVAR

  type variable

  type formula

  type fixed_point_formula

  exception bug

  exception NegationError of string * formula

  val mkstr : formula -> string

  (* SUBSTITUTIONS *)

  val subst: ACT.N.name -> ACT.N.name -> formula -> formula


  (* FORMULA EQUALITY *)

  val eq: formula * formula -> bool
 
  val eq_curried : formula -> formula -> bool

  val conjuncts : formula -> formula list

  (* CONSTRUCTORS *)

  val mk_true: formula

  val mk_false: formula

  val mk_eq: ACT.N.name -> ACT.N.name -> formula

  val mk_ineq: ACT.N.name -> ACT.N.name -> formula

  val mk_and: formula -> formula -> formula

  val mk_big_and: formula list -> formula

  val mk_or: formula -> formula -> formula

  val mk_big_or: formula list -> formula

  val mk_diamond: ACT.action -> formula -> formula

  val mk_box: ACT.action -> formula -> formula

  val mk_rooted_var: P.propvar -> (ACT.N.name list) -> formula

  val mk_rooted_gfp: P.propvar -> (ACT.N.name list) ->
                                     formula -> (ACT.N.name list) -> formula

  val mk_rooted_lfp: P.propvar -> (ACT.N.name list) ->
                                     formula -> (ACT.N.name list) -> formula

  val mk_rooted_con: CST.constant -> (ACT.N.name list) -> formula

  val mk_sigma: ACT.N.name -> formula -> formula

  val mk_bsigma: ACT.N.name -> formula -> formula

  val mk_pi: ACT.N.name -> formula -> formula

  val mk_exists: ACT.N.name -> formula -> formula

  val mk_forall: ACT.N.name -> formula -> formula

  
(* TESTERS *)


  val is_true: formula -> bool

  val is_false: formula -> bool

  val is_eq: formula -> bool

  val is_neq: formula -> bool

  val is_and: formula -> bool

  val is_or: formula -> bool

  val is_diamond_unbarred: formula -> bool

  val is_diamond_barred: formula -> bool

  val is_diamond_tau: formula -> bool 
 
  val is_box_unbarred: formula -> bool

  val is_box_barred: formula -> bool

  val is_box_tau: formula -> bool 

  val is_rooted_var: formula -> bool

  val is_rooted_gfp: formula -> bool

  val is_rooted_lfp: formula -> bool

  val is_rooted_con: formula -> bool

  val is_sigma: formula -> bool

  val is_bsigma: formula -> bool

  val is_pi: formula -> bool

  val is_exists: formula -> bool

  val is_forall: formula -> bool

  val is_GFP: fixed_point_formula -> bool

(* DESTRUCTORS *)

  val eq_left: formula -> ACT.N.name

  val eq_right: formula -> ACT.N.name

  val select_left: formula -> formula

  val select_right: formula -> formula

  val successor: ACT.N.name -> formula -> formula

  val get_propvar: fixed_point_formula -> P.propvar

  val get_arity: fixed_point_formula -> int

  val get_body: fixed_point_formula -> (ACT.N.name list) -> formula

  val get_left : formula -> ACT.N.name

  val root: fixed_point_formula -> (ACT.N.name list) -> formula

  val unroot: formula -> fixed_point_formula

  val params: formula -> ACT.N.name list

  val unfold: CST.constant -> formula -> formula

  val constants: fixed_point_formula -> CST.constant list

  val f_constants : formula -> CST.constant list

  val constant: formula -> CST.constant

  val free_names: formula -> ACT.N.name list

 
 
end






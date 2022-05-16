functor PFormula(structure PropVar: PROPVAR
                structure Constant: CONSTANT
                structure Action: ACTION): PFORMULA =

struct

  structure CST = Constant
  structure ACT = Action
  structure P = PropVar

  datatype variable = free of ACT.N.name 
                  |   bound of int
		
  datatype modality = Out
                   |  In 
                   |  Tau


  datatype formula = True 
                   | False
                   | IsEq of variable * variable
                   | IsNeq of variable * variable
                   | And of formula * formula
                   | Or of formula * formula
                   | Diamond of modality * variable * formula
                   | Box of modality * variable * formula
                   | RootedVar of P.propvar * variable list
                   | RootedGFP of
                         P.propvar * int * formula * variable list
                   | RootedLFP of
                         P.propvar * int * formula * variable list
                   | RootedCon of CST.constant * variable list
                   | Sigma of formula
                   | BSigma of formula
                   | Exists of formula
	  	       | Forall of formula
		
	
  datatype fixed_point_formula =
                     GFP of P.propvar * int * formula
                   | LFP of P.propvar * int * formula



  exception bug

  exception NegationError of string * formula

fun var_eq (bound(x)) (bound(y)) = (x=y)
  | var_eq (free(x)) (free(y)) =  ACT.N.eq(x,y)
  | var_eq _ _ = false

  fun mkstr (True) = "TT"
    | mkstr (False) = "FF"
    | mkstr (IsEq(v,w)) = (vmkstr v)^"="^(vmkstr w)
    | mkstr (IsNeq (v,w))= (vmkstr v)^"#"^(vmkstr w)
    | mkstr (And (f1,f2))= (mkstr f1)^"&"^(mkstr f2)
    | mkstr (Or (f1,f2)) = (mkstr f1)^"|"^(mkstr f2)
    | mkstr (RootedVar (p,vl)) =
	     (P.mkstr p)^"("^(Lib.mapconcat vmkstr vl ",")^")"
    | mkstr (RootedGFP (p,n,f,vl)) =
      let fun mkl 0 = ""
	    | mkl 1 = "v"^(Lib.mkstrint 1)
	    | mkl n = "v"^(Lib.mkstrint n)^","^(mkl (n-1))
      in
	  "(nu "^(P.mkstr p)^"("^(mkl n)^")."^(mkstr f)^")"
	  ^"("^(Lib.mapconcat vmkstr vl ",")^")"
      end
    | mkstr (RootedLFP (p,n,f,vl)) =
      let fun mkl 0 = ""
	    | mkl 1 = "v"^(Lib.mkstrint n)
	    | mkl n = "v"^(Lib.mkstrint n)^","^(mkl (n-1))
      in
	  "(mu "^(P.mkstr p)^"("^(mkl n)^")."^(mkstr f)^")"
	  ^"("^(Lib.mapconcat vmkstr vl ",")^")"
      end
    | mkstr (RootedCon(c,vl)) =
      (CST.mkstr c)^"("^(Lib.mapconcat vmkstr vl ",")^")"
    | mkstr (Sigma f) = "Sigma ("^(mkstr f)^")"
    | mkstr (BSigma f) = "BSigma ("^(mkstr f)^")"
    | mkstr (Exists f) = "Exists ("^(mkstr f)^")"
    | mkstr (Forall f) = "Forall ("^(mkstr f)^")"
    | mkstr (Diamond(m, a, f)) = "<"^mmkstr(m, a)^">"^mkstr(f)
    | mkstr (Box(m, a, f)) =   "["^mmkstr(m, a)^"]"^mkstr(f)

  and vmkstr (free n) = (ACT.N.mkstr n)
    | vmkstr (bound n) = "b"^(Lib.mkstrint n)

  and mmkstr (In, a) = vmkstr(a)
    | mmkstr (Out, a) = "'"^vmkstr(a)
    | mmkstr (Tau, a) = "tau"
    
  fun var_subst x y (free z) = if ACT.N.eq (y, z) then (free x) else (free z) 
    | var_subst x y (bound n) = bound n

  (* subst x y F: substitute x for y in F *)
  fun subst x y (True) = True 
    | subst x y (False) = False 
    | subst x y (IsEq(v,w)) = IsEq(var_subst x y v,var_subst x y w) 
    | subst x y (IsNeq(v,w)) = IsNeq(var_subst x y v,var_subst x y w) 
    | subst x y (And(F1,F2)) = And(subst x y F1,subst x y F2) 
    | subst x y (Or(F1,F2)) = Or(subst x y F1,subst x y F2) 
    | subst x y (Diamond(m, a, F)) = Diamond(m, var_subst x y a , subst x y F) 
    | subst x y (Box(m, a, F)) = Box(m, var_subst x y a, subst x y F) 
    | subst x y (RootedVar(X,vl)) = RootedVar(X,map (var_subst x y) vl) 
	      (* Remember fixed points are closed wrt name parameters! *)
    | subst x y (RootedGFP(X,n,F,vl)) =
        RootedGFP(X,n,F,map (var_subst x y) vl) 
      	  (* NB: The only free names of RootedGFP(X,n,F,vl) are in vl! *)
    | subst x y (RootedLFP(X,n,F,vl)) =
        RootedLFP(X,n,F,map (var_subst x y) vl) 
    | subst x y (RootedCon(U,vl)) = RootedCon(U,map (var_subst x y) vl)
    | subst x y (Sigma F) = Sigma (subst x y F) 
    | subst x y (BSigma F) = BSigma (subst x y F) 
    | subst x y (Exists F) = Exists (subst x y F)
    | subst x y (Forall F) = Forall (subst x y F) 

	

  (* eq ; check if two formulas are equal *)
  fun eq(False, False) = true 
    | eq(True, True) = true
    | eq( IsEq(x,y), IsEq(x1, y1)) = ((var_eq x x1) andalso (var_eq y y1)) 
                                   orelse ((var_eq x  y1) andalso (var_eq y x1))  
    | eq(IsNeq(x,y), IsNeq(x1, y1)) = ((var_eq x x1) andalso (var_eq y y1)) 
                                   orelse ((var_eq x y1) andalso (var_eq y x1)) 
    | eq(And(f1, f2), And(f3, f4)) = (eq(f1, f3) andalso eq(f2, f4)) orelse
                                     (eq(f1, f4) andalso eq(f2, f3))
    | eq(Or(f1, f2), Or(f3, f4)) = (eq(f1,f3) andalso eq(f2, f4)) orelse (eq(f1, f4) andalso eq(f2, f3))  
    | eq(Diamond(In, a, F), Diamond(In, a1, F1)) = (var_eq a a1) andalso eq(F, F1)
    | eq(Diamond(Out, a, F), Diamond(Out, a1, F1)) = (var_eq a a1) andalso eq(F, F1)
    | eq(Diamond(Tau, _, F), Diamond(Tau, _, F1)) = eq(F, F1)
    | eq(Box(In, a, F), Box(In, a1, F1)) = (var_eq a a1) andalso eq(F, F1)
    | eq(Box(Out, a, F), Box(Out, a1, F1)) = (var_eq a a1) andalso eq(F, F1)
    | eq(Box(Tau, _, F), Box(Tau, _, F1)) = eq(F, F1)
    | eq(RootedVar(p, v), RootedVar(p1, v1)) = (P.eq p p1) andalso McList.l_eq(var_eq) v v1
    | eq(RootedGFP(p, i, f, v), RootedGFP(p1, i1, f1, v1)) = (P.eq p p1) andalso (i=i1) andalso eq(f,f1) 
                andalso McList.l_eq(var_eq) v v1
    | eq(RootedLFP(p, i, f, v), RootedLFP(p1, i1, f1, v1)) = (P.eq p p1) andalso (i=i1) andalso eq(f,f1) 
                andalso McList.l_eq(var_eq) v v1
    | eq(RootedCon(c, vl), RootedCon(c1, vl1)) = (CST.eq c c1) andalso McList.l_eq(var_eq) vl vl1
    | eq(Sigma(f), Sigma (f1))   = eq(f, f1)
    | eq(BSigma(f), BSigma(f1)) = eq(f, f1)
    | eq(Exists(f), Exists(f1)) = eq(f, f1)
    | eq(Forall(f), Forall(f1)) = eq(f, f1)
    | eq(_,_)= false

fun eq_curried f1 f2 = eq(f1, f2)

(* Functions for binding free occurrences of names   *)
  fun bind_name l x (free y) = if ACT.N.eq (x, y) then bound l else free y 
    | bind_name l x (bound n) = bound (if n<l then n else n+1) (* n+1 *)

  (* bind x F: F is formula with de Bruijn index 1 made available for x  *)
  fun bind l x (True) = True 
    | bind l x (False) = False 
    | bind l x (IsEq(v,w)) = IsEq(bind_name l x v,bind_name l x w) 
    | bind l x (IsNeq(v,w)) = IsNeq(bind_name l x v,bind_name l x w) 
    | bind l x (And(F1,F2)) = And(bind l x F1,bind l x F2) 
    | bind l x (Or(F1,F2)) = Or(bind l x F1,bind l x F2) 
    | bind l x (Diamond(m, a, F)) = Diamond(m, bind_name l x a, bind l x F) 
    | bind l x (Box(m, a, F)) = Box(m, bind_name l x a, bind l x F) 
    | bind l x (RootedVar(X,vl)) = RootedVar(X,map (bind_name l x) vl) 
    | bind l x (RootedGFP(X,n,F,vl)) =
        RootedGFP(X,n,F,map (bind_name l x) vl) 
 	       (* NB: The only free names of RootedGFP(X,n,F,vl) are in vl! *)
    | bind l x (RootedLFP(X,n,F,vl)) =
        RootedLFP(X,n,F,map (bind_name l x) vl) 
    | bind l x (RootedCon(U,vl)) =
        RootedCon(U,map (bind_name l x) vl) 
    | bind l x (Sigma F) = Sigma (bind (l+1) x F) 
    | bind l x (BSigma F) = BSigma (bind (l+1) x F) 
    | bind l x (Exists F) = Exists (bind (l+1) x F)
    | bind l x (Forall F) = Forall (bind (l+1) x F) 

  fun bind_list l nil F = F 
    | bind_list l (x::nl) F = bind l x (bind_list l nl F)

(* Formula constructors *)

  val mk_true = True

  val mk_false = False

  fun mk_eq x y = IsEq(free x,free y)

  fun mk_ineq x y = IsNeq(free x,free y)

  fun mk_and F1 True = F1
    | mk_and True F2 = F2
    | mk_and F1 False = False
    | mk_and False F2 = False
    | mk_and F1 F2 = And(F1,F2)

  fun mk_big_and nil = True 
    | mk_big_and (F::nil) = F 
    | mk_big_and (F::fl) = mk_and F (mk_big_and fl)

  fun mk_or F1 True = True
    | mk_or True F2 = True
    | mk_or False F2 = F2
    | mk_or F1 False = F1
    | mk_or F1 F2 = Or(F1,F2)

  fun mk_big_or nil = False 
    | mk_big_or (F::nil) = F 
    | mk_big_or (F::fl) = mk_or F (mk_big_or fl)

fun mk_diamond x F = 
	if ACT.is_input(x) then
		Diamond(In, free  (ACT.name(x)), F) else
	if ACT.is_output(x) then 
		Diamond(Out, free (ACT.name(x)), F) else
		Diamond(Tau, bound 0, F)
		
fun mk_box x F = 
	if ACT.is_input(x) then
		Box(In, free (ACT.name(x)), F) else
	if ACT.is_output(x) then 
		Box(Out, free (ACT.name(x)), F) else
		Box(Tau, bound 0, F)

  fun mk_rooted_var X nl = RootedVar(X,(map free nl))

  fun mk_rooted_gfp X formal_params F actual_params =
        let val l = length formal_params
        in
          RootedGFP(X,l,bind_list 1 formal_params F,map free actual_params)
        end

  fun mk_rooted_lfp X formal_params F actual_params =
        let val l = length formal_params
        in
          RootedLFP(X,l,bind_list 1 formal_params F,map free actual_params)
        end

  fun mk_rooted_con U nl = RootedCon(U,map free nl)

  fun mk_sigma x F = Sigma(bind_list 1 [x] F)

  fun mk_bsigma x F = BSigma(bind_list 1 [x] F)

  fun mk_pi x F = Forall(bind_list 1 [x] F)

  fun mk_exists x F = Exists(bind_list 1 [x] F)

  fun mk_forall x F = Forall(bind_list 1[x] F)


  (* Testers *)

  fun is_true (True) = true 
    | is_true _ = false

  fun is_false (False) = true 
    | is_false _ = false

  fun is_eq (IsEq(_,_)) = true 
    | is_eq _ = false

  fun is_neq (IsNeq(_,_)) = true 
    | is_neq _ = false

  fun is_and (And(_,_)) = true 
    | is_and _ = false

  fun is_or (Or(_,_)) = true 
    | is_or _ = false

  fun is_diamond_unbarred (Diamond(In, _, _)) = true 
    | is_diamond_unbarred _ = false

  fun is_diamond_barred (Diamond(Out, _, _)) = true 
    | is_diamond_barred _ = false

  fun is_diamond_tau (Diamond(Tau, _, _)) = true 
    | is_diamond_tau _ = false

  fun is_box_unbarred (Box(In, _, _)) = true 
    | is_box_unbarred _ = false

  fun is_box_barred (Box(Out, _, _)) = true 
    | is_box_barred _ = false

  fun is_box_tau (Box(Tau, _, _)) = true 
    | is_box_tau _ = false

  fun is_rooted_var (RootedVar(_,_)) = true 
    | is_rooted_var _ = false

  fun is_rooted_gfp (RootedGFP(_,_,_,_)) = true 
    | is_rooted_gfp _ = false

  fun is_rooted_lfp (RootedLFP(_,_,_,_)) = true 
    | is_rooted_lfp _ = false

  fun is_rooted_con (RootedCon(_,_)) = true 
    | is_rooted_con _ = false

  fun is_sigma (Sigma _) = true 
    | is_sigma _ = false

  fun is_bsigma (BSigma _) = true 
    | is_bsigma _ = false

  fun is_pi (Forall _) = true 
    | is_pi _ = false

  fun is_exists (Exists _) = true 
    | is_exists _ = false

  fun is_forall (Forall _) = true |
      is_forall _ = false

  fun is_GFP (GFP(_,_,_)) = true |
      is_GFP _ = false

fun is_equalV(free(n1), free(n2)) = ACT.N.eq(n1, n2)
  | is_equalV(bound(i1), bound(i2)) = (i1=i2) 
  | is_equalV(_, _) = false
  
fun is_equalVlist([], [])= true
  | is_equalVlist(hd1::rest1, hd2::rest2)=
	is_equalV(hd1, hd2) andalso is_equalVlist(rest1, rest2)

  
    (* Destructors *)

  fun eq_left (IsEq(free x,free y)) = x |
      eq_left (IsNeq(free x,free y)) = x


  fun eq_right (IsEq(free x,free y)) = y |
      eq_right (IsNeq(free x,free y)) = y


  fun select_left (And(F1,F2)) = F1 |
      select_left (Or(F1,F2)) = F1

  fun select_right (And(F1,F2)) = F2 |
      select_right (Or(F1,F2)) = F2 |
      select_right (Diamond(_,_,F)) = F |
      select_right (Box(_,_, F))= F 

  fun get_left(Diamond(m, free a, f))=  a
    | get_left(Box(m, free a, f)) = a 	
    | get_left _ = raise bug

  fun instantiate_name n x (free y) = free y 
    | instantiate_name m x (bound n) =
        if n = m then free x else bound n (*(n-1)*)

  fun instantiate x (True) n = True 
    | instantiate x (False) n = False 
    | instantiate x (IsEq(v,w)) n =
        IsEq(instantiate_name n x v,instantiate_name n x w) 
    | instantiate x (IsNeq(v,w)) n =
        IsNeq(instantiate_name n x v,instantiate_name n x w)
    | instantiate x (And(F1,F2)) n = And(instantiate x F1 n,instantiate x F2 n) 
    | instantiate x (Or(F1,F2)) n = Or(instantiate x F1 n,instantiate x F2 n) 
    | instantiate x (Diamond(m, a,F)) n = Diamond(m, instantiate_name n x a,instantiate x F n) 
    | instantiate x (Box(m, a, F)) n = Box(m, instantiate_name n x a, instantiate x F n) 
    | instantiate x (RootedVar(X,vl)) n =
       RootedVar(X,map (instantiate_name n x) vl) 
    | instantiate x (RootedGFP(X,n,F,vl)) l =
        RootedGFP(X,n,F,map (instantiate_name l x) vl) 
        (* NB: The only free names of RootedGFP(X,n,F,vl) are in vl! *)
    | instantiate x (RootedLFP(X,n,F,vl)) l =
        RootedLFP(X,n,F,map (instantiate_name l x) vl) 
    | instantiate x (RootedCon(U,vl)) n =
        RootedCon(U, map (instantiate_name n x) vl) 
    | instantiate x (Sigma F) n = Sigma (instantiate x F (n+1)) 
    | instantiate x (BSigma F) n = BSigma (instantiate x F (n+1))
    | instantiate x (Exists F) n = Exists (instantiate x F (n+1))
    | instantiate x (Forall F) n = Forall (instantiate x F (n+1))

  fun instantiate_list n nil F = F 
    | instantiate_list n (x::nl) F = instantiate_list (n+1)(*LHE*) nl (instantiate x F n)

  fun successor x (Diamond(m, free a ,F)) = subst x a F     
    | successor x (Box(m, free a, F)) = subst x a F 
    | successor x (Sigma F) = instantiate x F 1 
    | successor x (BSigma F) = instantiate x F 1
    | successor x (Exists F) = instantiate x F 1
    | successor x (Forall F) = instantiate x F 1

  fun select_name nil = nil 
    | select_name ((free x)::vl) = x::(select_name vl)

  fun const_subst U X (True) = True
    | const_subst U X (False) = False 
    | const_subst U X (IsEq(v,w)) = IsEq(v,w) 
    | const_subst U X (IsNeq(v,w)) = IsNeq(v,w) 
    | const_subst U X (And(F1,F2)) =
        And(const_subst U X F1,const_subst U X F2) 
    | const_subst U X (Or(F1,F2)) =
        Or(const_subst U X F1,const_subst U X F2) 
    | const_subst U X (Diamond(m, a, F)) =
        Diamond(m, a,const_subst U X F) 
    | const_subst U X (Box(m, a,F)) =
        Box(m, a,const_subst U X F) 
    | const_subst U X (RootedVar(Y,vl)) =
        if P.eq X Y then RootedCon(U,vl) else RootedVar(Y,vl) 
    | const_subst U X (RootedGFP(Y,n,F,vl)) =
        RootedGFP(Y,n,const_subst U (P.next [X]) (*LHE*) F,vl) 
    | const_subst U X (RootedLFP(Y,n,F,vl)) =
        RootedLFP(Y,n,const_subst U (P.next [X])(*LHE*) F,vl) 
    | const_subst U X (RootedCon(V,vl)) = RootedCon(V,vl) 
    | const_subst U X (Sigma F) = Sigma(const_subst U X F) 
    | const_subst U X (BSigma F) = BSigma(const_subst U X F) 
    | const_subst U X (Exists F) = Exists (const_subst U X F)
    | const_subst U X (Forall F) = Forall (const_subst U X F)

  fun get_propvar (GFP(X,n,F)) = X 
    | get_propvar (LFP(X,n,F)) = X

  fun get_arity (GFP(X,n,F)) = n
    | get_arity (LFP(X,n,F)) = n

  fun get_body _ _ = raise Lib.disaster "F.get_body called"

  fun root (GFP(X,n,F)) nl = RootedGFP(X,n,F,map free nl) 
    | root (LFP(X,n,F)) nl = RootedLFP(X,n,F,map free nl)

  fun unroot (RootedGFP(X,n,F,nl)) = GFP(X,n,F) 
    | unroot (RootedLFP(X,n,F,nl)) = LFP(X,n,F)

  fun params (RootedCon(U,vl)) = select_name vl
    | params (RootedLFP(_,_,_,nl)) = select_name nl 
    | params (RootedGFP(_,_,_,nl)) = select_name nl 

  fun unfold U (RootedGFP(X,n,F,vl)) =
        const_subst U X (instantiate_list 1 (select_name vl) F)
    | unfold U (RootedLFP(X,n,F,vl)) =
        const_subst U X (instantiate_list 1 (select_name vl) F)

  fun f_constants (True) = nil 
    | f_constants (False) = nil 
    | f_constants (IsEq(v,w)) = nil 
    | f_constants (IsNeq(v,w)) = nil 
    | f_constants (And(F1,F2)) = (f_constants F1) @ (f_constants F2) 
    | f_constants (Or(F1,F2)) = (f_constants F1) @ (f_constants F2) 
    | f_constants (Diamond(m, a, F)) =  f_constants F 
    | f_constants (Box(m, a, F)) =  f_constants F 
    | f_constants (RootedVar(X,vl)) = nil 
    | f_constants (RootedGFP(X,n,F,vl)) = f_constants F 
    | f_constants (RootedLFP(X,n,F,vl)) = f_constants F 
    | f_constants (RootedCon(U,vl)) = [U] 
    | f_constants (Sigma F) = f_constants F 
    | f_constants (BSigma F) = f_constants F 
    | f_constants (Exists F) = f_constants F
    | f_constants (Forall F) = f_constants F  

  fun constants (GFP(X,n,F)) = f_constants F 
    | constants (LFP(X,n,F)) = f_constants F

  fun constant (RootedCon(U,_)) = U

  fun var_free_names (free x) = [x] 
    | var_free_names (bound n) = nil

  fun vl_free_names nil = nil 
    | vl_free_names ((free x)::vl) = x::(vl_free_names vl) 
    | vl_free_names ((bound n)::vl) = vl_free_names vl

  fun free_names (True) = nil 
    | free_names (False) = nil 
    | free_names (IsEq(v,w)) = (var_free_names v)@(var_free_names w) 
    | free_names (IsNeq(v,w)) = (var_free_names v)@(var_free_names w) 
    | free_names (And(F1,F2)) = (free_names F1) @ (free_names F2) 
    | free_names (Or(F1,F2)) = (free_names F1) @ (free_names F2) 
    | free_names (Diamond(m, a, F)) = (var_free_names a) @ (free_names F) 
    | free_names (Box(m, a, F)) =  (var_free_names a) @ (free_names F) 
    | free_names (RootedVar(X,vl)) = vl_free_names vl 
    | free_names (RootedGFP(X,n,F,vl)) = vl_free_names vl 
    | free_names (RootedLFP(X,n,F,vl)) = vl_free_names vl 
    | free_names (RootedCon(U,vl)) = vl_free_names vl 
    | free_names (Sigma F) = free_names F 
    | free_names (BSigma F) = free_names F 
    | free_names (Exists F) = free_names F
    | free_names (Forall F) = free_names F


fun conjuncts(form)= if is_and(form) then select_left(form)::conjuncts(select_right(form))
		     else []
  
(*   | conjuncts(_) = [] *)


end;    (* PFormula *)













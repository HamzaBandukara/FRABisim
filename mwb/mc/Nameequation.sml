functor Nameequation(structure Name : NAME) : NAMEEQUATION =


(* The datatype Nameequation is on the form of equivalences and
   in-equivalences between names, and is called Gamma in the 
   texts describing this calculus. A name-equation can look like
   x=y & y&z & z#w. Note that it is conjunctive and finite. 
  This implementation also performs closure to a set of equations.
  For the above example, a closure would mean that there are perhaps 
  more equations as a conclusion from the data structure:
  x#w (since x=y=z, and z#w.), and so on. This is achieved by the
  use of equivalence-classes: An eq-class is a list of names that 
  are all equal to each other. For each eq-class, there is a list of 
  references to other eq-classes, that are INequal to all names in this class.
  For the example above, we would get two  entries of the form
  [(eq-class), (list of eq-classes that are inequal to the current)]
  as:
  [(x,y,z), [ref(w)]],
  [(w), [ref(x,y,z)]] 
  as our name-equation.   

*)

struct
structure N = Name

type eqclass	=	N.name list 

type ineqclass	=	(eqclass ref) list 

type nameequation =	(eqclass * ineqclass) list  

exception inconsistence (* not implemented  *)




(* predicates *)
(*############*)
fun member(a, [])=false
  | member (a, b::lst)= 
    N.eq(a, b) orelse member(a, lst)
(*------------------------------------------*)
fun eq_implies(n1, n2, []) = if N.eq(n1,n2) then true else false
  | eq_implies(n1, n2, (eq, ineq)::rest) =
     member(n1, eq) andalso member(n2,eq)
     orelse eq_implies(n1, n2, rest)
(*------------------------------------------*)
fun ineq_implies(n1, n2, []) = if N.eq(n1, n2) then false else true
  | ineq_implies(n1, n2, (eq, ineq)::rest) =
let
   fun ineq_member(n, ineq) =
   case ineq of
    []			=> false
   |(ineqentry::lst)	=> member(n, !(ineqentry)) orelse
			   ineq_member(n, lst)
in
   member(n1, eq) andalso ineq_member(n2, ineq)
   orelse ineq_implies(n1, n2, rest)
end
(*------------------------------------------*)
(*fun eqclass_exists *)
fun eqclass_exists(name, []) = false
  | eqclass_exists(name, (eq, ineq)::rest) =
     member(name, eq) orelse eqclass_exists(name, rest)
(*------------------------------------------*)
fun name_in(name, []) = false
  | name_in(name, (eq, ineq)::rest) =
     member(name, eq) orelse name_in(name, rest)
(*------------------------------------------*)
fun is_consistent(n1, n2, [])= true  
  | is_consistent(n1, n2, gamma)=
     eq_implies(n1, n2, gamma) orelse not(ineq_implies(n1, n2, gamma))
(*------------------------------------------*)
(* functions *)
(* ######### *)
(* assumes name already in an eq-class in gamma *)
fun update1Eq(name, newName, (eq, ineqreflist)::rest) =
    if member(name, eq) then (newName::eq, ineqreflist)::rest
     else (eq, ineqreflist)::update1Eq(name, newName, rest)
(*------------------------------------------*)
(* special case when two equivalence-classes already exist *)
(* They must be merged along with their ineq-references *)
fun update2Eq(n1, n2, (eq, ineqreflist)::rest) =
let
   fun eqmerge((eq, ineqreflist), name, []) = (name::eq, ineqreflist)
   fun eqmerge((eq, ineqreflist), name, (eq1, ineq1)::rest) =
       if member(name, eq1) then (eq@eq1, ineqreflist@ineq1)::rest
        else (eq1, ineq1)::eqmerge((eq, ineqreflist), name, rest)
in
   if member(n1, eq) then eqmerge((eq, ineqreflist), n2, rest)
    else 
      if member(n2, eq) then eqmerge((eq, ineqreflist), n1, rest)
       else (eq, ineqreflist)::update2Eq(n1, n2, rest) 
end
(*------------------------------------------*)
fun addEq(n1, n2, []) = [([n1, n2],[])]
  | addEq(n1, n2, gamma)=
    if eq_implies(n1, n2, gamma) then gamma
    else
      if ineq_implies(n1, n2, gamma) then raise inconsistence
       else
	   let 
		val name1exists = eqclass_exists(n1, gamma)
		val name2exists = eqclass_exists(n2, gamma)
           in
	   if name1exists andalso name2exists then
	      update2Eq(n1, n2, gamma)
	   else if name1exists then update1Eq(n1, n2, gamma)
		 else if name2exists then
			 update1Eq(n2, n1,  gamma)
		      else ([n1, n2],[])::gamma	
	   end				 		
          		
(*--------------------------------------------*)
fun eqclassref(name, []) = ref []
  | eqclassref(name, (eq, ineqreflist)::rest)=
     if member(name, eq) then ref eq else eqclassref(name, rest)  
(*------------------------------------------*)
(* fun updateIneq *) 
(* no base case, not called if empty gamma *)
fun updateIneq(name1, name2, gamma) = 
let
   val n1eq = eqclassref(name1, gamma)
   val n2eq = eqclassref(name2, gamma)
   fun upd(n1, n2, n1eq, n2eq, []) = []
     | upd(n1, n2, n1eq, n2eq, (eq, ineqreflist)::rest) =
       if member(n1, eq) then
          (eq, n2eq::ineqreflist)::upd(n1, n2, n1eq, n2eq, rest)
        else 
            if member(n2, eq) then
               (eq, n1eq::ineqreflist)::upd(n1, n2, n1eq, n2eq, rest)
            else
               (eq, ineqreflist)::upd(n1, n2, n1eq, n2eq, rest) 
in 
  upd(name1, name2, n1eq, n2eq, gamma)
end
(*------------------------------------------*)
(* fun makeIneqEntry *)
fun makeIneqEntry(name1, ineq_ref)=
([([name1],[ineq_ref])])
(*------------------------------------------*)
fun addIneq(n1, n2, []) =
    let 
       val firstEntry = [n1]
       val secondEntry = [n2]
    in
      [(firstEntry,[ref secondEntry]), (secondEntry, [ref firstEntry])]
    end
  | addIneq(n1, n2, gamma) =
    let
       val name1exists = eqclass_exists(n1, gamma)
       val name2exists = eqclass_exists(n2, gamma)
    in
       if eq_implies(n1, n2, gamma) 
        then raise inconsistence
       else
        if name1exists andalso name2exists 
           then updateIneq(n1, n2, gamma)
         else
             if name1exists then 
		let
		   val newEntry = makeIneqEntry(n2, eqclassref(n1,gamma))
		in
	           updateIneq(n1, n2, newEntry@gamma)
                end  
		else 
		    if name2exists then 
		       let 
			val newEntry = makeIneqEntry(n1, eqclassref(n2, gamma))
		       in
				updateIneq(n1, n2, newEntry@gamma)
			end
		     else 
			 let
			    val firstEntry = [n1]
			    val secondEntry = [n2]
			 in
			    [(firstEntry,[ref secondEntry]), 
				(secondEntry, [ref firstEntry])]@gamma
			end
      end



(*------------------------------------------*)
fun allpairs(n1, []) = []
  | allpairs(n1, n2::rest)=
    [(n1, n2)]@allpairs(n1, rest)
(*------------------------------------------*)
fun namepairs([]) = []
  | namepairs(name::rest)=
    allpairs(name, rest)@namepairs(rest)
(*------------------------------------------*)
fun occ_names([]) = []
  | occ_names((eq, ineq)::rest) =
    eq@occ_names(rest)
(*------------------------------------------*)
fun imply_same(n1, n2, neqt1, neqt2)=
   if eq_implies(n1,n2, neqt2) andalso not(eq_implies(n1, n2, neqt1))
    then false  
   else if ineq_implies(n1, n2, neqt2) andalso not(ineq_implies(n1, n2, neqt1))
         then false
   else true
(*------------------------------------------*)
fun test_for_quiet( [], _, _) = true  
  | test_for_quiet((n1, n2)::namelist, neqt1, neqt2) =
if (name_in(n1, neqt1) andalso name_in(n2, neqt2))
   then 
    (imply_same(n1, n2, neqt1, neqt2)   
     andalso test_for_quiet(namelist, neqt1, neqt2))      
     else test_for_quiet(namelist, neqt1, neqt2)
(*------------------------------------------*)
(* nameequat1 is QUIET with respect to nameequat2 if no new 
   information on parameters/names occuring in nameequat1 is
   added to nameequat2. However, Nameequat2 may contain information
   about OTHER names/parameters, NOT occuring in nameequat1. *)
fun quiet(nameequat1, nameequat2)=
let
   val all_names = occ_names(nameequat2)
   val eq2names = namepairs(all_names)
in
  test_for_quiet(eq2names, nameequat1, nameequat2)
end
(*----------------------------------------*)
(* nameequation1 IMPLIES nameequation2 iff
   forall names (x,y) in nameequation2:
   if nameequation2 |-x=y then nameequation1 |-x=y
                       or
   if nameequation2 |-x#y then nameequation1 |-x=y    
this is a stronger relation than QUIET, because it demands that for every
occurence of an equation and its variables in nqet2, there MUST be a
similar entry in neqt1, unlike the quiet-relation, that only requires 
that IF the variables exist in neqt1, then they must have the same
relation as in neqt2. *)
fun equation_implies(neqt1, neqt2)=
let 
    val n2nameqs = namepairs(occ_names(neqt2))  
    fun test_for_neqt_implication([], _, _) = true
      | test_for_neqt_implication((x, y)::restnames, implier, impleyee)=
    ( eq_implies(x, y, impleyee) andalso eq_implies(x, y, implier)
                                 orelse
      ineq_implies(x,y,impleyee) andalso ineq_implies(x,y, implier) )
    andalso test_for_neqt_implication(restnames, implier, impleyee)
in 
 test_for_neqt_implication(n2nameqs, neqt1, neqt2)	   
end
(*------------------------------------------*)


fun get_all_equals(name, [])= []
  | get_all_equals(name, (eq, ineqref)::rest) =
    if member(name, eq) then eq else get_all_equals(name, rest)


fun get_all_eq_classes([])=[]
  | get_all_eq_classes((eq, ineqref)::rest)=
	eq::get_all_eq_classes(rest)


val  mk_empty = nil 


fun names([])=[]
  | names((eq,ineq)::rest) = eq@names(rest);



fun eq(ne1, ne2) = equation_implies(ne1, ne2) andalso equation_implies(ne2, ne1)



end;








functor StringFormula(structure PropVar: SPROPVAR
(*                 structure Constant: CONSTANT *)
                structure Act: SACTION): SFORMULA =
struct

(*   structure CST = Constant *)
  structure ACT = Act
  structure P = PropVar


(*     datatype variable = ACT.N.name *)
    datatype formula = True (* of unit *)
                   | False (* of unit *)
                   | IsEq of ACT.N.name * ACT.N.name
                   | IsNeq of ACT.N.name * ACT.N.name
                   | And of formula * formula
                   | Or of formula * formula
                   | Diamond of ACT.action * formula
                   | Box of ACT.action * formula
                   | RootedVar of P.propvar * ACT.N.name list
                   | RootedGFP of
                         P.propvar * ACT.N.name list * formula * ACT.N.name list
                   | RootedLFP of
                         P.propvar * ACT.N.name list * formula * ACT.N.name list
(*                    | RootedCon of CST.constant * ACT.N.name list *)
                   | Sigma of ACT.N.name * formula
                   | BSigma of ACT.N.name * formula
                   | Pi of ACT.N.name * formula
                   | Exists of ACT.N.name * formula
		   | Not of formula

    fun mkstr True = "TT"
      | mkstr False = "FF"
      | mkstr (IsEq(a,b)) = (ACT.N.mkstr a)^"="^(ACT.N.mkstr b)
      | mkstr (IsNeq(a,b))= (ACT.N.mkstr a)^"#"^(ACT.N.mkstr b)
      | mkstr (And(f,g)) = "("^(mkstr f)^" & "^(mkstr g)^")"
      | mkstr (Or(f,g)) = "("^(mkstr f)^" | "^(mkstr g)^")"
      | mkstr (Diamond(a,f)) = "<"^(ACT.mkstr a)^">"^(mkstr f)
      | mkstr (Box(a,f)) = "["^(ACT.mkstr a)^"]"^(mkstr f)
      | mkstr (RootedVar(p,nl)) = (P.mkstr p)^"("^(Lib.mapconcat ACT.N.mkstr nl ",")^")"
      | mkstr (RootedGFP(p,fl,f,al)) =
	"(max "^(P.mkstr p)^"("^(Lib.mapconcat ACT.N.mkstr fl ",")^")."^(mkstr f)^")("^(Lib.mapconcat ACT.N.mkstr al ",")^")"
      | mkstr (RootedLFP(p,fl,f,al)) =
	"(min "^(P.mkstr p)^"("^(Lib.mapconcat ACT.N.mkstr fl ",")^")."^(mkstr f)^")("^(Lib.mapconcat ACT.N.mkstr al ",")^")"
      | mkstr (Sigma(n,f)) = "Sigma "^(ACT.N.mkstr n)^"."^(mkstr f)
      | mkstr (BSigma(n,f)) = "Bsigma "^(ACT.N.mkstr n)^"."^(mkstr f)
      | mkstr (Pi(n,f)) = "all "^(ACT.N.mkstr n)^"."^(mkstr f)
      | mkstr (Exists(n,f)) = "some "^(ACT.N.mkstr n)^"."^(mkstr f)
      | mkstr (Not f) = "not("^(mkstr f)^")"

    fun free_names True = []
      | free_names False = []
      | free_names (IsEq(a,b)) = [a,b]
      | free_names (IsNeq(a,b)) = [a,b]
      | free_names (And(f,g)) = (free_names f)@(free_names g)
      | free_names (Or(f,g)) = (free_names f)@(free_names g)
      | free_names (Diamond(ACT.Tau,f)) = free_names f
      | free_names (Diamond(ACT.Input a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Diamond(ACT.Output a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Box(ACT.Tau,f)) = free_names f
      | free_names (Box(ACT.Input a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Box(ACT.Output a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (RootedVar(p,nl)) = nl
      | free_names (RootedGFP(p,fl,f,al)) =
	al@(Lib.filter (fn n=>not(Lib.member ACT.N.eq (n,fl))) (free_names f))
      | free_names (RootedLFP(p,fl,f,al)) =
	al@(Lib.filter (fn n=>not(Lib.member ACT.N.eq (n,fl))) (free_names f))
      | free_names (Sigma(a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (BSigma(a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Pi(a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Exists(a,f)) =
	Lib.filter (fn n=>not(ACT.N.eq(n,a))) (free_names f)
      | free_names (Not f) = (free_names f)

end;    (* Formula *)

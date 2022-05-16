signature SEQUENT =
sig

    structure F : FORMULA
    structure C : CONDITION
    structure D : DEF_LIST
    structure A : McAGENT

    datatype sequent = mk_sequent of
       C.cond * D.def_list * A.agent * F.formula

    val new_name: sequent -> F.ACT.N.name

end

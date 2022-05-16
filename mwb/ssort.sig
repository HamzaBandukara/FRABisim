signature SoSORT =
sig
    structure N : SoNAME
    structure A : SoAGENT
    structure E : ENV

    type sorting
    type obsort

    exception SortError of string

    val s_mkstr : sorting -> string
    val ob_mkstr : obsort -> string
    val sort : A.agent * A.agent E.env * 'a E.env -> sorting * obsort

    (* debugging *)
    val empty_obsort : unit -> obsort
    val obsort_add : N.name * obsort ref -> obsort
    val obsort_tail : obsort ref -> obsort ref
    val undefined_obsort : unit -> obsort
    val empty_sorting : unit -> sorting
    val add_obsort : N.name * obsort ref * sorting -> sorting
    type eqclass
    val empty_eqclass : string -> eqclass
    val eq_add : N.name * eqclass -> eqclass
    val add_eq_obsort : eqclass * obsort ref * sorting -> sorting

    val sort_lub : sorting * sorting -> sorting
end

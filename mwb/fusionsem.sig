signature FUSIONSEM =
sig
    structure A : FAGENT
    structure C : COND

    datatype commitment = Comm of C.cond * A.Act.action * A.agent

    val c_mkstr : commitment -> string
    val c_makstr : commitment * string list -> string
    val cw_mkstr : commitment -> string
    val cw_makstr : commitment * string list -> string

    (* commitments *)
    val commitments : A.agent * (A.agent * int) A.E.env -> commitment list
    (* weak commitments *)
    val weakcomm : A.agent * (A.agent * int) A.E.env -> commitment list

    val bisimilar : A.agent * A.agent * (A.agent * int) A.E.env -> bool
    val bisimulation : A.agent * A.agent * (A.agent * int) A.E.env -> (A.agent * A.agent) list
    val weakbisimilar : A.agent * A.agent * (A.agent * int) A.E.env -> bool
    val weakbisimulation : A.agent * A.agent * (A.agent * int) A.E.env -> (A.agent * A.agent) list

    (* commitments *)
    val ccommitments : C.cond -> A.agent * (A.agent * int) A.E.env -> commitment list
    (* weak commitments *)
    val cweakcomm : C.cond -> A.agent * (A.agent * int) A.E.env -> commitment list

    val cbisimilar : A.agent * A.agent * (A.agent * int) A.E.env * C.cond -> bool
    val cbisimulation : A.agent * A.agent * (A.agent * int) A.E.env * C.cond -> (A.agent * A.agent * C.cond) list
    val cweakbisimilar : A.agent * A.agent * (A.agent * int) A.E.env * C.cond -> bool
    val cweakbisimulation : A.agent * A.agent * (A.agent * int) A.E.env * C.cond -> (A.agent * A.agent * C.cond) list

    val cleartbls : unit -> unit
    val desctbls : unit -> unit
    val enabletbls : bool -> unit
    val enabledtbls : unit -> bool
end


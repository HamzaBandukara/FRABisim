signature OPENSEM =
sig
    structure B : OAGENT
    structure C : COND

    datatype commitment = Comm of C.cond * B.Act.action * B.agent

    val c_mkstr : commitment -> string
    val cw_mkstr : commitment -> string
    val c_makstr : commitment * (string list) -> string
    val cw_makstr : commitment * (string list) -> string

    val commitments : C.cond -> B.agent * B.agent B.E.env -> commitment list
    val tauclose : C.cond -> B.agent * B.agent B.E.env -> commitment list
    val weakcomm : C.cond -> B.agent * B.agent B.E.env -> commitment list

    val cleartbls : unit -> unit
    val desctbls : unit -> unit
    val enabletbls : bool -> unit
    val enabledtbls : unit -> bool

    val bisimilar : B.agent * B.agent * B.agent B.E.env * C.cond-> bool
    val bisimulation : B.agent * B.agent * B.agent B.E.env * C.cond -> (B.agent * B.agent * C.cond) list
    val weakbisimilar : B.agent * B.agent * B.agent B.E.env * C.cond -> bool
    val weakbisimulation : B.agent * B.agent * B.agent B.E.env * C.cond -> (B.agent * B.agent * C.cond) list
end
	

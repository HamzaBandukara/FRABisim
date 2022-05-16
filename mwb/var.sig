(************************************ Var ************************************)
(*                                                                           *)
(*  This is the definitions of "Variables".           Joachim Parrow Sept-86 *)
(*                                                                           *)
(*****************************************************************************)

signature VAR =
sig
   type var

   val mkvar : string -> var
   val mkstr : var -> string

   val eq    : var * var -> bool
   val le    : var * var -> bool
end


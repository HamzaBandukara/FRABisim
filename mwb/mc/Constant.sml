functor Constant():CONSTANT =
struct
  type constant = int

  fun mkstr (n:constant) = "C"^(Lib.mkstrint n)

  fun eq n m = n=m

  val init = 0

  fun next n = n+1

  fun l_eq (n:constant) (m:constant) = (n <= m)
 
  fun g_eq (n:constant) (m:constant) = (n >= m)

end;

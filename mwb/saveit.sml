let fun vrsn () =
	let val i = TextIO.openIn "Version"
	    val line = case TextIO.inputLine i of SOME x => x | NONE => ""
	    val ver = (fn (l) =>
		       if size l > 0 andalso substring(l,(size l)-1,1) = "\n"
			   then substring(l,0,(size l)-1)
		       else l) line
	in
	    TextIO.closeIn i;
	    ver
	end
    val date = Date.toString(Date.fromTimeLocal(Time.now()));
    val ver = vrsn() handle (IO.Io _) => "Unknown version"
in
    SMLofNJ.exportFn("mwb",(fn _ => (Top.toplevel(ver^", built "^date);
				     OS.Process.success)))
end

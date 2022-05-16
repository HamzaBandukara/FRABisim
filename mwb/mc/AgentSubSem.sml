functor AgentSubSem(structure Agent: McAGENT
                    structure NameSubstitution: NAMESUBSTITUTION
                    structure Boolean: COND
                    sharing NameSubstitution.B = Boolean
                    sharing Agent.B = Boolean
                    sharing NameSubstitution.N
                             = Agent.ACT.N
                    sharing Agent.ACT.N
                             = Boolean.N): AGENTSUBSEM =
struct

  structure A = Agent

  structure NS = NameSubstitution

  structure B = Boolean

  exception name_substitution_too_small

  exception open_agent_encountered

(*  exception not_yet_implemented *)

  exception normal_form_expected

  exception process_expected

  fun ns_inc ns = (* Urk. /BV *)
      (NS.pack (map (fn l=> map (fn n=>(NS.N.increment(n,1))) l)
		(NS.unpack ns)))

  fun normal_form A ns env =
    let val _ = if !Flags.tracelevel >1 then Lib.dprint(1,"*normal_form "^(A.mkstr A)^"\n") else ()
	val xx =
	if A.is_nil A env
        then A
        else
        if A.is_sum A env
        then A.mk_sum (normal_form (A.sum_left A env) ns env)
                      (normal_form (A.sum_right A env) ns env)
        else
        if A.is_prefix A env
        then A
        else
        if A.is_par A env
        then (* More than you'd think. /BV *)
	    let val al = (normal_form (A.par_left A env) ns env)
		val ar = (normal_form (A.par_right A env) ns env)
		fun absall p =
		    if not(A.is_concretion p env) then
			let val (n,q) = absall(A.abstraction_agent p env)
			in (n+1,q) end
		    else (0,p)
		fun concall p =
		    if A.is_restriction p env then
			let val (n,c,q) = concall(A.restriction_agent p env)
			in if null c then (0,[],p)
			   else (n+1,c,q)
			end
		    else if not(A.is_abstraction p env) then
			let val (n,c,q) = concall(A.concretion_right p env)
			in (n,(NS.N.increment((A.concretion_left p env),n))::c,
			    q)
			end
		    else (0,[],p)
		fun mkabs 0 p = p
		  | mkabs n p = A.mk_abstraction NS.N.Zero (mkabs (n-1) p)
		fun mkres 0 p = p
		  | mkres n p = A.mk_restriction NS.N.Zero (mkres (n-1) p)
		fun mkconc [] p = p
		  | mkconc (n::r) p = A.mk_concretion n (mkconc r p)
		fun incr n names ag =
		    let val sub = map (fn x=> (NS.N.increment(x,n),x)) names
		    in A.substitute sub ag
		    end
	    in
		if A.is_process al env andalso A.is_process ar env then
		    A.mk_par al ar
		else if (A.is_abstraction al env
			 andalso A.is_abstraction ar env) then
		     (* (\pP | \qQ) = (\pq)(P f+|\q|,b+|\q| | Q f+|\p| *)
		     (* meaning that in P you have to increment all free idx, *)
		     (* including the ones bound in the \p abstraction, *)
		     (* while in Q, you only increment the ones free in \Q *)
		     let val (nl,ql) = absall al
			 val fl = A.free_names ql
			 val (nr,qr) = absall ar
			 val fr = Lib.filter (fn n=>NS.N.code(n) >= nr) (A.free_names qr)
		     in
			 mkabs (nl+nr)
			 (A.mk_par
			  (incr nr fl ql)
			  (incr nl fr qr))
		     end
		else if (A.is_concretion al env
			 andalso A.is_concretion ar env) then
		    (* ((^n)[x]P | (^m)[y]Q) => (^nm)[x+m y](P fb+m | Q f+n) *)
		    (* similarly *)
		    let val (nl,cl,ql) = concall al
			val fl = A.free_names ql
			val (nr,cr,qr) = concall ar
			val fr = Lib.filter (fn n=>NS.N.code(n) >= nr) (A.free_names qr)
		    in
			mkres (nl+nr)
			(mkconc ((map (fn n=>NS.N.increment(n,nr)) cl)@cr)
			 (A.mk_par
			  (incr nr fl ql)
			  (incr nl fr qr)))
		    end
		else
		    A.mk_par al ar
	    end
			    
        else
        if A.is_conditional A env (* abstract syntax bAB, b a boolean *)
        then
          if McList.subset NS.N.curry_eq (B.domain (A.get_boolean A env)) (NS.domain ns)
          then
            if NS.entails ns (A.get_boolean A env)
            then normal_form (A.cond_positive A env) ns env
            else normal_form (A.cond_negative A env) ns env
          else raise name_substitution_too_small
        else
        if A.is_application A env
        then
          normal_form (A.abstraction_right (*A.mk_application*)
                          (A.appl_arg A env)
                          (normal_form (A.appl_fun A env) ns env) env) ns env
        else
        if A.is_restriction A env
        then
	    let val ag = A.restriction_agent A env
		val f = A.free_names ag
	    in
		if not (Lib.exists NS.N.zerop f)
		    (* restricted name not free *)
		    then normal_form (A.restriction_right NS.N.Zero A env) ns env
		else
		    let val nf = (normal_form ag
				  (NS.add_distinct NS.N.Zero (ns_inc ns)) env)
			fun bswap P =
			    A.substitute [(NS.N.Zero,NS.N.mkname("",1)),
					  (NS.N.mkname("",1),NS.N.Zero)] P
			fun ns_bswap ns =
			    NS.pack (map (fn l =>
					  map (fn n =>
					       if NS.N.zerop(n)
						   then NS.N.mkname("",1)
					       else if NS.N.eq(n,NS.N.mkname("",1))
							then NS.N.Zero
					       else n) l) (NS.unpack ns))
		    in
			if A.is_nil nf env
			    then nf	(* (^n)0 => 0 *)
			else if A.is_restriction nf env then
			    if not(A.is_abstraction (A.restriction_agent nf env) env) andalso not(A.is_restriction (A.restriction_agent nf env) env)
				(* A.is_concretion (A.restriction_agent nf env) env
				andalso not(A.is_process (A.restriction_agent nf env) env) *)
				then
				    let val _ = A.ag1 := A
				        val _ = A.ag2 := nf
					val s = A.restriction_agent nf env
					val n = A.concretion_left s env
				    in
					if NS.N.zerop n then
					    (* (^n)(^m)[m]P => (^m)[m](^n)P' *)
					    (A.mk_restriction NS.N.Zero
					     (normal_form
					      (A.mk_concretion n
					       (A.mk_restriction NS.N.Zero
						(bswap (A.concretion_right s env))))
					      (ns_inc (ns_bswap ns))
					      env))
					else
					    (A.mk_restriction NS.N.Zero nf)
				    end
			    else A.mk_restriction NS.N.Zero nf
			else if A.is_process nf env
			    then A.mk_restriction NS.N.Zero nf
			else if A.is_abstraction nf env 
			    then (* (^n)(\m)P => (\m)(^n)P{dec n,inc m} *)
				A.mk_abstraction NS.N.Zero
				(normal_form
				 (A.mk_restriction NS.N.Zero
				  (bswap (A.abstraction_agent nf env)))
				 (ns_inc (ns_bswap ns)) env)
			else if A.is_concretion nf env
				 then if NS.N.zerop (A.concretion_left nf env)
					  (* (^n)[n]P => (^n)[n]P *)
					  then A.mk_restriction NS.N.Zero nf
				      else
					  A.mk_concretion
					  (NS.N.pred (A.concretion_left nf env))
					  (normal_form
					   (A.mk_restriction NS.N.Zero
					    (A.concretion_right nf env))
					   ns env)
			else raise Lib.disaster ("unhandled case in ASS.normal_form: "^(A.mkstr nf))
		    end
	    end		     
(* ****************
          let val _ = if !Flags.tracelevel > 1 then print ("*is_restriction "^(A.mkstr A)^"\n") else ()
	      (* val x = NS.N.next (A.free_names A); *)
	      (* /LHE *)
	      val ns = NS.restrict ns (A.free_names A); 
              val bar = A.free_names A;
              val x = NS.N.next (bar);
              val _ = if !Flags.tracelevel > 1 then print ("free names: "^(Lib.mapconcat NS.N.mkstr bar ",")^"\n") else();
	      (* end /LHE *)
	      val A1 = normal_form (A.restriction_right x A env)
                               (NS.add_distinct x ns) env
          in
            if McList.member NS.N.curry_eq x (A.free_names A1)
            then
              if A.is_process A1 env
              then A.mk_restriction x A1
              else
              if A.is_abstraction A1 env
              then
                let val y = NS.N.next (A.free_names A1);
                    val A2 = A.abstraction_right y A1 env
                in A.mk_abstraction y (A.mk_restriction x A1) end
              else
              if A.is_concretion A1 env
              then
                if NS.N.eq ((A.concretion_left A1 env), x)
                then A.mk_bconcretion x A1
                else A.mk_concretion
                       (A.concretion_left A1 env)
                       (A.mk_restriction x (A.concretion_right A1 env))
              else (* A is bound concretion *)
                let val y = NS.N.next (A.free_names A1);
                    val A2 = A.bconcretion_right y A1 env
                in
                  A.mk_bconcretion y (A.mk_restriction x A2)
                end
            else A1
          end
**************** *)
        else
        if A.is_abstraction A env	(* Moved from before is_application /BV *)
        then A
        else
        if A.is_identifier A env
        then (* raise open_agent_encountered *)
	    normal_form (A.identifier_def A env) ns env
(*        else
        if A.is_recursive_agent A env
        then raise not_yet_implemented
       *)
        else A (* A is a concretion and thus in normal form *)
       val _ =  if !Flags.tracelevel > 1 then
          Lib.dprint (~1,"*=>"^(A.mkstr xx)^"\n") else ()
    in
	xx
            end

  fun is_normal_form A e =
        if A.is_nil A e
        then true
        else
        if A.is_sum A e
        then is_normal_form (A.sum_right A e) e
             andalso is_normal_form (A.sum_left A e) e
        else
        if A.is_prefix A e
        then true
        else
        if A.is_par A e
        then is_normal_form (A.par_right A e) e
             andalso is_normal_form (A.par_left A e) e
        else
        if A.is_conditional A e
        then false
        else
        if A.is_application A e
        then false
        else
        if A.is_restriction A e
        then
          A.is_bconcretion A e
          orelse
            let val x = NS.N.next (A.free_names A)
            in is_normal_form (A.restriction_right x A e) e end
        else
        if A.is_identifier A e
        then false
(*         else                        *)
(*         if A.is_recursive_agent A e *)
(*         then false                  *)
        else
        if A.is_concretion A e
        then true
        else A.is_abstraction A e
         

fun commitments ns A e =
 let val _ = if !Flags.tracelevel > 1 then print("*commitments "^(NS.mkstr ns)^(A.mkstr A)^" e\n") else ();
 in
      if is_normal_form A e
      then
        if A.is_nil A e
        then nil
        else
        if A.is_sum A e
        then (commitments ns (A.sum_right A e) e)@(commitments ns (A.sum_left A e) e)
        else
        if A.is_prefix A e
        then [(A.prefix_left A e,A.prefix_right A e)]
        else
        if A.is_par A e
        then
          let fun left_goes nil A2 = nil |
                  left_goes ((a,A1)::cl) A2 =
                      (a,A.mk_par A1 A2)::(left_goes cl A2);
              fun right_goes A1 nil = nil |
                  right_goes A1 ((a,A2)::cl) =
                      (a,A.mk_par A1 A2)::(right_goes A1 cl);
              fun match_filter (a,A1) nil ns = nil |
		  match_filter (a,A1) ((b,A2)::cl) ns =
		  if A.ACT.is_input(a) andalso A.ACT.is_output(b) then
		      if NS.is_eq (A.ACT.name a) (A.ACT.name b) ns
			  then
			      let val _ = if Flags.trace() then 
				  print("**matching "^(A.ACT.mkstr a)^" and "^(A.ACT.mkstr b)^"\n") else () in
			      (A.ACT.mk_tau(),A.pseudo_appl A1 A2 e)
			      ::(match_filter (a,A1) cl ns)
			      end
		      else match_filter (a,A1) cl ns
		  else if A.ACT.is_output(a) andalso A.ACT.is_input(b) then
		      if NS.is_eq (A.ACT.name a) (A.ACT.name b) ns
			  then 
			      let val _ = if Flags.trace() then 
				  print("**matching "^(A.ACT.mkstr a)^" and "^(A.ACT.mkstr b)^"\n") else () in
			      (A.ACT.mk_tau(),A.pseudo_appl A1 A2 e)
			      ::(match_filter (a,A1) cl ns) 
			      end
		      else match_filter (a,A1) cl ns
		  else match_filter (a,A1) cl ns
(*                  match_filter (A.ACT.mk_act x,A1)
                               ((A.ACT.mk_bar y,A2)::cl) ns =
                    if NS.is_eq x y ns
                    then (A.ACT.tau (),A.pseudo_appl A1 A2 e)
                            ::(match_filter (A.ACT.mk_act x,A1) cl ns)
                    else match_filter (A.ACT.mk_act x,A1) cl ns |
                  match_filter (A.ACT.mk_bar x,A1)
                               ((A.ACT.mk_act y,A2)::cl) ns =
                    if NS.is_eq x y ns
                    then (A.ACT.tau (),A.pseudo_appl A1 A2 e)
                            ::(match_filter (A.ACT.mk_bar x,A1) cl ns)
                    else match_filter (A.ACT.mk_bar x,A1) cl ns |
                  match_filter (a,A1) (hd::cl) ns = match_filter (a,A1) cl ns;
*)
              fun sync nil cl2 ns = nil |
                  sync ((a,A)::cl1) cl2 ns =
                    (match_filter (a,A) cl2 ns)@(sync cl1 cl2 ns)
              ; val lgarg = (commitments ns (A.par_left A e) e)
              ; val rgarg = (commitments ns (A.par_right A e) e)
              ; val _ = if !Flags.tracelevel > 1 then print("commitments par "^(NS.mkstr ns)^"  "^(A.mkstr A)^" e\n\n") else ()
              ; val _ = if !Flags.tracelevel > 1 then print((Lib.mapconcat (fn (ac,ag) => A.ACT.mkstr(ac)^" " ^A.mkstr(ag)) lgarg "\n")^"\n\n") else ()
              ; val _ = if !Flags.tracelevel > 1 then print((Lib.mapconcat (fn (ac,ag) => A.ACT.mkstr(ac)^" " ^A.mkstr(ag)) rgarg "\n")^"\n") else ()
          in (left_goes lgarg (A.par_right A e))
             @ (right_goes (A.par_left A e) rgarg)
             @ (sync lgarg rgarg ns)
          end
        else
        if A.is_process A e andalso A.is_restriction A e
        then
          let 
(* ****	      val x = NS.N.next (A.free_names A);
              val A1 = A.restriction_right x A e;
              val ns1 = NS.private x ns;
**** *)
	      val A1 = A.restriction_agent A e
	      val x = NS.N.Zero
	      val ns1 = NS.private x 
			(* Huga! /BV & LHE *)
			(ns_inc ns)
	      val _ = if !Flags.tracelevel > 1 then 
		  print("orig NS: "^(NS.mkstr ns)^"\npost NS: "^(NS.mkstr ns1)^"\n")
		  else ()
              fun filter nil = nil |
		  filter ((a,A2)::cl) =
		  if A.ACT.is_input(a) orelse A.ACT.is_output(a) then
		      if not(NS.N.le(NS.N.Zero,A.ACT.name a)) (* NS.N.eq(A.ACT.name a,x) *)
			  then filter cl
		      else ((a,A2)::(filter cl))
		  else (* tau *)
		      ((a,A2)::(filter cl))
(*                  filter ((A.ACT.mk_act y,A2)::cl) =
                    if NS.N.eq (x, y)
                    then filter cl
                    else ((A.ACT.mk_act y,A2)::(filter cl)) |
                  filter ((A.ACT.mk_bar y,A2)::cl) =
                    if NS.N.eq (x, y)
                    then filter cl
                    else ((A.ACT.mk_bar y,A2)::(filter cl)) |
                  filter ((A.ACT.tau (),A2)::cl) =
                    ((A.ACT.tau (),A2)::(filter cl))
*)
	      val cm = (commitments ns1 A1 e)
	      val _ = if !Flags.tracelevel > 1 then
		  print("commitments: \n "^(Lib.mapconcat (fn (a,t) => (A.ACT.mkstr a)^"."^(A.mkstr t)) cm "\n ")^"\n")
		  else ()
	      val redcm = (map (fn (a,ag) =>
				(* Huga again /BV *)
				(A.ACT.beta_reduce a ([NS.N.mkname("",~1)(*Zero*)],0),
				 if not (Lib.exists NS.N.zerop (A.free_names ag))
				     then (* restricted name not free, lose restriction *)
					 A.restriction_right NS.N.Zero (A.mk_restriction NS.N.Zero ag) e 
				 else
				     (* else reinstate restriction *)
				     A.mk_restriction NS.N.Zero ag))
			   cm)
	      val _ = if !Flags.tracelevel > 1 then
		  print("commitments real: \n "^(Lib.mapconcat (fn (a,t) => (A.ACT.mkstr a)^"."^(A.mkstr t)) redcm "\n ")^"\n")
		  else ()
          in filter redcm end
        else raise process_expected
      else raise normal_form_expected
 end
end

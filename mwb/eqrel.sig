signature EQREL =
    sig
	type 'a eqrel

	val mkstr   : 'a eqrel -> string
	val eq      : 'a eqrel * 'a eqrel -> bool
	val elements: 'a eqrel -> ('a list)
	val classes : 'a eqrel -> 'a list list
	val class_of : 'a * 'a eqrel -> 'a list
	val substitute : 'a * 'a * 'a eqrel -> 'a eqrel

	val isEmpty   : ('a * 'a -> bool) * ('a -> string) -> 'a eqrel
	val match   : ('a * 'a -> bool) * ('a -> string) -> 'a * 'a -> 'a eqrel
	val join    : 'a eqrel * 'a eqrel -> 'a eqrel

	val implies : 'a eqrel * 'a eqrel -> bool
    end


# Element Types:
# 0. Terminal
# 1. Output
# 2. Input
# 3. Match
# 4. Restriction
# 5. Sum
# 6. Parallel
# 7. Tau
# 8. Process
# 9. Root

class Element:
    def __init__(self, ptype: int):
        self.ptype = ptype

    def get_type(self) -> int:
        return self.ptype


class Terminal(Element):
    def __init__(self):
        Element.__init__(self, 0)

    def __str__(self):
        return "0"


class Output(Element):
    def __init__(self, channel: str, output: str, next: Element):
        Element.__init__(self, 1)
        self.channel = channel
        self.output = output
        self.next = next

    def __str__(s):
        return f"{s.channel}<{s.output}>.{s.next}"


class Input(Element):
    def __init__(self, channel: str, inp: str, next: Element):
        Element.__init__(self, 2)
        self.channel = channel
        self.input = inp
        self.next = next

    def __str__(s):
        return f"{s.channel}({s.input}).{s.next}"


class Equality(Element):
    def __init__(self, equal: bool, name_l: str, name_r: str, next: Element):
        Element.__init__(self, 3)
        self.equal = bool
        self.name_l = name_l
        self.name_r = name_r
        self.next = next

    def __str__(s):
        return f"[{s.name_l}{'=' if s.equal else '#'}{s.name_r}]{s.next}"


class Restriction(Element):
    def __init__(self, restrict: str, next: Element):
        Element.__init__(self, 4)
        self.restrict = restrict
        self.next = next

    def __str__(s):
        return f"^{s.restrict} {s.next}"


class Sum(Element):
    def __init__(self, left: Element, right: Element):
        Element.__init__(self, 5)
        self.left = left
        self.right = right

    def __str__(s):
        return f"({s.left} + {s.right})"


class Parallel(Element):
    def __init__(self, left: Element, right: Element):
        Element.__init__(self, 6)
        self.left = left
        self.right = right

    def __str__(s):
        return f"({s.left} | {s.right})"


class Tau(Element):
    def __init__(self, next: Element):
        Element.__init__(self, 7)
        self.next = next

    def __str__(s):
        return f"_TAU.{s.next}"


class Process(Element):
    def __init__(self, name: str, params: list):
        Element.__init__(self, 8)
        self.name = name
        self.params = params

    def __str__(s):
        return f"{s.name}({('{},' * len(s.params)).format(*s.params)[:-1]})"


class Root(Element):
    def __init__(self, next: Element):
        Element.__init__(self, 9)
        self.next = next

    def __str__(s):
        return str(s.next)

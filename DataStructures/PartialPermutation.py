from sympy.combinatorics import Permutation


# use for Rays
class PartialPermutation(Permutation):
    def __new__(cls, elems):
        pi = []
        t = []
        S = []
        if not len(elems) == 0:
            for e in elems:
                S.append(e[0])
                t.append(e[1])
            max_val = max(t) if max(t) > max(S) else max(S)
            counter = 0
            for i in range(max_val + 1):
                if i in S:
                    pi.append(t[S.index(i)])
                    continue
                while counter in t:
                    counter += 1
                pi.append(counter)
                counter += 1
        p = super().__new__(PartialPermutation, pi)
        p.s = S
        p.pi = {(i, p(i)) for i in p.s}
        assert elems == p.pi
        return p

    def __eq__(self, other: "PartialPermutation"):
        return self.pi == other.pi

    def __hash__(self):
        return hash(frozenset(self.pi))

    def __str__(self):
        return str(self.pi)

    def get(self, i):
        if i not in self.s:
            raise ValueError(f"Key {i} not in domain.")
        elem = Permutation.__call__(self, i)
        return elem

    def __invert__(self) -> "PartialPermutation":
        inverse = {self(i): i for i in self.s}
        return PartialPermutation(inverse)


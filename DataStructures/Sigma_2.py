from itertools import permutations
from copy import copy


class Sigma:

    ALL_SIGMA = {}

    def __init__(self, l1: list, l2: list, temp: bool = False):
        self.keys = l1
        self.values = l2
        if not temp:
            self.length = len(self.keys)
            self.blanks = []
            self.dom = set()
            self.rng = set()
            for i in range(self.length):
                if (l1[i] is not None) and (l2[i] is not None):
                    self.dom.add(l1[i])
                    self.rng.add(l2[i])
                elif (l1[i] is None) and (l2[i] is None):
                    self.blanks.append(i)

    def __str__(self):
        r = []
        for i in range(self.length):
            if self.keys[i] is None:
                continue
            r.append((self.keys[i], self.values[i]))
        return str(r)

    def __eq__(self, other: "Sigma"):
        return self.keys == other.keys and self.values == other.values

    def __getitem__(self, key):
        try:
            index = self.keys.index(key)
        except IndexError:
            raise IndexError("Error - key {} non-existent.".format(key))
        return self.values[index]

    def __hash__(self):
        return hash((tuple(self.keys), tuple(self.values)))

    def in_dom(self, s):
        return s in self.dom

    def in_rng(self, s):
        return s in self.rng

    def dom_sub(self, s: set):
        return s - self.dom

    def rng_sub(self, s: set):
        return s - self.rng

    def reverse(self):
        return Sigma(self.values, self.keys)

    def invert(self):
        t = self.values
        self.values = self.keys
        self.keys = t
        t = self.dom
        self.dom = self.rng
        self.rng = t

    def generate_temp_sigma(self, key, value):
        keys = list(self.keys)
        values = list(self.values)
        if key not in keys:
            keys.append(key)
            values.append(None)
        i1 = keys.index(key)
        if value not in values:
            keys.append(None)
            values.append(value)
        i2 = values.index(value)
        values[i2] = None
        values[i1] = value
        return Sigma(keys, values, True)

    @classmethod
    def generate_sigmas(cls, s1, s2):
        f1 = frozenset(s1)
        f2 = frozenset(s2)
        if (f1, f2) not in Sigma.ALL_SIGMA:
            l1 = list(s1)
            l2 = list(s2)
            all_sigmas = set()
            total = 2*len(l1) if len(l1) > len(l2) else 2*len(l2)
            while not len(l1) == total:
                l1.append(None)
            while not len(l2) == total:
                l2.append(None)
            perm = list(permutations(l2, total))
            # (1,None)(2,None)(None, 1)(None, 2)
            # (1, None)(2, None)(None, 2)(None, 1)
            # perm = perm_unique(l2)
            for p in perm:
                p = list(p)
                new_sig = Sigma(l1, p)
                if new_sig not in all_sigmas:
                    all_sigmas.add(Sigma(l1, p))
            Sigma.ALL_SIGMA[(f1, f2)] = frozenset(all_sigmas)
        return Sigma.ALL_SIGMA[(f1, f2)]

    @classmethod
    def combine(cls, sig_1: "Sigma", sig_2: "Sigma") -> "Sigma":
        return Sigma(sig_1.keys, sig_2.values)

    def is_id(self):
        for i in range(len(self.keys)):
            if not self.keys[i] == self.values[i]:
                return False
        return True

import itertools
from itertools import product, chain, combinations
from sympy.combinatorics import Permutation

class Sigma:

    ALL_SIGMA = {}
    ALL_PERMS = {}
    MEMO = {}

    def __init__(self, tuples):
        self.dom = set()
        self.rng = set()
        self.id = True
        self.tuple_inverse = list()
        self.length = len(tuples)
        self.tuple_form = list()
        self.keys = []
        self.values = []
        for pair in tuples:
            if (pair[0] is None) or (pair[1] is None):
                continue
            if pair[0] != pair[1]:
                self.id = False
            self.tuple_form.append(pair)
            self.keys.append(pair[0])
            self.values.append(pair[1])
            self.tuple_inverse.append((pair[1], pair[0]))
            self.dom.add(pair[0])
            self.rng.add(pair[1])

        self.hs = hash(frozenset(self.tuple_form))

    def len(self):
        return len(self.tuple_form)

    def __str__(self):
        if len(self.tuple_form) == 0:
            return "{}"
        return str(self.tuple_form).replace("\'", "")

    def __contains__(self, item):
        return item in self.keys

    def __add__(self, other: "Sigma"):
        new_tuples = set()
        for t in self.tuple_form:
            key, value = t
            if value in other:
                new_tuples.add((key, other[value]))
        return Sigma(new_tuples)

    def __eq__(self, other: "Sigma"):
        return set(self.tuple_form) == set(other.tuple_form)

    def __le__(self, other: "Sigma"):
        return self.tuple_form.issubset(other.tuple_form)

    def __getitem__(self, key):
        try:
            index = self.keys.index(key)
        except IndexError:
            raise IndexError("Error - key {} non-existent.".format(key))
        return self.values[index]

    def __hash__(self):
        return self.hs


    def in_dom(self, s):
        return s in self.dom

    def in_rng(self, s):
        return s in self.rng

    def dom_sub(self, s: set):
        return s - self.dom

    def rng_sub(self, s: set):
        return s - self.rng

    def reverse(self):
        return Sigma(self.tuple_inverse)

    def __copy__(self):
        return Sigma(self.tuple_form)

    def invert(self):
        return Sigma(self.tuple_inverse)

    def is_id(self):
        return self.id

    def get_tuple_form(self):
        return self.tuple_form

    def harpoon(self, q1, q2, RA) -> "Sigma":
        s1, s2 = RA.s_map[q1], RA.s_map[q2]
        new_tuples = set()
        for current_tuple in self.tuple_form:
            if (current_tuple[0] in s1) and (current_tuple[1] in s2):
                new_tuples.add(current_tuple)
        return Sigma(new_tuples)

    def generate_temp_sigma(self, key, value) -> "Sigma":
        keys = list(self.keys)
        values = list(self.values)
        if key not in keys:
            values.append(None)
            keys.append(key)
        i1 = keys.index(key)
        if value not in values:
            keys.append(None)
            values.append(value)
        i2 = values.index(value)
        values[i2] = None
        values[i1] = value
        # try:
        #     assert len(keys) == len(values)
        # except AssertionError:
        #     print(keys, key)
        #     print(values, value)
        #     exit(5)
        while None in keys:
            index = keys.index(None)
            keys.pop(index)
            values.pop(index)
        while None in values:
            index = values.index(None)
            keys.pop(index)
            values.pop(index)
        tuples = set(zip(keys, values))
        return Sigma(tuples)

    @classmethod
    def eliminate(cls, l1: list, l2: list, s: set) -> None:
        i = 0
        while i < len(l1):
            if l1[i] is None:
                i += 1
                continue
            if l1[i] not in s:
                del l1[i]
                del l2[i]
            else:
                i += 1

    @classmethod
    def generate_sigmas(cls, s1, s2):
        f1 = frozenset(s1)
        f2 = frozenset(s2)
        if (f1, f2) not in Sigma.ALL_SIGMA:
            all_sigmas = set()
            if len(s1) >= len(s2):
                length = len(s2)
                zip_set = s1
            else:
                length = len(s1)
                zip_set = s2
            f_temp = frozenset(zip_set)
            if not (f_temp, length) in Sigma.ALL_PERMS:
                Sigma.ALL_PERMS[(f_temp, length)] = set(itertools.permutations(zip_set, length))
            if len(s1) >= len(s2):
                perm = [list(zip(x, s2)) for x in Sigma.ALL_PERMS[(f_temp, length)]]
            else:
                perm = [list(zip(s1, x)) for x in Sigma.ALL_PERMS[(f_temp, length)]]
            for p in perm:
                new_sig = Sigma(set(p))
                if new_sig not in all_sigmas:
                    all_sigmas.add(new_sig)
                # sets = powerset(p)
                # for s in sets:
                #     new_sig = Sigma(set(s))
                #     if new_sig not in all_sigmas:
                #         all_sigmas.add(new_sig)
            Sigma.ALL_SIGMA[(f1, f2)] = frozenset(all_sigmas)
        return Sigma.ALL_SIGMA[(f1, f2)]


def unique_permutations(the_list: list):
    l_list = range(len(the_list) - 1, -1, -1)
    k_list = l_list[1:]
    the_list = sorted(the_list)
    while True:
        yield the_list
        found = False
        for k in k_list:
            if the_list[k] < the_list[k+1]:
                found = True
                break
        if not found:
            return
        val = the_list[k]
        for i in l_list:
            if val < the_list[i]:
                break
        the_list[k], the_list[i] = the_list[i], the_list[k]
        the_list[k + 1:] = the_list[-1:k:-1]


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

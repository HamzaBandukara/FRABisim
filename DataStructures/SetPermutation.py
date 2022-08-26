from sympy import Basic
from sympy.combinatorics import Permutation, PermutationGroup
# from sympy.core.basic import Basic
from copy import deepcopy
import functools


class SetPermutation(Permutation):

    DOM_MAP = None

    def __new__(cls, *args, **kwargs):
        if isinstance(args[0], PartialPermutation):
            full_domain = args[0].full_domain
            pi = args[0].pi
        else:
            full_domain = args[0]
            # pi = [x for x in range(len(full_domain))]
            pi = args[1]
        if not isinstance(full_domain, list):
            full_domain = list(full_domain)
        # p = super().__new__(cls, pi.array_form)
        self = object.__new__(cls)
        self._mhash = None  # will be set by __hash__ method.
        self._array_form = pi
        self._size = len(pi)

        self.full_domain = full_domain
        # self.domain_map = PartialPermutation.FULL_DOMAIN
        if cls.DOM_MAP is None:
            cls.DOM_MAP = {full_domain[i]: i for i in range(len(full_domain))}
        self.domain_map = cls.DOM_MAP
        try:
            self.permuted = self(full_domain)
        except TypeError:
            print(full_domain)
            print(pi)
            exit(-1)
        return self

    def __deepcopy__(self, memodict={}):
        raise TypeError("CALLED DEEPCOPY IN SETP")
        return SetPermutation(self.full_domain, self.pi)

    def __invert__(self):
        return SetPermutation(self.full_domain, (Permutation.__invert__(self)).array_form)

    def __str__(self):
        return "{}\t{}".format(self.full_domain, self.array_form)


class SetPermutationGroup(PermutationGroup):

    def __new__(cls, full_domain, *gens):
        self = object.__new__(cls)
        self._mhash = None  # will be set by __hash__ method.
        self.full_domain = full_domain
        if not gens:
            gens = [PartialPermutation(gens[0], set())]
        self._generators = gens
        self._order = None
        self._center = []
        self._is_abelian = None
        self._is_transitive = None
        self._is_sym = None
        self._is_alt = None
        self._is_primitive = None
        self._is_nilpotent = None
        self._is_solvable = None
        self._is_trivial = None
        self._transitivity_degree = None
        self._max_div = None
        self._is_perfect = None
        self._is_cyclic = None
        self._r = len(self._generators)
        self._degree = self._generators[0].size
        self._args = list(gens)

        # these attributes are assigned after running schreier_sims
        self._base = []
        self._strong_gens = []
        self._strong_gens_slp = []
        self._basic_orbits = []
        self._transversals = []
        self._transversal_slp = []

        # these attributes are assigned after running _random_pr_init
        self._random_gens = []

        # finite presentation of the group as an instance of `FpGroup`
        self._fp_presentation = None
        return self

    def __len__(self):
        return len(self._generators)

    def generate(self, method="coset", af=False):
        parent = super().generate(method, af)
        for x in parent:
            yield SetPermutation(self.full_domain, x)

    def contains(self, g, strict=False):
        next_gens = [f for f in self.generators if not f.identity]
        if len(next_gens) == 0: return g.identity
        try:
            return super().contains(g, strict)
        except ValueError:
            print(self.size, g)
            exit(-1)

    def __deepcopy__(self, memodict={}):
        raise TypeError("CALLED DEEPCOPY IN SETPG")
        return SetPermutationGroup(self.full_domain, *self.generators)

    def __hash__(self):
        return super.__hash__(self)


class PartialPermutation(SetPermutation):

    MEMO = {}
    MULMEMO = {}
    RESMEMO = {}
    ADDMEMO = {}
    FULL_DOMAIN = None

    def __new__(cls, *args, **kwargs):
        fs = None
        # NT: add a comment on the uses of this constructor
        if len(args) == 1:
            if isinstance(args[0], SetPermutation):
                print("F: ", args[0])
                s = args[0]
                args = [s.full_domain, s.full_domain, s.pi]
            else:
                raise ValueError
        if isinstance(args[1], set):
            fs = frozenset(args[1])
            if fs in cls.MEMO: return cls.MEMO[fs]
            full_domain, s = args[0], list(args[1])
            if cls.FULL_DOMAIN is None:
                cls.FULL_DOMAIN = {full_domain[i]: i for i in range(len(full_domain))}
            perm_array = [x for x in range(len(full_domain))]  # [a,b,c] [0,1,2]
            dom = [_[0] for _ in s]
            for i in range(len(s)):  # {(a,c)(b,b)(c,a)}
                p1, p2 = s[i]
                # dom[i] = p1
                i1, i2 = cls.FULL_DOMAIN[p1], cls.FULL_DOMAIN[p2]
                perm_array[i1] = i2
                # try:
                #     i1 = cls.FULL_DOMAIN[p1]
                # except KeyError:
                #     print(full_domain)
                #     print(cls.FULL_DOMAIN)
                #     print(p1)
                #     raise Exception("FAILED")
                # it = perm_array.index(cls.FULL_DOMAIN[p2])
                # perm_array[i1], perm_array[it] = perm_array[it], perm_array[i1]
            args = [dom, full_domain, perm_array] # NT: this is a hack ...
        if not isinstance(args[2], list):
            raise ValueError("NO LIST! ", *args)
        self = super().__new__(PartialPermutation, *args[1:], kwargs)
        self.domain = args[0]
        self.image = self.set_up_img()
        self.inverse = None
        self.hash = None
        if fs is not None:
            self.sf = fs
        else:
            self.sf = frozenset(zip(self.domain, self.image))
        if not self.size == len(self.full_domain):
            raise ValueError("HERE")
        cls.MEMO[self.sf] = self
        return self

    def identity(self):
        for s in self.sf:
            if s[0] != s[1]: return False
        return True

    def __le__(self, other: "PartialPermutation"):
        return self.set_form().issubset(other.set_form())

    def __mul__(self, other: "PartialPermutation") -> "PartialPermutation":
        try:
            return PartialPermutation.MULMEMO[(self, other)]
        except:
            pass
        try:
            return ~PartialPermutation.MULMEMO[(~other, ~self)]
        except:
            pass
        # a = self.array_form
        # __rmul__ makes sure the other is a Permutation
        # b = other.array_form
        # if not b:
        #     pi = a
        # else:
        #     b.extend(list(range(len(b), len(a))))
        #     pi = [b[i] for i in a] + b[len(a):]
        targets = set(self.image).intersection(set(other.domain))
        # domain = [k for k, v in self.dict_form.items() if v in targets]
        tuples = {(self.domain[i], self.image[i]) for i in range(len(self.image)) if self.image[i] in targets}
        # for i in range(len(self.image)):
        #     if self.image[i] in targets:
        #         domain.append(self.domain[i])
        fs = frozenset(tuples)
        x = PartialPermutation.MEMO.get(fs)
        if x is not None:
            PartialPermutation.MULMEMO[(self, other)] = x
        else:
            PartialPermutation.MULMEMO[(self, other)] = PartialPermutation(self.full_domain, tuples)
        return PartialPermutation.MULMEMO[(self, other)]

    # domain = [3, 2, 1]
    # image= [2, 1, 3]
    def __eq__(self, other: "PartialPermutation"): # MAKE THESE SETS
        return self.sf == other.sf

    def __deepcopy__(self, memodict={}):
        raise TypeError("CALLED DEEPCOPY")
        return PartialPermutation(self.domain, self.full_domain, self.pi)

    def add(self, key, value):
        try:
            return PartialPermutation.ADDMEMO[(self, key, value)]
        except:
            pass
        new_zip = list(self.sf)
        count = 0
        i = 0
        while i < len(new_zip) and count != 2:
            pair = new_zip[i]
            if pair[0] == key:
                x = new_zip.pop(i)
                count += 1
                if x[1] == value:
                    break
                continue
            if pair[1] == value:
                new_zip.pop(i)
                count += 1
                continue
            i += 1
        new_zip = set(new_zip)
        new_zip.add((key, value))
        PartialPermutation.ADDMEMO[(self, key, value)] = PartialPermutation(self.full_domain, new_zip)
        return PartialPermutation.ADDMEMO[(self, key, value)]

        # new_dom = set(self.domain)
        # if value in self.image:
        #     new_dom.remove(self.full_domain[self.permuted.index(value)])
        # new_dom.add(key)
        # new_pi = self.array_form
        # key_index = self.domain_map[key]
        # value_index = self.array_form.index(self.domain_map[value])
        # if not key_index == value_index:
        #     t = Permutation(key_index, value_index, size=len(self.full_domain))
        #     new_pi = t(new_pi)
        # next_copy = PartialPermutation(list(new_dom), self.full_domain, new_pi)
        # return next_copy

    def in_domain(self, v):
        return v in self.domain

    def img_sub(self, items):
        return set(items) - set(self.image)
        # return set(self.image) - set(items)

    def dom_sub(self, items):
        return set(items) - set(self.domain)
        # return set(self.domain) - set(items)

    def set_up_img(self):
        img = [self.permuted[self.domain_map[i]] for i in self.domain]
        # for x in self.domain:
        #     i = self.domain_map[x]
        #     img.append(self.permuted[i])
        return img


    def get(self, key):
        if self.in_domain(key):
            i = self.domain_map[key]
            return self.permuted[i]

    def get_domain(self):
        return set(self.domain)

    def get_image(self):
        return set(self.image)

    @functools.cache
    def restrict(self, dom, img=None) -> "PartialPermutation":
        try:
            return PartialPermutation.RESMEMO[(self, dom, img)]
        except:
            pass
        if img is None:
            sf = {(x, y) for x, y in self.set_form() if x in dom}
        else:
            sf = {(x, y) for x, y in self.set_form() if x in dom and y in img}
        PartialPermutation.RESMEMO[(self, dom, img)] = PartialPermutation(self.full_domain, sf)
        return PartialPermutation.RESMEMO[(self, dom, img)]
        # return PartialPermutation(self.full_domain, sf)

    def test_form(self):
        return "{}\t{}\t{}\t{}".format(self.domain, self.image, self.full_domain, self.array_form)

    def __str__(self):
        if len(self.sf) == 0: return "{}"
        s = "{"
        for x in self.sf:
            s += " "+str(x)+","
        return s[:-1]+" }"

    def __invert__(self):
        if self.inverse is None:
            sf = {(v,k) for k,v in self.sf}
            self.inverse = PartialPermutation(self.full_domain, sf)
        return self.inverse

    def __hash__(self):
        if self.hash is None:
            self.hash = hash(self.sf)
        return self.hash

    def set_form(self) -> frozenset:
        return self.sf

    def issubset(self, s):
        return self.set_form().issubset(s.set_form())


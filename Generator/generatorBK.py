import itertools

from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import *

from copy import deepcopy, copy


class InvalidPartition(Exception):
    pass


class LinkedList:
    def __init__(self, d, l=None):
        self.data = d
        self.next = l

    def __iter__(self):
        ptr = self
        while ptr is not None:
            yield ptr.data
            ptr = ptr.next
        return

    def __contains__(self, item):
        ptr = self
        while ptr is not None:
            if ptr.data == item:
                return True
            ptr = ptr.next
        return False

    def __str__(self):
        s = ""
        ptr = self
        while ptr is not None:
            s += f"{ptr.data} => "
            ptr = ptr.next
        s += "None"
        return s


class GeneratingSystem:
    MEMO = {}
    UMEMO = {}
    COUNTER = 0
    C_MAP = {}

    def __init__(self, *args):
        if len(args) == 2:
            partitions = args[0]
            self.RA = args[1]
            self.partition_dict = {}
            self.hash = None
            for partition in partitions:
                for state in partition.partition:
                    self.partition_dict[state] = partition
        else:
            self.RA = args[0]

    def clone(self):
        gs = GeneratingSystem(self.RA)
        gs.partition_dict = {k: v for k, v in self.partition_dict.items()}
        gs.hash = self.hash
        return gs

    def __getitem__(self, state):
        return self.partition_dict[state]
        # for partition in self.partition_set:
        #     if state in partition.partition:
        #         return partition

    def find_two(self, q, p):
        return self.partition_dict[q], self.partition_dict[p]
        # first = None
        # second = None
        # for part in self.partition_set:
        #     if q in part.partition:
        #         first = part
        #     if p in part.partition:
        #         second = part
        #     if (first is not None) and (second is not None):
        #         return first, second

    def set(self, state):
        self.partition_dict = state

    def get_state(self):
        return self.partition_dict.copy()

    def __iter__(self):
        return iter(self.partition_set)

    def is_member(self, q1: str, sigma: PartialPermutation, q2: str) -> bool:
        p1, p2 = self.find_two(q1, q2)
        if not p1 == p2:
            return False
        s1, s2 = p1.get_sigma(q1), ~p2.get_sigma(q2)
        s_hat = s1 * sigma * s2
        res = p1.sigma_in_g(s_hat)
        return res

    def check_inconsistency(self, bad):
        for elem in bad:
            if self.is_member(*elem):
                bad.bad_set.add(elem)
                return True
        return False

    def update(self, q: str, sigma: PartialPermutation, p: str):
        if self.is_member(q, sigma, p): return
        p1, p2 = self.find_two(q, p)
        try:
            part = GeneratingSystem.UMEMO[(p1, p2, q, sigma, p)]
            for state in part.partition:
                self.partition_dict[state] = part
            return
        except:
            part = p1.clone()
        for state in part.partition:
            self.partition_dict[state] = part
        sigma_q = part.get_sigma(q)
        part_p = p2
        sigma_p = part_p.get_sigma(p)
        sigma_hat = sigma_q * sigma * (~sigma_p)
        if self.same_set(p, q):
            if set(sigma_hat.get_domain()) == set(part.Xc):
                # Case 1a
                # print("CASE 1A")
                part.add_sigma(sigma_hat)
                GeneratingSystem.UMEMO[(p1, p2, q, sigma, p)] = part
                return
            # Case 1b
            # print("CASE 1B")
            I = set(part.get_Gc())
            I.add(sigma_hat)
        else:
            # Case 1c
            # print("CASE 1C")
            part.partition = part.partition.union(part_p.partition)
            I = set(part.get_Gc())
            sigma_hat_inv = ~sigma_hat
            for t in set(part_p.get_Gc()):
                t_hat = sigma_hat * t * sigma_hat_inv
                I.add(t_hat)
        # print("Starting BI")
        b_i = self.generate_BI(I)
        # print("Generated BI")
        part.Xc = list(b_i)
        new_Gc = set()
        for sigma in I:
            new_Gc.add(sigma.restrict(b_i))
        # print("RESTRICTED ALL SIGMAS")
        part.Gc = new_Gc
        part.update_group(new_Gc)
        # print("UPDATED GROUP")
        for key in part.sigmas:
            part.sigmas[key] = part.sigmas[key].restrict(b_i)
        # print("RESTRICTED ALL STATE SIGMAS")
        if isinstance(part_p, Partition):
            # new_sigmas = dict()
            for key in part_p.sigmas:
                part.sigmas[key] = sigma_hat * part_p.sigmas[key]
                self.partition_dict[key] = part
        GeneratingSystem.UMEMO[(p1, p2, q, sigma, p)] = part

    def generate_BI(self, I: {PartialPermutation}):
        fs = frozenset(I)
        if fs in GeneratingSystem.MEMO: return GeneratingSystem.MEMO[fs]
        domain = self.RA.get_registers()
        edges = {x: set() for x in domain}
        marked = set()
        domain = set(domain)
        for sigma in I:
            for pair in sigma.set_form():
                edges[pair[0]].add(pair[1])
                edges[pair[1]].add(pair[0])
            marked.update(domain - (sigma.get_domain().intersection(sigma.get_image())))
        bad = marked
        good = domain - marked
        result = frozenset(GeneratingSystem.bfs(good, bad, edges))
        GeneratingSystem.MEMO[fs] = result
        return result
        # b_i = {v for v in domain if not GeneratingSystem.breadth_first_search(edges, marked, v)}

    @staticmethod
    def bfs(good: set, bad: set, edges):
        while len(bad) > 0:
            root = bad.pop()
            seen = {root}
            visited = set()
            while len(seen) > 0:
                current = seen.pop()
                visited.add(current)
                bad.discard(current)
                good.discard(current)
                for vertex in edges[current]:
                    if vertex not in visited and vertex not in seen:
                        seen.add(vertex)
        return good

    """
    Returns True if can reach a marked vertex 
    """

    @staticmethod
    def breadth_first_search(edges, marked, root):
        if root in marked:
            return True
        seen = [root]
        visited = set()
        while len(seen) > 0:
            current = seen.pop()
            visited.add(current)
            for vertex in edges[current]:
                if vertex in marked:
                    marked.add(root)
                    return True
                if vertex not in seen and vertex not in visited:
                    seen.append(vertex)
        return False

    @staticmethod
    def marked_search(edges: dict, marked: set):
        visited = set()
        seen = list(marked)
        vertices = edges.keys()
        while len(seen) > 0:
            current = seen.pop()
            visited.add(current)
            for vertex in edges[current]:
                if vertex not in seen and vertex not in visited:
                    seen.append(vertex)
                    marked.add(vertex)
        return set(vertices) - marked

    def __str__(self):
        s = "Generating System:"
        for p in self.partition_dict.values():
            s += "\n- {}".format(str(p))
        return s

    def same_set(self, p, q):
        return self[p] == self[q]

    def __len__(self):
        total = 0
        for partition in set(self.partition_dict.values()):
            total += len(partition)
        return total

    def __hash__(self):
        if self.hash is None:
            self.hash = hash(frozenset(self.partition_dict.values()))
        return self.hash


class Partition:
    GROUPMEMO = {}

    def __init__(self, partition: {str}, representative: (str, {str}, {PartialPermutation}),
                 sigmas: {str: PartialPermutation}, dom: [str]):
        # NT: what is dom needed for?
        self.partition = partition
        self.qc, self.Xc, Gc = representative
        self.full_domain = dom
        self.group_form = SetPermutationGroup(self.full_domain, *Gc)
        self.sigmas = sigmas  # NT: I guess these are rays?
        self.hash = None
        self.members = set()
        if len(self.sigmas.keys()) != len(partition):
            print("Error - Invalid set Sigmas - states do not match partition!")
            raise InvalidPartition
        if self.qc not in self.partition:
            print("Error - rep not in partition")
            raise InvalidPartition

    def is_identity(self):
        if len(self.partition) == 2:
            p = list(self.partition)
            if p[0][1:] == p[1][1:]:
                for sigma in self.sigmas.values():
                    if not sigma.identity():
                        return False
                return True
        return False

    def __hash__(self):
        # if self.hash is None:
        hs = hash(self.group_form)
        self.hash = hash((self.qc, frozenset(self.Xc), hs))
        return self.hash

    def __len__(self):
        return len(self.group_form)

    def clone(self):
        partition = self.partition.copy()
        rep = self.qc, set(self.Xc), set(self.group_form.strong_gens)
        sigmas = self.sigmas.copy()
        p = Partition(partition, rep, sigmas, self.full_domain)
        p.members = self.members.copy()
        return p

    def add_sigma(self, sigma: PartialPermutation):
        print("1", self.group_form.strong_gens)
        self.group_form.strong_gens.append(sigma)
        if sigma in self.group_form: print("YES")
        print("2", self.group_form.strong_gens)

    def closure(self, RA: RegisterAutomata) -> set:
        memo = {}
        all_perm = {}
        registers = set(RA.get_registers())
        Cl_H = set()
        H = list(self.generate_h())
        length = len(H)
        for i in range(length):
            q1, sigma, q2 = H[i]
            dom, img = registers - sigma.get_domain(), registers - sigma.get_image()
            dom = dom.intersection(RA.s_map[q1])
            img = img.intersection(RA.s_map[q2])
            print("DOM: ", dom)
            print("IMG: ", img)
            f_dom, f_img = frozenset(dom), frozenset(img)
            if not (f_dom, f_img) in memo:
                all_sigmas = set()
                if len(dom) >= len(img):
                    length = len(img)
                    zip_set = dom
                else:
                    length = len(dom)
                    zip_set = img
                f_temp = frozenset(zip_set)
                if not (f_temp, length) in all_perm:
                    x = set(itertools.permutations(zip_set, length))
                    all_perm[(f_temp, length)] = x
                if len(dom) >= len(img):
                    perm = [list(zip(x, img)) for x in all_perm[(f_temp, length)]]
                else:
                    perm = [list(zip(dom, x)) for x in all_perm[(f_temp, length)]]
                print("PERM: ", perm)
                for p in perm:
                    sets = powerset(p)
                    for s in sets:
                        new_sig = PartialPermutation(self.full_domain, set(s))
                        if new_sig not in all_sigmas:
                            all_sigmas.add(new_sig)
                memo[(f_dom, f_img)] = frozenset(all_sigmas)
            for sig in memo[(f_dom, f_img)]:
                if (q1, sig, q2) not in H:
                    H.append((q1, sig, q2))
                    print(q1, sig, q2)
        i = 0
        while i < len(H):
            Cl_H.add(H[i])
            q1, sigma, q2 = H[i]
            inverse = (q2, ~sigma, q1)
            if inverse not in H:
                H.append(inverse)

            q1, sigma, q2 = inverse
            for j in range(len(H)):
                q3, sigma2, q4 = H[j]
                if not q2 == q3:
                    continue
                new_sigma = (sigma * sigma2)
                new_sigma = new_sigma.restrict(RA.s_map[q1], RA.s_map[q4])
                if (q1, new_sigma, q4) not in H:
                    H.append((q1, new_sigma, q4))
            i += 1
        return Cl_H

    def generate_h(self) -> set:
        H = set()
        for gc in self.group_form.strong_gens:
            H.add((self.qc, gc, self.qc))
        for state in self.partition:
            H.add((self.qc, self.sigmas[state], state))
        return H

    def get_Gc(self):
        return self.group_form.strong_gens

    def get_sigma(self, state: str) -> PartialPermutation:
        return self.sigmas[state]

    def get_partition(self):
        return self.partition

    def sigma_in_g(self, sigma: PartialPermutation) -> bool:
        if sigma in self.members: return True
        xc = set(self.Xc)
        if set(sigma.domain) == xc and set(sigma.image) == xc:
            res = sigma in self.group_form
            if res:
                self.members.add(sigma)
            return res
        return False

    def update_group(self, Gc):
        self.group_form = SetPermutationGroup(self.full_domain, *Gc)

    def __iter__(self):
        return iter(self.partition)

    def __str__(self):
        def set2str(A):
            if len(A) == 0: return "{}"
            s = "{"
            for x in A: s += " " + str(x) + ","
            return s[:-1] + " }"

        def dict2str(A):
            if len(A) == 0: return "{}"
            s = "{"
            for x, y in A.items(): s += " " + str(x) + ": " + str(y) + ","
            return s[:-1] + " }"

        return "Partition: {}, {}, {} -> {}".format(self.qc, self.Xc, set2str(set(self.group_form.strong_gens)),
                                                    dict2str(self.sigmas))


class BadGenerator:
    def __init__(self, RA: RegisterAutomata, G: GeneratingSystem):
        self.partition_dict = {}
        self.partition_set = set()
        self.RA = RA
        self.good = G

    def __deepcopy__(self, memodict={}):
        partitions = set()
        part_dict = {}
        for p in self.partition_set:
            x = p.clone()
            partitions.add(x)
            for s in x.partition:
                part_dict[s] = x
        G = BadGenerator(self.RA)
        G.partition_set = partitions
        G.partition_dict = part_dict
        return G

    def set(self, G: "GeneratingSystem"):
        self.partition_dict = G.partition_dict
        self.partition_set = G.partition_set

    def __iter__(self):
        return iter(self.partition_set)

    # any tuple below is not bisimilar
    def is_member(self, q1: str, sigma: PartialPermutation, q2: str) -> bool:
        # print("Input: ", q1, sigma, q2)
        if self.good.is_member(q1, sigma, q2):
            return False
        try:
            p1, p2 = self.partition_dict[q1], self.partition_dict[q2]
        except KeyError:
            return False
        # print("P1, P2: ", p1, p2)
        if not p1 == p2:
            # print("FALSE")
            return False
        s1, s2 = p1.get_sigma(q1), ~p2.get_sigma(q2)
        s_hat = s1 * sigma * s2
        # print("HAT: ", s_hat)
        # print(p1.Xc)
        res = p1.sigma_in_g(s_hat)
        # print("RES ", res)
        return res

    def update(self, q: str, sigma: PartialPermutation, p: str):
        # if self.is_member(q, sigma, p):
        #     return
        if q not in self.partition_dict:
            rep = (
                q,
                sigma.domain,
                {PartialPermutation(sigma.domain, sigma.full_domain, [x for x in range(len(sigma.full_domain))])}
            )
            part = Partition({q}, rep, {q: PartialPermutation(sigma.full_domain, set(zip(sigma.domain, sigma.domain)))},
                             sigma.full_domain)
            self.partition_dict[q] = part
            self.partition_set.add(part)
        if p not in self.partition_dict:
            rep = (
                p,
                sigma.image,
                {PartialPermutation(sigma.image, sigma.full_domain, [x for x in range(len(sigma.full_domain))])}
            )
            part = Partition({p}, rep, {p: PartialPermutation(sigma.full_domain, set(zip(sigma.image, sigma.image)))},
                             sigma.full_domain)
            self.partition_dict[p] = part
            self.partition_set.add(part)
        sigma_q = self.partition_dict[q].get_sigma(q)
        sigma_p = self.partition_dict[p].get_sigma(p)
        sigma_hat = sigma_q * sigma * (~sigma_p)
        part_p = None
        if self.partition_dict[q] == self.partition_dict[p]:
            part = self.partition_dict[q]
            if set(sigma_hat.get_domain()) == set(part.Xc):
                # Case 1a
                # print("CASE 1A")
                part.add_sigma(sigma_hat)
                return
            # Case 1b
            # print("CASE 1B")
            I = set(part.get_Gc())
            I.add(sigma_hat)
        else:
            # Case 1c
            # print("CASE 1C")
            part = self.partition_dict[q]
            part_p = self.partition_dict[p]
            part.partition = part.partition.union(part_p.partition)
            I = set(part.get_Gc())
            sigma_hat_inv = ~sigma_hat
            for t in set(part_p.get_Gc()):
                t_hat = sigma_hat * t * sigma_hat_inv
                I.add(t_hat)
            self.partition_set.remove(part_p)
        # print("Starting BI")
        b_i = self.generate_BI(I)
        # print("Generated BI")
        part.Xc = list(b_i)
        new_Gc = set()
        for sigma in I:
            new_Gc.add(sigma.restrict(b_i))
        # print("RESTRICTED ALL SIGMAS")
        part.Gc = new_Gc
        part.update_group(new_Gc)
        # print("UPDATED GROUP")
        for key in part.sigmas:
            part.sigmas[key] = part.sigmas[key].restrict(b_i)
        # print("RESTRICTED ALL STATE SIGMAS")
        if isinstance(part_p, Partition):
            # new_sigmas = dict()
            for key in part_p.sigmas:
                part.sigmas[key] = sigma_hat * part_p.sigmas[key]
                self.partition_dict[key] = part

    def generate_BI(self, I: {PartialPermutation}):
        domain = self.RA.get_registers()
        edges = {}
        marked = set()
        for x in domain:
            edges[x] = set()
        domain = set(domain)
        for sigma in I:
            for pair in sigma.set_form():
                edges[pair[0]].add(pair[1])
                edges[pair[1]].add(pair[0])
            marked = marked.union(domain - (sigma.get_domain().union(sigma.get_image())))
        # b_i = self.marked_search(edges, marked)
        b_i = set()
        # print("BFS")
        for v in domain:
            if not GeneratingSystem.breadth_first_search(edges, marked, v):
                b_i.add(v)
        return b_i

    """
    Returns True if can reach a marked vertex 
    """

    @staticmethod
    def breadth_first_search(edges, marked: set, root):
        if root in marked:
            return True
        seen = [root]
        visited = set()
        while len(seen) > 0:
            current = seen.pop()
            visited.add(current)
            for vertex in edges[current]:
                if vertex in marked:
                    marked.update(seen)
                    marked.update(visited)
                    return True
                if vertex not in seen and vertex not in visited:
                    seen.append(vertex)
        return False

    @staticmethod
    def marked_search(edges: dict, marked: set):
        visited = set()
        seen = list(marked)
        vertices = edges.keys()
        while len(seen) > 0:
            current = seen.pop()
            visited.add(current)
            for vertex in edges[current]:
                if vertex not in seen and vertex not in visited:
                    seen.append(vertex)
                    marked.add(vertex)
        return set(vertices) - marked

    def __str__(self):
        s = "Generating System:"
        for p in self.partition_set:
            s += "\n\t{}".format(str(p))
        return s


class SymmetricDownSet:
    def __init__(self, RA: RegisterAutomata):
        self.RA = RA
        self.partition_dict = {}
        self.size = 0
        self.bad_set = set()
        self.generators = set()
        # partition_dict[key = a state] = another_dict[value = state]
        # = set(all sigmas such that (key, sigma, value) is in the set represented by this Symmetric Down Set

    def __len__(self):
        return self.size

    def __iter__(self):
        for elem in self.generators: yield elem

    def is_member(self, q1: str, sigma: PartialPermutation, q2: str):
        if (q1, sigma, q2) in self.bad_set: return True
        if q1 not in self.partition_dict or q2 not in self.partition_dict[q1]:
            return False
        for sig in self.partition_dict[q1][q2]:
            if sigma.set_form().issubset(sig):
                self.bad_set.add((q1, sigma, q2))
                self.bad_set.add((q2, ~sigma, q1))
                return True
        return False

    # updates by adding (q,sigma,p) and its inverse
    # for each existing (q,sigma',p):
    # - if sigma <= sigma', remove (q,sigma',p)
    # - if sigma'<= sigma, do not add (q,sigma,p)
    def update(self, q: str, sigma: PartialPermutation, p: str):
        self.bad_set.add((q, sigma, p))
        self.bad_set.add((p, ~sigma, q))
        if q not in self.partition_dict:
            self.partition_dict[q] = {}
        if p not in self.partition_dict[q]:
            self.partition_dict[q][p] = set()
        if p not in self.partition_dict:
            self.partition_dict[p] = {}
        if q not in self.partition_dict[p]:
            self.partition_dict[p][q] = set()
        for s in set(self.partition_dict[q][p]):
            if sigma.issubset(s): return
            if s.issubset(sigma):
                # sigma_1 in the set. if sigma_1 is in the downward closure of sigma_2, we remove it
                self.partition_dict[q][p].remove(s)
                self.partition_dict[p][q].remove(~s)
                self.size -= 2
                self.generators -= {(q, sigma, p), (p, ~sigma, q)}
        self.generators.add((q, sigma, p))
        self.partition_dict[q][p].add(sigma)
        self.partition_dict[p][q].add(~sigma)
        self.size += 2

    def __str__(self):
        def list2str(L):
            if L == []: return "[]"
            s = "["
            for x in L:
                s += " " + str(x) + ","
            return s[:-1] + " ]"

        if self.size == 0: return "{}"
        s = "{"
        for p in self.partition_dict:
            for q in self.partition_dict[p]:
                s += " (" + str(p) + "," + str(q) + ") -> " + list2str(self.partition_dict[p][q])
        return s[:-1] + " }"


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

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

    def __contains__(self, item):
        ptr = self
        while ptr is not None:
            if ptr.data == item:
                return True
            ptr = ptr.next
        return False

class GeneratingSystem:
    def __init__(self, *args):
        if len(args) == 2:
            partitions = args[0]
            self.RA = args[1]
            self.partition_dict = {}
            self.partition_set = partitions
            for partition in partitions:
                for state in partition.partition:
                    if state in self.partition_dict:
                        raise InvalidPartition("Error - State appears twice.")
                    self.partition_dict[state] = partition
        else:
            self.RA = args[0]

    def __deepcopy__(self, memodict={}):
        partitions = set()
        for p in self.partition_set:
            x = p.clone()
            partitions.add(x)
        return GeneratingSystem(partitions, self.RA)

    def set(self, G: "GeneratingSystem"):
        self.partition_dict = G.partition_dict
        self.partition_set = G.partition_set

    def __iter__(self):
        return iter(self.partition_set)

    def is_bisimulation(self) -> bool:
        for partition in self.partition_set:
            qc = partition.qc
            for g in partition.Gc:
                if not self.one_step(qc, g, qc):
                    return False
            states = partition.partition
            for q in states:
                if not self.one_step(qc, partition.sigmas[q], q):
                    return False
        return True

    def is_member(self, q1: str, sigma: PartialPermutation, q2: str) -> bool:
        p1, p2 = self.partition_dict[q1], self.partition_dict[q2]
        if not p1 == p2:
            return False
        s1, s2 = p1.get_sigma(q1), ~p2.get_sigma(q2)
        s_hat = s1 * sigma * s2
        res = p1.sigma_in_g(s_hat)
        return res

    def one_step(self, q1: str, sigma: PartialPermutation, p1: str):
        RA = self.RA
        transitions_1, transitions_2 = RA.get_transitions(q1), RA.get_transitions(p1)
        for pair_1 in transitions_1:
            #  Known Transitions
            if pair_1[1] == "K":
                label_1 = pair_1[0]
                label_2 = sigma.get(label_1)
                if label_2 is not None:
                    pair_2 = label_2, "K"
                    for next_q1 in RA.get_trans_lbl(q1, pair_1):
                        found = False
                        for next_p1 in RA.get_trans_lbl(p1, pair_2):
                            r_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_p1])
                            if self.is_member(next_q1, r_sigma, next_p1):
                                found = True
                                break
                        if not found:
                            return False
                else:
                    for next_q1 in RA.get_trans_lbl(q1, pair_1):
                        found = False
                        for pair_2 in transitions_2:
                            if not pair_2[1] == "L":
                                continue
                            new_sigma = sigma.add(label_1, pair_2[0])
                            for next_p1 in RA.get_trans_lbl(p1, pair_2):
                                r_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_p1])
                                if self.is_member(next_q1, r_sigma, next_p1):
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            return False
            #  Locally-Fresh Transitions
            elif pair_1[1] == "L":
                label_1 = pair_1[0]
                for next_q1 in RA.get_trans_lbl(q1, pair_1):
                    found = False
                    for pair_2 in transitions_2:
                        if not pair_2[1] == "L":
                            continue
                        new_sigma = sigma.add(label_1, pair_2[0])
                        for next_p1 in RA.get_trans_lbl(p1, pair_2):
                            r_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_p1])
                            if self.is_member(next_q1, r_sigma, next_p1):
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        return False
                sub = sigma.img_sub(RA.s_map[p1])
                for label_2 in sub:
                    pair_2 = label_2, "K"
                    new_sigma = sigma.add(label_1, label_2)
                    for next_q1 in RA.get_trans_lbl(q1, pair_1):
                        found = False
                        for next_p1 in RA.get_trans_lbl(p1, pair_2):
                            r_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_p1])
                            if self.is_member(next_q1, r_sigma, next_p1):
                                found = True
                                break
                        if not found:
                            return False
        return True

    def update(self, q: str, sigma: PartialPermutation, p: str):
        # if self.is_member(q, sigma, p):
        #     return
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
        edges = {x: set() for x in domain}
        marked = set(domain)
        domain = set(domain)
        for sigma in I:
            for pair in sigma.set_form():
                edges[pair[0]].add(pair[1])
                edges[pair[1]].add(pair[0])
            marked = marked - sigma.get_domain() - sigma.get_image()
        bad = set(marked)
        good = domain - marked
        return GeneratingSystem.bfs(good, bad, edges)

    """
    Returns True if can reach a marked vertex 
    """
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
            s += "\n- {}".format(str(p))
        return s


class Partition:
    def __init__(self, partition: {str}, representative: (str, {str}, {PartialPermutation}),
                 sigmas: {str: PartialPermutation}, dom: [str]):
        # NT: what is dom needed for?
        self.partition = partition
        self.qc, self.Xc, self.Gc = representative
        self.group_form = None
        self.sigmas = sigmas # NT: I guess these are rays?
        self.full_domain = dom
        if len(self.sigmas.keys()) != len(partition):
            print("Error - Invalid set Sigmas - states do not match partition!")
            raise InvalidPartition
        if self.qc not in self.partition:
            print("Error - rep not in partition")
            raise InvalidPartition

    def clone(self):
        partition = self.partition.copy()
        rep = self.qc, set(self.Xc), set(self.Gc)
        sigmas = self.sigmas.copy()
        return Partition(partition, rep, sigmas, self.full_domain)

    def add_sigma(self, sigma: PartialPermutation):
        self.Gc.add(sigma)
        self.group_form = None

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
        for gc in self.Gc:
            H.add((self.qc, gc, self.qc))
        for state in self.partition:
            H.add((self.qc, self.sigmas[state], state))
        return H

    def get_Gc(self):
        return self.Gc

    def get_sigma(self, state: str) -> PartialPermutation:
        return self.sigmas[state]

    def get_partition(self):
        return self.partition

    def sigma_in_g(self, sigma: PartialPermutation) -> bool:
        # if set(self.Xc).issubset(sigma.domain):
        # print(self.group_form)
        # print(self.Xc, sigma.domain, sigma.image)
        if set(sigma.domain) == set(self.Xc) == set(sigma.image):
            # print("INIF")
            if self.group_form is None:
                self.group_form = SetPermutationGroup(self.full_domain, *self.Gc)
            return sigma in self.group_form
        return False

    def update_group(self, Gc):
        self.Gc = Gc
        self.group_form = None

    def __iter__(self):
        return iter(self.partition)

    def __str__(self):
        def set2str(A):
            if len(A) == 0: return "{}"
            s = "{"
            for x in A: s += " "+str(x)+","
            return s[:-1]+" }"

        def dict2str(A):
            if len(A) == 0: return "{}"
            s = "{"
            for x, y in A.items(): s += " "+str(x)+": "+str(y)+","
            return s[:-1]+" }"            
        
        return "Partition: {}, {}, {} -> {}".format(self.qc, self.Xc, set2str(self.Gc), dict2str(self.sigmas))


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
            part = Partition({q}, rep, {q: PartialPermutation(sigma.full_domain, set(zip(sigma.domain, sigma.domain)))}, sigma.full_domain)
            self.partition_dict[q] = part
            self.partition_set.add(part)
        if p not in self.partition_dict:
            rep = (
               p,
               sigma.image,
               {PartialPermutation(sigma.image, sigma.full_domain, [x for x in range(len(sigma.full_domain))])}
            )
            part = Partition({p}, rep, {p: PartialPermutation(sigma.full_domain, set(zip(sigma.image, sigma.image)))}, sigma.full_domain)
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
        # partition_dict[key = a state] = another_dict[value = state]
        # = set(all sigmas such that (key, sigma, value) is in the set represented by this Symmetric Down Set
        
    def is_member(self, q1: str, sigma: PartialPermutation, q2: str):
        if q1 not in self.partition_dict or q2 not in self.partition_dict[q1]:
            return False
        for sig in self.partition_dict[q1][q2]:
            if sigma.set_form().issubset(sig):
                return True
        return False

    # updates by adding (q,sigma,p) and its inverse
    # for each existing (q,sigma',p):
    # - if sigma <= sigma', remove (q,sigma',p)
    # - if sigma'<= sigma, do not add (q,sigma,p)
    def update(self, q: str, sigma: PartialPermutation, p: str):
        if q not in self.partition_dict:
            self.partition_dict[q] = {}
        if p not in self.partition_dict[q]:
            self.partition_dict[q][p] = []
        if p not in self.partition_dict:
            self.partition_dict[p] = {}
        if q not in self.partition_dict[p]:
            self.partition_dict[p][q] = []
        i = 0
        flagged = []
        while i < len(self.partition_dict[q][p]):
            s = self.partition_dict[q][p][i]
            if sigma.issubset(s): return
            if s.issubset(sigma):
                # sigma_1 in the set. if sigma_1 is in the downward closure of sigma_2, we remove it
                x = self.partition_dict[q][p].pop(i)
                self.size -= 1
                flagged.append(x)
            else:
                i += 1
        for x in flagged:
            self.partition_dict[p][q].remove(~x)
        self.partition_dict[q][p].append(sigma)
        self.partition_dict[p][q].append(~sigma)
        self.size += 2

    def __str__(self):
        def list2str(L):
            if L == []: return "[]"
            s = "["
            for x in L:
                s += " "+str(x)+","
            return s[:-1]+" ]"

        if self.size == 0: return "{}"
        s = "{"
        for p in self.partition_dict:
            for q in self.partition_dict[p]:
                s += " ("+str(p)+","+str(q)+") -> "+list2str(self.partition_dict[p][q])
        return s[:-1]+" }"

def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

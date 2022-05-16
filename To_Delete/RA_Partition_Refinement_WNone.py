from DataStructures.SetPermutation import *
from itertools import permutations
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import *
from Generator.generator import *
from datetime import datetime as dt

from random import choice
from RAStack.Generator import generate_stack as det
from RAStack.NDGenerator import generate_stack as ndet
from RAStack.Combiner import combiner
from copy import deepcopy as cp


def knuth_L_algorithm(seq):
    if len(seq) == 0:
        return [tuple(seq)]
    a = sorted(seq)
    limit = len(a) // 2
    r = []
    while True:
        ret = tuple(a[:limit])
        if ret not in r:
            r.append(tuple(ret))
        # k = limit - 1
        k = len(a) - 2
        while k > -1:
            if a[k] < a[k + 1]:
                break
            k -= 1
        if k < 0:
            return r
        i = len(a) - 1
        while i > k:
            if a[k] < a[i]:
                break
            i -= 1
        if i == k:
            raise ValueError
        a[k], a[i] = a[i], a[k]
        rev = [a[x] for x in range(len(a) - 1, k, -1)]
        index = 0
        for x in range(k + 1, len(a)):
            a[x] = rev[index]
            index += 1



def split(B: set, RA, partition_dict):
    B2 = []
    B1 = list(B)
    q1, s1 = B1.pop(0)
    while len(B1) > 0:
        q2, s2 = B1.pop(0)
        if simulate((q1, s1), (q2, s2), RA, partition_dict):
            if simulate((q2, s2), (q1, s1), RA, partition_dict):
                continue
        B2.append((q2, s2))
    for (q2, s2) in B2:
        partition_dict[q2][s2] = B2
        B.remove((q2, s2))
    return B2


def restrict(pair_1, pair_2, RA: RegisterAutomata):
    q1, s1 = pair_1
    q2, s2 = pair_2
    s1, s2 = list(s1), list(s2)
    y = set(RA.s_map[q1])
    y.add("#")
    diff = set(s1) - y
    remove_diff(s1, s2, diff)
    y = set(RA.s_map[q2])
    y.add("#")
    diff = set(s2) - y
    remove_diff(s2, s1, diff)
    while len(s1) > len(RA.s_map[q1]):
        remove_redundant(s1, s2)
    while len(s2) > len(RA.s_map[q2]):
        remove_redundant(s2, s1)
    while len(s1) < len(RA.s_map[q1]):
        s1.append("#")
    while len(s2) < len(RA.s_map[q2]):
        s2.append("#")
    return (q1, tuple(s1)), (q2, tuple(s2))


def remove_diff(s1, s2, diff):
    for index in range(len(s1)):
        if s1[index] not in diff:
            continue
        s1[index] = "#"
        try:
            s2[index] = "#"
        except IndexError:
            pass

def remove_redundant(s1, s2):
    flag = True
    if None in s2:
        flag = False
    i = 0
    while i < len(s1):
        if s1[i] == "#":
            if i < len(s2):
                if flag:
                    s2.pop(i)
                    break
                elif s2[i] == "#":
                    s2.pop(i)
                    break
            else:
                break
        i += 1
    if i == len(s1):
        print(s1)
        print(s2)
        raise ValueError
    s1.pop(i)

# ra = RegisterAutomata(combiner(det(2), det(2)))
# print(*restrict(("p1", (None, "2")), ("p1", ("1", "2")), ra))

def add(o_s1, o_s2, key, value):
    s1 = list(o_s1)
    s2 = list(o_s2)
    if len(s1) == 0:
        s1.insert(0, key)
        if value in s2:
            i = s2.index(value)
            s2[i] = None
        s2.insert(0, value)
        return s1, s2
    if len(s2) == 0:
        s2.insert(0, value)
        if key in s1:
            i = s1.index(key)
            s1[i] = None
        s1.insert(0, key)
        return s1, s2
    if key in s1:
        i = s1.index(key)
        if i < len(s2):
            if value in s2:
                v = s2.index(value)
                s2[v] = None
            s2[i] = value
            return s1, s2
    if value in s2:
        i = s2.index(value)
        if i < len(s1):
            if key in s1:
                k = s1.index(key)
                s1[k] = None
            s1[i] = key
            return s1, s2
    i = 0
    while i < len(s1) and i < len(s2):
        if s1[i] is None or s2[i] is None:
            break
        i += 1
    s1.insert(i, key)
    s2.insert(i, value)
    return s1, s2

def partition_refinement(representation: str):
    RA = RegisterAutomata(representation)
    full_domain = RA.get_states()
    partition = []
    partition_dict = dict()
    r = RA.get_registers()
    x = len(r)
    for _ in range(x):
        r.append("#")
    big_perm = knuth_L_algorithm(r)
    big_sf = frozenset(r)
    perms = {big_sf: big_perm}
    print("BOOP")
    for q in full_domain:
        partition_dict[q] = dict()
        registers = list(RA.s_map[q])
        reg_length = len(registers)
        for _ in range(reg_length):
            registers.append("#")
        sf = frozenset(registers)
        # registers = frozenset(RA.s_map[q])
        if sf not in perms:
            s = set(registers)
            perms[sf] = list()
            for i in range(len(big_perm) - 1, -1, -1):
            # for x in big_perm:
                x = big_perm[i]
                x = x[:reg_length]
                if set(x).issubset(s):
                    if x not in perms[sf]:
                        perms[sf].append(x)
                        partition.append((q, x))
                        partition_dict[q][x] = partition
            # perms[sf].sort(reverse=True)
            # perms[sf] = list(permutations(registers, reg_length))
            # perms[registers].sort()
        else:
            all = perms[sf]
            for i in range(len(all)):
                p = perms[sf][i]
                partition.append((q, p))
                partition_dict[q][p] = partition
    pi = [partition]
    # print("MODEL:\n\t", partition)
    for p in partition:
        print(p)
    print("Boop")
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(pi):
            B = pi[i]
            B2 = split(B, RA, partition_dict)
            if B2:
                changed = True
                pi.append(B2)
            i += 1
        print("Pass!")
        # print("NEW MODEL:")
        # for block in pi:
        #     print(f"\t{block}")
    return pi


def bisim_ok(pair_1, pair_2, partition_dict):
    # dom = list(sigma.domain)
    # while len(dom) < len(RA.s_map[q1]):
    #     dom.append(None)
    # rng = list(sigma.image)
    # while len(rng) < len(RA.s_map[q2]):
    #     rng.append(None)
    # return partition_dict[q1][tuple(dom)] == partition_dict[q2][tuple(rng)]
    # dom = tuple(sigma.domain)
    # rng = tuple(sigma.image)
    # for d1 in partition_dict[q1]:
    #     if d1[:len(dom)] == dom:
    #         for d2 in partition_dict[q2]:
    #             if d2[:len(rng)] == rng:
    #                 if partition_dict[q1][d1] == partition_dict[q2][d2]:
    #                     return True
    # return False
    q1, s1 = pair_1
    q2, s2 = pair_2
    try:
        return partition_dict[q1][s1] == partition_dict[q2][s2]
    except KeyError:
        print("PD: ")
        for (k,v) in partition_dict.items():
            print(k, v)
        print(*pair_1)
        print(*pair_2)
        print(partition_dict[q1])
        print(partition_dict[q2])
        print(partition_dict[q1][s1])
        print(partition_dict[q2][s2])
        exit(5)

def simulate(pair_1, pair_2, RA, partition_dict) -> bool:
    q1, s1 = pair_1
    q2, s2 = pair_2
    sigma = PartialPermutation(RA.get_registers(), set(zip(s1, s2)))
    transitions_1, transitions_2 = RA.get_transitions(q1), RA.get_transitions(q2)
    for pair in transitions_1:
        if pair[1] == "K":
            lb1 = pair[0]
            if sigma.in_domain(lb1):
                lb2 = sigma.get(lb1)
                pair_2 = (lb2, "K")
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        n_1, n_2 = restrict((next_q1, s1), (next_q2, s2), RA)
                        # n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                        if bisim_ok(n_1, n_2, partition_dict):
                        # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                            found = True
                            break
                    if not found:
                        return False
            elif lb1 in sigma.dom_sub(RA.s_map[q1]):
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for pair_2 in transitions_2:
                        if not pair_2[1] == "L":
                            continue
                        s1_n, s2_n = add(s1, s2, lb1, pair_2[0])
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                            if bisim_ok(n_1, n_2, partition_dict):
                            # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        return False

        elif pair[1] == "L":
            lb1 = pair[0]
            for next_q1 in RA.get_trans_lbl(q1, pair):
                found = False
                for pair_2 in transitions_2:
                    if pair_2[1] == "L":
                        s1_n, s2_n = add(s1, s2, pair[0], pair_2[0])
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                            if bisim_ok(n_1, n_2, partition_dict):
                            # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                found = True
                                break
                        if found:
                            break
                if not found:
                    return False

            sub = sigma.img_sub(RA.s_map[q2])
            for lb2 in sub:
                pair_2 = (lb2, "K")
                s1_n, s2_n = add(s1, s2, lb1, lb2)
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                        if bisim_ok(n_1, n_2, partition_dict):
                        # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                            found = True
                            break
                    if not found:
                        return False
    return True


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    # ra = det(2)
    ra = combiner(det(2), det(2))
    # ra = "{q0,q1,q2,p0,p1,p2}{q0}{(q0)(q1,1)(q2,1,2)(p0)(p1,2)(p2,2,1)}{(q0,1,L,q1)(q1,2,L,q2)(p0,2,L,p1)(p1,1,L,p2)}{}"
    times = []
    print("RA:", ra)
    t = dt.now()
    p = partition_refinement(ra)
    t = (dt.now() - t).total_seconds()
    times.append(t)
    print("Result: ")
    i = 1
    for partition in p:
        print(f"{i}:")
        for x in partition:
            print(f"\t{x}")
        i += 1
    print("\n\nTime taken: ", t)

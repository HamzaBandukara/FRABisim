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
        yield tuple(seq)
        return
    a = sorted(seq)
    limit = len(a) // 2
    while True:
        ret = list(a[:limit])
        yield tuple(ret)
        # k = limit - 1
        k = len(a) - 2
        while k > -1:
            if a[k] < a[k + 1]:
                break
            k -= 1
        if k < 0:
            return
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


def split(B, RA, partition_dict):
    B2 = list()
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

def partition_refinement(representation: str):
    global RA
    RA = RegisterAutomata(representation)
    full_domain = RA.get_states()
    partition = list()
    partition_dict = dict()
    perms = {}
    for q in full_domain:
        partition_dict[q] = dict()
        registers = list(RA.s_map[q])
        reg_length = len(registers)
        for _ in range(reg_length):
            registers.append("#")
        sf = frozenset(registers)
        # registers = frozenset(RA.s_map[q])
        if sf not in perms:
            perms[sf] = list(set((knuth_L_algorithm(registers))))
            perms[sf].sort(reverse=True)
            # perms[sf] = list(permutations(registers, reg_length))
            # perms[registers].sort()
        all = perms[sf]
        for i in range(len(all)):
            p = perms[sf][i]
            partition.append((q, p))
            partition_dict[q][p] = partition
    pi = [partition]
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
                # print("REFINED")
                # print(B)
                # print(B2)
            i += 1
        print("NEW MODEL:")
        for block in pi:
            print(f"\t{block}")
    return pi


def bisim_ok(q1, sigma: PartialPermutation, q2, partition_dict):
    global RA
    sf = sigma.set_form()
    s1, s2 = [], []
    for (x, y) in sf:
        s1.append(x)
        s2.append(y)
    # s1 = list(sigma.domain)
    # s2 = list(sigma.image)
    while len(s1) < len(RA.s_map[q1]):
        s1.append("#")
    while len(s2) < len(RA.s_map[q2]):
        s2.append("#")
    assert PartialPermutation(sigma.full_domain, set(zip(s1, s2))) == sigma
    s1, s2 = tuple(s1), tuple(s2)
    y = partition_dict[q1][s1] == partition_dict[q2][s2]
    return y

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
                        # n_1, n_2 = restrict((next_q1, s1), (next_q2, s2), RA)
                        n_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                        if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
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
                        # print("A")
                        # print(s1, s2)
                        new_sigma = sigma.add(lb1, pair_2[0])
                        # s1_n, s2_n = add(s1, s2, lb1, pair_2[0])
                        # print(s1_n, s2_n)
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            # n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                            # if bisim_ok(n_1, n_2, partition_dict):
                            n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
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
                        # print("B")
                        # print(s1, s2)
                        # s1_n, s2_n = add(s1, s2, pair[0], pair_2[0])
                        new_sigma = sigma.add(pair[0], pair_2[0])
                        # print(s1_n, s2_n)
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
                            # n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                            # print("HIT", *n_1, *n_2)
                            # if bisim_ok(n_1, n_2, partition_dict):
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
                # print("C")
                # print(s1, s2)
                # s1_n, s2_n = add(s1, s2, lb1, lb2)
                new_sigma = sigma.add(lb1, lb2)
                # print(s1_n, s2_n)
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        # n_1, n_2 = restrict((next_q1, s1_n), (next_q2, s2_n), RA)
                        # print("HIT", *n_1, *n_2)
                        # if bisim_ok(n_1, n_2, partition_dict):
                        n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                        if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
                        # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                            found = True
                            break
                    if not found:
                        return False
    return True

RA = None
if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    # ra = det(2)
    ra = combiner(det(2), det(2))
    # ra = "{q0,q1,q2,p0,p1,p2}{q0}{(q0)(q1,1)(q2,1,2)(p0)(p1,2)(p2,2,1)}{(q0,1,L,q1)(q1,2,L,q2)(p0,2,L,p1)(p1,1,L,p2)}{}"
    print("RA: ", RegisterAutomata(ra))
    times = []
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



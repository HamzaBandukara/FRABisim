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


def split(B: set, RA, partition_dict):
    B2 = set()
    B1 = list(B)
    q1, s1 = B1.pop(0)
    while len(B1) > 0:
        q2, s2 = B1.pop(0)
        sigma = PartialPermutation(RA.get_registers(), set(zip(s1, s2)))
        if simulate(q1, sigma, q2, RA, partition_dict):
            if simulate(q2, ~sigma, q1, RA, partition_dict):
                continue
        B2.add((q2, s2))
    for (q2, s2) in B2:
        partition_dict[q2][s2] = B2
        B.remove((q2, s2))
    return B2


def partition_refinement(representation: str):
    RA = RegisterAutomata(representation)
    full_domain = RA.get_states()
    partition = set()
    partition_dict = dict()
    perms = {}
    for q in full_domain:
        partition_dict[q] = dict()
        registers = frozenset(RA.s_map[q])
        # registers = frozenset(RA.s_map[q])
        if registers not in perms:
            perms[registers] = list(permutations(registers))
            # perms[registers].sort()
        all = perms[registers]
        for p in all:
            partition.add((q, p))
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
            i += 1
    return pi


def bisim_ok(q1, sigma: PartialPermutation, q2, partition_dict):
    dom = tuple(sigma.domain)
    rng = tuple(sigma.image)
    # return partition_dict[q1][dom] == partition_dict[q2][rng]
    for d1 in partition_dict[q1]:
        if d1[:len(dom)] == dom:
            for d2 in partition_dict[q2]:
                if d2[:len(rng)] == rng:
                    if partition_dict[q1][d1] == partition_dict[q2][d2]:
                        return True
    return False

def simulate(q1, sigma, q2, RA, partition_dict) -> bool:
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
                        n_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                        # n_sigma = sigma.harpoon(next_q1, next_q2, RA)
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
                        new_sigma = sigma.add(lb1, pair_2[0])
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
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
                        new_sigma = sigma.add(pair[0], pair_2[0])
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
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
                new_sigma = sigma.add(lb1, lb2)
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                        if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
                        # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                            found = True
                            break
                    if not found:
                        return False
    return True


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    ra = combiner(det(2), det(2))
    # ra = "{q0,q1,q2,p0,p1,p2}{q0}{(q0)(q1,1)(q2,1,2)(p0)(p1,2)(p2,2,1)}{(q0,1,L,q1)(q1,2,L,q2)(p0,2,L,p1)(p1,1,L,p2)}{}"
    times = []
    t = dt.now()
    p = partition_refinement(ra)
    t = (dt.now() - t).total_seconds()
    times.append(t)
    print("Result: ")
    for partition in p:
        print(partition)
    print("\n\nTime taken: ", t)



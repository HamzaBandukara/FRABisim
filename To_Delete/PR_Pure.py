# from DataStructures.SetPermutation import *
from itertools import permutations
# from DataStructures.RA_SF_A import RegisterAutomata
# from DataStructures.RA_SF_A import RegisterAutomata
# from DataStructures.SetPermutation import *
from Generator.generator import *
from datetime import datetime as dt
from time import process_time

from random import choice
from RAStack.Generator import generate_stack as det
from RAStack.NDGenerator import generate_stack as ndet
from RAStack.Combiner import combiner
from copy import deepcopy as cp


class NotBisimilarException(Exception):
    pass


def knuth_L_algorithm(seq):
    if len(seq) == 0:
        yield tuple(seq)
        return
    a = sorted(seq)
    limit = len(a) // 2
    while True:
        ret = list(a[:limit])
        for i in range(len(ret)):
            if ret[i] == "#":
                ret[i] = None
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


def split(B: set, RA, partition_dict):
    B2 = set()
    B1 = list(B)
    q1, s1 = B1.pop(0)
    while len(B1) > 0:
        q2, s2 = B1.pop(0)
        sigma = PartialPermutation(RA.get_registers(), set(zip(s1, s2)))
        if simulate(q1, sigma, q2, RA, partition_dict):
            # print("SIM1")
            if simulate(q2, ~sigma, q1, RA, partition_dict):
                # print("PASS")
                continue
        # print("FAILED")
        B2.add((q2, s2))
    for (q2, s2) in B2:
        partition_dict[q2][s2] = B2
        B.remove((q2, s2))
    return B2


def split_2(B: set, RA, partition_dict, pair_1, pair_2):
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
    if pair_1 in B2:
        if pair_2 not in B2:
            raise NotBisimilarException
    elif pair_2 in B2:
        raise NotBisimilarException
    return B2


def is_bisim(RA: RegisterAutomata, q1, q2, sigma):
    sigma = PartialPermutation(RA.get_states(), sigma)
    dom = sigma.domain
    img = sigma.image
    try:
        pr_2(RA, (q1, tuple(dom)), (q2, tuple(img)))
    except NotBisimilarException:
        return False
    return True


def pr_2(RA: RegisterAutomata, pair_1, pair_2):

    full_domain = RA.get_states()
    partition = set()
    # partition = {}
    partition_dict = dict()
    perms = {}
    for q in full_domain:
        partition_dict[q] = dict()
        registers = list(RA.s_map[q])
        sf = frozenset(registers)
        if sf not in perms:
            perms[sf] = list()
            for i in range(len(sf) + 1):
                perms[sf].extend(permutations(sf, i))
        all = perms[sf]
        for i in range(len(all)):
            p = perms[sf][i]
            partition.add((q, p))
            partition_dict[q][p] = partition
            # p = perms[sf][i]
            # if len(p) not in partition:
            #     partition[len(p)] = set()
            # partition[len(p)].add((q, p))
            # partition_dict[q][p] = partition[len(p)]
    pi = [partition]
    # pi = [partition[x] for x in partition]
    changed = True
    times = []
    while changed:
        start_time = process_time()
        changed = False
        i = 0
        while i < len(pi):
            B = pi[i]
            B2 = split_2(B, RA, partition_dict, pair_1, pair_2)
            if B2:
                changed = True
                pi.append(B2)
            i += 1
        times.append(process_time() - start_time)
        # print("PASS: ")
        # for block in pi:
        #     print("\t", block)

    return pi


def partition_refinement(representation: str, flag=True):
    set_up_start = process_time()
    RA = RegisterAutomata(representation)
    full_domain = RA.get_states()
    partition = {}
    partition_dict = dict()
    perms = {}
    for q in full_domain:
        partition_dict[q] = dict()
        registers = list(RA.s_map[q])
        sf = frozenset(registers)
        if sf not in perms:
            perms[sf] = list()
            for i in range(len(sf) + 1):
                perms[sf].extend(permutations(sf, i))
        all = perms[sf]
        for i in range(len(all)):
            p = perms[sf][i]
            if len(p) not in partition:
                partition[len(p)] = set()
            partition[len(p)].add((q, p))
            partition_dict[q][p] = partition[len(p)]
    pi = [partition[x] for x in partition]
    set_up_final = process_time()
    set_up_time = set_up_final - set_up_start
    times = []
    changed = True
    while changed:
        start = process_time()
        changed = False
        i = 0
        while i < len(pi):
            B = pi[i]
            B2 = split(B, RA, partition_dict)
            # print("REFINED!")
            # for block in pi:
            #     print(*block)
            # print("\n")
            if B2:
                changed = True
                pi.append(B2)
            i += 1
        times.append(process_time() - start)
        # print("PASS: ")
        # for block in pi:
        #     print("\t", block)
    print("Time Taken To Set-Up - ", set_up_time)
    for i in range(len(times)):
        print("\tPass {}: {}".format(i + 1, times[i]))
    return pi


def bisim_ok(q1, sigma: PartialPermutation, q2, partition_dict, RA):
    # dom = list(sigma.domain)
    # while len(dom) < len(RA.s_map[q1]):
    #     dom.append(None)
    # rng = list(sigma.image)
    # while len(rng) < len(RA.s_map[q2]):
    #     rng.append(None)
    # return partition_dict[q1][tuple(dom)] == partition_dict[q2][tuple(rng)]
    dom = tuple(sigma.domain)
    rng = tuple(sigma.image)
    return partition_dict[q1][dom] == partition_dict[q2][rng]
    # for d1 in partition_dict[q1]:
    #     if d1[:len(dom)] == dom:
    #         for d2 in partition_dict[q2]:
    #             if d2[:len(rng)] == rng:
    #                 if partition_dict[q1][d1] == partition_dict[q2][d2]:
    #                     return True
    # return False

def simulate(q1, sigma, q2, RA, partition_dict) -> bool:
    all_trans_1, all_trans_2 = RA.get_transitions(q1), RA.get_transitions(q2)
    # if set(all_trans_1.keys()) != set(all_trans_2.keys()):
    #     return False
    for tag in all_trans_1:
        if tag not in all_trans_2:
            return False
        transitions_1, transitions_2 = all_trans_1[tag], all_trans_2[tag]
        for pair in transitions_1:
            if pair[1] == "K":
                lb1 = pair[0]
                if sigma.in_domain(lb1):
                    lb2 = sigma.get(lb1)
                    pair_2 = (lb2, "K")
                    for next_q1 in RA.get_trans_lbl(q1, tag,pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag,pair_2):
                            n_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            # n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict, RA):
                            # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                found = True
                                break
                        if not found:
                            return False
                elif lb1 in sigma.dom_sub(RA.s_map[q1]):
                    for next_q1 in RA.get_trans_lbl(q1, tag,pair):
                        found = False
                        for pair_2 in transitions_2:
                            if not pair_2[1] == "L":
                                continue
                            new_sigma = sigma.add(lb1, pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag,pair_2):
                                n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                                if bisim_ok(next_q1, n_sigma, next_q2, partition_dict, RA):
                                # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            return False

            elif pair[1] == "L":
                lb1 = pair[0]
                for next_q1 in RA.get_trans_lbl(q1, tag,pair):
                    found = False
                    for pair_2 in transitions_2:
                        if pair_2[1] == "L":
                            new_sigma = sigma.add(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag,pair_2):
                                n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                                if bisim_ok(next_q1, n_sigma, next_q2, partition_dict, RA):
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
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict, RA):
                            # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                found = True
                                break
                        if not found:
                            return False
    return True


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    ra = combiner(det(7), det(7))
    # ra = "{q1,q2}{q1}{(q1,1,2)(q2,1,2)}{(q1,1,K,q1)(q1,1,L,q1)(q1,2,K,q1)(q2,1,K,q2)(q2,1,L,q2)(q2,2,K,q2)}{}"
    print("RA: ", ra)
    # ra = "{q0,q1,q2,p0,p1,p2}{q0}{(q0)(q1,1)(q2,1,2)(p0)(p1,2)(p2,2,1)}{(q0,1,L,q1)(q1,2,L,q2)(p0,2,L,p1)(p1,1,L,p2)}{}"
    times = []
    # print(is_bisim(RegisterAutomata(ra), "q0", "p0", set()))
    # print("RA:", ra)
    t = dt.now()
    p = partition_refinement(ra)
    t = (dt.now() - t).total_seconds()
    times.append(t)
    print("Result: ")
    # i = 1
    # for partition in p:
    #     print(f"{i}:")
    #     for x in partition:
    #         print(f"\t{x}")
    #     i += 1
    print("\n\nTime taken: ", t)



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


class NotBisimilarException(Exception):
    pass


class PartitionSystem:
    def __init__(self, RA: RegisterAutomata):
        full_domain = RA.get_states()
        partition = list()
        self.partition_dict = dict()
        perms = {}
        for q in full_domain:
            self.partition_dict[q] = dict()
            registers = list(RA.s_map[q])
            sf = frozenset(registers)
            if sf not in perms:
                perms[sf] = list()
                for i in range(len(sf) + 1):
                    perms[sf].extend(permutations(sf, i))
            all = perms[sf]
            for i in range(len(all)):
                p = perms[sf][i]
                partition.append((q, p))
                self.partition_dict[q][p] = partition
        self.pi = [partition]
        RA.set_up_reachables(partition)

    def __len__(self):
        return len(self.pi)

    def get(self, i):
        return self.pi[i]

    def add(self, B):
        self.pi.append(B)


def split(B, RA: RegisterAutomata, pi, next_targets, tag, gen_action):
    B2 = list()
    q1, s1 = B[0]
    pos = None
    if not gen_action == "FRESH":
        if gen_action in s1:
            pos = s1.index(gen_action)
        else:
            pos = len(s1)
    for i in range(1, len(B)):
        q2, s2 = B[i]
        sigma = PartialPermutation(RA.get_registers(), set(zip(s1, s2)))
        if gen_action == "FRESH":
            next_targets_2 = RA.get_next_blocks_specific((q2, s2), pi.partition_dict, pi.pi, tag, "FRESH2")
        elif gen_action in s1:
            next_targets_2 = RA.get_next_blocks_specific((q2, s2), pi.partition_dict, pi.pi, tag, s2[pos])
        else:
            next_targets_2 = RA.get_next_blocks_specific((q2, s2), pi.partition_dict, pi.pi, tag, "FRESH")


def compare_next(nxt_1, nxt_2, pi, sigma):
    for action in nxt_1:
        if action[1] == "K":

            for a2 in nxt_2:
                pass


    # while len(B1) > 0:
    # #     q2, s2 = B1.pop(0)
    # #     sigma = PartialPermutation(RA.get_registers(), set(zip(s1, s2)))
    # #     if simulate(q1, sigma, q2, RA, pi):
    # #         if simulate(q2, ~sigma, q1, RA, pi):
    # #             continue
    # #     B2.append((q2, s2))
    # for (q2, s2) in B2:
    #     pi.partition_dict[q2][s2] = B2
    #     B.remove((q2, s2))
    # return B2


# Reg_1, Reg_2 = sequence of dom, rng of sigma
# next_1, next_2 = Tag, (Action, reachable configurations)
def match(reg_1, reg_2, next_1, next_2) -> bool:
    tags = set(next_1.keys())
    if tags != set(next_2.keys()):
        return False
    for tag in tags:
        targets = set(next_1[tag].keys()).union(set(next_2[tag].keys()))
        for action in targets:
            if not is_match(reg_1, reg_2, next_1, next_2, action):
                return False
    return True

# def match(reg_1, reg_2, next_1, next_2) -> bool:
#     tags = set(next_1.keys())
#     if tags != set(next_2.keys()):
#         return False
#     for tag in tags:
#         targets = set(next_1[tag].keys()).union(set(next_2[tag].keys()))
#         for action in targets:
#             if not is_match(reg_1, reg_2, next_1, next_2, action):
#                 return False
#     return True

def local_match(reg_1, reg_2, next_1, next_2, action):
    targets = [(i, "K") for i in range(len(reg_1), len(reg_2))]
    flag = False
    for a2 in next_2:
        if a2[1] == "K":
            if a2 not in targets:
                continue
            if not next_1[action] == next_2[a2]:
                return False
            else:
                targets.remove(a2)
        elif a2[1] == "L":
            if next_1[action] == next_2[a2]:
                flag = True
                break
    if not flag:
        return False
    while len(targets) > 0:
        a2 = targets.pop(0)
        if a2 not in next_2:
            return False
        if next_2[a2] != next_1[action]:
            return False
    return True


def is_match(reg_1, reg_2, next_1, next_2, action):
    # Case: Known
    if action[1] == "K":
        if action[0] < len(reg_1) and action[0] < len(reg_2):
            if action not in next_1 or action not in next_2:
                return False
            return next_1[action] == next_2[action]
        if action in next_1:
            return known_match(next_1, next_2, action)
        else:
            return known_match(next_2, next_1, action)
    # Case: Local
    else:
        if action in next_1:
            if not local_match(reg_1, reg_2, next_1, next_2, action):
                return False
        if action in next_2:
            return local_match(reg_2, reg_1, next_2, next_1, action)


def known_match(next_1, next_2, action):
    for a2 in next_2:
        if a2[1] == "L":
            if next_1[action] == next_2[a2]:
                return True
    return False


def split_2(B: list, RA: RegisterAutomata, pi, pair_1, pair_2):
    B2 = list()
    B1 = list(B)
    q1, s1 = B1.pop(0)
    next_blocks = RA.get_next_blocks((q1, s1), pi.partition_dict, pi.pi)
    while len(B1) > 0:
        q2, s2 = B1.pop(0)
        next_2 = RA.get_next_blocks((q2, s2), pi.partition_dict, pi.pi)
        if not match(s1, s2, next_blocks, next_2):
            B2.append((q2, s2))
        # if next_blocks == next_2:
    for (q2, s2) in B2:
        pi.partition_dict[q2][s2] = B2
        B.remove((q2, s2))
    # if pair_1 in B2:
    #     if pair_2 not in B2:
    #         raise NotBisimilarException
    # elif pair_2 in B2:
    #     raise NotBisimilarException
    return B2


def is_bisim(RA: RegisterAutomata, q1, q2, sigma):
    sigma = PartialPermutation(RA.get_states(), sigma)
    dom = sigma.domain
    img = sigma.image
    pi = PartitionSystem(RA)
    try:
        pr_2(RA, pi, (q1, tuple(dom)), (q2, tuple(img)))
        i = 1
        for block in pi.pi:
            print(i, ":")
            for x in block:
                print("\t", x)
            i += 1

    except NotBisimilarException:
        i = 1
        for block in pi.pi:
            print(i, ":")
            for x in block:
                print("\t", x)
            i += 1
        return False
    return True


def pr_2(RA: RegisterAutomata, pi, pair_1, pair_2):
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(pi):
            B = pi.get(i)
            rep, rep_s = B[0]
            print(rep, rep_s)
            next_blocks = RA.get_next_blocks((rep, rep_s), pi.partition_dict, pi.pi)
            print(next_blocks)
            # for tag in next_blocks:
            #     for gen_action in next_blocks[tag]:
            #         B2 = split(B, RA, pi, next_blocks[tag][gen_action], tag, gen_action)
            #         if B2:
            #             changed = True
            #             pi.add(B2)
            i += 1
        # if changed:
        #     print("CHANGE")
        #     j = 0
        #     for block in pi.pi:
        #         print(j, ":")
        #         for x in block:
        #             print("\t", x)
        #         j += 1
    return pi


def bisim_ok(q1, sigma: PartialPermutation, q2, pi: PartitionSystem):
    dom = tuple(sigma.domain)
    rng = tuple(sigma.image)
    return pi.partition_dict[q1][dom] == pi.partition_dict[q2][rng]


def simulate(q1, sigma, q2, RA, partition_dict) -> bool:
    all_trans_1, all_trans_2 = RA.get_transitions(q1), RA.get_transitions(q2)
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
                            if bisim_ok(next_q1, n_sigma, next_q2, partition_dict):
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
                for next_q1 in RA.get_trans_lbl(q1, tag,pair):
                    found = False
                    for pair_2 in transitions_2:
                        if pair_2[1] == "L":
                            new_sigma = sigma.add(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag,pair_2):
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
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
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
    # ra = "{q1,q2,p1,p2}{q1}{(q1)(q2,1)(p1,1),(p2,1,2)}{(q1,1,L,q2)(p1,1,K,p2)(p1,1,L,p2)}{}"
    times = []
    print(is_bisim(RegisterAutomata(ra), "p1", "q1", set()))
    print("RA:", ra)
    # t = dt.now()
    # p = partition_refinement(ra)
    # t = (dt.now() - t).total_seconds()
    # times.append(t)
    # print("Result: ")
    # i = 1
    # for partition in p:
    #     print(f"{i}:")
    #     for x in partition:
    #         print(f"\t{x}")
    #     i += 1
    # print("\n\nTime taken: ", t)



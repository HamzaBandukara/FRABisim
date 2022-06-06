from copy import copy
from itertools import product
from datetime import datetime as dt
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma
# from DataStructures.RootedTree import Tree

from RAGen.Generator import generate_stack as det
from RAGen.GloGenerator import generate_stack as glodet
from RAGen.NDGenerator import generate_stack as ndet
from RAGen.Combiner import combiner
from RAGen.CPTGenerator import generate as cpt
from copy import deepcopy as cp

GLOBAL_COUNTER = 0
STATS_CALLS = 0
STATS_NEWCALLS = 0

def ra_bisim(RA: RegisterAutomata, q1=None, q2=None, sigma=None, stats=False):
    if q1 is None:
        q1 = RA.initial
    if q2 is None:
        q2 = RA.initial
    if sigma is None:
        sigma = set()
    if q1 not in RA.s_map:
        raise ValueError("Non-Existent State")
    if q2 not in RA.s_map:
        raise ValueError("Non-Existent State")
    sigma = Sigma(sigma)
    R = (q1, sigma, q2)
    memo, bad = {}, set()
    result = bisim_ok(R, RA, memo, set(), set(), bad)
    if stats:
        bisim = memo
        not_bisim = bad
        if not result:
            bisim = []
        return result, ("fwd_2", STATS_CALLS, STATS_NEWCALLS, memo, bisim, not_bisim)
    return result


def bisim_ok(triple: tuple, RA: RegisterAutomata, memo: dict, deleted: set, assumed: set, bad: set) -> bool:
    if triple in bad: return False
    try:
        if memo[triple] not in deleted:
            assumed.add(memo[triple])
            return True
    except:
        pass
    global GLOBAL_COUNTER
    q1, sigma, q2 = triple[0], triple[1], triple[2]
    inverse = sigma.invert()
    GLOBAL_COUNTER += 1
    memo[triple] = GLOBAL_COUNTER
    memo[(q2, inverse, q1)] = GLOBAL_COUNTER
    counter = GLOBAL_COUNTER
    if simulate(q1, sigma, q2, RA, memo, deleted, assumed, bad):
        if simulate(q2, inverse, q1, RA, memo, deleted, assumed, bad):
            return True
    bad.add(triple)
    bad.add((q2, inverse, q1))
    if memo[triple] in assumed:
        for i in range(counter, GLOBAL_COUNTER + 1):
            deleted.add(i)
            assumed.discard(i)
    return False


def simulate(q1, sigma, q2, RA, memo, deleted, assumed, bad) -> bool:
    all_trans_1, all_trans_2 = RA.get_transitions(q1), RA.get_transitions(q2)
    for tag in all_trans_1:
        if tag not in all_trans_2:
            return False
        transitions_1, transitions_2 = all_trans_1[tag], all_trans_2[tag]
        for pair in transitions_1:
            if pair[1] == "TAU":
                for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, tag, pair):
                        n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                        if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                            found = True
                            break
                    if not found:
                        return False
            if pair[1] == "K":
                lb1 = pair[0]
                if sigma.in_dom(lb1):
                    lb2 = sigma[lb1]
                    pair_2 = (lb2, "K")
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                                found = True
                                break
                        if not found:
                            return False
                elif lb1 in sigma.dom_sub(RA.s_map[q1]):
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for pair_2 in transitions_2:
                            if not pair_2[1] == "L":
                                continue
                            new_sigma = sigma.generate_temp_sigma(lb1, pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            return False

            elif pair[1] == "L":
                lb1 = pair[0]
                for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                    found = False
                    for pair_2 in transitions_2:
                        if pair_2[1] == "L":
                            new_sigma = sigma.generate_temp_sigma(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                                    found = True
                                    break
                            if found:
                                break
                    if not found:
                        return False
                sub = sigma.rng_sub(RA.s_map[q2])
                for lb2 in sub:
                    pair_2 = (lb2, "K")
                    new_sigma = sigma.generate_temp_sigma(lb1, lb2)
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                                found = True
                                break
                        if not found:
                            return False
            elif pair[1] == "G":
                for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                    found = False
                    for pair_2 in transitions_2:
                        if pair_2[1] == "G":
                            new_sigma = sigma.generate_temp_sigma(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, deleted, assumed, bad):
                                    found = True
                                    break
                            if found:
                                break
                    if not found:
                        return False
    return True

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(50000)
    # ra = generate_stack(50)
    # # ra = "{q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10}{q0}{(q0)(q1,1)(q2,1,2)(q3,1,2,3)(q4,1,2,3,4)(q5,1,2,3,4,5)(q6,1,2,3,4,5,6)(q7,1,2,3,4,5,6,7)(q8,1,2,3,4,5,6,7,8)(q9,1,2,3,4,5,6,7,8,9)(q10,1,2,3,4,5,6,7,8,9,10)}{(q0,1,L,q1)(q1,1,K,q0)(q1,2,L,q2)(q2,2,K,q1)(q2,3,L,q3)(q3,3,K,q2)(q3,4,L,q4)(q4,4,K,q3)(q4,5,L,q5)(q5,5,K,q4)(q5,6,L,q6)(q6,6,K,q5)(q6,7,L,q7)(q7,7,K,q6)(q7,8,L,q8)(q8,8,K,q7)(q8,9,L,q9)(q9,9,K,q8)(q9,10,L,q10)(q10,10,K,q9)}{}"
    # ra = combiner(ndet(10), ndet(11))
    # ra = "{q3,q4,q2,q1}{q1}{(q1)(q2,1)(q3,2,1)(q4,3,2,1)}{(q2,1,K,q1),(q2,2,L,q3),(q1,1,L,q2),(q3,3,L,q4),(q3,2,K,q2),(q4,3,K,q3)}{}"
    ra = cpt(200)
    ra2 = cpt(200)
    ra = RegisterAutomata(combiner(ra, ra2))
    # ra = "{q4,q10,q1,q11,q5,q12,q2,q6,q7,q3,q8,q9}{q1}{(q1)(q2,1)(q3,2)(q4,2)(q5,2,1)(q6,3,2)(q7,3,2)(q8,3,2,1)(q9,3,4,2)(q10,3,4,2)(q11,3,4,2,1)(q12,3,4,2,1)}{(q7,4,L,q9),(q7,1,L,q8),(q10,1,L,q12),(q9,4,K,q10),(q2,1,K,q1),(q4,3,L,q6),(q5,2,K,q1),(q4,1,L,q5),(q10,1,L,q11),(q6,3,K,q7),(q1,1,L,q2),(q3,2,K,q4),(q8,3,K,q4),(q11,4,K,q7),(q12,1,K,q10),(q1,2,L,q3)}{}"
    times = []
    # for i in range(1000000):
    #     t = dt.now()
    #     result = forward(ra, "q0", "p0", set())
    #     t = (dt.now() - t).total_seconds()
    #     times.append(t)
    #     print(t)
    #     print(result)
    # print("AVG", sum(times) / len(times))
    t = dt.now()
    result = ra_bisim(ra, "q1", "p1", set())
    t = (dt.now() - t).total_seconds()
    times.append(t)
    print(t)
    print(result)
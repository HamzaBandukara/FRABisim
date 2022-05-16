from copy import copy
from itertools import product
from datetime import datetime as dt
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma

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
    memo = dict()
    result = bisim_ok(R, RA, memo, [], set())
    if stats:
        bisim = {k for k,v in memo.items() if v}
        not_bisim = set(memo.keys()) - (bisim)
        if not result:
            bisim = []
        return result, ("fwd_1",STATS_CALLS, STATS_NEWCALLS, memo, bisim, not_bisim)
    return result


def bisim_ok(relation: tuple, RA: RegisterAutomata, memo: dict, old_visited: list, old_assumed: set) -> bool:
    global STATS_CALLS
    global STATS_NEWCALLS
    STATS_CALLS += 1
    if relation in memo:
        if memo[relation]:
            old_assumed.add(relation)
        return memo[relation]
    STATS_NEWCALLS += 1
    try:
        assert len(memo.keys()) == len(set(memo.keys()))
    except AssertionError:
        print(len(memo.keys()))
        print(len(set(memo.keys())))
        exit(95)
    q1, sigma, q2 = relation[0], relation[1], relation[2]
    memo[relation] = True
    inverse = sigma.invert()
    memo[(q2, inverse, q1)] = True
    visited = [relation, (q2, inverse, q1)]
    assumed = set()
    # assumed = copy(old_assumed)
    if simulate(q1, sigma, q2, RA, memo, visited, assumed):
        if simulate(q2, inverse, q1, RA, memo, visited, assumed):
            old_visited.extend(visited)
            for e in assumed:
                old_assumed.add(e)
            return True
    if relation in assumed or (q2, inverse, q1) in assumed:
        for triple in visited:
            if triple in memo:
                if memo[triple]:
                    del memo[triple]
    memo[relation] = False
    memo[(q2, inverse, q1)] = False
    return False


def simulate(q1, sigma, q2, RA, memo, visited, assumed) -> bool:
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
                        if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
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
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
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
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
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
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
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
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
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
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, visited, assumed):
                                    found = True
                                    break
                            if found:
                                break
                    if not found:
                        return False
    return True

# ra = open("../A-SF-RA-Cases/gloloG-3", "r").readline()
# ra = RegisterAutomata(ra)
# print("RA: ", ra)
# t = dt.now()
# result = ra_bisim(ra, "q0", "q0", set())
# print((dt.now() - t).total_seconds())
# print(result)

from itertools import product
from datetime import datetime as dt
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma
from RAStack.NDGenerator import generate_stack as ndet
from RAStack.Generator import generate_stack as det
from RAStack.Combiner import combiner


def ra_bisim(RA: RegisterAutomata, q1=None, q2=None, sigma=None):
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
    return bisim_ok(R, RA, {}, set())


def bisim_ok(relation: tuple, RA: RegisterAutomata, memo: dict, bad: set) -> bool:
    if relation in bad:
        return False
    q1, sigma, q2 = relation[0], relation[1], relation[2]
    inverse = sigma.invert()
    reverse = (q2, inverse, q1)
    if relation not in memo:
        memo[relation] = dict()
        memo[reverse] = dict()
    if simulate(q1, sigma, q2, RA, memo, bad):
        if simulate(q2, inverse, q1, RA, memo, bad):
            return True
    # print("FAILED")
    bad.add((q1,sigma,q2))
    bad.add((q2,inverse,q1))
    return False
    # q1 (visited q2) -> q2 (visited q1) -> q1 (return true) -> q2 (visited q1) -> q3


def simulate(q1, sigma, q2, RA, memo, bad) -> bool:
    # print("SIM", q1, sigma, q2)
    all_trans_1, all_trans_2 = RA.get_transitions(q1), RA.get_transitions(q2)
    for tag in all_trans_1:
        if tag not in all_trans_2:
            return False
        transitions_1, transitions_2 = all_trans_1[tag], all_trans_2[tag]
        for pair in transitions_1:
            comb = tag, pair
            # print("M", [str(k[0]) + " " + str(k[1] + " " + str(k[2])) + ": " + str(v) for k,v in memo.items()])
            if comb in memo[(q1,sigma,q2)]:
                # print("CONT")
                continue
            memo[(q1, sigma, q2)][comb] = True
            if pair[1] == "K":
                lb1 = pair[0]
                if sigma.in_dom(lb1):
                    lb2 = sigma[lb1]
                    pair_2 = (lb2, "K")
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        # print(next_q1)
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, bad):
                                found = True
                                break
                        if not found:
                            # print("F")
                            memo[(q1, sigma, q2)][comb] = False
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
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, bad):
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            memo[(q1, sigma, q2)][comb] = False
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
                                if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, bad):
                                    found = True
                                    break
                            if found:
                                break
                    if not found:
                        memo[(q1, sigma, q2)][comb] = False
                        return False
                sub = sigma.rng_sub(RA.s_map[q2])
                for lb2 in sub:
                    pair_2 = (lb2, "K")
                    new_sigma = sigma.generate_temp_sigma(lb1, lb2)
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                            if bisim_ok((next_q1, n_sigma, next_q2), RA, memo, bad):
                                found = True
                                break
                        if not found:
                            memo[(q1, sigma, q2)][comb] = False
                            return False
    return True

# ra = open("../A-SF-RA-Cases/cpt-3", "r").readline()
# print("RA: ", ra)
# t = dt.now()
# result = bisim_ok(("q1", Sigma(set()), "q1"), RegisterAutomata(ra), dict())
# print((dt.now() - t).total_seconds())
# print(result)

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    # ra = generate_stack(50)
    # # ra = "{q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10}{q0}{(q0)(q1,1)(q2,1,2)(q3,1,2,3)(q4,1,2,3,4)(q5,1,2,3,4,5)(q6,1,2,3,4,5,6)(q7,1,2,3,4,5,6,7)(q8,1,2,3,4,5,6,7,8)(q9,1,2,3,4,5,6,7,8,9)(q10,1,2,3,4,5,6,7,8,9,10)}{(q0,1,L,q1)(q1,1,K,q0)(q1,2,L,q2)(q2,2,K,q1)(q2,3,L,q3)(q3,3,K,q2)(q3,4,L,q4)(q4,4,K,q3)(q4,5,L,q5)(q5,5,K,q4)(q5,6,L,q6)(q6,6,K,q5)(q6,7,L,q7)(q7,7,K,q6)(q7,8,L,q8)(q8,8,K,q7)(q8,9,L,q9)(q9,9,K,q8)(q9,10,L,q10)(q10,10,K,q9)}{}"
    # ra = combiner(ndet(10), ndet(11))
    # ra = "{q3,q4,q2,q1}{q1}{(q1)(q2,1)(q3,2,1)(q4,3,2,1)}{(q2,1,K,q1),(q2,2,L,q3),(q1,1,L,q2),(q3,3,L,q4),(q3,2,K,q2),(q4,3,K,q3)}{}"
    ra = RegisterAutomata(combiner(det(1000),det(1000)))
    # ra = "{q4,q10,q1,q11,q5,q12,q2,q6,q7,q3,q8,q9}{q1}{(q1)(q2,1)(q3,2)(q4,2)(q5,2,1)(q6,3,2)(q7,3,2)(q8,3,2,1)(q9,3,4,2)(q10,3,4,2)(q11,3,4,2,1)(q12,3,4,2,1)}{(q7,4,L,q9),(q7,1,L,q8),(q10,1,L,q12),(q9,4,K,q10),(q2,1,K,q1),(q4,3,L,q6),(q5,2,K,q1),(q4,1,L,q5),(q10,1,L,q11),(q6,3,K,q7),(q1,1,L,q2),(q3,2,K,q4),(q8,3,K,q4),(q11,4,K,q7),(q12,1,K,q10),(q1,2,L,q3)}{}"
    times = []
    # for i in range(5):
    #     t = dt.now()
    #     result = forward(ra, "q0", "p0", set())
    #     t = (dt.now() - t).total_seconds()
    #     times.append(t)
    #     print(t)
    #     print(result)
    # print("AVG", sum(times) / len(times))
    result = None
    for _ in range(1):
        t = dt.now()
        result = ra_bisim(ra, "q0", "p0", set())
        t = (dt.now() - t).total_seconds()
        times.append(t)
        # assert not result
    print(times)
    # print(sum(times) / 5)
    print(result)
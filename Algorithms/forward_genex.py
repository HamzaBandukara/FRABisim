from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import *
from Generator.generator import *
from datetime import datetime as dt

from RAGen.Generator import generate_stack as det
from RAGen.GloGenerator import generate_stack as glodet
from RAGen.NDGenerator import generate_stack as ndet
from RAGen.Combiner import combiner
from copy import deepcopy as cp

FLAG_DEBUG = False
FLAG_CHK_TAGS = True
CHKED_TAGS = {}

def db_print(*args):
    if FLAG_DEBUG: print(*args)

def chk_tags(RA,q1,q2):
    if not FLAG_CHK_TAGS: return None
    if (q1,q2) in CHKED_TAGS: return CHKED_TAGS[(q1,q2)]
    t1 = RA.get_transitions(q1).keys()
    t2 = RA.get_transitions(q2).keys()
    CHKED_TAGS[(q1,q2)] = (t1 == t2)
    db_print("chk_tags: ",t1,t2,t1==t2)
    return CHKED_TAGS[(q1,q2)]

class WrongAssumption(Exception):
    pass

def ra_bisim(RA,q1,q2):
    return forward(RA,q1,q2,set())


def bisim_ok(G, RA, q1, sigma, q2, not_bisim):
    db_print("\nbisim_ok: ", q1, sigma, q2,"\nwith G: ", G,"\nand ~G:",not_bisim)
    if not_bisim.is_member(q1, sigma, q2):
        # print("NOT_MEMBER: ", q1, sigma, q2)
        return False
    if G.is_member(q1, sigma, q2):
        # print("IS_MEMBER: ", q1, sigma, q2)
        return True
    if FLAG_CHK_TAGS and chk_tags(RA,q1,q2) == False:
        not_bisim.update(q1, sigma, q2)
        not_bisim.update(q2, ~sigma, q1)
        return False
    G.update(q1, sigma, q2)
    if simulate(q1, sigma, q2, RA, G, not_bisim):
        if simulate(q2, ~sigma, q1, RA, G, not_bisim):
            return True
    not_bisim.update(q1, sigma, q2)
    not_bisim.update(q2, ~sigma, q1)
    db_print("UPDATE not_bisim: ",not_bisim)
    if G.is_member(q1, sigma, q2):
        raise WrongAssumption
    return False


def simulate(q1, sigma, q2, RA, G, not_bisim) -> bool:
    # print("SIM: ", q1, sigma, q2)
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
                        n_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                        if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
                            found = True
                            break
                    if not found:
                        return False
            if pair[1] == "K":
                lb1 = pair[0]
                if sigma.in_domain(lb1):
                    lb2 = sigma.get(lb1)
                    pair_2 = (lb2, "K")
                    for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                        found = False
                        for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                            n_sigma = sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                            if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
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
                            new_sigma = sigma.add(lb1, pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                                if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
                                # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
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
                            new_sigma = sigma.add(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                                if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
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
                            if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
                            # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                found = True
                                break
                        if not found:
                            return False
            elif pair[1] == "G":
                for next_q1 in RA.get_trans_lbl(q1, tag, pair):
                    found = False
                    for pair_2 in transitions_2:
                        if pair_2[1] == "G":
                            new_sigma = sigma.add(pair[0], pair_2[0])
                            for next_q2 in RA.get_trans_lbl(q2, tag, pair_2):
                                n_sigma = new_sigma.restrict(RA.s_map[next_q1], RA.s_map[next_q2])
                                if bisim_ok(G, RA, next_q1, n_sigma, next_q2, not_bisim):
                                # if bisim_ok((next_q1, n_sigma, next_q2), RA, visited, assumed, not_bisim):
                                    found = True
                                    break
                            if found:
                                break
                    if not found:
                        return False

    return True


def forward(RA: RegisterAutomata, q1: str, q2: str, sigma: set) -> bool:
    full_domain = RA.get_registers()
    sigma = PartialPermutation(full_domain, sigma)
    # NT: the domain of a PartialPermutation should be a subset of its sigma
    states = RA.get_states()
    partitions = []
    for q in states:
        dom = list(RA.s_map[q])
        rep = (
            q,
            dom,
            {PartialPermutation(dom, full_domain, [x for x in range(len(full_domain))])}
        )
        p = Partition({q}, rep, {q: PartialPermutation(full_domain, set(zip(dom, dom)))}, full_domain)
        partitions.append(p)
    G = GeneratingSystem(partitions, RA)
    not_bisim = SymmetricDownSet(G)
    db_print("\nTESTING: ", q1, sigma, q2,"\nfor A: ",RA,"\nwith G: ",G,"\nand ~G:",not_bisim)
    while True:
        try:
            return bisim_ok(cp(G), RA, q1, sigma, q2, not_bisim)
        except WrongAssumption:
            continue

def ra_bisim(RA, q1, q2, sigma=set()):
    return forward(RA, q1, q2, sigma)


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    # ra = generate_stack(50)
    # # ra = "{q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10}{q0}{(q0)(q1,1)(q2,1,2)(q3,1,2,3)(q4,1,2,3,4)(q5,1,2,3,4,5)(q6,1,2,3,4,5,6)(q7,1,2,3,4,5,6,7)(q8,1,2,3,4,5,6,7,8)(q9,1,2,3,4,5,6,7,8,9)(q10,1,2,3,4,5,6,7,8,9,10)}{(q0,1,L,q1)(q1,1,K,q0)(q1,2,L,q2)(q2,2,K,q1)(q2,3,L,q3)(q3,3,K,q2)(q3,4,L,q4)(q4,4,K,q3)(q4,5,L,q5)(q5,5,K,q4)(q5,6,L,q6)(q6,6,K,q5)(q6,7,L,q7)(q7,7,K,q6)(q7,8,L,q8)(q8,8,K,q7)(q8,9,L,q9)(q9,9,K,q8)(q9,10,L,q10)(q10,10,K,q9)}{}"
    # ra = combiner(ndet(10), ndet(11))
    # ra = "{q3,q4,q2,q1}{q1}{(q1)(q2,1)(q3,2,1)(q4,3,2,1)}{(q2,1,K,q1),(q2,2,L,q3),(q1,1,L,q2),(q3,3,L,q4),(q3,2,K,q2),(q4,3,K,q3)}{}"
    ra = ndet(200)
    ra2 = ndet(200)
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
    result = forward(ra, "q0", "p0", set())
    t = (dt.now() - t).total_seconds()
    times.append(t)
    # print(t)
    # print(result)

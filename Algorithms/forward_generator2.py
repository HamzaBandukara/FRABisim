from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import *
from Generator.generatorBK import *
from datetime import datetime as dt
from time import process_time

from RAGen.Generator import generate_stack as det
from RAGen.GloGenerator import generate_stack as glodet
from RAGen.NDGenerator import generate_stack as ndet
from RAGen.FlowerGenerator import generate as flw
from RAGen.CPTGenerator import generate as cpt
from RAGen.CliqueGenerator import generate_clique as cli
from RAGen.Combiner import combiner
from copy import deepcopy as cp

STATS_CALLS = 0
STATS_NEWCALLS = 0
STATS_STATESPACE = set()
FLAG_DEBUG = False
FLAG_CHK_TAGS = True
CHKED_TAGS = {}

def db_print(*args):
    if FLAG_DEBUG: print(*args);

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

def bisim_ok(G, RA, q1, sigma, q2, not_bisim):
    global STATS_CALLS
    STATS_CALLS += 1
    db_print("\nbisim_ok: ", q1, sigma, q2,"\nwith G: ", G,"\nand ~G:",not_bisim)
    if not_bisim.is_member(q1, sigma, q2):
        # print("NOT_MEMBER: ", q1, sigma, q2)
        return False
    if G.is_member(q1, sigma, q2):
        return True
    global STATS_NEWCALLS
    STATS_NEWCALLS += 1
    global STATS_STATESPACE
    STATS_STATESPACE = STATS_STATESPACE.union((q1, sigma, q2))
    STATS_STATESPACE = STATS_STATESPACE.union((q2, ~sigma, q1))
    if FLAG_CHK_TAGS and chk_tags(RA,q1,q2) == False:
        not_bisim.update(q1, sigma, q2)
        not_bisim.update(q2, ~sigma, q1)
        return False
    state = G.get_state()
    G.update(q1, sigma, q2)
    if simulate(q1, sigma, q2, RA, G, not_bisim):
        if simulate(q2, ~sigma, q1, RA, G, not_bisim):
            return True
    G.set(state)
    not_bisim.update(q1, sigma, q2)
    not_bisim.update(q2, ~sigma, q1)
    db_print("UPDATE not_bisim: ",not_bisim)
    # print("Returned False", q1, sigma, q2)
    return False


def simulate(q1, sigma, q2, RA, G, not_bisim) -> bool:
    db_print("\nSIM: ", q1, sigma, q2)
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


def forward(RA: RegisterAutomata, q1: str, q2: str, sigma: set, stats=False):
    full_domain = RA.get_registers()
    sigma = PartialPermutation(full_domain, sigma)
    # NT: the domain of a PartialPermutation should be a subset of its sigma
    states = RA.get_states()
    partitions = []
    fd = [x for x in range(len(full_domain))]
    for q in states:
        dom = list(RA.s_map[q])
        rep = (
            q,
            dom,
            {PartialPermutation(dom, full_domain, fd)}
        )
        p = Partition({q}, rep, {q: PartialPermutation(full_domain, set(zip(dom, dom)))}, full_domain)
        partitions.append(p)
    G = GeneratingSystem(partitions, RA)
    not_bisim = SymmetricDownSet(G)
    db_print("\nTESTING: ", q1, sigma, q2,"\nfor A: ",RA,"\nwith G: ",G,"\nand ~G:",not_bisim)
    result = bisim_ok(G, RA, q1, sigma, q2, not_bisim)
    # print(G)
    if stats:
        bisim = G
        if not result:
            bisim = []
        return result, ("fwd_g2", STATS_CALLS, STATS_NEWCALLS, STATS_STATESPACE, bisim, not_bisim)
    return result

def ra_bisim(RA, q1, q2, sigma=set()):
    return forward(RA, q1, q2, sigma)


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(500000)
    ra = det(200)
    ra2 = det(200)
    t = dt.now()
    ra = RegisterAutomata(combiner(ra, ra2))
    print("T: ", (dt.now() - t).total_seconds())
    times = []
    t = process_time()
    result = forward(ra, "q0", "p0", set())
    t = process_time() - t
    times.append(t)
    print(t)
    print(result)

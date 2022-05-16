from itertools import product
from exceptions import UniverseException

from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma


def valid_bisim(bisimulation, RA):
    u_0 = bisimulation
    for cf in u_0:
        if not SyS(RA, cf, u_0):
            print(*cf)
            return False
    return True


def is_bisim(representation: str, q1: str, p1: str, sigma=None):
    if sigma is None:
        sigma = set()
    sigma = Sigma(sigma)
    target = (q1, sigma, p1)
    RA = RegisterAutomata(representation)
    configs = RA.get_reachable_configurations().union(RA.get_reachable_configurations(p1))
    u, ids = get_universe(configs, RA)
    if not target in u:
        target = p1, sigma.invert(), q1
        if not target in u:
            print(RA)
            print(*target)
            print(representation)
            for member in u:
                print("\t", *member)
            raise UniverseException("Missing Element From Universe.")
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = []
        for cf in u:
            if SyS(RA, cf, u):
                u_next.append(cf)
            else:
                changed = True
        u = u_next
        i += 1
    return ((q1, sigma, p1) in u) or ((p1, sigma.invert(), q1) in u)

# RULES - SYM implemented within ra_bisim
def ID_Rule(q1, sigma, q2):
    if q1 == q2:
        return sigma.is_id()
    return False


def EXT_Rule(cf: tuple, memo: dict):
    q1, q2 = cf[0], cf[2]
    s = cf[1]
    if not (q1, q2) in memo:
        return False
    for sig in memo[(q1, q2)]:
        if sig <= s:
            return True
    return False

def TR_Rule(cf: tuple, memo: dict) -> set:
    q1, sig, q2, configs = cf[0], cf[1], cf[2], set()
    if not q1 in memo:
        memo[q1] = set()
    memo[q1].add(cf)
    if not q2 in memo:
        return configs
    for cfr in memo[q2]:
        sig2, q3 = cfr[1], cfr[2]
        generated_config = q1, sig + sig2, q3
        configs.add(generated_config)
    return configs


def get_universe(configs, RA):
    universe = []
    id = []
    list_ver = list(configs)
    for i in range(len(list_ver)):
        q1 = list_ver[i][0]
        # q1, s1 = list_ver[i]
        for j in range(i, len(list_ver)):
            q2 = list_ver[j][0]
            gen_sigmas = Sigma.generate_sigmas(RA.s_map[q1], RA.s_map[q2])
            for sigma in gen_sigmas:
                if ID_Rule(q1, sigma, q2):
                    id.append((q1, sigma, q2))
                universe.append((q1, sigma, q2))
    Sigma.ALL_PERMS = {}
    Sigma.ALL_SIGMA = {}
    return universe, id


def ra_bisim(text: str):
    RA = RegisterAutomata(text)
    configs = RA.get_reachable_configurations()
    u_0, ids = get_universe(configs, RA)
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = []
        for cf in u_0:
            if SyS(RA, cf, u_0):
                u_next.append(cf)
            else:
                changed = True
        u_0 = u_next
        i += 1
    return u_0


def ra_bisim_id(text: str):
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    u_0, ids = get_universe(configs, RA)
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = [x for x in ids]
        for cf in u_0:
            if cf in ids:
                continue
            elif SyS(RA, cf, u_0):
                u_next.append(cf)
            else:
                changed = True
        u_0 = u_next
        i += 1
    return u_0


def ra_bisim_ext(text: str):
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    u_0, ids = get_universe(configs, RA)
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = []
        ext_memo = {}
        for cf in u_0:
            if cf in u_next:
                continue
            if EXT_Rule(cf, ext_memo):
                u_next.append(cf)
                continue
            if not SyS(RA, cf, u_0):
                changed = True
                continue
            if not (cf[0], cf[2]) in ext_memo:
                ext_memo[(cf[0], cf[2])] = set()
            ext_memo[(cf[0], cf[2])].add(cf[1])
            u_next.append(cf)
        u_0 = u_next
        i += 1
    return u_0


def ra_bisim_tr(text: str):
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    u_0, ids = get_universe(configs, RA)
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = []
        memo = {}
        for cf in u_0:
            if cf in u_next:
                continue
            if SyS(RA, cf, u_0):
                u_next.append(cf)
                tr = TR_Rule(cf, memo)
                for cf2 in tr:
                    if not cf2 in u_next:
                        u_next.append(cf2)
            else:
                changed = True
        u_0 = u_next
        i += 1
    return u_0


def ra_bisim_3(text: str):
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    u_0, ids = get_universe(configs, RA)
    changed = True
    i = 1
    while changed:
        changed = False
        u_next = []
        for cf in u_0:
            if ID_Rule(*cf):
                u_next.append(cf)
                continue
            elif SyS(RA, cf, u_0):
                u_next.append(cf)
            else:
                changed = True
        u_0 = u_next
        i += 1
    return u_0


def SyS(RA, cf, u) -> bool:
    q1, sigma, q2 = cf[0], cf[1], cf[2]
    if simulate(RA , u, q1, sigma, q2):
        if simulate(RA, u, q2, sigma.invert(), q1):
            return True
    return False


def simulate(RA, u, q1, sigma, q2) -> bool:
    transitions_1, transitions_2 = RA.get_transitions(q1), RA.get_transitions(q2)
    for pair in transitions_1:
        if pair[1] == "K":
            lb1 = pair[0]
            if sigma.in_dom(lb1):
                lb2 = sigma[lb1]
                pair_2 = (lb2, "K")
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        n_sigma = sigma.harpoon(next_q1, next_q2, RA)
                        if (next_q1, n_sigma, next_q2) in u:
                            found = True
                            break
                        if (next_q2, n_sigma.invert(), next_q1) in u:
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
                        new_sigma = sigma.generate_temp_sigma(lb1, pair_2[0])
                        for next_q2 in transitions_2[pair_2]:
                            n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                            if (next_q1, n_sigma, next_q2) in u:
                                found = True
                                break
                            if (next_q2, n_sigma.invert(), next_q1) in u:
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
                        new_sigma = sigma.generate_temp_sigma(pair[0], pair_2[0])
                        for next_q2 in RA.get_trans_lbl(q2, pair_2):
                            n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                            if (next_q1, n_sigma, next_q2) in u:
                                found = True
                                break
                            if (next_q2, n_sigma.invert(), next_q1) in u:
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
                for next_q1 in RA.get_trans_lbl(q1, pair):
                    found = False
                    for next_q2 in RA.get_trans_lbl(q2, pair_2):
                        n_sigma = new_sigma.harpoon(next_q1, next_q2, RA)
                        if (next_q1, n_sigma, next_q2) in u:
                            found = True
                            break
                        if (next_q2, n_sigma.invert(), next_q1) in u:
                            found = True
                            break
                    if not found:
                        return False
    return True

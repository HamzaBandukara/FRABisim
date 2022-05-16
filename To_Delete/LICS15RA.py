from copy import copy
from DataStructures.RA import RegisterAutomata
from DataStructures.Sigma import Sigma


# Identity Rule
def ID_Rule(q1: int, s1: set, sigma: Sigma, q2: int, s2: set) -> bool:
    if q1 == q2:
        if s1 == s2:
            return sigma.is_id()
    return False


# Symmetry Rule
def Sym_Rule(q1: int, s1: set, sigma: Sigma, q2: int, s2: set) -> tuple:
    sig_prime = sigma.reverse()
    return q2, s2, sig_prime, q1, s1


# Extension Rule
def EXT_Rule(q1: int, s1: set, sig: Sigma, q2: int, s2: set, sig_prime: Sigma) -> tuple:
    # s1 <= s2 <= s3 <= s4 ...
    # s1 = (1,1)
    # => (1,1)(2,2) (1,1)(3,3) ...
    if sig <= sig_prime:
        return q1, s1, sig_prime, q2, s2
    else:
        return q1, s1, sig, q2, s2


# Transitive Rule
def TR_Rule(t1: tuple, t2: tuple) -> tuple:
    sig_1, sig_2 = t1[2], t2[2]
    new_sig = sig_1 + sig_2
    return t1[0], t1[1], new_sig, t2[3], t2[4]

# (q_0, 1L, q_1)(q_1, 1K, q_1)(q_1, 1K, q_0)

def get_universe(configs):
    # Universe members:
    # q1, S1, sig, q2, S2
    universe = []
    list_ver = list(configs)
    generated_sigmas = {}
    for i in range(len(list_ver)):
        c1 = list_ver[i]
        for j in range(len(list_ver)):
            c2 = list_ver[j]
            q1 = c1[0]
            s1 = c1[1]
            q2 = c2[0]
            s2 = c2[1]
            if (s1, s2) not in generated_sigmas:
                generated_sigmas[(s1, s2)] = Sigma.generate_sigmas(s1, s2)
            for sigma in generated_sigmas[(s1, s2)]:
                universe.append((q1, s1, sigma, q2, s2))
    return universe


def simulate(u, RA, q1, s1, sigma, q2, s2):
    transitions1 = RA.get_transitions(q1)
    transitions2 = RA.get_transitions(q2)
    for pair in transitions1:
        if len(transitions1[pair]) == 0:
            continue

        elif pair[1] == "K":
            lb1 = pair[0]
            if sigma.in_dom(lb1):
                lb2 = sigma[lb1]
                pair_2 = (lb2, "K")
                found = False
                for next_q1 in transitions1[pair]:
                    for next_q2 in transitions2[pair_2]:
                        if (next_q1, s1, sigma, next_q2, s2) in u:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
            elif lb1 in sigma.dom_sub(s1):
                found = False
                for next_q1 in transitions1[pair]:
                    for pair_2 in transitions2:
                        if not pair_2[1] == "L":
                            continue
                        temp_sigma = sigma.generate_temp_sigma(lb1, pair_2[0])
                        for next_q2 in transitions2[pair_2]:
                            if (next_q1, s1, temp_sigma, next_q2, set(s2).add(pair_2[1])) in u:
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if not found:
                    return False

        elif pair[1] == "L":
            lb1 = pair[0]
            found = False
            new_s1 = set(s1)
            new_s1.add(lb1)
            new_s1 = frozenset(new_s1)
            for pair_2 in transitions2:
                if len(transitions2[pair_2]) == 0:
                    continue
                if pair_2[1] == "L":
                    new_s2 = set(s2)
                    new_s2.add(pair_2[0])
                    new_s2 = frozenset(new_s2)
                    new_sig = sigma.generate_temp_sigma(pair[0], pair_2[0])
                    for next_q1 in transitions1[pair]:
                        for next_q2 in transitions2[pair_2]:
                            if (next_q1, new_s1, new_sig, next_q2, new_s2) in u:
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
            if not found:
                return False

            sub = sigma.rng_sub(s2)
            for lb2 in sub:
                label = (lb2, "K")
                if len(transitions2[label]) == 0:
                    return False
                found = False
                new_s2 = set(s2)
                new_s2.add(lb2)
                new_sigma = sigma.generate_temp_sigma(lb1, lb2)
                for next_q1 in transitions1[pair]:
                    for next_q2 in transitions2[label]:
                        if (next_q1, new_s1, new_sigma, next_q2, new_s2) in u:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
    return True


def SyS(RA, config, u):
    q1 = config[0]
    s1 = config[1]
    sigma = config[2]
    q2 = config[3]
    s2 = config[4]
    if simulate(u, RA, q1, s1, sigma, q2, s2):
        sigma.invert()
        if simulate(u, RA, q2, s2, sigma, q1, s2):
            sigma.invert()
            return True
        sigma.invert()
    return False


def ra_bisim(text: str):
    Sigma.ALL_SIGMA = {}
    gen = 0
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    i = 1
    u_0 = get_universe(configs)
    # print("U_0: ")
    # for config in u_0:
    #     print("\t{}, {}, {}, {}, {}".format(*config))
    # for config in u_0:
    #     print("{} {} {} {} {}".format(config[0], config[1], config[2], config[3], config[4]))
    # (1, None)(2, None)(None, 1)(None, 2)
    # (1, None)(2, None)(None, 2)(None, 1)
    # A = [1,2,3,4, None, None, None, None]
    # B = [1,2,3,4, None, None, None, None] <- Gets Permuted
    # (1,1)(2,2)(3,3)(4,4)
    changed = True
    while changed:
        # print("Universe {}: Configs: {}".format(gen, len(u_0)))
        # exit(50)
        changed = False
        u = []
        for i in range(len(u_0)):
            config = u_0[i]
            if SyS(RA, config, u_0):
                u.append(config)
                # print("Appending:\t{} {} {} {} {}".format(config[0], config[1], config[2], config[3], config[4]))
            else:
                # print("Removing:\t{} {} {} {} {}".format(config[0], config[1], config[2], config[3], config[4]))
                changed = True
        u_0 = u
        gen += 1
    # print("Universe {}: Configs: {}".format(gen, len(u_0)))
    return u_0

def ra_bisim_2(text: str):
    Sigma.ALL_SIGMA = {}
    gen = 0
    RA = RegisterAutomata(text)
    configs = RA.get_configurations()
    i = 1
    u_0 = get_universe(configs)
    # print("U_0: ")
    # for config in u_0:
    #     print("\t{}, {}, {}, {}, {}".format(*config))
    changed = True
    while changed:
        # print("Universe {}: Configs: {}".format(gen, len(u_0)))
        memo_start = {}  # when q2 is at the end (see paper)
        memo_end = {}  # when q2 is at the start (see paper)
        changed = False
        u = []
        # add ID before everything
        for i in range(len(u_0)):
            config = u_0[i]
            if config in u:
                continue
            if ID_Rule(*config):
                u.append(config)
                continue
            if SyS(RA, config, u_0):
                queue = [config]
                while len(queue) > 0:
                    cf = queue.pop(0)
                    if cf in u:
                        continue
                    u.append(cf)
                    u.append(Sym_Rule(*cf))
                    if cf[0] in memo_end:
                        for cf2 in memo_end[cf[0]]:
                            new_t = (cf2[0], cf2[1], cf2[2] + cf[2], cf[3], cf[4])
                            if new_t in u:
                                continue
                            if new_t in queue:
                                continue
                            queue.append(new_t)
                    if cf[3] in memo_start:
                        for cf2 in memo_start[cf[3]]:
                            new_t = (cf[0], cf[1], cf[2] + cf2[2], cf2[3], cf2[4])
                            if new_t in u:
                                continue
                            if new_t in queue:
                                continue
                            queue.append(new_t)
                    if cf[0] not in memo_start:
                        memo_start[cf[0]] = []
                    if cf[3] not in memo_end:
                        memo_end[cf[3]] = []
                    memo_start[cf[0]].append(cf)
                    memo_end[cf[3]].append(cf)
                # print("Appending:\t{} {} {} {} {}".format(config[0], config[1], config[2], config[3], config[4]))
            else:
                # print("Removing:\t{} {} {} {} {}".format(config[0], config[1], config[2], config[3], config[4]))
                changed = True
        u_0 = u
        gen += 1
    # print("Universe {}: Configs: {}".format(gen, len(u_0)))
    return u_0

def bisim_test(text: str):
    u_0 = ra_bisim(text)
    u_1= ra_bisim_2(text)
    return set(u_0) == set(u_1)

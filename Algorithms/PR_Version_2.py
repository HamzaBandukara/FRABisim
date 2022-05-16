from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import PartialPermutation
from RAStack.Generator import generate_stack as det
from RAStack.Combiner import combiner
from time import process_time


def knuth_L_algorithm(seq, length):
    if len(seq) == 0:
        yield tuple(seq)
        return
    a = sorted(seq)
    while True:
        yield tuple(a[:length])
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


def split(i, pi, partition_dict, RA: RegisterAutomata, tag, name):
    # print(i, tag, name)
    B = pi[i]
    q_rep = B.pop()
    B1 = {q_rep}
    B2 = set()
    # print("Getting q_next ...")
    qnext = RA.get_reachables_by_tag(q_rep, partition_dict, tag, name)
    while len(B) > 0:
        q_2 = B.pop()
        # print("Getting q_2's next ...", q_2)
        if RA.get_reachables_by_tag(q_2, partition_dict, tag, name) == qnext:
            B1.add(q_2)
        else:
            B2.add(q_2)
    pi[i] = B1
    if len(B2) != 0:
        new_i = len(pi)
        for element in B2:
            partition_dict[element[0]][element[1]] = new_i
        pi.append(B2)
        # print("Split! True")
        return True
    # print("Split! False")
    return False


def partition_refinement(RA: RegisterAutomata):
    t = process_time()
    # print("Beginning Algorithm ... ")
    r = RA.max_r()
    Q = RA.get_states()
    names = [x for x in range((2 * r) + 1)]
    # print("Generated Names! ", process_time() - t)
    t = process_time()
    permutations = set(knuth_L_algorithm(names, r))
    # print("Generated Permutations! ", process_time() - t)
    t = process_time()
    configs = set()
    partition_dict = {}
    for q in Q:
        partition_dict[q] = dict()
        for perm in permutations:
            cfg = (q, perm)
            configs.add(cfg)
            partition_dict[q][perm] = 0
    pi = [configs]
    # print("Prepared Configs! Size =", len(configs), process_time() - t)
    t = process_time()
    RA.set_reachables_by_name(configs)
    # print("Got Reachables!", process_time() - t)
    changed = True
    while changed:
        t = process_time()
        # print("Iteration ... ")
        changed = False
        i = 0
        while i < len(pi):
            for tag in RA.tags:
                for name in names:
                    if split(i, pi, partition_dict, RA, tag, name):
                        changed = True
            i += 1
        # print(process_time() - t)
    return pi, partition_dict


def is_bisimilar(ra: RegisterAutomata, q1, q2, sigma):
    sigma = PartialPermutation(ra.get_registers(), sigma)
    pi, pi_dict = partition_refinement(ra)
    # for i in range(len(pi)):
        # print(i + 1)
        # for elem in pi[i]:
            # print("\t", *elem)
    for perm_1 in pi_dict[q1]:
        for perm_2 in pi_dict[q2]:
            if not pi_dict[q1][perm_1] == pi_dict[q2][perm_2]:
                continue
            set_form = set()
            for i in range(len(perm_1)):
                if perm_1[i] in perm_2:
                    set_form.add((ra.get_registers()[i], ra.get_registers()[perm_2.index(perm_1[i])]))
            sig = PartialPermutation(ra.get_registers(), set_form)
            sig = sig.restrict(ra.s_map[q1], ra.s_map[q2])
            if sig == sigma:
                return True
    return False

if __name__ == '__main__':
    ra = combiner(det(2), det(2))
    # ra = "{q1,q2,p1,p2}{q1}{(q1,1)(p1,1)}{(q1,1,L,q2)(p1,1,L,p2)}{}"
    # ra = "{q1,q2}" \
    #      "{q1}" \
    #      "{(q1,1,2)(q2,1,2)}" \
    #      "{(q1,1,K,q1)" \
    #       "(q1,2,K,q1)" \
    #       "(q1,1,L,q1)" \
    #       "(q2,1,K,q2)" \
    #       "(q2,2,K,q2)" \
    #       "(q2,2,L,q2)}" \
    #      "{}"
    # print(RegisterAutomata(ra))
    # print(is_bisimilar(RegisterAutomata(ra), "q0", "p0", set()))
    # print(is_bisimilar(("q1", set(), "q2"), RegisterAutomata(ra)))
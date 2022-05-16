from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma
import itertools
import Powerset


class Relation:
    def __init__(self, RA: RegisterAutomata):
        self.blocks = []
        self.state_map = {}
        self.RA = RA
        self.size = 1

    @classmethod
    def generate_relation(cls, RA: str) -> "Relation":
        RA = RegisterAutomata(RA)
        relation = Relation(RA)
        block = []
        map = relation.state_map
        configs = list(RA.get_configurations())
        memory = {}
        while len(configs) > 0:
            q1, s1 = configs.pop(0)
            if s1 in memory:
                permutations = memory[s1]
            else:
                permutations = []
                subsets = Powerset.powerset(list(s1))
                for s in subsets:
                    p = itertools.permutations(s)
                    for perm in p:
                        perm = list(perm)
                        perm = tuple(perm)
                        permutations.append(perm)
            for perm in permutations:
                block.append((q1, perm))
                map[(q1, perm)] = 0
        relation.blocks = [block]
        return relation

    def print(self):
        print("Relation: ")
        i = 1
        for b in self.blocks:
            z = [(str(x), str(list(y))) for (x, y) in b]
            s = "{:5} => {}".format(i, str(z)).replace("\"", "").replace("\'", "")
            print(s)
            i += 1

    def refine(self):
        i = 1
        actions = self.RA.get_actions()
        changed = True
        while changed:
            changed = False
            index = 0
            while index < len(self.blocks):
                for a in actions:
                    if self.split(index):
                        print("Refinement {} - ".format(i))
                        i += 1
                        self.print()
                        changed = True
                index += 1

    def split(self, index) -> bool:
        b = list(self.blocks[index])
        s = b.pop(0)
        flag = False
        actions = self.RA.delta[s[0]]
        if len(actions) == 0:
            b = self.blocks[index]
            b1 = {s}
            b2 = set()
            for s_b in b:
                q2, s2 = s_b
                if len(self.RA.delta[q2]) == 0:
                    b1.add(s_b)
                else:
                    b2.add(s_b)
                    self.state_map[s_b] = self.size + 1
            self.blocks[index] = b1
            if len(b2) > 0:
                self.blocks.append(b2)
                self.size += 1
                return True
            return False
        for a in actions:
            b = self.blocks[index]
            b1 = {s}
            b2 = set()
            for s_b in b:
                if s_b == s:
                    continue
                if self.same_partition(s, s_b, a):
                    b1.add(s_b)
                else:
                    b2.add(s_b)
                    self.state_map[s_b] = self.size + 1
            self.blocks[index] = b1
            if len(b2) > 0:
                self.blocks.append(b2)
                self.size += 1
                flag = True
            try:
                assert len(b1.union(b2)) == len(b1) + len(b2)
            except AssertionError:
                print("B1", b1)
                print("B2", b2)
                print("B", b)
                exit(-2)
        return flag

    def get_next(self, state, register, type, perm) -> set:
        perm = tuple(perm)
        action = register, type
        targets = self.RA.get_next_transitions(state, action)
        p = set()
        for t in targets:
            try:
                p.add(self.state_map[(t, perm)])
            except KeyError:
                # permutation does not exist
                print(t)
                print(perm)
                print(self.state_map)
                exit("PERMUTATION DOES NOT EXIST")
        return p

    @classmethod
    def eliminate(cls, l1: list, l2: list, s: set) -> None:
        i = 0
        while i < len(l1):
            if l1[i] is None:
                i += 1
                continue
            if l1[i] not in s:
                del l1[i]
                del l2[i]
            else:
                i += 1

    def match(self, config_1, action_1, config_2, action_2, sigma) -> bool:
        q1, p1 = config_1
        q2, p2 = config_2
        sigma = sigma.generate_temp_sigma(action_1[0], action_2[0])
        sigma = sigma.harpoon(q1, q2, self.RA)
        perm1, perm2 = sigma.keys, sigma.values
        return self.get_next(q1, *action_1, perm1) == self.get_next(q2, *action_2, perm2)

    def same_partition(self, config_1, config_2, action):
        # Major flaw - you check the same permutations MULTIPLE times!
        register, label = action
        q1, s1 = config_1
        q2, s2 = config_2
        sigma = Sigma(set(zip(s1, s2)))
        t_q2 = self.RA.get_transitions(q2)
        if label == "K":
            if register in sigma:
                a2 = (sigma[register], "K")
                return self.get_next(q1, *action, s1) == self.get_next(q2, *a2, s2)
            elif register not in sigma.dom:
                for a2 in t_q2:
                    if a2[1] == "L":
                        if self.match(config_1, action, config_2, a2, sigma):
                            return True
            else:
                raise ValueError("Shouldn't be here - oops")
            return False
        elif label == "L":
            flag = False
            for a2 in t_q2:
                if a2[1] == "L":
                    if self.match(config_1, action, config_2, a2, sigma):
                        flag = True
                        break
            if not flag:
                return False
            targets = list(sigma.rng_sub(set(s2)))
            while len(targets) > 0:
                current_target = targets.pop(0)
                a2 = current_target, "K"
                if a2 not in self.RA.delta[q2]:
                    return False
                if not self.match(config_1, action, config_2, a2, sigma):
                    return False
            return True
        else:
            raise ValueError("That type doesn't exist!")

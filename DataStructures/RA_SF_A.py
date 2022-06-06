from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from RAGen.Generator import generate_stack
from re import findall


class Transition:
    def __init__(self, src, tag, lbl, t_type, tgt):
        self.tag = tag
        self.src = src
        self.lbl = lbl
        t_type = t_type.upper()
        if t_type not in ["K", "L", "G", "TAU"]:
            raise ValueError("Invalid Transition Type \"" + t_type + "\".")
        if t_type == "G":
            self.tag = "G_" + self.tag
        elif t_type in ["K", "L"]:
            self.tag = "L_" + self.tag
        self.type = t_type
        self.trg = tgt

    def __str__(self):
        return "{} -{},{}{}> {}".format(self.src, self.tag, self.lbl, self.type, self.trg)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)


class RegisterAutomata:
    def __init__(self, representation: str=None):
        self.initial = 0
        self.pos_actions = set()
        self.tags = set()
        self.s_map = {}
        self.r_map = set()
        self.transitions = set()
        self.final = set()
        self.registers = []
        self.r_list = []
        self.filled = set()
        self.delta = {}
        self.states = 0
        self.tags = set()
        self.reachables = dict()
        self.registers = []
        self.states = []
        self.delta = None
        self.r_list = []
        if representation is not None:
            self.set_up(representation)
            self.complete_setup()
            # self.registers = list(self.r_map)
            # self.states = list(self.s_map.keys())
            # self.delta = self._get_delta()
            # self.r_list = list(self.r_map)

    def complete_setup(self):
        self.registers = list(self.r_map)
        self.states = list(self.s_map.keys())
        self.delta = self._get_delta()
        self.r_list = list(self.r_map)
        for s in self.states:
            self.s_map[s] = frozenset(self.s_map[s])

    def __str__(self):
        states = self.states
        registers = ["{}: {}".format(s, self.s_map[s]) for s in self.s_map]
        transitions = ["{}".format(t) for t in self.transitions]
        start = self.initial
        end = [f for f in self.final]
        return "( "+("{} , {} , {} , {} , {}".format(states, registers, transitions, start, end)).replace("\'", "").replace("[", "{").replace("]", "}").replace("\"", "")+" )"

    def set_up(self, representation):
        s = findall("{(.*?)}", representation)

        # Handles the states
        for state in s[0].split(","):
            if state not in self.s_map:
                self.s_map[state] = set()

        # Handles the registers
        reg = findall("\((.*?)\)", s[2])
        for r in reg:
            r = r.replace(" ", "")
            r = r.split(",")
            temp_s = r[0]
            for i in range(1, len(r)):
                # r[i] = int(r[i])
                if r[i] not in self.r_map:
                    self.r_map.add(r[i])
                    self.registers.append(r[1])
                # if r[1] != "#":
                #     self.filled.add(r[0])
                # self.filled.add(self.r_map[r[i]])
                self.filled.add(r[i])
                # self.registers.append(r[1])
                self.s_map[temp_s].add(r[i])
                # self.s_map[temp_s].add(self.r_map[r[i]])

        # Handles all the transitions
        tran = findall("\((.*?)\)", s[3])
        for t in tran:
            t = t.replace(" ", "")
            t = t.split(",")
            if len(t) == 4:
                t.insert(1, "NA")
            self.tags.add(t[1])
            t = Transition(t[0], t[1], t[2], t[3], t[4])
            self.transitions.add(t)

        # initial state
        self.initial = s[1]

        # Handles final state(s)
        s[4] = s[4].replace(" ", "")
        fin = s[4].split(",")
        for f in fin:
            if len(f) == 0:
                continue
            self.final.add(f)

    def _get_delta(self):
        delta = {s: {} for s in self.s_map}
        sorted_t = list(self.transitions)
        sorted_t.sort()
        for t in sorted_t:
            pair = t.lbl, t.type
            tag = t.tag
            if tag not in delta[t.src]:
                delta[t.src][tag] = dict()
            if pair not in delta[t.src][tag]:
                delta[t.src][tag][pair] = set()
            delta[t.src][tag][pair].add(t.trg)
        return delta

    def get_configurations(self):
        configurations = set()
        for s in self.s_map:
            configurations.add((s, frozenset(self.s_map[s])))
        return configurations

    def get_next_transitions(self, pair, partition_dict, partitions) -> dict:
        configurations = dict()
        for tag in self.reachables[pair]:
            configurations[tag] = dict()
            for action in self.reachables[pair][tag]:
                configurations[tag][action] = set()
                for target in self.reachables[pair][tag][action]:
                    configurations[tag][action].add(partitions.index(partition_dict[target[0]][target[1]]))
        return configurations

    def get_next_blocks_specific(self, pair, partition_dict, partitions, tag, gen_action) -> dict:
        configurations = dict()
        for tag in self.tags:
            configurations[tag] = dict()
            for available_register in self.s_map[pair[0]]:
                configurations[tag][available_register] = dict()
            configurations[tag]["FRESH"] = dict()
            if tag in self.reachables[pair]:
                for action in self.reachables[pair][tag]:
                    key = action[0] if action[1] == "K" else "FRESH"
                    configurations[tag][key][action] = set()
                    for target in self.reachables[pair][tag][action]:
                        configurations[tag][key][action].add(partitions.index(partition_dict[target[0]][target[1]]))
        return configurations

    def get_next_blocks(self, pair, partition_dict, partitions) -> dict:
        configurations = dict()
        for tag in self.tags:
            configurations[tag] = dict()
            for available_register in self.s_map[pair[0]]:
                configurations[tag][available_register] = dict()
            configurations[tag]["FRESH"] = dict()
            if tag in self.reachables[pair]:
                for action in self.reachables[pair][tag]:
                    key = action[0] if action[1] == "K" else "FRESH"
                    configurations[tag][key][action] = set()
                    for target in self.reachables[pair][tag][action]:
                        configurations[tag][key][action].add(target)
                        # configurations[tag][key][action].add(partitions.index(partition_dict[target[0]][target[1]]))
        return configurations

    def print_transitions(self) -> None:
        trans = [str(t) for t in self.transitions]
        trans = sorted(trans)
        for t in trans:
            print(t)

        # state, s = pair
        # configurations = dict()
        # for tag in self.delta[state]:
        #     configurations[tag] = dict()
        #     for action in self.delta[state][tag]:
        #         register, type = action
        #         new_s = list(s)
        #         if register not in new_s:
        #             new_s.append(register)
        #         pos = new_s.index(register)
        #         configurations[tag][(pos, type)] = set()
        #         for target in self.delta[state][tag][action]:
        #             ts = list(new_s)
        #             for reg in new_s:
        #                 if reg not in self.s_map[target]:
        #                     ts.remove(reg)
        #             ts = tuple(ts)
        #             configurations[tag][(pos, type)].add(partitions.index(partition_dict[target][ts]))
        # return configurations

    def get_r(self):
        return len(self.get_registers())


    # q1, ()
    # (q1, ["1", "2"]), (p1, ["2", "1"])
    # q1 -> "1"K, p1 -> "2"K
    # q1 -> "3"L, p1 -> "3"K -> p2, (p2, ["2", "1", "3"])
    # q1 -> 0K, p1 -> 0K
    # q1 -> 0L
    def set_up_reachables(self, configs):
        self.reachables = dict()
        # (state, sigma dom/rng)
        for pair in configs:
            state, s = pair
            configurations = dict()
            for tag in self.delta[state]:
                configurations[tag] = dict()
                for action in self.delta[state][tag]:
                    register, type = action
                    new_s = list(s)
                    if register not in new_s:
                        new_s.append(register)
                    pos = new_s.index(register)
                    self.pos_actions.add((pos, type))
                    configurations[tag][action] = set()
                    # configurations[tag][(pos, type)] = set()
                    for target in self.delta[state][tag][action]:
                        # ts = list(new_s)
                        # for reg in new_s:
                        #     if reg not in self.s_map[target]:
                        #         ts.remove(reg)
                        # ts = tuple(ts)
                        # configurations[tag][action].add((target, ts))
                        configurations[tag][action].add((target, tuple(new_s)))
            self.reachables[pair] = configurations
        # return configurations
        # self.reachables = dict()
        # for cf in configs:
        #     self.reachables[cf] = dict()
        #     state, registers = cf
        #     trans = self.delta[state]
        #     for tag in trans:
        #         self.reachables[cf][tag] = dict()
        #         for action in trans[tag]:
        #             self.reachables[cf][tag][action] = set()
        #             new_s = list(registers)
        #             if action[0] not in new_s:
        #                 if action[1] == "L":
        #                     new_s.append(action[0])
        #             new_s = tuple(new_s)
        #             for target_state in trans[tag][action]:
        #                 self.reachables[cf][tag][action].add((target_state, new_s))
        # for cf in self.reachables:
        #     print(cf, ":")
        #     for tag in self.reachables[cf]:
        #         print("\t", tag)
        #         for action in self.reachables[cf][tag]:
        #             print("\t\t", action)
        #             for cf2 in self.reachables[cf][tag][action]:
        #                 print("\t\t\t", cf2)

    def get_reachable_configurations(self, qi=None):
        configurations = set()
        if qi is None:
            qi = self.initial
        queue = [(qi, frozenset(self.s_map[qi]))]
        while not len(queue) == 0:
            current_config = queue.pop(0)
            configurations.add(current_config)
            transitions = self.get_transitions(current_config[0])
            for tag in transitions:
                for pair in transitions[tag]:
                    if len(transitions[pair]) == 0:
                        continue
                    for next in transitions[pair]:
                        config = (next, frozenset(self.s_map[next]))
                        if config not in configurations:
                            configurations.add(config)
                            queue.append(config)
        return configurations

    def set_reachables_by_name(self, configs: set):
        self.reachables = dict()
        names = [x for x in range((2 * self.get_r()) + 1)]
        for pair in configs:
            state, s = pair
            configurations = dict()
            for tag in self.delta[state]:
                configurations[tag] = dict()
                for action in self.delta[state][tag]:
                    new_s = []
                    index = self.registers.index(action[0])
                    if action[1] == "L":
                        list_form = list(s)
                        for name in names:
                            if name not in s:
                                list_form[index] = name
                                new_s.append((name, tuple(list_form)))
                    else:
                        new_s.append((s[index], s))
                    for target in self.delta[state][tag][action]:
                        for ns in new_s:
                            if ns[0] not in configurations[tag]:
                                configurations[tag][ns[0]] = set()
                            configurations[tag][ns[0]].add((target, ns[1]))
            self.reachables[pair] = configurations

    def get_registers(self):
        return list(self.r_map)

    def get_states(self):
        return self.states

    def get_transitions(self, state):
        return self.delta[state]

    def get_trans_lbl(self, s, tag, lbl):
        if lbl in self.delta[s][tag]:
            return self.delta[s][tag][lbl]
        return set()

    def max_r(self):
        return len(self.s_map[max(self.s_map, key=lambda x: len(self.s_map[x]))])

    def get_reachables_by_tag(self, pair, partition_dict, tag, name):
        configurations = set()
        if tag not in self.reachables[pair]:
            return configurations
        if name not in self.reachables[pair][tag]:
            return configurations
        for target in self.reachables[pair][tag][name]:
            configurations.add(partition_dict[target[0]][target[1]])
        return configurations


def ra_to_xml(text: str):
    split = findall("{(.*?)}", text)
    state_dict = {}
    RA = Element("dra")

    states = SubElement(RA, "states")
    for state in split[0].split(","):
        s = SubElement(states, "state")
        id = SubElement(s, "id")
        id.text = state
        state_dict[state] = s

    for registers in findall("\((.*?)\)", split[2]):
        reg = registers.split(",")
        available = SubElement(state_dict[reg[0]], "available-registers")
        for i in range(1, len(reg)):
            r = SubElement(available, "register")
            r.text = reg[i]

    initial = SubElement(RA, "initial-state")
    initial.text = split[1]

    transitions = SubElement(RA, "transitions")
    for tran in findall("\((.*?)\)", split[3]):
        resplit = tran.split(",")
        t = SubElement(transitions, "transition")
        f = SubElement(t, "from")
        f.text = resplit[0]
        f = SubElement(t, "input")
        f.text = resplit[1]
        op = SubElement(t, "op")
        if resplit[3] == "K":
            resplit[3] = "Read"
        elif resplit[3] == "L":
            resplit[3] = "LFresh"
        elif resplit[3] == "G":
            resplit[3] = "GFresh"
        else:
            print(resplit)
            raise ValueError
        op.text = resplit[3]
        register = SubElement(t, "register")
        register.text = resplit[2]
        to = SubElement(t, "to")
        to.text = resplit[4]

    return RA

if __name__ == '__main__':
    rep = "{q0,q1,q2,q3}{q0}{(q0)(q1,1)(q2,1,2)(q3,1,2,3)}{(q0,push,1,G,q1)(q1,pop,1,K,q0)(q1,push,2,G,q2)(q2,pop,2,K,q1)(q2,push,3,G,q3)(q3,pop,3,K,q2)}{}"
    print(RegisterAutomata(rep))
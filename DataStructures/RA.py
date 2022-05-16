from re import findall


class Transition:
    def __init__(self, src, lbl, t_type, tgt):
        self.src = src
        self.lbl = lbl
        t_type = t_type.upper()
        if t_type not in ["K", "L"]:
            raise ValueError("Invalid Transition Type \"" + t_type + "\".")
        self.type = t_type
        self.trg = tgt

    def __str__(self):
        return "{}-{}{}>{}".format(self.src, self.lbl, self.type, self.trg)


class RegisterAutomata:
    def __init__(self, representation: str):
        # RegEx to handle string input
        # e.g. "{0,1,2}{(1,a)}{(0,1,k,1)(1,1,l,2)}{0}{}"

        self.initial = 0
        self.s_map = {}
        self.r_map = {}
        self.transitions = set()
        self.final = set()
        self.registers = []
        self.filled = set()

        self.set_up(representation)

        self.states = len(self.s_map)
        self.delta = self._get_delta()


    def __str__(self):
        states = self.states
        registers = ["({},{})".format(i, self.registers[i]) for i in self.filled]
        # registers = ["({},{})".format(i, self.registers[i]) for i in range(len(self.registers))]
        # transitions = self.delta
        transitions = ["{}".format(t) for t in self.transitions]
        start = self.initial
        end = [f for f in self.final]
        return ("{} | {} | {} | {} | {}".format(states, registers, transitions, start, end)).replace("\'", "").replace("[", "").replace("]", "")

    def set_up(self, representation):
        s = findall("{(.*?)}", representation)

        # Handles the states
        for state in s[0].split(","):
            if state not in self.s_map:
                self.s_map[state] = len(self.s_map)

        # Handles the registers
        reg = findall("\((.*?)\)", s[1])
        for r in reg:
            r = r.replace(" ", "")
            r = r.split(",")
            if r[0] in self.r_map:
                raise ValueError("Register given twice")
            self.r_map[r[0]] = len(self.r_map)
            # if r[1] != "#":
            #     self.filled.add(r[0])
            self.filled.add(r[0])
            self.registers.append(r[1])
        self.filled = frozenset(self.filled)

        # Handles all the transitions
        tran = findall("\((.*?)\)", s[2])
        for t in tran:
            t = t.replace(" ", "")
            t = t.split(",")
            if t[2] == "G":
                t[2] = "L"
            t = Transition(t[0], t[1], t[2], t[3])
            self.transitions.add(t)

        self.initial = s[3]

        # Handles final state(s)
        s[4] = s[4].replace(" ", "")
        fin = s[4].split(",")
        for f in fin:
            if len(f) == 0:
                continue
            self.final.add(self.s_map[f])

    def _get_delta(self):
        delta = {}
        for s in self.s_map:
        # for s in range(self.states):
            delta[s] = {}
            for r in self.r_map:
            # for r in range(len(self.registers)):
                delta[s][r, "K"] = set()
                delta[s][r, "L"] = set()
        for t in self.transitions:
            try:
                delta[t.src][t.lbl, t.type].add(t.trg)
            except KeyError:
                print(t.src)
                print(delta)
                exit(-2)
        return delta

    # def get_configurations(self):
    #     # Symbolic Configuration - (Q, S)
    #     # Where Q is a state, S is the set of filled registers.
    #     configurations = set()
    #     initial_config = (self.initial, self.filled)
    #     configurations.add(initial_config)
    #     queue = [initial_config]
    #     while len(queue) > 0:
    #         current_config = queue.pop(0)
    #         state = current_config[0]
    #         try:
    #             d = self.delta[state]
    #         except KeyError:
    #             print(current_config)
    #             print(state)
    #             print(self.delta)
    #             exit("HERE")
    #         for pair in d:
    #             f = set(current_config[1])
    #             if len(d[pair]) == 0:
    #                 continue
    #             t_type = pair[1]
    #             if pair[0] not in f:
    #                 if t_type == "K":
    #                     continue
    #                 f.add(pair[0])
    #             for next in d[pair]:
    #                 config = (next, frozenset(f))
    #                 if config not in configurations:
    #                     configurations.add(config)
    #                     queue.append(config)
    #     return configurations

    def get_configurations(self):
        configurations = set()
        for s in self.s_map:
            # configurations.add(s)
            configurations.add((s, self.filled))
        return configurations

    def get_transitions(self, state):
        return self.delta[state]

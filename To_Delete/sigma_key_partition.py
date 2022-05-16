from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma


class Relation:

    def __init__(self):
        self.partitions = {}

    def __getitem__(self, sigma) -> set:
        return self.partitions[sigma]

    def add_partition(self, sigma) -> None:
        if sigma in self.partitions:
            raise KeyError("Key {} already exists in partitions.".format(sigma))
        self.partitions[sigma] = set()

    @classmethod
    def generate_relation(cls, RA: RegisterAutomata) -> "Relation":
        relation = Relation()
        pi = relation.partitions
        configs = list(RA.get_configurations())
        memory = {}
        while len(configs) > 0:
            q1, s1 = configs[0]
            for i in range(len(configs)):
                q2, s2 = configs[i]
                if s1 < s2:
                    key, state_pair = (s1, s2), (q1, q2)
                else:
                    key, state_pair = (s2, s1), (q2, q1)
                if key in memory:
                    for sigma in memory[key]:
                        pi[sigma].add(state_pair)
                    continue
                mapper = set()
                memory[key] = mapper
                sigmas = Sigma.generate_sigmas(s1, s2)
                for sigma in sigmas:
                    mapper.add(sigma)
                    if sigma not in pi:
                        pi[sigma] = set()
                    pi[sigma].add(state_pair)
            configs.pop(0)
        return relation

    def print(self) -> None:
        print("Relation: ")
        for key, value in self.partitions.items():
            print("\t{:100} ===> {}".format(str(key), [str(v) for v in value]).replace("\"", "").replace("\'", ""))

# Python imports
# import itertools

# Personal Imports
from Algorithms.A_SF import valid_bisim
from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.SetPermutation import PartialPermutation, SetPermutation
from Generator.generator import Partition, GeneratingSystem


#  Automaton Generation
s = "{q0,q1,q2,q3,q4}" \
    "{q0}{(q0)(q1,1)(q2,2)(q3,1)(q4,1,2)}" \
    "{(q0,1,L,q1)(q0,2,L,q2)(q0,1,L,q3)(q1,2,L,q4)(q2,1,L,q4)(q3,2,L,q4)(q4,2,L,q4)}" \
    "{}"
RA = RegisterAutomata(s)
length = len(RA.registers)
print("Automaton: ", s)
print("Domain: ", RA.registers)

#  ## Partition Generation
# Partition (Diamond)
diamonds = [
    {"q0"},
    {"q1", "q2", "q3"},
    {"q4"}
]

#  Representatives
rep_states = ["q0", "q1", "q4"]
x = [
    # {("1", "1"), ("2", "2")}
    {("1", "2"), ("2", "1")}
    # set()
]
# x = [set()]
Gc = [[set()], [{("1", "1")}], x]
reps = []
for i in range(len(rep_states)):
    qc = rep_states[i]
    xc = set(RA.s_map[qc])
    gc = [PartialPermutation(RA.registers, x) for x in Gc[i]]
    reps.append((qc, xc, gc))
# for r in reps:
#     print("{}\t{}\t{}".format(r[0], r[1], ("{}, " * len(r[2])).format(*r[2])))


#  Sigmas
sigmas = [
    {
        "q0": PartialPermutation(RA.registers, set()),
    },
    {
        "q1": PartialPermutation(RA.registers, {("1", "1")}),
        "q2": PartialPermutation(RA.registers, {("1", "2")}),
        "q3": PartialPermutation(RA.registers, {("1", "1")})
        # "q1": PartialPermutation(RA.registers, set()),
        # "q2": PartialPermutation(RA.registers, set()),
        # "q3": PartialPermutation(RA.registers, set())
    },
    {
        "q4":  PartialPermutation(RA.registers, set())
        # "q4":  PartialPermutation(RA.registers, {("1", "1"), ("2", "2")})
    }
]

#  Creation
print("\nPartitions: ")
partitions = []
for i in range(3):
    p = Partition(diamonds[i], reps[i], sigmas[i], RA.registers)
    partitions.append(p)
    print(p)
    for h in p.generate_h():
        print("\t{}\t{}\t{}".format(*h))

# Cl_H = set()
# for p in partitions:
#     Cl_H = Cl_H.union(p.closure(RA))
#
# print("\nCl(H): ")
# for t in Cl_H:
#     print("\t({}, {}, {})".format(*t))

G = GeneratingSystem(set(partitions), RA)
print(G.is_bisimulation())
# print("\n\n")
# print(G.is_member("q2", PartialPermutation(RA.registers, set()), "q3"))
# print(G.is_member("q3", PartialPermutation(RA.registers, {("1", "2")}), "q2"))
# print(G.is_member("q3", PartialPermutation(RA.registers, {("2", "1")}), "q2"))

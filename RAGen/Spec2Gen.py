def generate(size: int):
    states = "q0" + (",q{}" * (size-1)).format(*range(1, size))
    registers = "(q0" + (",{}" * size).format(*range(1, size+1)) + ")"
    for i in range(1, size):
        registers += f"(q{i}" + (",{}" * size).format(*range(1, size + 1)) + ")"
    initial = "q0"
    transitions = ""
    finals = ""
    for i in range(size):
        for j in range(1, size+1):
            transitions += "(q{},tag,{},K,q{})".format(i, j, i+1)
        transitions += "(q{},tag,{},L,q{})".format(i, i+1, i+1)
    transitions = transitions.replace(f"q{size}", "q0")
    automaton = "{" + "{}|{}|{}|{}|{}".format(states, initial, registers, transitions, finals).replace("|", "}{") + "}"
    return automaton


if __name__ == '__main__':
    print(generate(3))
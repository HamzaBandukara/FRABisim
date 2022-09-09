def generate(size: int):
    states = "q0"
    registers = "(q0" + (",{}" * size).format(*range(1, size+1)) + ")"
    initial = "q0"
    transitions = ""
    finals = ""
    for i in range(1, size+1):
        transitions += "(q0,tag,{},L,q0)".format(i)
        transitions += "(q0,tag,{},K,q0)".format(i)
    automaton = "{" + "{}|{}|{}|{}|{}".format(states, initial, registers, transitions, finals).replace("|", "}{") + "}"
    return automaton


if __name__ == '__main__':
    print(generate(3))
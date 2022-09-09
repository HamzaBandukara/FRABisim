def generate(size: int):
    states = ""
    initial = "q1"
    registers = ""
    transitions = ""
    finals = ""
    # Step 1: States
    for i in range(size):
        state = "q{}".format(i + 1)
        states += state + ","
        registers += "({}".format(state)
        for j in range(i):
            registers += ",{}".format(j + 1)
        registers += ")"
        if i < size:
            transitions += "({},{},{},G,{})".format(state, "populate", i+1, "q{}".format(i+2))
        for j in range(i, 0, -1):
            transitions += "({},{},{},K,{})".format(state, "populate",  j, state)
    q = size + 1
    registers += "(q{}".format(q)
    for j in range(q - 1):
        registers += ",{}".format(j + 1)
    registers += ")"
    state = "q{}".format(q)
    states += state
    for j in range(size):
        tag = "t{}".format(j + 1)
        for x in range(1, size + 1):
            transitions += "({},{},{},K,{})".format(state, tag, x, state)
            transitions += "({},{},{},L,{})".format(state, tag, x, state)
    automaton = "{" + "{}|{}|{}|{}|{}".format(states, initial, registers, transitions, finals).replace("|", "}{") + "}"
    return automaton


if __name__ == '__main__':
    print(generate(3))
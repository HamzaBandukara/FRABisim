def generateOLD(size: int) -> str:
    labels = [x for x in range(1, size + 1)]
    second_labels = [labels[x] for x in range(1, size)]
    second_labels.append(labels[0])
    s = "{q1,p1}{q1}{"
    tmp = "(q1"
    for i in range(1, size + 1):
        tmp += "," + str(i)
    tmp += ")(p1"
    for i in range(1, size + 1):
        tmp += "," + str(i)
    s += tmp + ")}{"
    for tag in range(size):
        for i in range(size):
            s += f"(q1,{tag},{labels[i]},K,q1)(p1,{tag},{labels[i]},K,p1)"
        s += f"(q1,{tag},{labels[tag]},L,q1)(p1,{tag},{second_labels[tag]},L,p1)"
    s += "}{}"
    return s

def generate(size: int) -> str:
    states = "q0"
    initial = "q0"
    registers = "(q0" + (",{}" * size).format(*range(1, size+1)) + ")"
    transitions, finals = "", ""
    for i in range(1, size + 1):
        for tag in [f"t{x}" for x in range(1, size+1)]:
            transitions += "(q0,{},{},K,q0)".format(tag, i)
        transitions += "(q0,{},{},L,q0)".format(f"t{i}", i)
    automaton = "{" + "{}|{}|{}|{}|{}".format(states, initial, registers, transitions, finals).replace("|", "}{") + "}"
    return automaton

if __name__ == '__main__':
    print(generate(3))

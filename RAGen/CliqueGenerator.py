def generate_clique(size: int) -> str:
    states = set([f"q{i}" for i in range(size)])
    initial = set(["q0"])
    registers = set()
    transitions = "{"
    t = "({},X,{},{},{})"
    r = "{}," * size
    r = r.format(*range(size))[:-1] + ")"
    for i in range(size):
        state = f"q{i}"
        registers.add(f"({state},{r}")
        for j in range(size):
            transitions += t.format(state, j, "K", f"q{j}")
            if j != i:
                transitions += t.format(state, j, "L", f"q{j}")
    transitions += "}"
    s = "{}{}{}{}".format(states, initial, registers, transitions) + "{}"
    return s.replace("\'", "").replace(" ", "")


if __name__ == '__main__':
    print(generate_clique(3))
def generate_stack(registers: int, char="q") -> str:
    # States
    RA = "{"
    states = registers + 1
    for i in range(states):
        RA += "{}{}".format(char, i) + ","
    RA = RA[:-1] + "}"

    # Initial State
    RA += "{" + char + "0}"

    # Registers
    RA += "{"
    reg_set = set()
    counter = 0
    for i in range(states):
        if len(reg_set) == 0:
            RA += "({}{})".format(char, i)
        else:
            RA += "({}{},{})".format(char, i, str(reg_set)[1:-1])
        counter += 1
        reg_set.add(registers + 1 - counter)
    RA += "}"

    # Transitions
    RA += "{"
    for r in range(1, registers + 1):
        RA += "({}{},push,{},L,{}{})".format(char, r-1, registers + 1 - r, char, r)
        for i in range(r):
            RA += "({}{},pop,{},K,{}{})".format(char, r, registers + 1 - r, char, i)
    RA += "}{}"

    return RA.replace(" ", "")

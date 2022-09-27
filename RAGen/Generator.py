def generate_stack(registers: int)  -> str:
    # States
    RA = "{"
    states = registers + 1
    for i in range(states):
        RA += "q{}".format(i) + ","
    RA = RA[:-1] + "}"

    # Initial State
    RA += "{q0}"

    # Registers
    RA += "{"
    reg_set = set()
    counter = 0
    for i in range(states):
        if len(reg_set) == 0:
            RA += "(q{})".format(i)
        else:
            RA += "(q{},{})".format(i, str(reg_set)[1:-1])
        counter += 1
        reg_set.add(counter)
    RA += "}"

    # Transitions
    RA += "{"
    for r in range(1, registers + 1):
        RA += "(q{},push,{},G,q{})".format(r-1, r, r)
        RA += "(q{},pop,{},K,q{})".format(r, r, r-1)
    RA += "}{}"

    return RA.replace(" ", "")


# print(generate_stack(3))
def generate_xml_stack(registers: int):
    pass

if __name__ == '__main__':
    print(generate_stack(2))
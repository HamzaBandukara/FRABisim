from re import findall
from DataStructures.RA_SF_A import RegisterAutomata, Transition


def convert(lines, ra: RegisterAutomata=None) -> RegisterAutomata:
    if ra is None:
        ra = RegisterAutomata()
        start = "s0"
    else:
        start = "t0"
        lines = lines.replace("s", "t")
    if isinstance(lines, str):
        lines = lines.split("\n")[:-1]
    pi = dict()
    pi[start] = lines[0].split(" |- ")[1].replace("\n", "")
    if pi[start][0] == "(":
        pi[start] = pi["s0"][1:-1]
    ra.initial = start
    ra.s_map[start] = set()
    x = findall("{(.*?)}", lines[0])
    x = findall("\((.*?)\)", x[0])
    for elem in x:
        ra.s_map[start].add(elem.split(",")[0])
        ra.r_map.add(elem.split(",")[0])
        ra.actions.add((elem.split(",")[0], "K"))
        ra.actions.add((elem.split(",")[0], "L"))
        ra.actions.add((elem.split(",")[0], "G"))
        ra.filled.add((elem.split(",")[0]))
        # states += "," + elem.split(",")[0]
    for i in range(1, len(lines)):
        t = None
        lines[i] = lines[i].replace("\n", "")
        x = lines[i].split("  ")
        y = x[1]
        known_flag = False
        if "\'" in y:
            y = y.split("\'")
            known_flag = True
        else:
            y = y.split(" ")
        if len(y) == 2:
            y[1] = y[1].replace("^", "").replace("*", "")
        # if (y[0] == "1" or y[1] == "1") and x[0] != "s0":
        #     continue
        x[-1] = x[-1].replace(" ", "")
        tgt = x[-1].split("=")[0]
        if tgt not in ra.s_map:
            pi[tgt] = lines[i].split(" |- ")[1].replace("\n", "")
            if pi[tgt][0] == "(":
                pi[tgt] = pi[tgt][1:-1]
            # all_states += "," + tgt
            ra.s_map[tgt] = set()
            tmp = findall("{(.*?)}", x[-1])
            tmp = findall("\((.*?)\)", tmp[0])
            for elem in tmp:
                ra.s_map[tgt].add(elem.split(",")[0])
                ra.r_map.add(elem.split(",")[0])
                ra.actions.add((elem.split(",")[0], "K"))
                ra.actions.add((elem.split(",")[0], "L"))
                ra.actions.add((elem.split(",")[0], "G"))
                ra.filled.add((elem.split(",")[0]))
        x[1] = x[1][2:]
        symb = None
        if len(y) == 1:
            ra.transitions.add(Transition(x[0], "Tau", "0", "K", tgt))
            continue
        if x[1] == "": x[1] = "0"
        if x[1][-1] == "^":
            symb = "G"
            ra.transitions.add(Transition(x[0], "out1", y[0], "K", f"{x[0]}out{y[0]}"))
            ra.transitions.add(Transition(f"{x[0]}out{y[0]}", "out2", y[1], "G", tgt))
            if f"{x[0]}out{y[0]}" not in ra.s_map:
                ra.s_map[f"{x[0]}out{y[0]}"] = ra.s_map[x[0]]
        elif x[1][-1] == "*":
            symb = "L"
            ra.transitions.add(Transition(x[0], "inp1", y[0], "K", f"{x[0]}inp{y[0]}"))
            ra.transitions.add(Transition(f"{x[0]}inp{y[0]}", "inp2", y[1], "L", tgt))
            if f"{x[0]}inp{y[0]}" not in ra.s_map:
                ra.s_map[f"{x[0]}inp{y[0]}"] = ra.s_map[x[0]]
        else:
            symb = "K"
            if x[1] != "0" and not known_flag:
                ra.transitions.add(Transition(x[0], "inp1", y[0], "K", f"{x[0]}inp{y[0]}"))
                ra.transitions.add(Transition(f"{x[0]}inp{y[0]}", "inp2", y[1], "K", tgt))
                if f"{x[0]}inp{y[0]}" not in ra.s_map:
                    ra.s_map[f"{x[0]}inp{y[0]}"] = ra.s_map[x[0]]
        if known_flag and symb != "G":
            ra.transitions.add(Transition(x[0], "out1", y[0], "K", f"{x[0]}out{y[0]}"))
            ra.transitions.add(Transition(f"{x[0]}out{y[0]}", "out2", y[1], "L", tgt))
            if f"{x[0]}out{y[0]}" not in ra.s_map:
                ra.s_map[f"{x[0]}out{y[0]}"] = ra.s_map[x[0]]

    ra.complete_setup()
    # return "{" + all_states + "}{" + initial + "}{" + states + "}{" + transitions + "}{}"
    return ra


if __name__ == '__main__':
    with open("pifra/vk-fin-st2.txt", "r") as f:
        x = (convert(f.readlines()))
        print(x)

#  Prove that if two pi-calculus processes are bisimilar, /
#  their xpi-calculus equivelent processes are also bisimilar /

#  If two xpi equiv, their FRAs are equivalent (and vice versa)
#  assume R between xpi that is bisimulation, define R' that contains translations of R,
#  Show that it is a bisimulation
#  Start bisimulation R in FRAs, construct bisimulation R' in xpi from R

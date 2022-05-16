import multiprocessing
import string


#  https://stackoverflow.com/a/64647186
def lexstringsold(max_length: int=-1, alphabet=string.ascii_uppercase):
    yield ""
    if max_length == 0: return
    for first in alphabet:
        for suffix in lexstrings(max_length - 1, alphabet=alphabet):
            yield first + suffix


def lexstrings(max_length: int=-1, alphabet=string.ascii_uppercase):
    if max_length == 0: return
    for first in alphabet:
        yield first
    for first in alphabet:
        for suffix in lexstrings(max_length - 1, alphabet=alphabet):
            yield first + suffix

def g_cpt_populate(prev, p, g, x):
    s = ""
    flag = True
    for i in range(1, len(prev)):
        prev2 = [y for y in prev]
        # x = next(g)
        prev2[i] = x
        t = (f"[{x}#{'{}'}]" * (len(prev)-1)).format(*[y for y in prev if y!=x])
        s += f"({prev[0]}({x}).{t}{prev[0]}<{prev[0]}>.{p}(" + ("{}," * len(prev2)).format(*prev2)[:-1] + "))+"
    return s[:-1]



def g_push(g, prev, p_next):
    c_next = next(g)
    c_current = prev[-1]
    t = (f"[{c_next}#{'{}'}]" * (len(prev))).format(*prev)
    s = f"({prev[0]}({c_next}).{t}{prev[0]}<{prev[0]}>.{p_next}(" + ("{}," * len(prev)).format(*prev) + f"{c_next}))"
    # s = f"{prev[1]}({c_next})." + (f"[{c_next}!={'{}'}]" * len(prev)).format(*prev) + f"{p_next}(" + ("{}," * len(prev)).format(*prev) + f"{c_next})"
    # s = f"{prev[0]}'<{prev[0]}>.${c_next}.{prev[1]}'<{c_next}>.{p_next}(" + ("{}," * len(prev)).format(*prev) + f"{c_next})"
    # s = f"${c_next}.{prev[1]}({c_next}).{p_next}(" + ("{}," * len(prev)).format(*prev) + f"{c_next})"
    prev.append(c_next)
    return s


def g_pop(p, prev):
    c_current = prev[-1]
    t = (f"[{c_current}#{'{}'}]" * (len(prev) - 1)).format(*prev[:-1])
    s = f"({prev[0]}<{prev[-1]}>.{p}({('{},' * (len(prev) - 1)).format(*prev[:-1])[:-1]}))"
    return s


def g_dequeue(p, prev):
    tmp = [x for x in prev]
    t = (f"[{prev[-1]}#{'{}'}]" * (len(tmp)-1)).format(*tmp[:-1])
    x = tmp.pop(1)
    s = f"({prev[0]}<{x}>.{p}({('{},' * (len(prev) - 1)).format(*tmp)[:-1]}))"
    return s


def g_cptpop(prev, next_process):
    s = ""
    slice = prev[1:]
    for c in slice:
        s += f"({prev[0]}<{c}>.{next_process}) + "
    return s[:-3]


def stack_builder(size=2, p_names=lexstrings(), c_names=None, p=None):
    if c_names is None:
        c_names = lexstrings(-1, alphabet=string.ascii_lowercase)
        next(c_names)
        next(c_names)
    final_string = ""
    c_prev = [next(lexstrings(-1, alphabet=string.ascii_lowercase))]
    # c_prev = [next(c_names), next(c_names)]
    original_size = size
    next(p_names), next(p_names)
    p_next = next(p_names)
    p_current = p_next
    while size >= 0:
        p_prev = p_current
        p_current = p_next
        definition = p_current + "(" + ("{}," * len(c_prev)).format(*c_prev)[:-1] + ") = "
        deef = ""
        if size != original_size:
            deef += g_pop(p_prev, c_prev)
        if size != 0 and size != original_size:
            deef += " + "
        if size != 0:
            p_next = next(p_names)
            deef += g_push(c_names, c_prev, p_next)
        definition += "(" + deef + ")"
        final_string += definition + "\n"
        size -= 1
    return final_string


def queue_builder(size=2, p_names=lexstrings(), p=None):
    c_names = lexstrings(-1, alphabet=string.ascii_lowercase)
    final_string = ""
    c_prev = [next(c_names)]
    # c_prev = [next(c_names), next(c_names)]
    original_size = size
    next(p_names), next(p_names)
    p_next = next(p_names)
    p_current = p_next
    while size >= 0:
        p_prev = p_current
        p_current = p_next
        definition = p_current + "(" + ("{}," * len(c_prev)).format(*c_prev)[:-1] + ") = "
        deef = ""
        if size != original_size:
            deef += g_dequeue(p_prev, c_prev)
        if size != 0 and size != original_size:
            deef += " + "
        if size != 0:
            p_next = next(p_names)
            deef += g_push(c_names, c_prev, p_next)
        deef = deef.replace(" ", "")
        definition += "(" + deef + ")"
        final_string += definition + "\n"
        size -= 1
    return final_string


def cpt_builder(size=2, p_names=lexstrings(), p=None):
    c_names = lexstrings(-1, alphabet=string.ascii_lowercase)
    final_string = ""
    c_prev = [next(c_names)]
    original_size = size
    next(p_names), next(p_names)
    p_next = next(p_names)
    p_current = p_next
    while size >= 0:
        p_prev = p_current
        p_current = p_next
        definition = p_current + "(" + ("{}," * len(c_prev)).format(*c_prev)[:-1] + ") = "
        if size != original_size:
            if size != 0:
                next_process = p_next
            else:
                next_process = p_current
            next_process += "(" + ("{}," * len(c_prev))[:-1].format(*c_prev) + ")"
            definition += g_cptpop(c_prev, next_process)
        if size != 0 and size != original_size:
            definition += " + "
        if size != 0:
            p_next = next(p_names)
            definition += f"({g_push(c_names, c_prev, p_next)})"
        # if size == 0:
        #     definition += "+"+g_cpt_populate(c_prev, p_current, c_names, next(c_names))
        final_string += definition + "\n"
        size -= 1
    return final_string


def piet_queue_builder(lines1, lines2):
    ret = ""
    first, second = None, None
    for line in lines1.split("\n")[:-1]:
        if first is None:
            first = line.split(" = ")[0]
        if "+" in line:
            line = line.split(" = ")
            defi = line[0]
            line = line[1]
            line = line.split("+")
            line = defi + " := " + line[0][1:-1] + "+" + line[1][1:-1]
        else:
            line = line.split(" = ")
            line = line[0] + " := " + line[1]
        line = "AGENT " + line + ";\n"
        ret += line
    for line in lines2.split("\n")[:-1]:
        if second is None:
            second = line.split(" = ")[0]
        if "+" in line:
            line = line.split(" = ")
            defi = line[0]
            line = line[1]
            line = line.split("+")
            line = defi + " := " + line[0][1:-1] + "+" + line[1][1:-1]
        else:
            line = line.split(" = ")
            line = line[0] + " := " + line[1]
        line = "AGENT " + line + ";\n"
        ret += line
    ret += f"TEST {first}\nWITH {second};;"
    return ret


def par(gen_1, size_1, gen_2, size_2, g =None):
    g2 = lexstrings(-1, alphabet=string.ascii_lowercase)
    next(g2)
    process_1 = gen_1(size=size_1, c_names=g2)
    process_2 = gen_2(size=size_2, c_names=g2)
    if g is None:
        g = lexstrings()
    p1 = process_1.split(" = ")[0]
    p2 = process_2.split(" = ")[0]
    process = f"{next(g)}(a) = ({p1}|{p2})\n{process_1}{process_2}"
    return process

def gen(size, gen, p="A"):
    process = gen(size)
    p1 = process.split(" = ")[0]
    process = f"{p}(a) = GEN(a)|{p1}\nGEN(a) = $b.a<b>.GEN(a)\n" + process
    return process

def wrapper(p1, p2, tmp):
    from pibisim import pi_bisim as bisim
    tmp.extend(bisim(p1, p2))


def piet_gen(gen1, size1, gen2, size2, tmp):
    process_1 = gen1(size=size1)
    process_2 = gen2(size=size2)
    p1, p2 = process_1.split(" = ")[0], process_2.split(" = ")[0]
    p = multiprocessing.Process(target=wrapper, args = (process_1, process_2, tmp))
    p.start()
    p.join()
    if p.is_alive():
        p.terminate()
    lines = tmp[3]
    lines = f"AGENT A(a):=GENONE(a)|{p1};\nAGENT B(a):=GENONE(a)|{p2};\n" + lines
    lines = "AGENT GENONE(a):=^b a<b>.GENONE(a);\n" + lines
    lines = lines[:lines.rfind("\n")]
    lines = lines[:lines.rfind("\n")]
    lines += "\nTEST A(a)\nWITH B(a);;"
    while len(tmp) > 0: tmp.pop()
    return lines

if __name__ == '__main__':
    from pibisim import pi_bisim as bisim
    for i in range(1, 11):
        print(bisim(gen(i, cpt_builder),gen(i, cpt_builder)))

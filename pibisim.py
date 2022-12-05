import string
import time

from DataStructures.SetPermutation import PartialPermutation
from pifra_2_ra import *
from pi2fra.pyfra import *
from pi2fra.parser.antler import main as parse
from Algorithms.forward_generator import ra_bisim as fwd
# from Algorithms.forward_exception import ra_bisim as fwd
# from Algorithms.forward_algorithm_2 import ra_bisim as fwd
from Algorithms.forward_algorithm_3 import ra_bisim as fwd
# from Algorithms.forward_genex import ra_bisim as fwd
from Algorithms.forward_generator2 import ra_bisim as fwd
from pibuilders import stack_builder as stack, queue_builder as queue, cpt_builder as cpt, piet_queue_builder as pietq, \
    par, lexstrings

from datetime import datetime as dt
import os
import subprocess
import os


def mwb_bisim(process1, process2):
    process1 = bytes("agent " + process1 + "\n",'utf-8')
    process2 = bytes("agent " + process2 + "\n",'utf-8')
    # s = b"agent P(a) = a(b).'b<a>.0\n"
    s2 = b"eq P Q"
    p1 = subprocess.Popen('sml @SMLload=./mwb/mwb', shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    p1.stdin.write(process1)
    p1.stdin.write(process2)
    p1.stdin.write(s2)
    out, err = p1.communicate(b"")
    return b"The two agents are equal" in out


def piet_bisim(lines, type="see"):
    with open("piet_input", "w", newline="\n") as f:
        f.write(lines)
    cmd = f"./piet {type} 500000 piet_input cmp"
    args = ["./piet", type, "500000", "piet_input", "cmp"]
    if os.name == 'nt':
        args.insert(0, "wsl")
        cmd = "wsl " + cmd
    # p1 = os.popen(cmd)
    try:
        x = str(subprocess.check_output(args, stderr=subprocess.STDOUT, timeout=60))
    except subprocess.TimeoutExpired:
        return None, 60000
    x = x.replace("'", "").replace("b", "")
    x = x.split("\\n")
    # p1 = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # x = p1.readlines()
    # try:
    #     p1 = subprocess.run(args, capture_output=True, timeout=30)
    # except subprocess.TimeoutExpired:
    #     return None, 30
    # exit(5)
    # p1 = os.popen(cmd)
    # p1 = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # x = str(p1.stdout)[2:-1]
    # x = x.split("\\n")
    # print(out, err)
    # print(x)
    # print(x[1][:2])
    if x[1][:2] == "NO":
        b = False
    else:
        b = True
    x[2] = x[2].split(" ")
    try:
        t = (int(x[2][2]) * 1000) + (float(x[2][4]) * 10)
    except IndexError:
        print(x)
        raise Exception("FAILED PiET")
    return b, t

def time_convert(t):
    pass



def get_lines(pi):
    with open("tmp.pi", "w") as f:
        f.write(pi)
    pi = os.popen("pifra -n 2000000 tmp.pi -v")
    t = pi.read()
    x = t.splitlines()[-7:]
    print(x[-2])
    print(x[-1])
    lts_time = x[-1].split(" ")[-1]
    print(lts_time)
    print(x[-1][-2] == "µ")
    exit(5)
    return t


def piet_lines(process_1, process_2):
    # print(process_1)
    # print(process_2)
    ret = ""
    one, two = None, None
    for line in process_1.split("\n")[:-1]:
        if one is None:
            one = line.split(" = ")[0]
        line = line.replace(" = ", " := ")
        ret += f"AGENT {line};\n"
    for line in process_2.split("\n")[:-1]:
        if two is None:
            two = line.split(" = ")[0]
        line = line.replace(" = ", " := ")
        ret += f"AGENT {line};\n"
    ret += f"TEST {one}\nWITH {two};;"
    print(piet_bisim(ret))

def pi_bisim(process_1, process_2, par=None):
    proc_1 = parse(process_1)
    proc_2 = parse(process_2)
    pyfra_t = time.process_time_ns()
    re1, reg, root1 = proc_1.buildLTS()
    i1, ra = Process.gen_FRA(lambda k, v: (k in re1 and v.size > 0), r=root1)
    Process.lts = {}

    if not process_2 is None:
        re2, reg2, root2 = proc_2.buildLTS()
        reg = reg.union(reg2)
        i2, ra = Process.gen_FRA(lambda k, v: (k in re2 and v.size > 0), ra, r=root2)
        q1 = "q0"
    else:
        i2, root2 = i1, root1
        q1 = "s0"
    pyfra_t = time.process_time_ns() - pyfra_t
    pyfra_t /= (10 ** 9)
    ra.r_map = reg
    ra.registers = list(ra.r_map)
    mapper = set()
    for key in i1:
        if key in i2:
            mapper.add((i1[key], i2[key]))
    # ra.print_transitions()
    bis_t = time.process_time_ns()
    result = fwd(ra, "s0", q1, mapper)
    bis_t = time.process_time_ns() - bis_t
    bis_t /= (10 ** 9)
    piet_lines = ""
    for symb in RawProcess.vardefn:
        children, proc = RawProcess.vardefn[symb]
        piet_lines += (f"AGENT {symb}({('{},' * len(children)).format(*children)[:-1]}):={proc.to_piet()}") + ";\n"
    piet_lines += f"TEST {root1.proc.to_piet()}\nWITH {root2.proc.to_piet()};;"
    RawProcess.support = {}
    RawProcess.vardefn = {}
    Process.lts = {}
    PartialPermutation.FULL_DOMAIN = None
    return pyfra_t, bis_t, result, piet_lines


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(1003)
    # print(cpt(2))
    # print(pi_bisim(stack(2), stack(2)))
    # q = pietq(queue(100), queue(100))
    # print(q)
    # print(piet_bisim(q)
    # print(x)
    g = lexstrings()
    # p1 = par(stack, 2, stack, 2, g)
    # p2 = par(stack, 2, stack, 2, g)
    x = stack(10)
    first = x.split("(")[0]
    x = f"A(a) = GEN(a)|{first}(a)\nGEN(a)=$b.a<b>.GEN(a)\n{x}"
    y = stack(10)
    first = y.split("(")[0]
    y = f"B(a) = GEN(a)|{first}(a)\n{y}"
    # print(x)
    # print(y)
    t1, t2 = [], []
    for i in range(3):
        x = pi_bisim(cpt(50), cpt(50))
        print(x[0], x[1])
        t1.append(x[0])
        t2.append(x[1])
    print((sum(t1)/3) + (sum(t2)/3))

    # x = queue(2)
    # print(x)
    # print(pi_bisim(queue(2), queue(2)))
    # x = """"""
    # print(pi_bisim(p1, p2))
    # piet_lines(cpt(3), cpt(3))
    # pi_bisim(cpt(5), cpt(5))
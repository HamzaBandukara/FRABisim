import os
import statistics
from datetime import datetime as dt
from time import process_time_ns
from time import process_time
from time import thread_time_ns
from time import perf_counter_ns
from time import time
from threading import Timer
import timeit
import multiprocessing
import time
import gc
import subprocess

# from DataStructures.RA_SF_A import RegisterAutomata as RA
# from DataStructures.Sigma import Sigma
# from sympy import *
from DataStructures.RA_SF_A import RegisterAutomata
from RAConverter import ra_to_xml
from RAGen.Generator import generate_stack as gen_det
from RAGen.NDGenerator import generate_stack as gen_ndet
from RAGen.RLGenerator import generate_stack as rl_gen_det
from RAGen.RLNDGenerator import generate_stack as rl_gen_ndet
from RAGen.CPTGenerator import generate as gen_cpt
from RAGen.FlowerGenerator import generate as gen_flw
from RAGen.CliqueGenerator import generate_clique as gen_cli
from RAGen.Combiner import combiner

from Algorithms.forward_generator2 import forward as fwd_g
from Algorithms.A_SF import is_bisim as nve
from Algorithms.forward_algorithm_3 import ra_bisim as fwd_m
from Algorithms.forward_exception import ra_bisim as fwd_e
from Algorithms.PR_Version_2 import is_bisimilar as pr

# import matplotlib as plt
import sys

sys.setrecursionlimit(5000)


def __stack_test(num: int, method_1, method_2, generator):
    for i in range(1, num):
        s = generator(i)
        u_1 = method_1(s)
        u_2 = method_2(s)
        try:
            assert u_1 == u_2
        except AssertionError:
            print(u_1)
            print(u_2)
            exit(-2)
    print("Stack Test Passed for size {}".format(num))


def __all_states_test(num1: int, num2: int, method_1, method_2, generator):
    a = generator(num1)
    c2 = "q2"
    if not num2 == -1:
        a2 = generator(num2)
        a = combiner(a, a2)
        c2 = "p"
    for m1 in range(num1 + 1):
        for m2 in range(num2 + 1):
            u_1 = method_1(a, "q{}".format(m1), "{}{}".format(c2, m2))
            u_2 = method_2(a, "q{}".format(m1), "{}{}".format(c2, m2))
            assert u_1 == u_2


def __diff_stack_test(num1: int, num2: int, method_1, method_2, generator):
    a1 = generator(num1)
    a2 = generator(num2)
    a = combiner(a1, a2)
    u_1 = method_1(a, "q0", "p0")
    u_2 = method_2(a, "q0", "p0")
    print(u_1, u_2)
    assert u_1 == u_2


def det_stack_test(num: int, method_1, method_2):
    __stack_test(num, method_1, method_2, gen_det)


def ndet_stack_test(num: int, method_1, method_2):
    __stack_test(num, method_1, method_2, gen_ndet)


def file_test(dir: str, method_1, method_2):
    for f in os.listdir(dir):
        with open(dir + f, "r") as file:
            s = file.readline().replace(" ", "").replace("\n", "")
        print(f)
        u_1 = method_1(s)
        u_2 = method_1(s)
        try:
            assert u_1 == u_2
        except AssertionError:
            print("Experiment failed at file {}".format(f))
            print("Result of u_1: ")
            print_u(u_1)
            print("\nResult of u_2: ")
            print_u(u_2)
            exit("FAILED FOR FILE {}".format(f))
    print("Success for all files in {}".format(dir))


def print_u(u):
    print(u)
    for r in u:
        print(("{}\t" * len(r)).format(*r))


def method_wrapper(tmp, method, representation, q1, p1, sigma):
    start = time.process_time()
    # print("S", start)
    u = method(representation, q1, p1, sigma)
    finish = time.process_time()
    t = finish - start
    # print("START", start, "END", finish, "DIFF", t)
    tmp.append((u, t * 1000))


def __single_time_test(RA: RegisterAutomata, q1: str, sigma, p1: str, method):
    TIMEOUT = 30
    manager = multiprocessing.Manager()
    tmp = manager.list()
    # print("tmp", tmp)
    # print("INPUT: ", q1, p1, sigma)
    p = multiprocessing.Process(target=method_wrapper, args=(tmp, method, RA, q1, p1, sigma))
    p.start()
    p.join(TIMEOUT)
    p.terminate()
    if len(tmp) == 0:
        tmp.append((None, TIMEOUT))
    u, t = tmp.pop(0)
    # print("FIN.", tmp, u, t.total_seconds())
    return t, u


def record(path, file, representation, q1, s, q2, repetitions=3):
    print("Testing", path, file)
    ra = RegisterAutomata(representation)
    line = "{},{},{},{},".format(path, file, len(ra.get_states()), len(ra.transitions))
    representation = representation.replace(" ", "")
    q1 = q1.replace(" ", "")
    q2 = q2.replace(" ", "")
    # dirs = ["fwd_e", "fwd_g"]
    # methods = [fwd_e, fwd_g]
    dirs = ["fwd_m", "fwd_e", "fwd_g"]
    methods = [fwd_m, fwd_e, fwd_g]
    # dirs = ["nve", "fwd_m", "fwd_e", "fwd_g"]
    # methods = [nve, fwd_m, fwd_e, fwd_g]
    results = {}
    for index in range(len(dirs)):
        times, res = [], []
        for _ in range(repetitions):
            time, result = __single_time_test(ra, q1, s, q2, methods[index])
            if result is not None:
                times.append(time)
                res.append(result)
        try:
            assert len(set(res)) <= 1
        except AssertionError:
            print("TEST FAILED ON REPEAT.")
            print(path, file, dirs[index])
            print(representation)
            print(q1, s, q2)
            print(res)
            exit(-4)
        result = None
        time = 30000
        if len(set(res)) == 1:
            result = res.pop(0)
            time = sum(times) / len(times)
        line += "{:.16f}".format(time) + ","
        if result is not None:
            results[dirs[index]] = result
    with open("Benchmarks_SETTA.csv", "a") as f:
        line = line[:-1] + "," + str(set(results.values()))
        f.write(line)
    try:
        assert len(set(results.values())) <= 1
    except AssertionError:
        print("TEST FAILED HERE.")
        print(path, file)
        print(representation)
        print(q1, s, q2)
        print(results)
        exit(-5)


def deq(a1, a2, repetitions=3):
    file = open("xml_1.xml", "w")
    file.write(ra_to_xml(a1))
    file.close()
    file = open("xml_2.xml", "w")
    file.write(ra_to_xml(a2))
    file.close()
    file = open("./xml_1.xml", "r")
    # print(file.readlines())
    file.close()
    times, results = [], []
    for _ in range(repetitions):
        # x = os.popen("deq ./deq/examples/cptR-3.xml ./deq/examples/cptR-3.xml").read()
        x = os.popen("deq ./xml_1.xml ./xml_2.xml").read()
        # print(x)
        x = x.replace(" ", "").replace("\n", "").split(",")
        # print(x)
        times.append(float(x[3]))
        results.append(x[2])
    time = sum(times) / len(times)
    assert len(set(results)) == 1
    return results[0], time


def rabitjrunner(a1, a2, repetitions, triple):
    f = open("./xml_1.xml", "w")
    f.write(ra_to_xml(a1))
    f.close()
    f = open("./xml_2.xml", "w")
    f.write(ra_to_xml(a2))
    f.close()
    times, results = [], []
    if len(triple[1]) == 0: triple = triple[0], "{}", triple[2]
    else: triple = triple[0], str(triple[1]).replace("'", "").replace(" ", ""), triple[2]
    for _ in range(repetitions):
        try:
            x = str(subprocess.check_output(["java", "-jar", "./rabitj/rabit.jar", "./xml_1.xml", "./xml_2.xml", "({},{},{})".format(*triple)], stderr=subprocess.STDOUT, timeout=60))
            x = x.replace("'", "").replace("b", "")
            x = x.split(" ")
            times.append(float(x[1][:-4]))
            results.append(x[0])
        except subprocess.TimeoutExpired:
            pass
    if len(times) == 0 and len(results) == 0:
        times.append(30 * 1000)
        results.append(None)
    time = sum(times) / len(times)
    if time > 30000: time = 30000
    assert len(set(results)) == 1
    return results[0], time

def lois(method, det_1, size_1, det_2, size_2, timeout, repetitions=3):
    # print("PARAMS: ", method, size_1, size_2, det_1, det_2, timeout)
    det_1 = "det" if det_1 else "ndet"
    det_2 = "det" if det_2 else "ndet"
    times, results = [], []
    for _ in range(repetitions):
        # print(f"lois_bisim.exe {method} {size_1} {det_1} {size_2} {det_2} {timeout}")
        p = os.popen(f"lois_bisim.exe {method} {size_1} {det_1} {size_2} {det_2} {timeout}")
        x = p.read()
        # x = subprocess.Popen(["lois_bisim.exe", method, str(size_1), det_1, str(size_2), det_2, str(timeout)], stdout=subprocess.PIPE)
        # x = str(x.stdout.read())[2:-3]
        # print(x)
        # print(x)
        x = x.split(",")
        if "TO" in x[0]:
            continue
        else:
            times.append(float(x[1]))
            results.append(True if "YES" in x[0] else False)
        gc.collect(generation=2)
    if len(times) == 0:
        time = timeout * 1000
    else:
        time = sum(times) / len(times)
    if len(results) == 0:
        results.append(None)
    assert len(set(results)) == 1
    return results[0], time


def benchmarks(size=30, repetitions=1, start=1, steps=1):
    # if not os.path.exists("./Benchmarks"):
    #     os.mkdir("./Benchmarks")
    # # output_file = open("Benchmarks_SETTA.csv", "w")
    # # output_file.write(
    # #     "TestCode,RA,States,Transitions,Memo,Exception,Generator,Result,DEQ-Result,DEQ-Time,LOIS FW Result,LOIS FW Time,LOIS PR Result,LOIS PR Time\n")
    # # # output_file.write("TestCode,RA,Naive,Memo,Exception,Generator\n")
    # # output_file.close()
    # timeout = 30
    # # open("JTimes", "w").close()
    # # Test_01_B - LR Deterministic Stacks
    # for i in range(start, size, steps):
    #     r1, r2 = gen_det(i), gen_det(i)
    #     result, time = rabitjrunner(r1, r2, repetitions, ("q0", set(), "q0"))
    #     with open("JTimes", "a") as f:
    #         f.write("Test_01_B,LR_DS_{},{}\n".format(i, time))
    #     # representation = gen_det(i)
    #     # q1 = representation.split("{")[2][:-1]
    #     # q2 = q1.replace("q", "p")
    #     # representation = combiner(representation, rl_gen_det(i))
    #     # record("Test_01_B", "LR_DS_{}".format(i), representation, q1, set(), q2, repetitions)
    #     # output_file = open("Benchmarks_SETTA.csv", "a")
    #     # result, time = deq(representation, representation, repetitions)
    #     # output_file.write(",{},{:.16f}".format(result, float(time)))
    #     # if size < 21:
    #     #     result, time = lois("FW", True, i, True, i, timeout, repetitions)
    #     #     output_file.write(",{},{:.16f}".format(result, float(time)))
    #     #     result, time = lois("PR", True, i, True, i, timeout, repetitions)
    #     #     output_file.write(",{},{:.16f}\n".format(result, float(time)))
    #     # else:
    #     #     output_file.write(",NA,30000,NA,30000\n")
    #     # output_file.close()
    #
    # # Test_01_D - LR Non-Deterministic Stacks
    # for i in range(start, size, steps):
    #     r1, r2 = gen_ndet(i), gen_ndet(i)
    #     result, time = rabitjrunner(r1, r2, repetitions, ("q0", set(), "q0"))
    #     with open("JTimes", "a") as f:
    #         f.write("Test_01_D,LR_NDS_{},{}\n".format(i, time))
    #     # representation = gen_ndet(i)
    #     # q1 = representation.split("{")[2][:-1]
    #     # q2 = q1.replace("q", "p")
    #     # representation = combiner(representation, rl_gen_ndet(i))
    #     # record("Test_01_D", "LR_NDS_{}".format(i), representation, q1, set(), q2, repetitions)
    #     # output_file = open("Benchmarks_SETTA.csv", "a")
    #     # output_file.write(",NA,NA,NA,NA,NA,NA\n")
    #     # output_file.close()
    #
    # # Test 01_F - CPT
    # for i in range(start, size, steps):
    #     r1, r2 = gen_cpt(i), gen_cpt(i)
    #     result, time = rabitjrunner(r1, r2, repetitions, ("q0", set(), "q0"))
    #     with open("JTimes", "a") as f:
    #         f.write("Test_01_F,CPT_{},{}\n".format(i, time))
    #     # representation = gen_cpt(i)
    #     # q1 = representation.split("{")[2][:-1]
    #     # q2 = q1.replace("q", "p")
    #     # representation = combiner(representation, representation)
    #     # record("Test_01_F", "CPT_{}".format(i), representation, q1, set(), q2, repetitions)
    #     #
    #     # output_file = open("Benchmarks_SETTA.csv", "a")
    #     # output_file.write(",NA,NA,NA,NA,NA,NA\n")
    #     # output_file.close()
    #
    # # Test 01_F - Flower
    # for i in range(start, size, steps):
    #     r1, r2 = gen_flw(i), gen_flw(i)
    #     result, time = rabitjrunner(r1, r2, repetitions, ("q0", set(), "q0"))
    #     with open("JTimes", "a") as f:
    #         f.write("Test_01_F,FLW_{},{}\n".format(i, time))
    #     # representation = gen_flw(i)
    #     # representation = combiner(representation, representation)
    #     # q1 = representation.split("{")[2][:-1]
    #     # q2 = q1.replace("q", "p")
    #     # record("Test_01_F", "FLW_{}".format(i), representation, q1, set(), q2, repetitions)
    #     #
    #     # output_file = open("Benchmarks_SETTA.csv", "a")
    #     # output_file.write(",NA,NA,NA,NA,NA,NA\n")
    #     # output_file.close()

    # Test 01_G - Clique
    for i in range(start, size, steps):
        r1, r2 = gen_cli(i), gen_cli(i)
        result, time = rabitjrunner(r1, r2, repetitions, ("q0", set(), "q0"))
        with open("JTimes", "a") as f:
            f.write("Test_01_G,CLI_{},{}\n".format(i, time))
        # representation = gen_cli(i)
        # q1 = representation.split("{")[2][:-1]
        # representation = combiner(representation, representation)
        # q2 = q1.replace("q", "p")
        # record("Test_01_G", "CLI_{}".format(i), representation, q1, set(), q2, repetitions)
        #
        # output_file = open("Benchmarks_SETTA.csv", "a")
        # output_file.write(",NA,NA,NA,NA,NA,NA\n")
        # output_file.close()
    return


if __name__ == '__main__':
    benchmarks(size=201, repetitions=3, start=30, steps=10)

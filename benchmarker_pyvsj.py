import os
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
from DataStructures.RA_SF_A import ra_to_xml
import xml.etree.cElementTree as ET


# from DataStructures.RA_SF_A import RegisterAutomata as RA
# from DataStructures.Sigma import Sigma
# from sympy import *
from DataStructures.RA_SF_A import RegisterAutomata
from Generator.generatorBK import GeneratingSystem as GS
from RAConverter import ra_to_xml
from RAGen.Generator import generate_stack as gen_det
from RAGen.NDGenerator import generate_stack as gen_ndet
from RAGen.RLGenerator import generate_stack as rl_gen_det
from RAGen.RLNDGenerator import generate_stack as rl_gen_ndet
from RAGen.CPTGenerator import generate as gen_cpt
from RAGen.FlowerGenerator import generate_flower as gen_flw
from RAGen.Combiner import combiner
from RAGen.CliqueGenerator import generate_clique as gen_cli

from Algorithms.forward_generator import forward as fwd_g
from Algorithms.forward_generator2 import forward as fwd_g2
from Algorithms.A_SF import is_bisim as nve
from Algorithms.forward_algorithm_2 import ra_bisim as fwd_m
from Algorithms.forward_algorithm_3 import ra_bisim as fwd_m2
from Algorithms.forward_exception import ra_bisim as fwd_e
from Algorithms.PR_Version_2 import is_bisimilar as pr
import xml.etree.cElementTree as ET

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
    start = time.process_time_ns()
    # print("S", start)
    u = method(representation, q1, p1, sigma, False)
    finish = time.process_time_ns()
    t = finish - start
    # print("START", start, "END", finish, "DIFF", t)
    tmp.append((u, t / (10 ** 6)))


def __single_time_test(RA: RegisterAutomata, q1: str, sigma, p1: str, method):
    TIMEOUT = 30
    manager = multiprocessing.Manager()
    tmp = manager.list()
    # print("tmp", tmp)
    p = multiprocessing.Process(target=method_wrapper, args=(tmp, method, RA, q1, p1, sigma))
    p.start()
    p.join(TIMEOUT)
    p.terminate()
    if len(tmp) == 0:
        tmp.append((None, TIMEOUT))
    u, t = tmp.pop(0)
    # print("FIN.", tmp, u, t.total_seconds())
    return t, u


def record(representation, q1, s, q2, repetitions,filename,method=fwd_g2):
    representation = representation.replace(" ", "")
    ra = RegisterAutomata(representation)
    q1 = q1.replace(" ", "")
    q2 = q2.replace(" ", "")
    results = set()
    times, res = [], []
    for _ in range(repetitions):
        time, result = __single_time_test(ra, q1, s, q2, method)
        if result is not None:
            times.append(time)
            res.append(result)
    try:
        assert len(set(res)) <= 1
    except AssertionError:
        print("TEST FAILED ON REPEAT.")
        print(file, method)
        print(representation)
        print(q1, s, q2)
        print(res)
        exit(-4)
    result = None
    time = 30000
    if len(set(res)) == 1:
        result = res.pop(0)
        time = sum(times) / len(times)
    line = "{:.16f}".format(time) + ","
    if result is not None:
        results.add(result)
    with open(filename, "a") as f:
        line = line[:-1] + "," + str(results)
        f.write(line)
    try:
        assert len(results) <= 1
    except AssertionError:
        print("TEST FAILED HERE.")
        print(file)
        print(representation)
        print(q1, s, q2)
        print(results)
        exit(-5)


def rabitjrunner(a1, a2, repetitions):
    f = open("./xml_1.xml", "w")
    f.write(ra_to_xml(a1))
    f.close()
    f = open("./xml_2.xml", "w")
    f.write(ra_to_xml(a2))
    f.close()
    times, results = [], []
    for _ in range(repetitions):
        try:
            x = str(subprocess.check_output(["java", "-jar", "./rabitj/rabit.jar", "./xml_1.xml", "./xml_2.xml", "(q0,{},q0)"], stderr=subprocess.STDOUT, timeout=60))
            x = x.replace("'", "").replace("b", "")
            x = x.split(" ")
            times.append(float(x[1][:-6]))
            results.append(x[0])
        except subprocess.TimeoutExpired:
            pass
    if len(times) == 0 and len(results) == 0:
        times.append(60 * 1000)
        results.append(None)
    time = sum(times) / len(times)
    assert len(set(results)) == 1
    return results[0], time


def test(size1, size2, file, gen1, gen2, code, repetitions):
    with open(file, "a") as f:
        f.write("{},{},{},".format(code, size1, size2))
    r1 = gen1(size1)
    q1 = r1.split("{")[2][:-1]
    r2 = gen2(size2)
    q2 = "p0"
    representation = combiner(r1, r2)
    record(representation, q1, set(), q2, repetitions, file)
    output_file = open(file, "a")
    result, time = rabitjrunner(representation, representation, repetitions)
    output_file.write(",{:.16f},{}\n".format(time, result))
    output_file.close()


def benchmarker(sizes, file, repetitions=3):
    with open(file, "w") as f:
        f.write("Code,size1,size2,python,pyres,java,javares\n")
    for size in sizes:
        test(size, size, file, gen_det, gen_det, "DET", repetitions)
    for size in sizes:
        test(size, size, file, gen_ndet, gen_ndet, "NDET", repetitions)


if __name__ == '__main__':
    sizes = list(range(2, 11, 1))
    sizes.extend(range(10, 201, 10))
    file = "./Benchmarks/Benchmarks_pyvsj.csv"
    benchmarker(range(90, 91, 1), file)
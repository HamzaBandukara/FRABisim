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
from RAGen.FlowerGenerator import generate as gen_flw
from RAGen.Combiner import combiner
from RAGen.CliqueGenerator import generate_clique as gen_cli

from Algorithms.forward_generator2 import forward as fwd_g2


# import matplotlib as plt
import sys

sys.setrecursionlimit(5000)


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
    results = set(res)
    result = None
    time = 30000
    if len(set(res)) == 1:
        result = res.pop(0)
        time = statistics.median(times)
    # line = "{:.16f}".format(time) + ","
    # if result is not None:
    #     results.add(result)
    # with open(filename, "a") as f:
    #     line = line[:-1] + "," + str(results.pop())
    #     f.write(line)
    try:
        assert len(results) <= 1
    except AssertionError:
        print("TEST FAILED HERE.")
        print(file)
        print(representation)
        print(q1, s, q2)
        print(results)
        exit(-5)
    result = None
    if len(results) > 0: result = results.pop()
    return result, time


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


def deq(a1, a2, repetitions=3):
    f = open("./xml_1.xml", "w")
    f.write(ra_to_xml(a1))
    f.close()
    f = open("./xml_2.xml", "w")
    f.write(ra_to_xml(a2))
    f.close()
    times, results = [], []
    for _ in range(repetitions):
        try:
            x = str(subprocess.check_output(["deq", "./xml_1.xml", "./xml_2.xml"], stderr=subprocess.STDOUT, timeout=60))
            x = x.replace(" ", "").replace("\n", "").replace("\'", "").split(",")
            times.append(float(x[3].replace("\\", "").replace("n", "").replace("r", "")))
            results.append(x[2])
        except subprocess.TimeoutExpired:
            pass
    if len(times) == 0 and len(results) == 0:
        times.append(60 * 1000)
        results.append(None)
    time = sum(times) / len(times)
    assert len(set(results)) == 1
    return results[0], time


def test(size1, size2, file, gen1, gen2, code, repetitions, triple, deqbool=False):
    with open(file, "a") as f:
        f.write("{},{},{},".format(code, size1, size2))
    r1 = gen1(size1)
    q1 = triple[0]
    r2 = gen2(size2)
    q2 = triple[2].replace("q", "p")
    representation = combiner(r1, r2)
    result, t1 = record(representation, q1, triple[1], q2, repetitions, file)
    output_file = open(file, "a")
    output_file.write("{:.16f},{}".format(t1, result))
    result, t2 = rabitjrunner(r1, r2, repetitions, triple)
    output_file.write(",{:.16f},{}".format(t2, result))
    if deqbool:
        result, t3 = deq(r1, r2, repetitions)
        output_file.write(",{:.16f},{}\n".format(float(t3), result))
    else:
        t3 = 60000
        output_file.write(",NA,NA\n")
    output_file.close()
    if t1 == 30000 and t2 == 30000 and t3 == 60000:
        return False
    return True


def benchmarker(sizes, file, repetitions=3):
    # Initialize File
    with open(file, "w") as f:
        f.write("Code,size1,size2,python,pyres,java,javares,DEQ,DEQres\n")

    # Tests the same state
    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_det, gen_det, "DET_SAME", repetitions, ("q0", set(), "q0"), True)
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("DET_SAME", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_ndet, gen_ndet, "NDET_SAME", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("NDET_SAME", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_cli, gen_cli, "CLI_SAME", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CLI_SAME", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_flw, gen_flw, "FLW_SAME", repetitions, ("q0", set(), "q0"), True)
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("FLW_SAME", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_cpt, gen_cpt, "CPT_SAME", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CPT_SAME", size, size))

    # Tests the different state
    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_det, gen_det, "DET_DIFFQ", repetitions, ("q0", set(), "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("DET_DIFFQ", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size , size, file, gen_ndet, gen_ndet, "NDET_DIFFQ", repetitions, ("q0", set(), "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("NDET_DIFFQ", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_cli, gen_cli, "CLI_DIFFQ", repetitions, ("q0", set(), "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CLI_DIFFQ", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_flw, gen_flw, "FLW_DIFFQ", repetitions, ("q0", set(), "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("FLW_DIFFQ", size, size))

    # Tests the different sizes
    result = True
    for size in sizes:
        if result:
            result = test(size, size+1, file, gen_det, gen_det, "DET_DIFFS", repetitions, ("q0", set(), "q0"), True)
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("DET_DIFFS", size, size+1))

    result = True
    for size in sizes:
        if result:
            result = test(size, size+1, file, gen_ndet, gen_ndet, "NDET_DIFFS", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("NDET_DIFFS", size, size+1))

    result = True
    for size in sizes:
        if result:
            result = test(size, size+1, file, gen_cli, gen_cli, "CLI_DIFFS", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CLI_DIFFS", size, size+1))

    result = True
    for size in sizes:
        if result:
            result = test(size, size+1, file, gen_flw, gen_flw, "FLW_DIFFS", repetitions, ("q0", set(), "q0"), True)
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("FLW_DIFFS", size, size+1))

    result = True
    for size in sizes:
        if result:
            result = test(size, size+1, file, gen_cpt, gen_cpt, "CPT_DIFFS", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CPT_DIFFS", size, size+1))

    # Tests from q1 instead of q0
    x = set()
    x.add(("1", "1"))
    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_det, gen_det, "DET_SKIP", repetitions, ("q1", x, "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("DET_SKIP", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_ndet, gen_ndet, "NDET_SKIP", repetitions, ("q1", x, "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("NDET_SKIP", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_cli, gen_cli, "CLI_SKIP", repetitions, ("q1", x, "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("CLI_SKIP", size, size))

    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_flw, gen_flw, "FLW_SKIP", repetitions, ("q1", x, "q1"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("FLW_SKIP", size, size))


    # Det vs NDet
    result = True
    for size in sizes:
        if result:
            result = test(size, size, file, gen_det, gen_ndet, "DET_NDET", repetitions, ("q0", set(), "q0"))
        else:
            with open(file, "a") as f:
                f.write("{},{},{},30000,None,30000,None,NA,NA".format("DET_NDET", size, size))


if __name__ == '__main__':
    sizes = list(range(2, 11, 1))
    sizes.extend(range(10, 201, 10))
    file = "./Benchmarks/Benchmarks_pyvsj.csv"
    benchmarker(sizes, file)
    # benchmarker(range(2, 3, 1), file)
# Dependencies
import multiprocessing
import os
import statistics
import subprocess
import sys
# from time import time
import time
from time import process_time_ns, thread_time_ns
import string

from DataStructures.RA_SF_A import RegisterAutomata
from RAGen.Combiner import combiner
from pi2fra.pyfra import RawProcess
from pibuilders import lexstrings

# Generators
from pibuilders import stack_builder as pi_stack
from pibuilders import queue_builder as pi_queue
from pibuilders import cpt_builder as pi_cpt
from pibuilders import piet_queue_builder as piet_queue
from pibuilders import gen
from pibuilders import piet_gen

# Tools
from pibisim import piet_bisim as piet
from pibisim import pi_bisim as fwd_pi


def single_time_test(m1, m2, s1, s2, isgen=False):
    sys.setrecursionlimit(5000000)
    alpha = string.ascii_uppercase
    generator = lexstrings(alphabet=alpha)
    if isgen:
        pi_1 = gen(s1, m1, "A")
        pi_2 = gen(s2, m2, "B")
    else:
        pi_1 = m1(s1)
        pi_2 = m2(s2)
    pi_1 = pi_1.split("\n")
    pi_2 = pi_2.split("\n")
    root_1, root_2 = pi_1[0].replace(" ","").split("=")[0], pi_2[0].replace(" ","").split("=")[0]
    f = open("../tmp.pi", "w")
    for line in pi_1:
        line = line.replace("\n", "")
        f.write(line + "\n")
    for line in pi_2:
        line = line.replace("\n", "")
        f.write(line + "\n")
    f.write(f"TEST {root_1} WITH {root_2}")
    f.close()
    rb_res, rb_time, _ = rabitjrunner_pi("../tmp.pi")
    print(rb_res, rb_time)
    return rb_time / 1000, rb_res

def rabitjrunner_pi(file):
    times, results = [], []
    try:
        x = str(subprocess.check_output(["java", "-jar", "./rabitj/rabit.jar", "-pi", file], stderr=subprocess.STDOUT, timeout=60))
        x = x.replace("'", "").replace("b", "")
        x = x.split(" ")
        print(x)
        times.append(float(x[1][:-4]))
        results.append(False) if x[0] == "false" else results.append(True)
    except subprocess.TimeoutExpired:
        pass
    if len(times) == 0 and len(results) == 0:
        times.append(60 * 1000)
        results.append(None)
    time = sum(times) / len(times)
    if time > 60000: time = 60000
    assert len(set(results)) <= 1
    try:
        st = statistics.pstdev(times)
    except:
        st = -1
    return results[0], time, st

# def single_time_test(gen_1, gen_2, size1, size2, isgen=False, tmp=None):
#     sys.setrecursionlimit(5000000)
#     alpha = string.ascii_uppercase
#     generator = lexstrings(alphabet=alpha)
#     if isgen:
#         process_1 = gen(size1, gen_1, "A")
#         process_2 = gen(size2, gen_2, "B")
#     else:
#         process_1 = gen_1(size1, generator, p="A")
#         process_2 = gen_2(size2, generator, p="B")
#     print("Entering ... ")
#     if tmp is None:
#         manager = multiprocessing.Manager()
#         print("List set up!")
#         tmp = manager.list()
#     else:
#         while len(tmp) > 0: tmp.pop()
#     print("Manager set up!")
#     p = multiprocessing.Process(target=method_wrapper, args=(tmp, [process_1, process_2]))
#     p.start()
#     p.join(30)
#     print("JOINED!")
#     if p.is_alive():
#         p.terminate()
#     try:
#         py_time, fwd_time, fwd_res, piet_lines = tmp
#         if fwd_res is None:
#             py_time, fwd_time = 15, 15
#     except:
#         py_time, fwd_time, fwd_res, piet_lines = 15, 15, None, piet_gen(gen_1, size1, gen_2, size2, tmp)
#     print(py_time, fwd_res, fwd_time)
#     print("TMP: ", *tmp)
#     while tmp.__len__() > 0: tmp.pop()
#     # manager = multiprocessing.Manager()
#     print("INIT QUEUE ...")
#     p = multiprocessing.Process(target=piet_wrapper, args=(tmp, piet_lines))
#     print("./PIET")
#     p.start()
#     p.join(30)
#     print("JOINED!")
#     if p.is_alive(): p.terminate()
#     print("TMP: ", *tmp)
#     try:
#         piet_res, piet_time = tmp[0], tmp[1]
#     except:
#         piet_res, piet_time = None, 30
#     print(piet_res, piet_time)
#     try:
#         if fwd_res is not None and piet_res is not None:
#             assert piet_res == fwd_res
#     except AssertionError:
#         print("EXPERIMENT FAILED AT ^\nRESULTS: ",piet_res, fwd_res)
#         print(process_1)
#         print(process_2)
#         exit(5)
#     print("PREE")
#     managerr = None
#     print("FINISHED")
#     return py_time, fwd_time, piet_time, fwd_res


def benchmark(size=2, repetitions=1, start=1, steps=1):
    tmp = multiprocessing.Manager().list()
    # if not os.path.exists("./Benchmarks"):
    #     os.mkdir("./Benchmarks")
    file = "../Benchmarks/pibench_extra2.csv"
    # output_file = open(file, "w")
    # output_file.write("P1Type,P1Size,P2Type,P2Size,RABiT,Result\n")
    # output_file.close()
    result=None
    timeout = 30

    # Test 01 - Stack vs Stack (Same Size)
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING SS: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_stack, pi_stack, i, i)
    #         times_py.append(results[0])
    #         result = results[1]
    #     py_time = sum(times_py) / len(times_py)
    #     with open(file, "a") as f:
    #         f.write(f"Stack,{i},Stack,{i},{py_time},{result}\n")

    # TEST 2 CPT
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING CC: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_cpt, i, i)
    #         times_py.append(results[0])
    #         result = results[1]
    #     py_time = sum(times_py) / len(times_py)
    #     with open(file, "a") as f:
    #         f.write(f"FLW,{i},FLW,{i},{py_time},{result}\n")

    # # TEST 3 Gen | Stack
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING GG: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_stack, pi_stack, i, i, True)
    #         times_py.append(results[0])
    #         result = results[1]
    #         # exit(10)
    #     py_time = sum(times_py) / len(times_py)
    #     with open(file, "a") as f:
    #         f.write(f"Gen|Stack,{i},Gen|Stack,{i},{py_time},{result}\n")
    #
    # # TEST 4 Gen | CPT
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING QQ: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_cpt, i, i, True)
    #         times_py.append(results[0])
    #         times_fwd.append(results[1])
    #         times_pi.append(results[2])
    #         result = results[3]
    #     py_time = sum(times_py) / len(times_py)
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     print(times_fwd, times_py)
    #     with open(file, "a") as f:
    #         f.write(f"Gen|CPT,{i},Gen|CPT,{i},{py_time},{fwd_time},{fwd_time + py_time},{pi_time},{result}\n")


    # # Test 01 - Stack n vs Stack n + 1
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING SS: ", i, i+1)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_stack, pi_stack, i, i + 1)
    #         times_py.append(results[0])
    #         result = results[1]
    #     py_time = sum(times_py) / len(times_py)
    #     with open(file, "a") as f:
    #         f.write(f"Stack,{i},Stack,{i+1},{py_time},{result}\n")
    #
    # # Test 02 - CPT n vs CPT n + 1
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING CC: ", i, i+1)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_cpt, i, i + 1)
    #         times_py.append(results[0])
    #         result = results[1]
    #     py_time = sum(times_py) / len(times_py)
    #     with open(file, "a") as f:
    #         f.write(f"FLW,{i},FLW,{i+1},{py_time},{result}\n")


    # TEST 3 Gen | Stack
    for i in range(start, size + 1, steps):
        times_py, times_fwd, times_pi = [], [], []
        print("TESTING GG: ", i, i+1)
        for _ in range(repetitions):
            results = single_time_test(pi_stack, pi_stack, i, i+1, True)
            times_py.append(results[0])
            result = results[1]
        py_time = sum(times_py) / len(times_py)
        with open(file, "a") as f:
            f.write(f"Gen|Stack,{i},Gen|Stack,{i+1},{py_time},{result}\n")

    # # TEST 4 Gen | CPT
    # for i in range(start, size + 1, steps):
    #     times_py, times_fwd, times_pi = [], [], []
    #     print("TESTING QQ: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_cpt, i, i+1, True)
    #         times_py.append(results[0])
    #         times_fwd.append(results[1])
    #         times_pi.append(results[2])
    #         result = results[3]
    #     py_time = sum(times_py) / len(times_py)
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     print(times_fwd, times_py)
    #     with open(file, "a") as f:
    #         f.write(f"Gen|CPT,{i},Gen|CPT,{i},{py_time},{fwd_time},{fwd_time + py_time},{pi_time},{result}\n")

    # TEST 2 CPT vs Stack
    # times_py, times_fwd, times_pi = [], [], []
    # for i in range(start, size + 1, steps):
    #     print("TESTING CC: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_stack, i, i)
    #         times_py.append(results[0])
    #         times_fwd.append(results[1])
    #         times_pi.append(results[2])
    #         result = results[3]
    #     py_time = sum(times_py) / len(times_py)
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     with open(file, "a") as f:
    #         f.write(f"C,{i},S,{i},{py_time},{fwd_time},{fwd_time + py_time},{pi_time},{result}\n")

    # # Queues Vs Queues
    # times_py, times_fwd, times_pi = [], [], []
    # for i in range(start, size + 1, steps):
    #     print("TESTING QQ: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_queue, pi_queue, i, i)
    #         times_py.append(results[0])
    #         times_fwd.append(results[1])
    #         times_pi.append(results[2])
    #         result = results[3]
    #     py_time = sum(times_py) / len(times_py)
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     with open(file, "a") as f:
    #         f.write(f"Q,{i},Q,{i},{py_time},{fwd_time},{fwd_time + py_time},{pi_time},{result}\n")


    # output_file.close()


if __name__ == '__main__':
    sys.setrecursionlimit(500000)
    benchmark(size=13,start=1,steps=1,repetitions=3)
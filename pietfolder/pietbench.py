# Dependencies
import os
import sys
# from time import time
import time
import string
from Benchmarks_2.pibuilders import lexstrings

# Generators
from Benchmarks_2.pibuilders import stack_builder as pi_stack

# Tools
from Benchmarks_2.pibisim import piet_bisim as piet
from Benchmarks_2.pibisim import pi_bisim as fwd_pi

def single_time_test(gen_1, gen_2, size1, size2):
    if not isinstance(gen_1, str):
        alpha = string.ascii_uppercase
        generator = lexstrings(alphabet=alpha)
        process_1 = gen_1(generator, size=size1).split("\n")[:-1]
        process_2 = gen_2(generator, size=size2).split("\n")[:-1]
    else:
        process_1 = gen_1.split("\n")
        process_2 = gen_2.split("\n")
    process = ""
    for i in range(len(process_1)):
        process += process_1[i] + "\n"
    for i in range(len(process_2)):
        process += process_2[i] + "\n"
    process = process[:-1]
    p1 = process_1[0].split(" ")[0]
    p2 = process_2[0].split(" ")[0]
    start = time.process_time()
    piet_lines, fwd_res = fwd_pi(process, p1, p2)
    fwd_time = time.process_time() - start
    piet_res, piet_time = piet(piet_lines)
    try:
        assert piet_res
    except AssertionError:
        print("EXPERIMENT FAILED AT ^\nRESULTS: ",piet_res, fwd_res)
        exit(5)
    return fwd_time, piet_time, fwd_res


def benchmark(size=2, repetitions=1, start=1, steps=1):
    if not os.path.exists("./Benchmarks"):
        os.mkdir("./Benchmarks")
    file = "./Benchmarks/pibench.csv"
    output_file = open(file, "w")
    output_file.write("P1Type,P1Size,P2Type,P2Size,fwd_pi,piet,Result\n")
    output_file.close()
    timeout = 30

    # Test 01 - Stack vs Stack (Same Size)
    times_fwd, times_pi = [], []
    for i in range(start, size + 1, steps):
        print("TESTING SS: ", i, i)
        for _ in range(repetitions):
            results = single_time_test(pi_stack, pi_stack, i, i)
            times_fwd.append(results[0])
            times_pi.append(results[1])
            result = results[2]
        fwd_time = sum(times_fwd) / len(times_fwd)
        pi_time = sum(times_pi) / len(times_pi)
        with open(file, "a") as f:
            f.write(f"S,{i},S,{i},{fwd_time},{pi_time},{result}\n")

    # Test 02 - Book Examples
    # times_fwd, times_pi = [], []
    # for file_name in os.listdir("./pibisim_examples"):
    #     if file_name[-1] == "2": continue
    #     print(file_name)
    #     print(f"TESTING : {file_name[:-1]}")
    #     with open(f"./pibisim_examples/{file_name}", "r") as f:
    #         lines = f.read()
    #     with open(f"./pibisim_examples/{file_name[:-1]}2", "r") as f:
    #         lines2 = f.read()
    #     for _ in range(repetitions):
    #         results = single_time_test(lines, lines2, None, None)
    #         times_fwd.append(results[0])
    #         times_pi.append(results[1])
    #         result = results[2]
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     with open(file, "a") as f:
    #         f.write(f"E,{file_name},E,{file_name},{fwd_time},{pi_time},{result}\n")

    # # Queues Vs Queues
    # times_fwd, times_pi = [], []
    # for i in range(start, size + 1, steps):
    #     print("TESTING QQ: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_queue, pi_queue, i, i)
    #         times_fwd.append(results[0])
    #         times_pi.append(results[1])
    #         result = results[2]
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     with open(file, "a") as f:
    #         f.write(f"Q,{i},Q,{i},{fwd_time},{pi_time},{result}\n")

    # times_fwd, times_pi = [], []
    # for i in range(start, size + 1, steps):
    #     print("TESTING CC: ", i, i)
    #     for _ in range(repetitions):
    #         results = single_time_test(pi_cpt, pi_cpt, i, i)
    #         times_fwd.append(results[0])
    #         times_pi.append(results[1])
    #         result = results[2]
    #     fwd_time = sum(times_fwd) / len(times_fwd)
    #     pi_time = sum(times_pi) / len(times_pi)
    #     with open(file, "a") as f:
    #         f.write(f"C,{i},C,{i},{fwd_time},{pi_time},{result}\n")

    output_file.close()


if __name__ == '__main__':
    sys.setrecursionlimit(500000)
    benchmark(size=20,start=1,steps=1,repetitions=1)
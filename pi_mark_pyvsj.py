# Dependencies
import os
import statistics
import subprocess
import sys
# from time import time
import time
from time import process_time_ns, thread_time_ns
import string
from pibuilders import lexstrings

# Generators
from pibuilders import stack_builder as pi_stack
from pibuilders import queue_builder as pi_queue
from pibuilders import cpt_builder as pi_cpt

# Tools
from pibisim import piet_bisim as piet
from pibisim import pi_bisim as fwd_pi

def to_piet(file):
    with open(file, "r") as f:
        lines = f.readlines()
    text = ""
    for i in range(len(lines)-1):
        line = lines[i]
        line = "AGENT " + line.replace("=", ":=").replace("\n", ";\n")
        # if i == 0:
        #     line = line.replace(".", "").replace("$", "^")
        if "$" in line:
            line = line.replace("$", "^").replace(".", " ", 1)
        text += line
    text = text + lines[-1].replace(" WITH", "\nWITH") + ";;"
    return text


def single_time_test(file):
    piet_lines = to_piet(file)
    piet_res, piet_time = piet(piet_lines, type="wee")
    print(piet_res, piet_time)
    rb_res, rb_time, _ = rabitjrunner_pi(file)
    print(rb_res, rb_time)
    try:
        results = {rb_res, piet_res}
        results.discard(None)
        assert len(results) <= 1
    except AssertionError:
        print("FAILED AT: ", file, rb_res, piet_res)
        exit(5)
    exit(10)
    return rb_time, piet_time, rb_res

def rabitjrunner_pi(file):
    times, results = [], []
    try:
        x = str(subprocess.check_output(["java", "-jar", "./rabitj/rabit.jar", "-piw", file], stderr=subprocess.STDOUT, timeout=60))
        x = x.replace("'", "").replace("b", "")
        x = x.split(" ")
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


def benchmark(repetitions=1):
    if not os.path.exists("./Benchmarks"):
        os.mkdir("./Benchmarks")
    file = "./Benchmarks/pibench_w.csv"
    # output_file = open(file, "w")
    # output_file.write("Type,Size,RABiT,PiET,Result\n")
    # output_file.close()
    timeout = 30

    # Test 01 - Stack vs Stack (Same Size)
    files = list(os.listdir("./examples/PI_TAU_ST"))
    files.sort(key=lambda x: int(x.replace("_", "")))
    print(files)
    for f1 in files:
        times_pi, times_rb = [], []
        print("TESTING STACK: ", f1)
        result = None
        for _ in range(repetitions):
            results = single_time_test("./examples/PI_TAU_ST/" + f1)
            times_pi.append(results[1])
            times_rb.append(results[0])
            result = results[2]
        pi_time = sum(times_pi) / len(times_pi)
        rb_time = sum(times_rb) / len(times_rb)
        print("RB: ", rb_time, times_rb)
        print("PI: ", pi_time, times_pi)
        with open(file, "a") as f:
            f.write(f"TST,{f1.replace('_', '')},{rb_time},{pi_time},{result}\n")

    # Test 01 - Stack vs Stack (Same Size)
    files = list(os.listdir("./examples/PI_TAU_CPT"))
    files.sort(key=lambda x: int(x.replace("_", "")))
    print(files)
    for f1 in files:
        times_pi, times_rb = [], []
        print("TESTING CPT: ", f1)
        result = None
        for _ in range(repetitions):
            results = single_time_test("./examples/PI_TAU_CPT/" + f1)
            times_pi.append(results[1])
            times_rb.append(results[0])
            result = results[2]
        pi_time = sum(times_pi) / len(times_pi)
        rb_time = sum(times_rb) / len(times_rb)
        print("RB: ", rb_time, times_rb)
        print("PI: ", pi_time, times_pi)
        with open(file, "a") as f:
            f.write(f"TCPT,{f1.replace('_', '')},{rb_time},{pi_time},{result}\n")


if __name__ == '__main__':
    sys.setrecursionlimit(500000)
    benchmark(3)

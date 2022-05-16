import os
from datetime import datetime
from Tester.graph_converter import convert
from Algorithms.A_SF import ra_bisim as RB, ra_bisim_id as RB_ID, ra_bisim_ext as RB_EXT, ra_bisim_tr as RB_TR
from RAStack.Generator import generate_stack
import matplotlib.pyplot as plt
from DataStructures.Sigma import Sigma


def time_test(f="times"):
    open("./outputs/{}".format(f), "w").close()

    times = {}
    for i in range(1, 10):
        Sigma.ALL_SIGMA = {}
        RA = generate_stack(i)
        u, then = single_time_test(RB, RA)
        for config in u:
            print(("{}\t"*len(config)).format(*config))
        print("{}:\t{}".format(i, then))
        times[i] = then.total_seconds()
        with open("./outputs/{}".format(f), "a") as f:
            f.write("{},{}\n".format(i, then.total_seconds()))

    convert("./outputs/{}".format(f))


def single_time_test(m, RA):
    Sigma.ALL_SIGMA = {}
    now = datetime.now()
    u = m(RA)
    then = datetime.now() - now
    return u, then


def rule_time_test():
    row = ("{:^20} |" * 5)[:-2]
    files = ["NORMAL", "ID", "EXT", "TR"]
    files = ["stack_test_{}".format(f) for f in files]
    print(row.format("SIZE", "REGULAR", "ID", "EXT", "TR"))
    for f in files:
        open("./outputs/{}".format(f), "w").close()
    for i in range(1, 8):
        RA = generate_stack(i)
        u_norm, t_norm = single_time_test(RB, RA)
        u_id, t_id = single_time_test(RB_ID, RA)
        u_ext, t_ext = single_time_test(RB_EXT, RA)
        u_tr, t_tr = single_time_test(RB_TR, RA)
        if not (set(u_norm) ==  set(u_id) == set(u_ext) == set(u_tr)):
            print("BAD RESULT STACK SIZE {}".format(i))
            print("CASE NORMAL:")
            for config in u_norm:
                print(("{}\t" * len(config)).format(*config))
            print()
            print("CASE ID:")
            for config in u_id:
                print(("{}\t" * len(config)).format(*config))
            print()
            print("CASE EXT:")
            for config in u_ext:
                print(("{}\t" * len(config)).format(*config))
            print()
            print("CASE TR:")
            for config in u_tr:
                print(("{}\t" * len(config)).format(*config))
            print()
            exit(-2)
        res = (t_norm, t_id, t_ext, t_tr)
        print(row.format(i, str(res[0]), str(res[1]), str(res[2]), str(res[3])))
        for j in range(len(files)):
            with open("./outputs/{}".format(files[j]), "a") as f:
                f.write("{},{}\n".format(i, res[j]))


rule_time_test()

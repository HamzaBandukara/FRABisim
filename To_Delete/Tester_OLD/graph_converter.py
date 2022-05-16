import matplotlib.pyplot as plt
from math import log


def convert(file):
    times = []
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line.split(",")
            times.append(float(line[1]))

    # for i in range(len(times)):
    #     try:
    #         times[i] = log(times[i])
    #     except ValueError:
    #         pass

    times = {str(i + 1): times[i] for i in range(len(times))}

    plt.plot(list(times.keys()), list(times.values()))
    plt.plot(list(times.keys()), list(times.values()), 'ro')
    # plt.scatter(list(times.keys()), list(times.values))
    plt.xlabel("Number of Registers")
    plt.ylabel("Time Taken (s)")
    plt.title("Bisimulation Stack Time Test")
    # plt.plot(list(times.keys()), list(times.values()))
    plt.show()

# convert()
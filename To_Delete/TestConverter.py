import os

table = {}
root = "./Benchmarks"

csv = open("../Benchmarks.csv", "w")
csv.write(",Forward,ForwardException,Naive,\n")
for dir_name in os.listdir(root):
    line = "{},{},{},{}"
    for subdir in os.listdir("./{}/{}".format(root, dir_name)):
        if subdir not in table:
            table[subdir] = {}
        current = table[subdir]
        for file in os.listdir("./{}/{}/{}".format(root, dir_name, subdir)):
            print(file)
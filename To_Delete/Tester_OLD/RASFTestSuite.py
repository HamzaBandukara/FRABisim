import os
from datetime import datetime
from Algorithms.A_SF import ra_bisim as rb, bisim_test

# passed = 0
# total = 0
# for f in os.listdir("../TestCasesRA"):
#     total += 1
#     file = open("../TestCasesRA/{}".format(f), "r")
#     ra = file.readline().replace("\n", "")
#     file.close()
#     res = bisim_test(ra)
#     if res:
#         passed += 1
#     txt = "Case {}: {}".format(f, "Passed" if res else "Failed")
#     print(txt)
# print("\nCases Passed: {}/{}".format(passed, total))

times = {}
for f in os.listdir("../../A-SF-RA-Cases"):
    file = open("../A-SF-RA-Cases/{}".format(f), "r")
    ra = file.readline().replace("\n", "")
    file.close()
    now = datetime.now()
    u = rb(ra)
    then = datetime.now() - now
    result = open("./sf_a_output/{}".format(f), "w")
    result.write("{}: {}\n".format(f, then))
    for config in u:
        result.write("{}, {}, {}\n".format(*config))
    result.close()
    times[f] = then
    print("{:18}{}".format(f, then))

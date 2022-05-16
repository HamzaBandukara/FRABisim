import os
from To_Delete.LICS15RA import bisim_test

passed = 0
total = 0
for f in os.listdir("../TestCasesRA"):
    total += 1
    file = open("../TestCasesRA/{}".format(f), "r")
    ra = file.readline().replace("\n", "")
    file.close()
    res = bisim_test(ra)
    if res:
        passed += 1
    txt = "Case {}: {}".format(f, "Passed" if res else "Failed")
    print(txt)
print("\nCases Passed: {}/{}".format(passed, total))
# times = {}
# for f in os.listdir("../TestCasesRA"):
#     file = open("../TestCasesRA/{}".format(f), "r")
#     ra = file.readline().replace("\n", "")
#     file.close()
#     now = datetime.now()
#     u = ra_bisim(ra)
#     then = datetime.now() - now
#     result = open("./output/{}".format(f), "w")
#     result.write("{}: {}".format(f, then))
#     for config in u:
#         result.write("{}, {}, {}, {}, {}\n".format(config[0], config[1], config[2], config[3], config[4]))
#     result.close()
#     times[f] = then
#     print("{}: {}".format(f, then))

# s = "{0,1,2}{(0,a)(1,#)}{(0,0,k,1)(1,0,k,0)}{0}{}"
# s = "{0,1,2}{(0,a)(1,#)}{(0,0,k,1)(1,0,k,0)(1,0,k,2)(2,0,k,1)}{0}{}"
# s = "{0,1,2}{(0,a)(1,#)}{(0,0,k,1)(1,0,k,0)(1,0,k,2)(2,0,k,1)}{0}{}"
# # s = "{0,1}{(0,a)(1,#)}{(0,0,l,1)(1,0,l,0)}{0}{}"
#
# u = ra_bisim(s)
# print("Bisimilar Universe:")
# for config in u:
#     print("\t{}, {}, {}, {}, {}".format(config[0], config[1], config[2], config[3], config[4]))

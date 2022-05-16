import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import subprocess
from random import choice
from datetime import datetime as dt
#
# with open ("piet_input", "r") as f:
#     lines = f.readlines()
#
# for i in range(len(lines)):
#     line = lines[i]
#     line = line.replace("\n", "")
#     line = "AGENT " + line + ";\n"
#     lines[i] = line
#
# with open("piet_input", "w", newline="\n") as f:
#     f.writelines(lines)

# p1 = subprocess.Popen('./PiET/piet', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# print(p1.stdout.readlines())
# out, err = p1.communicate(b"")
# print(out)
# print(err)

# df = pd.read_csv("./paper_times/stacks_1.csv")
# # print(df)
# df = df.drop(["TestCode", "States", "Transitions", "Result", "DEQ-Result"], axis=1)
# df = df.iloc[:, 1:]
# g = sns.lineplot(data=df, palette=["Yellow", "Purple", "Black", "Red", "Brown", "Blue", "Green"])
# g.xaxis.set_major_locator(ticker.MultipleLocator(1))
# g.xaxis.set_major_formatter(ticker.ScalarFormatter())
# g.set_xticklabels(range(0, 15))
# g.set_xlabel("Stack Size", fontsize = 10)
# g.set_ylabel("Time (ms)", fontsize = 10)
# plt.savefig("./paper_times/stacks_1.png")
# plt.show()
#
#
#
# df = pd.read_csv("./paper_times/stacks_2.csv")
# # print(df)
# df.reset_index(drop=True, inplace=True)
# df = df.drop(["TestCode", "States", "Transitions", "Result", "DEQ-Result", "RA"], axis=1)
# print(df)
# g = sns.lineplot(data=df,palette=["Purple", "Red","Blue", "Green"])
# #
# g.xaxis.set_major_locator(ticker.MultipleLocator(1))
# g.xaxis.set_major_formatter(ticker.ScalarFormatter())
# g.set_xticklabels(range(0, 1001, 100))
# g.set_xlabel("Stack Size", fontsize = 10)
# g.set_ylabel("Time (ms)", fontsize = 10)
# plt.savefig("./paper_times/stacks_2.png")
# plt.show()
#
# df = pd.read_csv("./paper_times/ndet_stacks.csv")
# # print(df)
# df.reset_index(drop=True, inplace=True)
# df = df.drop(["TestCode", "States", "Transitions", "Result", "RA"], axis=1)
# print(df)
# g = sns.lineplot(data=df,palette=["Red","Blue", "Green"])
# g.xaxis.set_major_locator(ticker.MultipleLocator(1))
# g.xaxis.set_major_formatter(ticker.ScalarFormatter())
# g.set_xticklabels(range(0, 1001, 100))
# g.set_xlabel("Stack Size", fontsize = 10)
# g.set_ylabel("Time (ms)", fontsize = 10)
# plt.savefig("./paper_times/ndet_stacks.png")
# plt.show()
#
# df = pd.read_csv("./paper_times/stacks_non.csv")
# # print(df)
# df.reset_index(drop=True, inplace=True)
# df = df.drop(["TestCode", "States", "Transitions", "Result", "RA"], axis=1)
# print(df)
# g = sns.lineplot(data=df,palette=["Red","Blue", "Green"])
# g.xaxis.set_major_locator(ticker.MultipleLocator(1))
# g.xaxis.set_major_formatter(ticker.ScalarFormatter())
# g.set_xticklabels(range(0, 1001, 100))
# g.set_xlabel("Stack Size", fontsize = 10)
# g.set_ylabel("Time (ms)", fontsize = 10)
# plt.savefig("./paper_times/stacks_non.png")
# plt.show()
#
def convert_row(row):
    return int(row["RA"].split("_")[-1])

def to_graph(t_df, test_code, lois):
    sns.set_theme()
    df = pd.concat([t_df], ignore_index =True)
    for index, row in df.iterrows():
        if row["TestCode"] not in test_code:
            df.drop(index=index, inplace=True, axis=0)
    df["RA"] = [x.split("_")[-2] for x in df["RA"]]
    print(df)
    df=df.drop(labels=["TestCode", "States", "Transitions", "Result", "DEQ-Result", "LOIS FW Result", "LOIS PR Result"], axis=1)
    if lois:
        df["LOIS PR"].fillna(30000, inplace=True)
        df["LOIS FW"].fillna(30000, inplace=True)
    df['Generator'] = np.log10(df['Generator'])
    df['DEQ'] = np.log10(df['DEQ'])
    df['Base'] = np.log10(df['Base'])
    # df['Exception'] = np.log10(df['Exception'])
    if lois:
        df['LOIS FW'] = np.log10(df['LOIS FW'])
        df['LOIS PR'] = np.log10(df['LOIS PR'])
    # df[df < 0] = 0
    # print(df)
    d = {x: x for x in df}
    d["Generator"] = "Gen"
    df = df.rename(columns=d)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        if lois:
            df = pd.melt(df, id_vars=['Size'], value_vars=['Gen', "Base", "DEQ", "LOIS FW", "LOIS PR"])
        else:
            df = pd.melt(df, id_vars=['Size', "RA"], value_vars=['Gen', "Base"])
            df["variable"] = df["RA"] + ", " + df["variable"]
    d = {k: k for k in df}
    d["variable"] = "Tool"
    df = df.rename(columns=d)
    g = sns.lineplot(data=df,x="Size",y="value", hue="Tool",marker="o",style="Tool")
    g.set_xlabel("Size", fontsize = 10)
    g.set_ylabel("Time (ms)", fontsize = 10)
    g.xaxis.set_major_locator(ticker.MultipleLocator(20))
    print([y for y in g.get_yticks()])
    plt.ylim(-1, 5)
    plt.xlim(-10, 210)
    g.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ylabels = ['{}'.format(int(10 ** x)) for x in g.get_yticks() if x%1 == 0]
    ylabels = []
    for x in g.get_yticks():
        if x % 1 == 0:
            ylabels.append("{}".format(int(10**x)))
        else:
            ylabels.append(" ")
    ylabels[-3] = "30000"
    ylabels[0] = " "
    ylabels[1] = " "
    g.set_yticklabels(ylabels)
    handles, labels = g.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t))
    g.legend(handles=handles, labels=labels)
    plt.subplots_adjust(right=0.99, left=0.15, top=0.95)
    plt.legend(loc='lower right')
    plt.savefig(f"./ATVA/{test_code}.eps", format='eps')
    plt.show()

df1 = pd.read_csv("./Benchmarks/Benchmarks_small03052022.csv")
# pd.set_option('display.precision', 4)
df2 = pd.read_csv("./Benchmarks/Benchmarks_03052022.csv")
df2 = df2.drop(labels=["Memo"], axis=1)
d1 = {k: k for k in df1}
d2 = {k: k for k in df2}
d1["DEQ-Time"] = "DEQ"
d2["DEQ-Time"] = "DEQ"
d2["Gen2"] = "Generator"
d1["LOIS PR Time"] = "LOIS PR"
d1["LOIS FW Time"] = "LOIS FW"
df1 = df1.rename(columns=d1)
df2 = df2.rename(columns=d2)
frames = [df1, df2]
df3 = pd.concat(frames)
df3["Size"] = df3.apply(lambda row: convert_row(row), axis=1)
df3 = df3.sort_values(["TestCode", "Size"])
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df3)
# print([x for x in df1])
# df1 = df1.drop(axis=1,labels=["States", "Transitions", "DEQ-Result", "LOIS FW Result", "LOIS PR Result", "Exception"])
# print([x for x in df1])
# df1 = df1.Base.apply(lambda x: round(x, 4 - int(np.floor(np.log10(abs(x))))) if x != 0 else 0)
# print(df1.to_latex())
# df2 = df2.drop(axis=1, labels=["States", "Transitions", "DEQ-Result", "Exception"])
# print([x for x in df2])
# print(df2.to_latex())
to_graph(df3, ["Test_01_B"], True)
# to_graph(df3, ["Test_01_G", "Test_01_D"], False)
# to_graph(df3, ["Test_01_F", "Test_02_H"], False)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import subprocess
from random import choice
from datetime import datetime as dt


def convert_row(row):
    return int(row["RA"].split("_")[-1])

def to_graph2(t_df, test_code=None):
    sns.set_theme()
    df = pd.concat([t_df], ignore_index =True)
    # for index, row in df.iterrows():
    #     if row["Result"] != test_code:
    #         df.drop(index=index, inplace=True, axis=0)
    # df=df.drop(labels=["P1Type"], axis=1)
    # df[df < 0] = 0
    d = {k: k for k in df}
    d["RABiT"] = "Gen"
    d["piet"] = "PiET"
    d["P1Size"] = "Size"
    df = df.rename(columns=d)
    for _ in 'Gen', 'PiET':
        df[_] = np.log10(df[_])
        df.loc[df[_] < -1.75, _] = -1.75
    print(df)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     df = pd.melt(df, id_vars=['Size', "P1Type"], value_vars=["Gen", "PiET"])
    #     df["type"] = df["P1Type"] + ", " + df["variable"]
        # print(df)
    g = sns.lineplot(data=df,x="Size",y="Gen", hue="Result",marker="o",style="Result")
    # plt.ylim(0, 5)
    g.set_xlabel("Size", fontsize = 10)
    g.set_ylabel("Time (s)", fontsize = 10)
    # print(np.log10(-3), np.log10(1.5))
    plt.ylim(-2, 2)
    plt.xlim(0, 21)
    g.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    print([y for y in g.get_yticks()], 10 ** 2)
    # g.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # ylabels = ['{}'.format(10 ** x) for x in g.get_yticks()]
    ylabels = []
    counter = 0
    for x in g.get_yticks():
        if not (counter - 1) % 4: ylabels.append("{}".format(10 ** x))
        else: ylabels.append(" ")
        counter += 1
    ylabels[-3] = 60
    ylabels[1] = ""
    ylabels[2] = 0
    # ylabels = ['$10^{{{}}}$'.format(x) for x in g.get_yticks()]
    # ylabels = ['$10^({})'.format(float(10 ** x)) for x in g.get_yticks()]
    g.set_yticklabels(ylabels)
    g.xaxis.set_major_locator(ticker.MultipleLocator(2))
    handles, labels = g.get_legend_handles_labels()
    g.legend(handles=handles, labels=labels)
    plt.subplots_adjust(right=0.99, left=0.15, top=0.95)
    plt.savefig(f"./SETTA/{test_code}.eps", format='eps')
    plt.show()



def to_graph(t_df, test_code):
    sns.set_theme()
    df = pd.concat([t_df], ignore_index =True)
    for index, row in df.iterrows():
        if row["Result"] != test_code:
            df.drop(index=index, inplace=True, axis=0)
    # df=df.drop(labels=["P1Type"], axis=1)
    # df[df < 0] = 0
    d = {k: k for k in df}
    d["RABiT"] = "Gen"
    d["piet"] = "PiET"
    d["P1Size"] = "Size"
    df = df.rename(columns=d)
    for _ in 'Gen', 'PiET':
        df[_] = np.log10(df[_])
        df.loc[df[_] < -1.75, _] = -1.75
    # df['Gen'] = np.log10(df['Gen'])
    # df['PiET'] = np.log10(df['PiET'])


    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        df = pd.melt(df, id_vars=['Size', "P1Type"], value_vars=["Gen", "PiET"])
        df["type"] = df["P1Type"] + ", " + df["variable"]
        # print(df)
    g = sns.lineplot(data=df,x="Size",y="value", hue="type",marker="o",style="type")
    # plt.ylim(0, 5)
    g.set_xlabel("Size", fontsize = 10)
    g.set_ylabel("Time (s)", fontsize = 10)
    # print(np.log10(-3), np.log10(1.5))
    plt.ylim(-2, 2)
    plt.xlim(4, 51)
    g.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    print([y for y in g.get_yticks()], 10 ** 2)
    # g.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ylabels = ['{}'.format(10 ** x) for x in g.get_yticks()]
    ylabels = []
    counter = 0
    for x in g.get_yticks():
        if not (counter - 1) % 4: ylabels.append("{}".format(10 ** x))
        else: ylabels.append(" ")
        counter += 1
    # ylabels[-3] = 60
    ylabels[-4] = 30
    ylabels[1] = ""
    ylabels[2] = 0
    # ylabels = ['$10^{{{}}}$'.format(x) for x in g.get_yticks()]
    # ylabels = ['$10^({})'.format(float(10 ** x)) for x in g.get_yticks()]
    g.set_yticklabels(ylabels)
    g.xaxis.set_major_locator(ticker.MultipleLocator(5))
    handles, labels = g.get_legend_handles_labels()
    g.legend(handles=handles, labels=labels)
    plt.subplots_adjust(right=0.99, left=0.15)
    plt.savefig(f"./SETTA/{test_code}.eps", format='eps')
    plt.show()


df1 = pd.read_csv("./Benchmarks/pibench3JAVA.csv")
pd.set_option('display.precision', 4)
# df1 = df1.drop(labels=["pyfra", "fwd", "P2Type"], axis=1)
df1 = df1.drop(labels=["P2Type", "P2Size"], axis=1)
# d = {k: k for k in df1}
# d["P1Type"] = "Type"
# d["P1Size"] = "Size 1"
# d["P2Size"] = "Size 2"
# df1 = df1.rename(columns=d)
# print(df1.to_latex())
# to_graph(df1, True)
# to_graph(df1, False)
to_graph2(df1)

# df1 = pd.read_csv("./Benchmarks/Benchmarks_small03052022.csv")
# pd.set_option('display.precision', 4)
# df2 = pd.read_csv("./Benchmarks/Benchmarks_03052022.csv")
# df2 = df2.drop(labels=["Memo"], axis=1)
# d1 = {k: k for k in df1}
# d2 = {k: k for k in df2}
# d1["DEQ-Time"] = "DEQ"
# d2["DEQ-Time"] = "DEQ"
# d2["Memo2"] = "Memo"
# d2["Gen2"] = "Generator"
# d1["LOIS PR Time"] = "LOIS PR"
# d1["LOIS FW Time"] = "LOIS FW"
# df1 = df1.rename(columns=d1)
# df2 = df2.rename(columns=d2)
# frames =  [df1, df2]
# df3 = pd.concat(frames)
# df3["Size"] = df3.apply(lambda row: convert_row(row), axis=1)
# df3 = df3.sort_values(["TestCode", "Size"])
# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# #     print(df3)
#
# to_graph(df3, "Test_01_B", True)
# to_graph(df3, "Test_01_F", False)

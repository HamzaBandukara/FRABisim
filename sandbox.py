import os

from RAGen.Generator import generate_stack as st
from RAGen.RLGenerator import generate_stack as ts
from RAGen.NDGenerator import generate_stack as lst
from RAGen.CPTGenerator import generate as flw
from RAGen.CliqueGenerator import generate_clique as cli
from RAGen.FlowerGenerator import generate_flower as cpt

from pibuilders import stack_builder as pist, cpt_builder as picpt


a, b = [st, ts, lst, flw, cli, cpt, pist, picpt], \
       ["ST", "TS", "LST", "CPT", "CLI", "FLW", "PI_ST", "PI_CPT"]
for i in range(8):
    os.mkdir(f"./examples/{b[i]}")
    for size in range(1, 20):
        with open(f"./examples/{b[i]}/_{size}", "w") as f:
            f.write(a[i](size))
    if i < 5:
        for size in range(21, 201):
            with open(f"./examples/{b[i]}/_{size}", "w") as f:
                f.write(a[i](size))
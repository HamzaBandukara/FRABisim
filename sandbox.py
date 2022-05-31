from RAStack.Generator import generate_stack as st
from RAStack.NDGenerator import generate_stack as lst
from RAStack.CPTGenerator import generate as flw
from RAStack.CliqueGenerator import generate_clique as cli
from RAStack.FlowerGenerator import generate_flower as cpt

from pibuilders import stack_builder as pist, cpt_builder as picpt


a, b = [st, lst, cpt, cli, flw, pist, picpt], \
       ["ST", "LST", "CPT", "CLI", "FLW", "PI_ST", "PI_CPT"]
for i in range(7):
    for size in range(2, 20):
        with open(f"./examples/{b[i]}_{size}", "w") as f:
            f.write(a[i](size))

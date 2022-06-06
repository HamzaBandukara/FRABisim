import re
import time

from Algorithms.forward_algorithm_3 import ra_bisim as fwd
from Algorithms.forward_exception import ra_bisim as fwd_ex
from Algorithms.forward_generator2 import ra_bisim as fwd_gen
from pibisim import pi_bisim as fwd_pi
from RAStack.Combiner import combiner
from DataStructures.RA_SF_A import RegisterAutomata
import sys
import sympy

def alter_states(fra):
    states, initial, registers, transitions, finals = re.findall("{(.*?)}", fra)
    i = 0
    s_map = {}
    for s in states.split(","):
        s_map[s] = f"q{i}"
        i += 1
    states = list(s_map.values())
    states = str(states)[1:-1].replace(" ", "")
    initial = s_map[initial]
    r_new = ""
    for r in re.findall("\((.*?)\)", registers):
        r = list(r.split(","))
        r[0] = s_map[r[0]]
        if len(r) > 1:
            r_new += str(tuple(r))
        else:
            r_new += str(tuple(r)).replace(",", "")
    t_new = ""
    for t in re.findall("\((.*?)\)", transitions):
        t = list(t.split(","))
        t[0] = s_map[t[0]]
        t[-1] = s_map[t[-1]]
        t_new += str(tuple(t))
    finals = ""
    if len(finals) > 0:
        finals = list([s_map[x] for x in finals.split(",")])
        finals = str(finals)[1:-1].replace(" ", "")
    x= "{" + states + "}{" + initial + "}{" + r_new + "}{" + t_new + "}{" + finals + "}"
    x = x.replace("'", "")
    return x


def set_up_fra(fra1, fra2):
    fra1 = alter_states(fra1)
    fra2 = alter_states(fra2)
    fra = RegisterAutomata(combiner(fra1, fra2))
    sigma = set()
    for r in fra.s_map["q0"]:
        if r in fra.s_map["p0"]:
            sigma.add((r, r))
    return fra, "q0", "p0", sigma

if __name__ == '__main__':
    args = sys.argv
    alg = fwd_gen
    if "-g" in args:
        args.remove("-g")
    elif "-f" in args:
        args.remove("-f")
        alg = fwd
    elif "-e" in args:
        args.remove("-e")
        alg = fwd_ex
    elif "-p" in args:
        args.remove("-p")
        alg = fwd_pi
    else:
        msg = """Usage: python runit.py <TYPE>> f1 f2
Where:  f1 = file containing first FRA / Pi-Calculus Process
        f2 = file containing second FRA / Pi-Calclus Process
        <TYPE> = algorithm type, where:
        -f = on-the=fly 
        -g = on-the-fly generator
        -e = on-the-fly exception
        -p = pi-calculus processes (experimental)
        
Structure for FRAs:
{<States>}{<initial state>}{<available registers>}{<Transition function>}{<final states>}

Structure for Pi-Calculus Processes:
root    : line+ EOF  ;
line    : process NEWLINE | process | definition NEWLINE | definition ;
definition: PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')' '=' process  ;
process :   '(' process ')' | process PAR process | process SUM process | zero | write | read | nu | eq | neq | defined;
zero    : '0'  ;
write   : CHANNEL '<' CHANNEL '>.' process ;
read  : CHANNEL '(' CHANNEL ').' process;
nu      : '$' CHANNEL '.' process ;
eq      : '[' CHANNEL '=' CHANNEL ']' process ;
neq     : '[' CHANNEL '#' CHANNEL ']' process ;
defined     : PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')';
CHANNEL     : [a-z]+ ;
PROCESSNAME : ([A-Z] | [0-9])+ ;
PAR         : '|'  ;
SUM         : '+'  ;
        """
        print(msg)
        sys.exit(0)
    entities = []
    for file in args[1], args[2]:
        with open(file, "r") as f:
            entities.append(f.readline().replace("\n", ""))
    if alg == fwd_pi:
        args = entities[0], entities[1]
        ret = alg(*args)
        t, result = ret[0] + ret[1], ret[2]
    else:
        args = set_up_fra(entities[0], entities[1])
        t = time.process_time_ns()
        result = alg(*args)
        t = (time.process_time_ns() - t) / (10 ** 9)
    print("Result:", result)
    print(f"Time: {t} seconds")


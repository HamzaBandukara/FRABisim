from pi2fra.pyfra import *
from pi2fra.parser.antler import main as parse
from Algorithms.forward_generator import forward as fwd

# # UNIT TESTS ##
test=5
size=3
if test == 1:
    # print("TEST 1: Stack of size", size)
    a=Name();b=Name();c=Name()
    p = RawProcess("inp",(a,b,RawProcess("var",("P",[b]))))
    p = RawProcess("sum",(RawProcess("sum",(RawProcess("zero"),p)),RawProcess("inp",(a,b,RawProcess("inp",(b,c,RawProcess("zero")))))))
    RawProcess.addDefinition("P",[a],p)

    q = Process({0},{a:0},p)
    # print("\nBuilding LTS for",q)

    P = [None for _ in range(size)]
    V = ["P"+str(i) for i in range(size)]
    n = [Name() for _ in range(size)]
    for i in range(size):
        if i==0:
            P[i]=RawProcess("inp",(n[0],n[1],RawProcess("var",(V[1],[n[0],n[1]]))))
        elif i==size-1:
            P[i]=RawProcess("out",(n[0],n[size-1],RawProcess("var",(V[size-2],n[:size-1]))))
            for j in range(i):
                P[i]=RawProcess("neq",(n[i],n[j],P[i]))
        else:
            push = RawProcess("inp",(n[0],n[i+1],RawProcess("var",(V[i+1],n[:i+2]))))
            pop = RawProcess("out",(n[0],n[i],RawProcess("var",(V[i-1],n[:i]))))
            for j in range(i):
                pop=RawProcess("neq",(n[i],n[j],pop))
                push=RawProcess("neq",(n[i],n[j],push))
            P[i] = RawProcess("sum",(push,pop))
        RawProcess.addDefinition(V[i],n[:i+1],P[i])
        proc = Process({0}, {n[0]: 0}, RawProcess("var", (V[0], [n[0]])))
elif test == 2:
    proc = parse("P(b,c)=$a.b<c>.b<a>.0")
elif test == 3:
    proc = parse("P(a)=$b.a<b>.P(b)")
elif test == 4:
    proc = parse("P(a,c)=(a(b).0)|(a<c>.0)")
elif test == 5:
    proc = parse("P(a,c)=(a(d).c<c>.0)|($b.a<b>.c<c>.0)")  # Close
elif test == 6:
    proc = parse("P(a,c)=(a(d).d<d>.0)|($b.a<b>.c<c>.0)")  # Close
elif test == 7:
    proc = parse("P(a,c)=(a(d).c<c>.0)|($b.a<b>.b<b>.0)")  # Close
elif test == 8:
    proc = parse("P(a)=(a(d).d<d>.0)|($b.a<b>.b<b>.0)")   # Comm
elif test == 9:
    proc = parse("P(a,b)=(a<b>.0) + (b<a>.0)")
elif test == 10:
    proc = parse("P(a)=a(b).P(b)")
elif test == 11:
    proc = parse("P(a,b)=a<b>.P(b,a)")
elif test == 12:
    proc = parse("P(b)=$a.[a#b]b<a>.0")
elif test == 13:
    proc = parse("P(b)=b(a).[a=b]b<a>.0")
elif test == 14:
    proc = parse("P(a,b)=(a<b>.0)|(b<a>.0)")
elif test == 15:
    proc = parse("P(b,c)=b<c>.b<b>.0")
else:
    raise Exception("Test not found")

# Printouts
print("Definitions")
for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)
for k,(ns,df) in RawProcess.vardefn.items(): print(df.to_piet())

# print("LTS")
# print(proc)
r, reg = proc.buildLTS()
proc.printLTS(lambda k,v : k in r)
i1, ra = Process.gen_FRA(lambda k,v : (k in r and v.size>0))
i2, ra = Process.gen_FRA(lambda k,v : (k in r and v.size>0), ra)
ra.r_map = reg
ra.registers = list(ra.r_map)
mapper = set()
for key in i1:
    if key in i2:
        mapper.add((i1[key], i2[key]))
print(fwd(ra, "s0", "q0", mapper))
# Process.printLTS(lambda k,v : (k in r and v.size>0))
x = TransitionSet()
for k in Process.lts:
    x.update(Process.lts[k])
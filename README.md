<h1>RABiT</h1>
</hr>
RABiT (Register Automata Bisimulation Tool) is a tool that can determine strong bisimulation equivalence of two register automata by incorporating on-the-fly techniques.
<h2>Directory Structure</h2>
The directory structure is as follows:

- A-SF-RA-Cases: Contains some small test examples that help test for correctness
- ATVA: Contains the generated graphs for the companion paper
- Algorithms: Contains all bisimulation algorithms (complete and experimental)
- Benchmarks: Contains csv files with benchmarking times
- DataStructures: Contains all custom built data structures for the tool
- Generator: Contains two versions of the generating system used
- LOIS: Contains the LOIS bisimulation tool used for benchmarking
- RAGen: Contains scripts that can generate automata of any size
- DEQ: Contains the code for the DEQ tool
- Examples: Contains RA examples to use with the tool
- pi2fra: Contains the prototype code for converting a Pi-Calculus process to FRA

<h2>Requirements</h2>

The following are needed in order to run RABiT:

- Python 3.9+
- SymPy (https://www.sympy.org/en/index.html)
- Antlr4 Version 4.3.9 (https://www.antlr.org/)

<h2>Usage</h2>
This section describes how to use the RABiT tool.

<h3>Tool Usage</h3>
In order to run the tool, enter the following from the command line from the project root directory:

`python rabit.py <TYPE> file1 file2 `

where file1, file2 are the paths to the two register automata / processes, and `<TYPE>` is the specific bisimulation type, with the following options:
  
- -f for on-the-fly standard
- -g for on-the-fly generator
- -e for on-the-fly exception
- -p for pi-calculus processes

For example, to test two stacks of size 5, 10 against each other using the on-the-fly generator algorithm, you can run from the root directory:
  
`python rabit.py -g examples/st/_5 examples/st/_10`

<h3>Fresh-Register Automata</h3>
The structure for fresh-register automata are as follows:
  
```
{<States>}{<initial state>}{<available registers>}{<Transition relation>}{<final states>}
```

where:

- states is the set of states of the automaton, including an initial state and a set of final states
- available registers is a map assigning the registers available at each state; each map entry should be of the form (<state>, <registers>)
- transition relation is the transition relation, where each transition is of the form (src, tag, register, type, tgt), where:
  - src and tgt are the source and target states
  - tag is a label from a finite set of tags
  - register is a register index (an integer)
  - type is one of K (known), L ( locally-fresh) or G (globally-fresh)
- final states is the set of states the automaton can terminate at.
  
For example, creating a stack of size 2 would look like this:
  
```
{q0,q1,q2}{q0}{(q0)(q1,1)(q2,1,2)}{(q0,push,1,L,q1)(q1,pop,1,K,q0)(q1,push,2,L,q2)(q2,pop,2,K,q1)}{}
```

Where:
  
- q0, q1 and q2 are states
- q0 is the initial state
- q0 has no available register, q1 has only the register 1 available and q2 has the registers 1 and 2 available to it
- The transitions available to the automaton are as follows:
  - (q0,push,1,L,q1) is a transition from q0, with the tag 'push' on register 1 which is a locally-fresh transition
  - (q1,pop,1,K,q0) is a transition from q1, with the tag 'pop' on register 1 which is a known transition
  - (q1,push,2,L,q2) is a transition from q0, with the tag 'push' on register 1 which is a locally-fresh transition
  - (q2,pop,2,K,q1) is a transition from q1, with the tag 'pop' on register 1 which is a known transition
- And there are no final states

At each push operation, the stack reads in a name that is not currently in its registers (hence the L type). Thus, the stack will always contain distinct names.
  
<h3>Pi-Calculus Processes</h3>
Pi-Calculus processes have a grammar defined as such for processes:
  
```
file    : (line '\n')*line EOF  ;
line    : process | definition ;
definition: PROCESSNAME '(' (CHAN ',')* CAHN ')' '=' process  ;
process :   '(' process ')' | process '|' process | process '+' process | zero | input | output | nu | eq | neq | proc;
zero    : '0'  ;
output   : CHAN '<' CHAN '>.' process ;
input  : CHAN '(' CHAN ').' process;
nu      : '$' CHAN '.' process ;
eq      : '[' CHAN '=' CHAN ']' process ;
neq     : '[' CHAN '#' CHAN ']' process ;
proc     : PROCNAME '(' (CHAN ',')* CHAN ')';
CHAN     : [a-z]+ ;
PROCNAME : ([A-Z] | [0-9])+ ;
```

For example, a process could be:
`A(a) = a(b).A(b)`
for a process that receives some name on channel 'a', binds it to 'b' and then repeats using the name 'b'.

With processes, the first line will be the process that is tested.
For example, if file 1 is:

```
A(b) = a(b).B(a)
B(a) = a<a>.A(a)
```
  
and file 2 is:
  
```
C(a) = $b.a<b>.D(a)
D(a) = $c.a<c>.C(c)
```
  
The tool will test whether C(a) and A(b) are bisimilar. 
  
RABiT can check bisimilarity for finite control processes (i.e. no parallel composition within recursive definitions) and assumes that processes follow a Barendregt convention on bound names (each bound name is distinct from free and other bound names).

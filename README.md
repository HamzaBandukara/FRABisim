# FRABisim

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
- RAStack: Contains scripts that can generate automata of any size
- DEQ: Contains the code for the DEQ tool
- Examples: Contains RA examples to use with the tool
- pi2fra: Contains the prototype code for converting a Pi-Calculus process to FRA

<h2>Requirements</h2>:

- Python 3.9+
- SymPy (https://www.sympy.org/en/index.html)
- Antlr4 Version 4.3.9 (https://www.antlr.org/)

<h2>Usage</h2>
This section describes how to use the RABiT tool.

<h3>Tool Usage</h3>
In order to run the tool, enter the following from the command line from the project root directory:

`python runit.py <TYPE> file1 file2 `

where file1, file2 are the paths to the  <TYPE> is the specific bisimulation type, with the following options:
  
- -f for on-the-fly standard
- -g for on-the-fly generator
- -e for on-the-fly exception
- -p for pi-calculus processes

For example, to test two stacks of size 5, 10 against each other using the on-the-fly generator algorithm, you can run from the root directory:
  
`python runit.py -g examples/st5 examples/st10`

<h3>Fresh-Register Automata</h3>
The structure for fresh-register automata are as follows:
  
'{<States>}{<initial state>}{<available registers>}{<Transition function>}{<final states>}'

<h3>Pi-Calculus Processes</h3>
Pi-Calculus processes have a grammar defined as such for processes:
  
```
root    : line+ EOF  ;
line    : process NEWLINE | process | definition NEWLINE | definition ;
definition: PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')' '=' process  ;
process :   '(' process ')' | process PAR process | process SUM process | zero | input | output | nu | eq | neq | proc;
zero    : '0'  ;
output   : CHANNEL '<' CHANNEL '>.' process ;
input  : CHANNEL '(' CHANNEL ').' process;
nu      : '$' CHANNEL '.' process ;
eq      : '[' CHANNEL '=' CHANNEL ']' process ;
neq     : '[' CHANNEL '#' CHANNEL ']' process ;
proc     : PROCESSNAME '(' (CHANNEL ',')* CHANNEL ')';
CHANNEL     : [a-z]+ ;
PROCESSNAME : ([A-Z] | [0-9])+ ;
```

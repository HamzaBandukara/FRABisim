from GameApproach.agent import Agent

from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma

from RAStack.Generator import generate_stack
from RAStack.CPTGenerator import generate


s = generate(3)
RA = RegisterAutomata(s)
sigma = Sigma(set())

attacker = Agent(RA, "q0", True)
defender = Agent(RA, "q0", False)

previous_states = set()
while True:
    state = attacker.get_state(), sigma, defender.get_state()
    if state in previous_states:
        print("Previous State Repeated ({}, {}, {}), Defender Wins!".format(*state))
        break
    previous_states.add(state)
    a_moves = list(attacker.all_possible_moves())
    if len(a_moves) == 0:
        print("Attacker has no moves remaining. Defender Wins!")
        break
    print("Turn: Attacker. Current State:", attacker.get_state())
    print("Attacker's Moves: ")
    for i in range(len(a_moves)):
        print("{}. - {}{} -> {}".format(i + 1, *a_moves[i][0], a_moves[i][1]))
    choice = int(input("Choose a move: ")) - 1
    a_move = a_moves[choice]
    print("Attacker Moves: {} - {}{} -> {}".format(attacker.get_state(), *a_move[0], a_move[1]))
    attacker.accept_transition(a_move[1])
    d_moves = list(defender.matching_moves(sigma, a_move[0]))
    if len(d_moves) == 0:
        print("Defender has no moves remaining. Attacker Wins!")
        break
    print("Turn: Defender. Current State:", defender.get_state())
    print("Defender's Moves: ")
    for i in range(len(d_moves)):
        print("{}. - {}{} -> {}".format(i + 1, *d_moves[i][0], d_moves[i][1]))
    choice = int(input("Choose a move: ")) - 1
    d_move = d_moves[choice]
    print("Defender Moves: {} - {}{} -> {}".format(defender.get_state(), *d_move[0], d_move[1]))
    defender.accept_transition(d_move[1])
    sigma = sigma.generate_temp_sigma(a_move[0][0], d_move[0][0])
    sigma = sigma.harpoon(attacker.get_state(), defender.get_state(), RA)

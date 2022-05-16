from DataStructures.RA_SF_A import RegisterAutomata
from DataStructures.Sigma import Sigma


class Agent:
    def __init__(self, RA: RegisterAutomata, start_state: str, attacker: bool):
        self.RA = RA
        self.state = start_state
        self.is_attacker = attacker

    def all_possible_moves(self) -> set:
        moves = set()
        actions = self.RA.get_transitions(self.state)
        for action in actions:
            targets = self.RA.get_next_transitions(self.state, action)
            for state in targets:
                moves.add((action, state))
        return moves

    # Add that case in: L -> Matches K
    def matching_moves(self, sigma: Sigma, action: tuple) -> set:
        moves = set()
        register, label = action
        if label == "K" and register in sigma:
            r = sigma[register]
            targets = self.RA.get_next_transitions(self.state, (r, "K"))
            for state in targets:
                moves.add((action, state))
        else:
            actions = self.RA.get_transitions(self.state)
            for action in actions:
                if action[1] == "L":
                    targets = self.RA.get_next_transitions(self.state, action)
                    for state in targets:
                        moves.add((action, state))
        return moves

    def accept_transition(self, state):
        self.state = state

    def get_state(self):
        return self.state

    # Run 1: Defender Wins
    # Attacker: q1 -> 1L -> q2
    # Defender: q1 -> 2L -> q2

    # Run 2: Attacker Wins
    # Attacker: q1 -> 1K -> q2
    # Defender: Cannot match

    # Training so that it can always find a way to win (can have a winning strategy)

# Here you will receive the parameters from input.py and
# create the graph structure accordingly
# then you will use the graph structure to simulate the NFA
# the user should have some way to enter the symbol after each move

#Example of initializing the NFA with parameters received from input.py
from NFA import NFA
class NFASimulation:
    def __init__(self, alphabet: list[str], numStates: int,
                 startStates: list[int], finalStates: list[int],
                 transitions: dict[tuple[int, str], list[int]]):
        self.nfa = NFA(alphabet, numStates, startStates, finalStates, transitions)
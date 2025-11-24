class NFA:
    def __init__(self, alphabet: list[str], numStates: int,
                 startStates: list[int], finalStates: list[int],
                 transitions: dict[tuple[int, str], list[int]]):

        self.alphabet = alphabet
        self.numStates = numStates
        self.startStates = startStates
        self.finalStates = finalStates
        self.transitions = transitions
        self.currentStates = set(startStates)

        # Initialize with lambda-closure(start states)
        self.reset()

    # λ-closure (using '#' instead of λ)
    def lambdaClosure(self, states: set[int]) -> set[int]:
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            key = (state, '#')

            if key in self.transitions:
                for nextState in self.transitions[key]:
                    if nextState not in closure:
                        closure.add(nextState)
                        stack.append(nextState)

        return closure

    def reset(self):
        # Start states + lambda closure
        self.currentStates = self.lambdaClosure(set(self.startStates))

    def move(self, symbol: str):
        nextStates = set()

        for state in self.currentStates:
            key = (state, symbol)
            if key in self.transitions:
                for nxt in self.transitions[key]:
                    nextStates.add(nxt)

        # After moving with actual symbol, apply lambda closure again
        self.currentStates = self.lambdaClosure(nextStates)

    def isAccepted(self):
        return any(state in self.finalStates for state in self.currentStates)
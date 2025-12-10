import simulationData as sd
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
        self.reset()
        self.simulationData = sd.SimulationData()

    # check all current states and assign their lambda closures and record them (DFS approach)
    def lambdaClosure(self, states, currentStep=0):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            key = (state, '#')
            if key in self.transitions:
                for nxt in self.transitions[key]:
                    if nxt not in closure:
                        prev_closure = closure.copy()
                        closure.add(nxt)
                        # Check acceptance for the current closure
                        is_accepted = any(s in self.finalStates for s in closure)
                        self.simulationData.recordLambdaMove(prev_closure, closure.copy(), is_accepted, currentStep)
                        stack.append(nxt)
        return closure

    

    def reset(self):
        # Start states + lambda closure
        # Initial step is 0
        self.currentStates = self.lambdaClosure(set(self.startStates), 0)

    def move(self, symbol: str, currentStep=0):
        nextStates = set()

        for state in self.currentStates:
            key = (state, symbol)
            if key in self.transitions:
                for nxt in self.transitions[key]:
                    nextStates.add(nxt)
        
        # Record the move with the symbol
        # Note: We record before lambda closure of the next states
        self.simulationData.recordMove(symbol, set(self.currentStates), nextStates.copy(), self.isAccepted(), currentStep)

        # After moving with actual symbol, apply lambda closure again
        self.currentStates = self.lambdaClosure(nextStates, currentStep)

    def isAccepted(self):
        return any(state in self.finalStates for state in self.currentStates)
    
    def getCurrentStates(self) -> set[int]:
        return self.currentStates
    
    # # This is the main function it will receive the input string and process it
    def processString(self, inputString):
       step = 0
         # Record initial state
       self.simulationData.recordMove(None, set(), self.currentStates.copy(), self.isAccepted(), step)
       for symbol in inputString:
              step += 1
              self.move(symbol, step)
       return self.simulationData
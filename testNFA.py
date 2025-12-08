# just a testing for the NFA class

# initialize an NFA

import NFA as nfa

class TestNFA:

    pass

    def test_nfa_initialization(self):
        alphabet = ['a', 'b', '#']
        numStates = 3
        startStates = [0]
        finalStates = [2]
        transitions = {
              (0, 'a'): [0, 1],
              (1, 'b'): [2],
              (0, '#'): [2]
                }

        automaton = nfa.NFA(alphabet, numStates, startStates, finalStates, transitions)

        assert automaton.alphabet == alphabet
        assert automaton.numStates == numStates
        assert automaton.startStates == startStates
        assert automaton.finalStates == finalStates
        assert automaton.transitions == transitions
        assert automaton.getCurrentStates() == {0, 2}  # lambda closure from start state

    def test_nfa_move_and_acceptance(self):
        alphabet = ['a', 'b', '#']
        numStates = 3
        startStates = [0]
        finalStates = [2]
        transitions = {
            (0, 'a'): [0, 1],
            (1, 'b'): [2],
            (0, '#'): [2]
        }

        automaton = nfa.NFA(alphabet, numStates, startStates, finalStates, transitions)

        # Initial state should be {0, 2} due to lambda closure
        assert automaton.getCurrentStates() == {0, 2}
        assert automaton.isAccepted() == True  # State 2 is accepting

        # Move with 'a'
        automaton.move('a')
        assert automaton.getCurrentStates() == {0, 1, 2}  # From state 0 with 'a' goes to 0 and 1; state 2 remains
        assert automaton.isAccepted() == True  # State 2 is still accepting

        # Move with 'b'
        automaton.move('b')
        assert automaton.getCurrentStates() == {2}  # From state 1 with 'b' goes to 2; state 0 has no transition with 'b'
        assert automaton.isAccepted() == True  # State 2 is accepting

def test_nfa_with_string(input_string, expected_states, expected_acceptance):
    alphabet = ['a', 'b', '#']
    numStates = 3
    startStates = [0]
    finalStates = [2]
    transitions = {
        (0, 'a'): [0, 1],
        (1, 'b'): [2],
        (0, '#'): [2]
    }
    input_string = input_string

    automaton = nfa.NFA(alphabet, numStates, startStates, finalStates, transitions)
    automaton.processString(input_string)

    assert automaton.getCurrentStates() == expected_states
    assert automaton.isAccepted() == expected_acceptance


def run_tests():
    test_instance = TestNFA()
    test_complex_simulation()

def test_complex_simulation():
    alphabet = ['a', 'b', '#']
    numStates = 3
    startStates = [0]
    finalStates = [2]
    transitions = {
        (0, 'a'): [0, 1],
        (1, 'b'): [2],
        (0, '#'): [2],
        (1, '#'): [0],
        (2, '#'): [1]
    }
    automaton = nfa.NFA(alphabet, numStates, startStates, finalStates, transitions)
    simulation = automaton.processString("abababa")
    
    expected_results = [
        {0: {"symbol": None, "fromStates": set(), "toStates": {0, 1, 2}, "isAccepted": True}},
        {1: {"symbol": 'a', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {2: {"symbol": 'b', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {3: {"symbol": 'a', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {4: {"symbol": 'b', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {5: {"symbol": 'a', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {6: {"symbol": 'b', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}},
        {7: {"symbol": 'a', "fromStates": {0, 1, 2}, "toStates": {0, 1, 2}, "isAccepted": True}}
    ]
    
    actual_results = simulation.getResults()
    
    print("Expected output:")
    for result in expected_results:
        print(result)
    print("\nActual output:")
    for result in actual_results:
        print(result)
    
    assert actual_results == expected_results, f"Expected {expected_results}, but got {actual_results}"

if __name__ == "__main__":
    run_tests()
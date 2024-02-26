import re

class AFD:
    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions

    def run(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if not self.alphabet.match(symbol):
                return False
            
            next_state = None
            for transition, state in self.transitions.items():
                if transition[0] == current_state and re.match(transition[1], symbol):
                    next_state = state
                    break
            
            if next_state is None:
                return False
            
            current_state = next_state
        
        return current_state in self.accepting_states


# Compile the regular expression for the alphabet
alphabet = re.compile(r'[\w\s.]')

# Define transitions using strings instead of regular expression objects
transitions = { ('q0', r'\d'): 'q1',
                ('q0', r'\w'): 'q2',
                ('q0', r'[^a-zA-Z0-9_]'): 'q5',
                ('q1', r'[^a-zA-Z0-9_]'): 'q3',
                ('q2', r'\w'): 'q2',
                ('q2', r'[^a-zA-Z0-9_]'): 'q4'}

# Example usage:
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
initial_state = 'q0'
accepting_states = {'q3', 'q4', 'q5'}

afd = AFD(states, alphabet, initial_state, accepting_states, transitions)

input_string = 'hola_123.'
print(afd.run(input_string))  # Output: True

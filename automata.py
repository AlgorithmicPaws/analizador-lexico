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
        row, column = 1, 1
        for symbol in input_string:

            if symbol == '\n':
                row += 1
                column = 1
            elif not re.match(r'\s', symbol):
                column += 1
            
            
            if not self.alphabet.match(symbol):
                print('Lexical error at row:', row, 'column:', column)
                return False
            
            next_state = None
            for transition, state in self.transitions.items():
                if transition[0] == current_state and re.match(transition[1], symbol):
                    print(state)
                    next_state = state
                    break
            
            if next_state is None:
                print('Lexical a error at row:', row, 'column:', column)
                return False
            
            current_state = next_state
        
        return current_state in self.accepting_states

esp_characters = ['/','%','@','<','>','&','|','^','~',':','=','!','(',')','[',']','{','}',';',':','.','-','+','*']
regex_esp_characters =  '|'.join(re.escape(esp_character) for esp_character in esp_characters)

# Compile the regular expression for the alphabet
alphabet = re.compile(r'[\w\s]' + f'|[{regex_esp_characters}]')

# Define transitions using strings instead of regular expression objects
transitions = { ('q0', r'\d'): 'q1',    
                ('q0', r'\w'): 'q2',
                ('q0', r'[^a-zA-Z0-9_]|\s'): 'q5',
                ('q1', r'[^a-zA-Z0-9_]|\s'): 'q3',
                ('q2', r'\w'): 'q2',
                ('q2', r'[^a-zA-Z0-9_]|\s'): 'q4',
                ('q5', r'[^a-zA-Z0-9_]'): 'q5'
                }


states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
initial_state = 'q0'
accepting_states = {'q3', 'q4', 'q5'}

afd = AFD(states, alphabet, initial_state, accepting_states, transitions)

input_string = "ab."

print(afd.run(input_string))

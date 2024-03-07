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
        print(current_state)
        row, column = 1, 0
        expression = ''
        print(input_string)

        for index, symbol in enumerate(input_string):
            print(index)

            print('simbol'+symbol)
            if symbol == '\n':
                row += 1
                column = 1
            else:
                column += 1
            if not self.alphabet.match(symbol):
                print('Lexical error at row:', row, 'column:', column)
                return False

            next_state = None
            for transition, state in self.transitions.items():
                if transition[0] == current_state and re.match(transition[1], symbol):
                    print(state)

                    if not re.match(r'\s', symbol):
                        expression += symbol

                    if len(expression) == 1:
                        expression_start_row = row
                        expression_start_column = column
                    next_state = state

                    break
            if next_state is None:
                print('Lexical a error at row:', row, 'column:', column)
                return False
            
            current_state = next_state
            if index == len(input_string) - 1:
                self.tokenizer(expression, expression_start_row, expression_start_column)

            elif current_state in self.accepting_states:
                self.tokenizer(expression, expression_start_row, expression_start_column)
                expression = ''
                current_state = self.initial_state
        print(current_state)
        return current_state in self.accepting_states
        
    
    def tokenizer(self, expression, start_row, start_column):
        # Implement your tokenizer logic here
        print('Tokenizing:', expression, 'starting at row:', start_row, 'column:', start_column)

def create_regex_from_list(characters):
    regex = '|'.join(re.escape(character) for character in characters)
    return regex
    
esp_characters_list = ['/','%','@','<','>','&','|','^','~',':','=','!','(',')','[',']','{','}',';',':','.','-','+','*']
unique_characters_list = ['(',')','[',']','{','}',';','.','~']
initial_compouse_character_list = ['%','@','&','|','^',':','=','!',':','-','+','*']
regex_esp_characters =  create_regex_from_list(esp_characters_list)

alphabet = re.compile(r'[\w\s]|[' + regex_esp_characters + ']')
unique_character = re.compile(r'[' + create_regex_from_list(unique_characters_list) + ']')
initial_compouse_character = re.compile(r'' + create_regex_from_list(initial_compouse_character_list))

transitions = {('q0', r'\d'): 'q1',    
              ('q0', r'[a-zA-Z]'): 'q2',
              ('q0', initial_compouse_character): 'q5',
              ('q0', '>'): 'q6',
              ('q0', '<'): 'q7',
              ('q0', '*'): 'q8',
              ('q0', '-'): 'q9',
              ('q0', '/'): 'q10',
              ('q0', unique_character): 'q14',
              ('q1', r'\d'): 'q1', 
              ('q1', r'[^\w\s]|\s'): 'q3',
              ('q2', r'\w'): 'q2',
              ('q2', r'[^\w\s]|\s'): 'q4',
              ('q5', '='): 'q11',
              ('q5', r'[^\w\s]|\s'): 'q18',
              ('q6', '>'): 'q12',
              ('q6', '='): 'q11',
              ('q7', '<'): 'q12',
              ('q7', '='): 'q11',
              ('q8', '*'): 'q12',
              ('q8', '='): 'q11',
              ('q9', '>'): 'q13',
              ('q9', '='): 'q11',
              ('q10', '/'): 'q12',
              ('q10', '='): 'q11',
              ('q11', r'[^\w\s]|\s'): 'q15',
              ('q12', '='): 'q11',
              ('q12', r'[^\w\s]|\s'): 'q16',
              ('q14', r'[^\w\s]|\s'): 'q17',
              }



states = {'q0','q1','q2','q3','q4','q5','q6', 'q7', 'q8', 'q9', 'q10', 'q11','q12', 'q13', 'q14','q15', 'q16','q17', 'q18'}
initial_state = 'q0'
accepting_states = {'q3', 'q4', 'q13','q15', 'q16', 'q17', 'q18'}
afd = AFD(states, alphabet, initial_state, accepting_states, transitions)

input_string = "mondongo_23 21 "

print(afd.run(input_string))

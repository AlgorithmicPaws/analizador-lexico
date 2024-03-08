import re

class AFD:
    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions

    def run(self, input_string):
        input_list = list(input_string)  # Transform input string into a list
        current_state = self.initial_state
        print(current_state)
        row, column = 1, 0
        expression = ''
        print(input_list)

        for index in range(len(input_list)):
            symbol = input_list[index]
            print(index)
            print('symbol: ' + symbol)
            if symbol == '\n':
                row += 1
                column = 1
            else:
                column += 1
            if not self.alphabet.match(symbol):
                print('Lexical error at row:', row, 'column:', column)
                return False

            next_state = None
            for transition in self.transitions:
                if transition[0] == current_state and re.match(transition[1], symbol):
                    state = transition[2]
                    print(state)

                    if not re.match(r'\s', symbol):
                        expression += symbol

                    if len(expression) == 1:
                        expression_start_row = row
                        expression_start_column = column
                    next_state = state

                    break
            if next_state is None:
                print('Lexical error at row:', row, 'column:', column)
                return False
            
            current_state = next_state
            if index == len(input_list) - 1:
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
unique_characters_list = ['(',')','[',']','{','}',';','~']
initial_compouse_character_list = ['%','@','&','|','^',':','=','!',':','-','+','*']
regex_esp_characters =  create_regex_from_list(esp_characters_list)

alphabet = re.compile(r'[\w\s]|[' + regex_esp_characters + ']')
unique_character = re.compile(r'[' + create_regex_from_list(unique_characters_list) + ']')
initial_compouse_character = re.compile(r'' + create_regex_from_list(initial_compouse_character_list))

#d digitos
#s espacios en blanco y tabs
#w letras y digitos y _
transitions = [
    ('q0', r'\d', 'q1'),    #
    ('q0', r'[a-zA-Z]', 'q2'),  #
    ('q0', '-', 'q4'), #
    ('q0', '\*', 'q5'),#
    ('q0', '\>', 'q6'),#
    ('q0', '\<', 'q7'),#
    ('q0', '\/', 'q8'),#
    ('q0', initial_compouse_character, 'q9'),#
    ('q0', unique_character, 'q10'),#
    ('q0', r'\n', 'q29'),#
    ('q0', '_', 'q28'),#
    ('q0', '\.', 'q29'),#
    ('q1', r'\d', 'q1'),#      
    ('q1', '\.', 'q13'),#
    ('q1', r'[^\d|.]', 'q11'),#
    ('q2', r'[a-zA-Z]', 'q2'),   #
    ('q2', r'[\d|_]', 'q3'),    #
    ('q2', r'[^\w]', 'q14'),
    ('q3', r'\w', 'q3'),    #
    ('q3', r'[^\w]', 'q15'), #
    ('q4', '\>', 'q16'),#
    ('q4', r'[^>]', 'q10'),#
    ('q5', '\*', 'q18'),#
    ('q5', '\=', 'q26'),#
    ('q5', r'[^=|*]', 'q10'),#
    ('q18', '\*', 'q19'),#
    ('q6', '\>', 'q20'),#
    ('q6', '\=', 'q26'),#
    ('q6', r'[^>|*]', 'q10'),#
    ('q7', '\<', 'q22'),#
    ('q7', '\=', 'q26'),#
    ('q7', r'[^<|*]', 'q10'),#
    ('q8', '\/', 'q24'),#
    ('q8', '\=', 'q26'),#
    ('q8', r'[^/|*]', 'q10'),#
    ('q9', '\=', 'q26'),#
    ('q9', r'[^=]', 'q28'),#
    ('q16', alphabet, 'q17'),
    ('q18', '\=', 'q26'),#
    ('q18', alphabet, 'q19'),
    ('q20', '\=', 'q26'),#
    ('q20', alphabet, 'q21'),
    ('q22', '\=', 'q26'),#
    ('q22', alphabet, 'q23'),
    ('q24', '\=', 'q26'),#
    ('q24', alphabet, 'q25'),
    ('q26', alphabet, 'q27'),
]

states = {'q0','q1','q2','q3','q4','q5','q6', 'q7','q8','q9','q10',
        'q11','q12','q13', 'q14','q15', 'q16','q17','q18','q19','q20',
        'q21','q22','q23','q24','q25','q26','q27','q28','q29'}
initial_state = 'q0'
accepting_states = {'q10','q11','q13','q14','q15','q17', 'q19', 'q21','q23','q25','q27','q28','q29'}
afd = AFD(states, alphabet, initial_state, accepting_states, transitions)

input_string = ">.// @. @="

print(afd.run(input_string))

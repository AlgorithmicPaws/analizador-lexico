import re

class AFD:
    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.row = 1
        self.column = 0
        self.token_list = []
        self.result = False

    def counter(self, symbol):
        if symbol == '\n':
            self.row += 1
            self.column = 1
        else:
            self.column += 1
        

    def run(self, input_list):
        
        current_state = self.initial_state
        print(current_state)
        expression = ''
        print(input_list)

        for index in range(len(input_list)):
            symbol = input_list[index]
            print('index'+ str(index))
            print('symbol: ' + symbol)

            if not self.alphabet.match(symbol):
                print('Lexical error at row:9', self.row, 'column:', self.column)
                return False

            
            self.counter(symbol)

            next_state = None
            for transition in self.transitions:
                if transition[0] == current_state and re.match(transition[1], symbol):
                    state = transition[2]
                    print('state' + state)

                    
                    expression += symbol

                    if len(expression) == 1:
                        expression_start_row = self.row
                        expression_start_column = self.column
                    next_state = state
                    break

            if next_state is None:
                print('Lexical error at row:8', self.row, 'column:', self.column)
                return False
            
            current_state = next_state

            if index == len(input_list) - 1:
                print('entre')
                expression = expression[:-1]
                self.tokenizer(expression, expression_start_row, expression_start_column,current_state)
                return True
            elif current_state in self.accepting_states:
                if len(expression) > 1: 
                    expression = expression[:-1]
                    self.tokenizer(expression, expression_start_row, expression_start_column, current_state)
                    self.column-= 1 
                    expression = ''
                    print('bb')
                    self.result = True
                    print('pene' + str(input_list[index:]))
                    return input_list[index:]
                    #input_list.insert(index + 1, symbol)
                else:
                    self.tokenizer(expression, expression_start_row, expression_start_column, current_state)
                    expression = ''
                    current_state = self.initial_state
                    print('a')
                    self.result = True
                    print('pene' + str(input_list[index:]))
                    return input_list[index:]

    
    def tokenizer(self, expression, start_row, start_column, finalState):
        # Implement your tokenizer logic here
        key_words= [ 
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',  
        'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 
        'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 
        'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf', 'erfc', 'exp', 
        'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 
        'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'ldexp', 
        'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'perm', 'pi', 'pow', 
        'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 
        'trunc', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 
        'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 
        'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 
        'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 
        'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 
        'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 
        'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 
        'sum', 'super', 'tuple', 'type', 'vars', 'zip', 'Ellipsis', 'NotImplemented' 
        'os', 'sys', 'math', 'random', 'datetime', 're', 'json', 'csv', 'pickle', 'time', 
        'collections', 'itertools', 'functools', 'operator', 'logging', 'pathlib', 'gzip', 'zipfile', 
        'io', 'shutil', 'platform', 'subprocess', 'threading', 'multiprocessing', 'socket', 'http', 'urllib', 
        'ftplib', 'ssl', 'email', 'smtplib', 'imaplib', 'poplib', 'xml', 'html', 'cgi', 'sqlite3', 
        'multiprocessing', 'concurrent', 'asyncio', 'unittest', 'doctest', 'pytest', 'argparse', 'getopt', 
        'configparser', 'logging', 'tkinter', 'pygame', 'pandas', 'numpy', 'matplotlib', 'scipy', 'seaborn', 
        'sklearn', 'tensorflow', 'pytorch', 'flask', 'django', 'sqlalchemy', '_'
        ] 

    
        symbols = {
         '+': 'tk_plus', '-': 'tk_minus', '*': 'tk_asterisk', '**': 'tk_double_asterisk',
        '/': 'tk_slash', '//': 'tk_double_slash', '%': 'tk_percent', '@': 'tk_at',
        '<<': 'tk_left_shift', '>>': 'tk_right_shift', '&': 'tk_ampersand', '|': 'tk_pipe',
        '^': 'tk_caret', '~': 'tk_tilde', ':=': 'tk_walrus',
        '<': 'tk_less_than', '>': 'tk_greater_than', '<=': 'tk_less_than_or_equal_to',
        '>=': 'tk_greater_than_or_equal_to', '==': 'tk_equal_to', '!=': 'tk_not_equal_to',
        '(': 'tk_left_parenthesis', ')': 'tk_right_parenthesis',
        '[': 'tk_left_square_bracket', ']': 'tk_right_square_bracket',
        '{': 'tk_left_curly_brace', '}': 'tk_right_curly_brace',
        ',': 'tk_comma', ':': 'tk_colon', '.': 'tk_dot', ';': 'tk_semicolon', '=': 'tk_equal',
        '->': 'tk_arrow', '+=': 'tk_plus_equal', '-=': 'tk_minus_equal', '*=': 'tk_multiply_equal',
        '/=': 'tk_divide_equal', '//=': 'tk_double_divide_equal', '%=': 'tk_modulus_equal',
        '@=': 'tk_at_equal', '&=': 'tk_and_equal', '|=': 'tk_or_equal', '^=': 'tk_xor_equal',
        '>>=': 'tk_right_shift_equal', '<<=': 'tk_left_shift_equal', '**=': 'tk_double_asterisk_equal',
        '!': 'tk_exclamation'
        }   

        if (finalState == 'q14' or finalState == 'q15'): #_ esta aca
            if (expression in key_words):
                self.token_list.append((expression, start_row, start_column))
            else: 
                tipo_token = "Id"
                self.token_list.append((tipo_token, expression, start_row, start_column))

        elif finalState == 'q15':
            tipo_token = "Id"
            self.token_list.append((tipo_token, expression, start_row, start_column))

        elif finalState in ['q19', 'q17', 'q21', 'q23', 'q25', 'q28', 'q29','q27','q10']:
            if expression in symbols:
                tipo_token = symbols[expression]
                self.token_list.append((tipo_token, expression, start_row, start_column))

        elif finalState == 'q13':
            tipo_token = "tk_float"
            self.token_list.append((tipo_token, expression, start_row, start_column))

        elif finalState == 'q11':
            tipo_token = "tk_integer"
            self.token_list.append((tipo_token, expression, start_row, start_column))

        else:
            return 

        #falta dejar los tokens en una tupla con formato: (tipo_de_token, lexema, fila, columna) o (tipo_de_token, fila, columna) 
        #falta enviar cada token a la funcion format_token de lexycal 
    def rerun(self, input_list):
        actual_input = self.run(input_list)
        while True:    
            if actual_input == True:
                break
            elif actual_input == False:
                break
            else:
                actual_input = self.run(actual_input)

def create_regex_from_list(characters):
    regex = '|'.join(re.escape(character) for character in characters)
    return regex
    
esp_characters_list = ['/','%','@','<','>','&','|','^','~',':','=','!','(',')','[',']','{','}',';',':','.','-','+','*']
unique_characters_list = ['(',')','[',']','{','}',';','~']
initial_compouse_character_list = ['%','@','&','|','^',':','=','!',':','-','+','*']
regex_esp_characters =  create_regex_from_list(esp_characters_list)

alphabet = re.compile(r'[\w\s]|[' + regex_esp_characters + ']')
unique_character = re.compile(r'[' + create_regex_from_list(unique_characters_list) + ']')
initial_compouse_character = re.compile(r'[' + create_regex_from_list(initial_compouse_character_list) + ']')

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
    ('q0', r'[\n\s]', 'q29'),#
    ('q0', '_', 'q28'),#
    ('q0', '\.', 'q29'),#
    ('q1', r'\d', 'q1'),#      
    ('q1', '\.', 'q12'),#
    ('q1', r'[^\d|.]', 'q11'),#
    ('q2', r'[a-zA-Z]', 'q2'),   #
    ('q2', r'[\d|_]', 'q3'),    #
    ('q2', r'[^\w]', 'q14'),
    ('q3', r'\w', 'q3'),    #
    ('q3', r'[^\w]', 'q15'), #
    ('q4', '\>', 'q16'),#
    ('q4', '\=', 'q26'),#
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
    ('q12', r'\d', 'q12'),#
    ('q12', r'[^\d]', 'q13'),#
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
    ('q29', r'\s', 'q29'),
    ('q29', alphabet, 'q30'),

]
#falta definición de un número complejo numero_complejo = a + b * 1j, ej: 0.02 + 3j 

states = {'q0','q1','q2','q3','q4','q5','q6', 'q7','q8','q9','q10',
        'q11','q12','q13', 'q14','q15', 'q16','q17','q18','q19','q20',
        'q21','q22','q23','q24','q25','q26','q27','q28','q29','q30'}
initial_state = 'q0'
accepting_states = {'q10','q11','q13','q14','q15','q17', 'q19', 'q21','q23','q25','q27','q28','q30'}
afd = AFD(states, alphabet, initial_state, accepting_states, transitions)



input_string = "mondongo_23=48=36.43  while == = //= >> -=  \n mondongo"

print(afd.rerun(list(input_string + ' ')))
print(afd.token_list)
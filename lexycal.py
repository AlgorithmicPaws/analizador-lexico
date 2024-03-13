import os
import re
import automata

def read_file(file_name):
    """
    Read the contents of a Python file and return a list of lines.

    Args:
        filename (str): The name of the Python file to read.

    Returns:
        list: A list containing the lines of the file.

    Raises:
        ValueError: If the provided filename does not end with '.py'.
        FileNotFoundError: If the file with the provided filename does not exist.
    """
    try:
        if not file_name.endswith('.py'):
            raise ValueError("Error: Only .py files are supported.")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'examples', file_name), 'r') as file:
            return file.readlines()
        
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []
    
def format_token(token):
    """
    Format a token into a string representation.

    Args:
        token (tuple): A tuple representing the token. It should have the format (token_type, lexeme, row, column)
                       or (token_type, row, column) depending on the presence of lexeme.

    Returns:
        str: A string representation of the token in the format "<token_type,lexeme,row,column>" or "<token_type,row,column>".

    Raises:
        ValueError: If the token format is invalid.
    """
    if len(token) == 4:
        token_type = token[0]
        lexeme, row, column = token[1:]
        return f"<{token_type},{lexeme},{row},{column}>\n"
    elif len(token) == 3:
        token_type = token[0]
        row, column = token[1:]
        return f"<{token_type},{row},{column}>\n"
    elif len(token) == 2:
        row = token[0]
        column = token[1]
        return f">>> lexical error,{row},{column}>\n"
    else:
        raise ValueError("Invalid token format")

def save_tokens_to_file(tokens, file_name):
    """
    Save a list of tokens to a file.

    Args:
        tokens (list): A list of tokens to be saved.
        file_name (str): The name of the file to save the tokens to.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        PermissionError: If permission is denied to write to the specified file.
        ValueError: If there is an issue with the format of any token.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'results', file_name), 'w') as file:
            for token in tokens:
                formatted_token = format_token(token)
                file.write(formatted_token)
        print("File created successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_name}'.")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    """
    Main function to execute the program.
    """
    def create_regex_from_list(characters):
        regex = '|'.join(re.escape(character) for character in characters)
        return regex
    
    esp_characters_list = ['#','/','%','@','<','>','&','|','^','~',':','=','!','(',')','[',']','{','}',';',':','.','-','+','*']
    unique_characters_list = ['(',')','[',']','{','}',';','~']
    initial_compouse_character_list = ['%','@','&','|','^',':','=','!',':','-','+','*']
    regex_esp_characters =  create_regex_from_list(esp_characters_list)

    alphabet = re.compile(r'[\w\s]|[' + regex_esp_characters + ']')
    unique_character = re.compile(r'[' + create_regex_from_list(unique_characters_list) + ']')
    initial_compouse_character = re.compile(r'[' + create_regex_from_list(initial_compouse_character_list) + ']')

    #d digits
    #s spaces and tabs
    #w letters, digits, and _
    transitions = [
        ('q0', r'\d', 'q1'),    #
        ('q0', r'[a-zA-Z]|_', 'q2'),  #
        ('q0', '-', 'q4'), #
        ('q0', '\*', 'q5'),#
        ('q0', '\>', 'q6'),#
        ('q0', '\<', 'q7'),#
        ('q0', '\/', 'q8'),#
        ('q0', initial_compouse_character, 'q9'),#
        ('q0', unique_character, 'q31'),#
        ('q0', r'[\n\s]', 'q29'),#
        ('q0', '\.', 'q29'),#
        ('q0', r'#', 'q40'),# modifica
        ('q1', r'\d', 'q1'),#
        ('q1', '_', 'q37'),#  modifica
        ('q1', r'e|E', 'q33'),# m
        ('q1', r'j|J', 'q35'),#  m
        ('q1', '\.', 'q12'),#
        ('q1', r'[^.\de]', 'q11'),#
        ('q2', r'[a-zA-Z]', 'q2'),   #
        ('q2', r'[\d|_]', 'q3'),    #
        ('q2', r'[^\w]', 'q14'),
        ('q3', r'\w', 'q3'),    #
        ('q3', r'[^\w]', 'q15'), #    #
        ('q4', '\>', 'q16'),#
        ('q4', '\=', 'q26'),#
        ('q4', r'[^>]', 'q10'),#
        ('q5', '\*', 'q18'),#
        ('q5', '\=', 'q26'),#
        ('q5', r'[^=|*]', 'q10'),#
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
        ('q9', r'[^\=]', 'q28'),#
        ('q12', r'\d', 'q12'),# r
        ('q12', '_', 'q41'),# r
        ('q12', r'e', 'q33'),#  
        ('q12', r'[^\d]', 'q13'),#
        ('q16', alphabet, 'q17'),
        ('q18', '\=', 'q26'),#
        ('q18', '\*', 'q19'),#
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
        ('q32', r'\d', 'q12'),    #
        ('q31', alphabet, 'q10'),
        ('q33', r'\d', 'q33'),
        ('q33', alphabet, 'q34'),
        ('q35', alphabet, 'q36'),
        ('q37', r'\d', 'q38'),
        ('q38', r'\d', 'q1'),
        ('q38', '\.', 'q41'),
        ('q38', '\.', 'q41'),
        ('q38', alphabet, 'q11'),
        ('q40', r'[^\n]', 'q40'),
        ('q40', r'\n', 'q40'),
        ('q41', r'\d', 'q12'),
    ]
    #todo define complex number complex_number = a + b * 1j, eg: 0.02 + 3j 

    states = {'q0','q1','q2','q3','q4','q5','q6', 'q7','q8','q9','q10',
            'q11','q12','q13', 'q14','q15', 'q16','q17','q18','q19','q20',
            'q21','q22','q23','q24','q25','q26','q27','q28','q29','q30',
            'q31','q32','q33','q34','q35','q36','q37','q38','q39','q40','q41','q42'}
    initial_state = 'q0'
    accepting_states = {'q10','q11','q13','q14','q15','q17', 'q19', 'q21','q23','q25','q27','q28','q30','q34','q36'}
    afd = automata.Automaton(states, alphabet, initial_state, accepting_states, transitions)

    # Example usage:

    file_name = 'tokens.txt'
    filename = input("Enter the filename: ")
    file_lines = read_file(filename)
    print(file_lines)
    if file_lines:
        print("File content:")
        for line in file_lines:
            result = afd.rerun(list(line))
            if result == False:
                print(1)
                break
    else:
        print("Unable to read the file.")
    save_tokens_to_file(afd.token_list, file_name)

if __name__ == "__main__":
    main()

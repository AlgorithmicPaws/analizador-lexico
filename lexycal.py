import os

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
    token_type = token[0]
    if len(token) == 4:
        lexeme, row, column = token[1:]
        return f"<{token_type},{lexeme},{row},{column}>\n"
    elif len(token) == 3:
        row, column = token[1:]
        return f"<{token_type},{row},{column}>\n"
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
    # Example usage:
    tokens = [
    ('IDENTIFIER', 'variable', 1, 1),
    ('ASSIGNMENT_OPERATOR', '=', 1, 10),
    ('INTEGER', '10', 1, 12),
    ('NEWLINE', 2, 1),
    ('INDENT', 3, 1),
    ('DEDENT', 3, 1),]
    file_name = 'tokens.txt'
    save_tokens_to_file(tokens, file_name)
    filename = input("Enter the filename: ")
    file_lines = read_file(filename)
    if file_lines:
        print("File content:")
        for line in file_lines:
            print(line.strip())
    else:
        print("Unable to read the file.")

if __name__ == "__main__":
    main()

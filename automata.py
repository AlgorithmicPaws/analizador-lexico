import os

def read_file(filename):
    try:
        # Check if the file extension is .py
        if not filename.endswith('.py'):
            print("Error: Only .py files are supported.")
            return []

        # Get the current working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the full path to the file in the 'examples' directory
        file_path = os.path.join(current_dir, 'examples', filename)
        print(file_path)
        
        # Open the file and read its lines
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def main():
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

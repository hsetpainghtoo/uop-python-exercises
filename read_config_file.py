def read_config_file(filename):
    try:
        # Attempting to open and read a file
        print(f"Attempting to open: {filename}")
        with open(filename, 'r') as file:
            data = file.read()
            print("File content read successfully.")
            return data
            
    except FileNotFoundError:
        # This block runs ONLY if the file does not exist
        print(f"Error: The file '{filename}' was not found. Please check the file path.")
    
    except PermissionError:
        # This block handles cases where the file exists but is locked/protected
        print(f"Error: You do not have the required permissions to read '{filename}'.")

# Test the program with a non-existent file
read_config_file("settings_v1.txt")

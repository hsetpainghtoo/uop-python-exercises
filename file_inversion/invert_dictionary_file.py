import os

def invert_dictionary_file(input_file, output_file):
    original_dict = {}
    inverted_dict = {}

    try:
        # Step 1: Read from the input file
        with open(input_file, 'r') as fin:
            for line in fin:
                # Basic cleaning: remove whitespace and skip empty lines
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                # Split key and value(s)
                key, values = line.split(':', 1)
                key = key.strip()
                # Handle comma-separated values (like black, green)
                value_list = [v.strip() for v in values.split(',')]
                
                # Store in original dict (standard representation)
                original_dict[key] = value_list

        # Step 2: Invert the dictionary
        # Inversion logic: colors become keys, fruits become values
        for fruit, colors in original_dict.items():
            for color in colors:
                if color not in inverted_dict:
                    inverted_dict[color] = [fruit]
                else:
                    inverted_dict[color].append(fruit)

        # Step 3: Write the inverted dictionary to the output file
        with open(output_file, 'w') as fout:
            fout.write("{\n")
            for color, fruits in inverted_dict.items():
                # Format list as a comma-separated string
                fruits_str = ", ".join(fruits)
                fout.write(f"  {color}: {fruits_str}\n")
            fout.write("}\n")
            
        print(f"Success! Inverted dictionary written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the program
if __name__ == "__main__":
    invert_dictionary_file('original_dict.txt', 'inverted_dict.txt')

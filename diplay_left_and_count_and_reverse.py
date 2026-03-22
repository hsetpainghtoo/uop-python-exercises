try:
    name = input("Enter your name: ")
except ValueError:
    print("Please enter a valid string.")
    name = ""

try:
    n = int(input("Enter the number of characters to display from the left: "))
except ValueError:
    print("Please enter a valid integer.")
    n = 0

left_n_chars = name[:n]
print(f"First {n} characters: '{left_n_chars}'")

vowels = "aeiouAEIOU"
count = 0
for char in name:
    if char in vowels:
        count += 1
print(f"Number of vowels: {count}")

reversed_name = name[::-1]
print(f"Reversed name: '{reversed_name}'")
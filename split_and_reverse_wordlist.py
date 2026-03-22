# --- Step 1: Define the sentence ---
sentence = "Data Analysis with Python is powerful"
print(f"Original Sentence: '{sentence}'")

# --- Step 2: Convert sentence to wordlist ---
# The split() method breaks a string into a list based on whitespace.
word_list = sentence.split()
print("Word List:", word_list)

# --- Step 3: Reverse the wordlist ---
# The reverse() method reverses the elements of the list in-place.
word_list.reverse()
print("Reversed Word List:", word_list)
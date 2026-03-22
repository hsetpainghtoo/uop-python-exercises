# Creating two lists with the same content
shopping_list_A = ["Apples", "Bananas", "Cherries"]
shopping_list_B = ["Apples", "Bananas", "Cherries"]

# Print shopping lists
print("Shopping List A: ", shopping_list_A)
print("Shopping List B: ", shopping_list_B)

# Check Equivalence (Values)
print(f"Are the lists equivalent? {shopping_list_A == shopping_list_B}") 
# Output: True, because the contents are the same.

# Check Identity (Memory Objects)
print(f"Are the lists identical? {shopping_list_A is shopping_list_B}") 
# Output: False, because they are two distinct objects in memory.

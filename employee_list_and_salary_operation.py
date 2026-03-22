# --- Step 1: Initialize the list of 10 employees ---
employee_list = [
    "Alice", "Bob", "Charlie", "David", "Eve", 
    "Frank", "Grace", "Heidi", "Ivan", "Judy"
]
print("Original Employee List:", employee_list)

# --- Step 2: Split the list into two sub-lists ---
# Slicing is used here. [:5] gets index 0 to 4. [5:] gets index 5 to the end.
subList1 = employee_list[:5]
subList2 = employee_list[5:]

print("\nsubList1:", subList1)
print("subList2:", subList2)

# --- Step 3: Add "Kriti Brown" to subList2 ---
# The append() method adds an element to the end of the list.
subList2.append("Kriti Brown")
print("subList2 after adding Kriti:", subList2)

# --- Step 4: Remove the second employee from subList1 ---
# The second employee is at index 1. pop(1) removes the element at that index.
removed_emp = subList1.pop(1)
print(f"subList1 after removing {removed_emp}:", subList1)

# --- Step 5: Merge both lists ---
# The + operator concatenates two lists.
merged_list = subList1 + subList2
print("\nFinal Merged Employee List:", merged_list)

# --- Step 6: Salary Operations ---
# We create a dummy salary list for the current employees (10 employees total).
salaryList = [50000, 60000, 55000, 72000, 48000, 80000, 62000, 59000, 53000, 45000]

print("\nOriginal Salaries:", salaryList)

# Give a rise of 4% to every employee.
# We use a list comprehension to multiply every item 's' by 1.04.
salaryList = [s * 1.04 for s in salaryList]
print("Salaries after 4% rise:", salaryList)

# --- Step 7: Sort and show Top 3 Salaries ---
# sort(reverse=True) sorts the list in descending order (highest to lowest).
salaryList.sort(reverse=True)

# Slicing [:3] grabs the first three elements.
top_3_salaries = salaryList[:3]

print("\nTop 3 Salaries:", top_3_salaries)
def boost_scores(scores_list):
	"""
	Adds 5 extra points to every score in the list.
	"""
	for i in range(len(scores_list)):
		scores_list[i] += 5  # Modify the object in place

# Main execution
student_scores = [85, 90, 78]

print("Before function: ", student_scores)


# Function Call
boost_scores(student_scores)

print("After funcion: ", student_scores)

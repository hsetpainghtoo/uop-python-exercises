# Stage 3: Final calculation and removal of scaffolding.
def trapezoid_area(base1, base2, height):
    """
    Calculates the area of a trapezoid using the formula: A = 0.5 * (b1 + b2) * h.
    """
    # Calculate the sum of the bases
    sum_of_bases = base1 + base2
    
    # Final calculation of the area
    area = 0.5 * sum_of_bases * height
    
    # Return the final result
    return area

print(trapezoid_area(10, 10, 1))
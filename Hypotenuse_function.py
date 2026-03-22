import math

def hypotenuse(a, b):
    """
    Calculates the length of the hypotenuse (c) for a right triangle with legs a and b,
    using the Pythagorean theorem: c = sqrt(a^2 + b^2).
    """
    a_squared = a ** 2      
    b_squared = b ** 2      
    sum_of_squares = a_squared + b_squared
    
    result = math.sqrt(sum_of_squares)
    
    return result

print(hypotenuse(1, 1))
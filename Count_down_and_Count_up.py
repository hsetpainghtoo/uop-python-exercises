def countdown(n):
    """Counts down from n to 1 and prints 'Blastoff!'"""
    if n <= 0:
        print('Blastoff!')
    else:
        print(n)
        countdown(n-1)

def countup(n):
    """Counts up from a negative number to -1 and prints 'Blastoff!'"""
    if n >= 0:
        print('Blastoff!')
    else:
        print(n)
        countup(n+1)

# Main program
user_input = input("Enter a number: ")
number = int(user_input)

if number > 0:
    countdown(number)
elif number < 0:
    countup(number)
else:
    # For zero, I choose to call countdown
    countdown(number)
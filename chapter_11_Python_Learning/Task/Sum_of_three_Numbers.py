# Create a program to sum of three number from the user input,
# if user doesn't enter any number', use default as 100, 200, 300
# Logic Building
# Step 1 - I/O and O/P
# I/O -  int
# O/P - int
# Step 2 - Rough Logic
# return n1+n2+n3

# Sum of three numbers with default values

def sum_of_three(n1=100, n2=200, n3=300):
    return n1 + n2 + n3


# Take user input (press Enter to skip and use default)
num1 = input("Enter first number (default 100): ")
num2 = input("Enter second number (default 200): ")
num3 = input("Enter third number (default 300): ")

# If input is empty, use default; otherwise convert to int
n1 = int(num1) if num1 else 100
n2 = int(num2) if num2 else 200
n3 = int(num3) if num3 else 300

result = sum_of_three(n1, n2, n3)
print("Sum of three numbers:", result)
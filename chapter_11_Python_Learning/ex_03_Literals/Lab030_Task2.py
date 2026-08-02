# Task for the Today
# Take a 2 input from the user
# Print the Quotient and Remainder
# 15 ->  num1
# 2 -> num2
# Q -> 7
# R -> 1

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

# Method 1
quotient = num1 // num2
remainder = num1 % num2
print("Quotient: ", quotient)
print("Remainder: ", remainder)

# Method 2
quotient, remainder = divmod(num1, num2)
print("Quotient: ", quotient)
print("Remainder: ", remainder)
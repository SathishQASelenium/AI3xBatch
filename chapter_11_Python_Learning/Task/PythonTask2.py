# Task for the Today
# Take a 2 input from the user
# Print the Quotient and Remainder
# 15 ->  num1
# 2 -> num2
# Q -> 7
# R -> 1

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

quotient, remiander = divmod(num1, num2)

print("Quotient: ", quotient)
print("Remainder: ", remiander)
# Task for the Today
# Take a 2 input from the user
# perform the add, sub, mul and div
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

add = num1 + num2
sub = num1 - num2
mul = num1 * num2
div = num1 / num2

print("Addition: ", add)
print("Subtraction: ", sub)
print("Multiplication: ", mul)
print("Division: ", div)

# Function with parameters and return type
def math_operations(a, b):
    return a + b, a - b, a * b, a / b

sum_result, diff_result, mul_result, div_result = math_operations(num1, num2)
print("Addition: ", sum_result)
print("Subtraction: ", diff_result)
print("Multiplication: ", mul_result)
print("Division: ", div_result)
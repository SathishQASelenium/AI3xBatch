nums = [1, 2, 3, 4, 5, 6]

# Function, which will return True if the number is even, otherwise False
def even_num(x):
    return x%2==0

# Using filter() to filter out only even numbers from the list
print(list(filter(even_num, nums)))
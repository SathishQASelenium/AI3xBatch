squares = [1, 4, 9, 16, 25]
print(squares)  # [1, 4, 9, 16, 25]
print(squares.pop()) # Remove and return item at index (default last)
print(squares) # [1, 4, 9, 16]
print(squares.pop(1)) # Remove and return item at index 1
print(squares) # [1, 9, 16]

squares.clear() # Remove all items from the list.
print(squares) # []

# index(element, start, end)
# Returns the index of the first occurrence of the element.
numbers = [10, 20, 30, 20, 40]
print(numbers.index(20))
print(numbers.count(20))

numbers.sort()
print(numbers) # [10, 20, 20, 30, 40]

numbers.sort(reverse=True)
print(numbers) # [40, 30, 20, 20, 10]

# max() / min() / sum() Works for numerical lists.
print(max(numbers))  # 40
print(min(numbers))  # 10
print(sum(numbers))  # 120

# Slicing (start, end-1) - index
print(numbers)  # [10, 20, 20, 30, 40]
print(numbers[1:4]) # [20, 20, 30]


print("apple" in numbers) # False
print(20 in numbers) # True

l = list(range(1, 5)) # [1, 2, 3, 4]
print(l) # [1, 2, 3, 4]

# Nested Lists
matrix = [[1,2,3], [4,5,6], [7,8,9]]
print(matrix[1][2]) # 6

del numbers[0]
print(numbers) # [20, 20, 30, 40]
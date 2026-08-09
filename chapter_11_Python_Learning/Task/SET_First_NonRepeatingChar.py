# Coding Program
# Find the first non-repeating character in a string
# swiss -> s=3, w=0, i=0
# w

user_input = input("Enter a string: ")
print(user_input)

s=set()

def first_non_repeating_char(string):
    for char in string:
        if string.count(char) == 1:
            s.add(char)
            return char
    return None

print("First non-repeating character is:", first_non_repeating_char(user_input))
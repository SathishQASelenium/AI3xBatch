# Coding Program
# Print all non-repeating characters in a string
# swiss -> s=3, w=0, i=0
# {w, i}

user_input = input("Enter a string: ")
print(user_input)

s=set()

def all_non_repeating_char(string): # will return all non repeating characters in a string in form of set
    s.clear()  # Clear the set before each function call
    for char in string:
        if string.count(char) == 1:
            s.add(char) # Add the non-repeating character to the set            
    return s # Return the set of non-repeating characters

print("All Non repeating characters in the above string : ", all_non_repeating_char(user_input))
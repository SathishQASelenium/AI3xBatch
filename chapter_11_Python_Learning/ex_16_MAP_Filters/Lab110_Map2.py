name = ["pramod", "dutta", "qa", "lucky"]

# Using map() function to convert all names in the list to uppercase
def upper_case(string):
    return string.upper()


upper_names = list(map(upper_case, name))
print(upper_names)
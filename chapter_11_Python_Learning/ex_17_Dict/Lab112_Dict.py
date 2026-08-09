# dict is a collection of key-value pairs. It is unordered, mutable, and indexed. 
# In Python, dictionaries are defined using curly braces {}.
my_dict = {
    "name": "Aman",
    "age": 34,
    "role": "SDET",
    "exp": 3
}

print(my_dict)
print(my_dict["age"])
print(my_dict["role"])

my_dict["role"] = "Manual Tester"
print(my_dict)

del my_dict["age"]
print(my_dict)

for key, value in my_dict.items():
    print(key, value)

print("age" in my_dict) # Will check for the presence of key "age" in the dictionary and return False
print("role" in my_dict) # Will check for the presence of key "role" in the dictionary and return True
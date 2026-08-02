cities = ("London", "Paris", "Los Angeles", "Tokyo")
print(len(cities)) # 4
print("Paris" in cities) # True
print("New Delhi" in cities) # False

t = (12, 34, 56)
# t.append(12) # Append method is not available for tuples, as they are immutable

ENV_API_URLS = tuple(["abc.com/get", "xyz.com/post", "qwe.com/put"])
print(ENV_API_URLS) # ('abc.com/get', 'xyz.com/post', 'qwe.com/put')

colors = ("red", "green", "blue")
for c in colors:
    print(c) # Prints each color in the tuple


my_list = [1, 2, 3]
my_tuple = tuple(my_list) # List to tuple conversion
print(my_tuple)    # (1, 2, 3)


back_to_list = list(my_tuple) # Tuple to list conversion
print(back_to_list)   # [1, 2, 3]
print(max(back_to_list))   # 3
# type
print(type(back_to_list))   # <class 'list'>
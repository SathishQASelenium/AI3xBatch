# my_list = [1, 2, 3]

# my_list[0] = "Pramod"
# my_list[1] = "Dutta"
# my_list[1] = "Dutta"

# print(my_list)
# # It will overwrite because a list is mutable. 

# for element in my_list:
#     print(element)

# # range() this also return the list
# for i in range(1, 5):  # 1,2,3,4
#     print(i)


my_list = [1, 2, 3]
# Indexing
print("element at the index 0 - ", my_list[0])
print("element at the index 1 - ", my_list[1])
print("element at the index 2 - ", my_list[2])

# append() - # Append object to the end of the list.
my_list.append(4)
print(my_list) 
# [1, 2, 3, 4]

my_list.append(5)
print(my_list)
# [1, 2, 3, 4, 5]

# extend() - Append a new list
my_list.extend([7, 8, 10, 9])
print(my_list)
# [1, 2, 3, 4, 5, 7, 8, 10, 9]

# insert()
my_list.insert(1,"Dutta") # insert "Dutta" at index 1
print(my_list)
print(len(my_list)) # length of the list
# [1, 'Dutta', 2, 3, 4, 5, 7, 8, 10, 9]
# 10

my_list.insert(0, 0)
print(my_list)
# [0, 1, 'Dutta', 2, 3, 4, 5, 7, 8, 10, 9]

my_list[1] = "Amit" # replace the element at index 1 with "Amit". So 1 is replaced with "Amit"
print(my_list)
# [0, 'Amit', 'Dutta', 2, 3, 4, 5, 7, 8, 10, 9]

my_list.remove("Amit") # remove the element "Amit" from the list
print(my_list)
# [0, 'Dutta', 2, 3, 4, 5, 7, 8, 10, 9]

my_copy_list = my_list.copy()
print(my_list)
print(my_copy_list)

my_copy_list.remove("Dutta") # remove the element "Dutta" from the copied list

print(my_list) # 'Dutta' is still present in the original list
print(my_copy_list) # 'Dutta' is removed from the copied list
# [0, 'Dutta', 2, 3, 4, 5, 7, 8, 10, 9]
# [0, 2, 3, 4, 5, 7, 8, 10, 9]
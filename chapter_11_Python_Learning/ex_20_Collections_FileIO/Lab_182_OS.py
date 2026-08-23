import os
print(os.getcwd()) # Get current working directory
full_path = os.path.join(os.getcwd(), "chapter_11_Python_Learning/ex_20_Collections_FileIO/pramod.txt") # Get full path of the file
print(full_path) # Print full path of the file

file = open(full_path, 'r')
print(file.read()) # Read the file and print its contents
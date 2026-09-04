# with  open('testdata.txt', 'r') as file
# file = open('testdata.txt', 'r')
import os

file_path = os.path.join(os.getcwd(),'chapter_11_Python_Learning/ex_20_Collections_FileIO/testdata.txt')
file_data = open(file_path,'r')

try:
    with open(file_path, 'r') as file:
        content = file.read()
    # content = file.readlines() # list manner
        print(content)
except FileNotFoundError as fnfe:
    print(fnfe)
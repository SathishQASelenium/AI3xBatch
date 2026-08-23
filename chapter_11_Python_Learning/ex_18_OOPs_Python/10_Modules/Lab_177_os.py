import os

print(os.name) # nt for Windows and posix for Linux or Mac
print(os.getcwd()) # get current working directory
# print(os.mkdir("AI")) # create a new directory
print(os.listdir()) # list all files and directories in the current working directory

#print(os.remove("AI.txt")) # remove a file
# print(os.rename("AI.txt","testdata.txt")) # rename a file

print(os.environ.get("PATH")) # get the value of the PATH environment variable
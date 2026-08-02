pb_global_b = 12

def my_function():
    pb_a = 10
    print(pb_a)
    print(pb_global_b)
    

# print(pb_a) We cannot access the local variable pb_a outside the function, so this line is commented out.
print(pb_global_b) # We can access the global variable pb_global_b outside the function, so this line is not commented out.
my_function()
# We use * which indicates that we can pass infinite number of arguments to the function. The arguments will be stored in a tuple.
def print_mul_arg(*pramod_list):
    # args - List
    for i in pramod_list:
        print(i)


print_mul_arg("pramod")
print_mul_arg(2, 3, 1, 4, 3, 2, 2, 2, 2, 2, 2)
print_mul_arg("pramod", "dutta")
print_mul_arg("pramod", "dutta", "third")
print_mul_arg("pramod", "dutta", "third", 3.14)
print_mul_arg("pramod", "dutta", "third", 3.14, True)
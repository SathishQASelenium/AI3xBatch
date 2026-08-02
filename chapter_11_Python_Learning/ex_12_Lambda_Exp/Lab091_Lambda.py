def add(n):
    return n + 10 # default function to add 10 to the given number

l_add = lambda n:n+10 # lambda function to add 10 to the given number
print(l_add(30))


def mul(a, b):
    return a * b # default function to multiply two numbers


mul_l = lambda a, b: a * b # lambda function to multiply two numbers
print(mul_l(3, 4))


def sum_three_num(a, b, c): # default function to add three numbers
    return a + b + c


op_f = lambda a, b, c: a + b + c # lambda function to add three numbers
print(op_f(3, 4, 5))
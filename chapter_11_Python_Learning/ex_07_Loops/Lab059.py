# This program prints all odd numbers from 0 to 9 using a for loop and the range function.
for number in range(10):
    if number % 2 == 0:
        continue
    else:
        print(number)
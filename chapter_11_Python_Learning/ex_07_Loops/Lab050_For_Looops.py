for i in range(3, 5):
    print(i)

# This is not a proper way to use range, as the step is negative and the start is less than the stop. This will not print anything.
for i in range(1, 10,-1):
    print(i) 

for i in range(10): # 0 to 9, 10 Times [with start as 0 and step as 1 by default]
    print("Hello World!")

for test_id in range(1,6):
    print("Running the test case : ",test_id)
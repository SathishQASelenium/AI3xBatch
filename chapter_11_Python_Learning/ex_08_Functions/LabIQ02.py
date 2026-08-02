def f1():
    print("Welcome")
    #Step 1- Declare
    def f2():
        print("Hi")
    #Step 2 - Call
    f2()


f1()
# f2() Can't call f2() because it is defined inside f1() and is not accessible outside of f1().
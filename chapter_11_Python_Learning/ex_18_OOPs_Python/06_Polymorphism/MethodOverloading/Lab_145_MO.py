class MathClass:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c=10):
        return a + b + c


obj_ref = MathClass()
print(obj_ref.add(3, 4, 5)) # This will call the second add method with three parameters, so it will return 3 + 4 + 5 = 12.
print(obj_ref.add(3, 4))    # This will call the second add method with two parameters, so it will return 3 + 4 + 10 = 17, since c has a default value of 10.
print(obj_ref.add(3.14, 4.14)) # This will call the second add method with two parameters, so it will return 3.14 + 4.14 + 10 = 17.28, since c has a default value of 10.
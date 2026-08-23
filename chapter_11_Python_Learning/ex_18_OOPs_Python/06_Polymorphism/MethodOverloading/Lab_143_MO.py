# If we define a method with the same name in a class, the latest defined method will override the previous one. 
# This is known as method overriding. In Python, we cannot have multiple methods with the same name but different parameters (method overloading) like in some other programming languages. 
# The last defined method will be the one that is used.

class MathClass:
    # def add(self, a,b):
    #     return a+b

    def add(self,a,b):
        return a-b

obj_ref = MathClass()
print(obj_ref.add(3,4))
print(obj_ref.add(3.12,4.45))
class Home:
    def __init__(self):
        self.public_var = "father"
        self._protected_var = "brother"
        self.__private_var= "baby"

    def mom(self):
        print(self.__private_var)
        self.__wife()

    def __wife(self):
        print("Private Wife")


object_ref = Home()
# Accessing public variable
print(object_ref.public_var)

# Accessing protected variable
print(object_ref._protected_var)

# Accessing private variable
# print(object_ref.__private_var)  # This will raise an AttributeError

# Accessing private method
# object_ref.__wife()  # This will raise an AttributeError
object_ref.mom()

# object_ref.__wife()
# object_ref.__private_var
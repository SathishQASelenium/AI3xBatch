class Person:
    def say_name(self, name): # This method will NOT be considered
        print("Hi", name)

# This method will be considered as an overloaded method, but in reality, it will override the previous method with the same name.
# Also to note, we have lastname as a default parameter, so if we don't pass it, it will take the default value.
    def say_name(self, name, lastname="Kumar"):
        print("Hi,", name, lastname)


t = Person()
t.say_name("Sathish")
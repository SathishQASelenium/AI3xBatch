# Method Overriding in Python
class BaseTest:
    def run(self):
        print("Running the Base Test")

class LoginTest(BaseTest):
    def run(self):
        print("Runnning Login Test")

# t = BaseTest()
t = LoginTest()
t.run() # This code demonstrates method overriding in Python. The `BaseTest` class has a method called `run`, which prints "Running the Base Test". The `LoginTest` class inherits from `BaseTest` and overrides the `run` method to print "Running Login Test".
class TestSuite:
    def info(self):
        print("Test suite information")

class BaseTest(TestSuite): # inheritance and method overriding
    def setup(self):
        print("Base setup")

    def run(self):
        print("Base test execution")

class LoginTest(BaseTest): # inheritance and method overriding
    def run(self):  # overriding
        print("Login test execution")

class APITest(BaseTest): # inheritance and method overriding
    def run(self):  # overriding
        print("API test execution")


# t = LoginTest() # The LoginTest class inherits from the BaseTest class and overrides the run method. When we create an instance of LoginTest and call the run method, it will execute the overridden method in the LoginTest class, printing "Login test execution".
# t = APITest()  # The APITest class also inherits from the BaseTest class and overrides the run method. When we create an instance of APITest and call the run method, it will execute the overridden method in the APITest class, printing "API test execution".
t = BaseTest() # The BaseTest class is instantiated, and when we call the run method on this instance, it will execute the run method defined in the BaseTest class, printing "Base test execution".
t.run()
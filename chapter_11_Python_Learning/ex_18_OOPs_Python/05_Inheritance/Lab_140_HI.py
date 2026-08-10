# Hierarchical Inheritance, BaseTest is the parent class and LoginTest and SignupTest are child classes
class BaseTest:
    def setup(self):
        print("Setup from BaseTest")

class LoginTest(BaseTest):
    def run(self):
        print("Running Login Test")

class SignupTest(BaseTest):
    def run(self):
        print("Running Signup Test")



LoginTest().setup()
LoginTest().run()
SignupTest().setup()
SignupTest().run()
class BaseTest:
    driver = "chrome"
    __driver2 = "FF"
    def setUp(self):
        print("Base Test Setup done!")

class LoginTest(BaseTest): # BaseTest is the parent class and LoginTest is the child class
    def run(self):
        self.setUp()
        print("Running the Testcases -> " + self.driver)


t = LoginTest()
t.run()
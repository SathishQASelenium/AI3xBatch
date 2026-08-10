a = 10 # Global Variable

class Person:
    b = 11 # Instance, Class , Attribute...property
    def print_infor(self):
        l = 12 # local l varaible
        print("Printing Instance variable b: ", self.b)
        print("Printing local variable l: ", l)

    def talk(self):
        print("Printing Instance variable b within talk(): ", self.b)
        print("Printing global variable a: ", a)

# Create the object of the class and call the methods
sathy = Person()
sathy.print_infor()
sathy.talk()

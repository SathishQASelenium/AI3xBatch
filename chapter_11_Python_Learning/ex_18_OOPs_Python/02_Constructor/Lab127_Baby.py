class Baby:
    name: None

    def __init__(self,nameGiven):
        self.name = nameGiven
    def printName(self):
        print(self.name)



b = Baby("kutty")

b2 = Baby("pattu")
b.printName()
b2.printName()
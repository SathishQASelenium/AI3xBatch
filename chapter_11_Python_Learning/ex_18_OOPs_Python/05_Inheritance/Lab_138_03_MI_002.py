class Father1:
    def money(self):
        print("F1 Money")

class Father2:
    def money(self):
        print("F2 Money")

class Child(Father1, Father2): # Multiple Inheritance, Child inherits from both Father1 and Father2, But order will be considered for MRO
    def give_money(self):
        print("Son")
        self.money()


c = Child()
c.give_money() #MRO


class Child2(Father2, Father1): # Multiple Inheritance, Child inherits from both Father1 and Father2, But order will be considered for MRO
    def give_money(self):
        print("Daughter")
        self.money()


c2 = Child2()
c2.give_money() #MRO
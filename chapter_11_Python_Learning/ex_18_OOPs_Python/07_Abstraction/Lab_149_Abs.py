# Abstraction
# Hide the details and show what is required.

# Car - with key _ __private, tyres -> public,

# Car -> multiple - Engine, GearBox
# Car -> driver -> Engine, gearbox?

from abc import ABC, abstractmethod

class Animal(ABC):

    def __init__(self,name):
        self.name = name

    @abstractmethod
    def sound(self):
        pass

class Dog(Animal): # Dog is a child class of Animal

    def sound(self): # Once we create a child class, we have to implement the abstract method of parent class.
        print("Bark!")

dog = Dog("PP")
dog.sound()
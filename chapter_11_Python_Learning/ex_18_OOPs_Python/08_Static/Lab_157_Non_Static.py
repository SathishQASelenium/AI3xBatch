class MathOperation:

    def div(self, a, b): # Non static method
        return a / b

    @staticmethod # Static method
    def sum(a, b):
        return a + b

t = MathOperation()
print(t.div(10, 10)) # Calling non-static method

print(MathOperation.sum(10, 10)) # Calling static method
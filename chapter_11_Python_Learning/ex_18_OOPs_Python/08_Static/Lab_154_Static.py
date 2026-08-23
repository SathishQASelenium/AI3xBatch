class TestCounter:
    count = 0 # static variable

    def __init__(self):
        TestCounter.count +=1

t1 = TestCounter()
t2 = TestCounter()
print(TestCounter.count)

#Each time an object is created, count increases.
# count is shared across all objects.
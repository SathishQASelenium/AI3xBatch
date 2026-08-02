def before_after_ui_test(func):
     def wrapper():
          print("Before the TC code execute!")
          func()
          print("After the TC Done")
     return wrapper()


@before_after_ui_test
def test_ui():
     print("Hi, I am testing a UI Test")

# Notes:
# 1. The decorator function is defined with the name before_after_ui_test.
# 2. The decorator function takes a function as an argument (func) and defines a wrapper function that adds behavior before and after the execution of the original function.
# 3. The wrapper function prints a message before and after calling the original function (func).
# 4. The decorator function returns the wrapper function, which is then executed when the decorated function (test_ui) is called.
# 5. The test_ui function is decorated with the @before_after_ui_test decorator
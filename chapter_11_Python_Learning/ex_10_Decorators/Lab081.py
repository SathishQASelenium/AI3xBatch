# This is a simple example of a decorator in Python that adds functionality before and after a function is called.
def start():
    print("Before the running UI TC")
    print("Start the Browser ")

def end():
    print("End the running UI TC")
    print("Quit the Browser ")

def test_ui():
    print("I will Test the UI")


start()
test_ui()
end()
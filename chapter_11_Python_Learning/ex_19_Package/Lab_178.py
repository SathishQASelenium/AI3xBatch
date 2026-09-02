from package import util_module,util_module2 # Multiple python classes can be imported from a single package using the above syntax.

util_module.blah("sathish")
util_module2.blah("Kumar")

# This module is a normal Python file where you can directly call the functions.
import mymodule
print(mymodule.greet("Magesh"))
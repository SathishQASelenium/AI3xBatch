def add_security(func):
    def wrapper():
        print("1.Before the function is called.")
        print("2.Add Helmet, Dashcash, gloves, knee guards, License")
        func()
        print("3.After the function is called.")
        print("4.Secure Driving, Leave all the items")
    return wrapper

@add_security # This is a decorator that adds security measures before and after the function is called.
def drive_ola_scooter():
    print("I am driving ola scooter")


drive_ola_scooter()

@add_security
def drive_zypp_scooter():
    print("Driving Zypp scooter")

drive_zypp_scooter()

# Notes:
# 1. The add_security function is a decorator that takes a function as an argument (func) and defines a wrapper function that adds security measures before and after the execution of the original function.
# 2. The wrapper function prints messages before and after calling the original function (func).
# 3. The add_security function returns the wrapper function, which is then executed when the decorated functions (drive_ola_scooter and drive_zypp_scooter) are called
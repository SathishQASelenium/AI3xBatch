import time


def print_logs(func):
    def wrapper():
        print("Start the logs")
        func()
        print("End of the log")
    return wrapper

def time_decorator(func):
    def wrapper():
        start_time = time.time()
        start_time_str = time.strftime("%H:%M:%S", time.localtime(start_time))
        print(start_time_str)
        func()
        end_time = time.time()
        end_time_str = time.strftime("%H:%M:%S", time.localtime(end_time))
        print(end_time_str)
        print("Total Time Take by Func -> ", end_time - start_time)
    return wrapper


@time_decorator
@print_logs
def test_ui_1():
    print("Add a function, time taken by this function 1")
    time.sleep(2)

@time_decorator
@print_logs
def test_ui_2():
    print("Add a function, time taken by this function 2")
    time.sleep(5)

test_ui_1()
test_ui_2()

# 17:55:59
# Start the logs
# Add a function, time taken by this function 1
# End of the log
# 17:56:01
# Total Time Take by Func ->  2.0012176036834717
# 17:56:01
# Start the logs
# Add a function, time taken by this function 2
# End of the log
# 17:56:06
# Total Time Take by Func ->  5.000854969024658
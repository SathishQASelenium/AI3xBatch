test_results = ["PASS", "FAIL", "PASS", "SKIP", "FAIL"]
# Using filter() to filter out only "PASS" results from the list
pass_give = list(filter(lambda x: x == "PASS", test_results))
print(pass_give)
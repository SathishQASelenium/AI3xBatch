def make_pizza(*toppings):
    print(toppings) # Will print the tuple of toppings
    for i in toppings: # Will print each topping in the tuple
        print(i)

pramod = make_pizza("cheese","corn")
yoga = make_pizza("cheese","corn","paneer","capsicm")
vinay = make_pizza("tomato")
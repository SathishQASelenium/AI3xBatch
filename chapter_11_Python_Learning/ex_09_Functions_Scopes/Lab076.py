public_toilet = "PB"

def home():
    private_toilet = "PT"
    print(public_toilet)
    print(private_toilet)

def stranger():
    print(public_toilet)
    # print(private_toilet) We cannot access the local variable private_toilet outside the function, so this line is commented out.

home() # Will print both public_toilet and private_toilet
stranger() # Will print only public_toilet, as private_toilet is not accessible in this function
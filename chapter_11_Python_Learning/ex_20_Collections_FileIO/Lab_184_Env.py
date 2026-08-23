from dotenv import load_dotenv
import os
load_dotenv() 

print(os.getenv('DB_PASSWORD'))

if os.getenv('DB_PASSWORD') == "demo_pass":
    print("Welcome Demo User")
else:
    print("Goodbye")
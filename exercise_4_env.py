from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read the environment variable
my_key = os.getenv("MY_KEY")

print("Loaded MY_KEY:", my_key)

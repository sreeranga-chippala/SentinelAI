from dotenv import load_dotenv
import os
import requests

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

r = requests.get(url)

print("Status:", r.status_code)
print(r.text)
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = "https://app.pennylane.com/api/external/v2/customer_invoices?sort=-id"

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set. Check your .env file.")

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

if not os.path.exists("JSON"):
    os.makedirs("JSON")

file_path = os.path.join("JSON", "2.json")

try:
    json_data = response.json()
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)
    print(f"Successfully saved data to {file_path}")

except json.JSONDecodeError:
    print("Response was not valid JSON. Saving raw text.")
    with open(file_path, "w") as f:
        f.write(response.text)
    print(f"Successfully saved raw text to {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

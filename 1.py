import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = "https://app.pennylane.com/api/external/v2/customer_invoices"

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set. Check your .env file.")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

# Sample Input 
payload1 = {
    "currency": "EUR",
    "language": "en_GB",
    "date": "2023-10-27",
    "deadline": "2023-11-27",
    "customer_id": 6873,
    "invoice_lines": [
        {
            "vat_rate": "FR_21",
            "label": "Software License",
            "quantity": 1,
            "section_rank": 1,
            "raw_currency_unit_price": "100.00",
            "unit": "unit"
        }
    ]
}

# Example usage 
response1 = requests.post(url, json=payload1, headers=headers)

# Ensure JSON directory exists
if not os.path.exists("JSON"):
    os.makedirs("JSON")

file_path = os.path.join("JSON", "1.json")

try:
    json_data = response1.json()
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)
    print(f"Successfully saved data to {file_path}")
except json.JSONDecodeError:
    print("Response was not valid JSON. Saving raw text.")
    with open(file_path, "w") as f:
        f.write(response1.text)
    print(f"Successfully saved raw text to {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

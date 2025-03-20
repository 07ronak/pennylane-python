import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = "https://app.pennylane.com/api/external/v2/customer_invoices/import"

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set. Check your .env file.")

payload = {
    "import_as_incomplete": False,
    "currency": "EUR",
    "file_attachment_id": 42,
    "date": "2023-08-08",
    "deadline": "2023-08-08",
    "customer_id": 42,
    "currency_amount_before_tax": "100",
    "currency_amount": "120",
    "currency_tax": "20",
    "invoice_lines": [
        {
            "vat_rate": "FR_21",
            "currency_amount": "120",
            "currency_tax": "20",
            "label": "Demo label",
            "quantity": 12,
            "raw_currency_unit_price": "33",
            "unit": "piece"
        }
    ]
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)

# Ensure JSON directory exists
if not os.path.exists("JSON"):
    os.makedirs("JSON")

file_path = os.path.join("JSON", "3.json")

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

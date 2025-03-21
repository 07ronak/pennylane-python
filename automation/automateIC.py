import json
import requests
import os

# Paths
parent_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(parent_dir, "saved JSON", "Customer.json")
done_file_path = os.path.join(parent_dir, "done2.json")

# API details
url = "https://app.pennylane.com/api/external/v2/individual_customers"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

# Load customer data
with open(json_file_path, "r") as file:
    data = json.load(file)

customers = data.get("QueryResponse", {}).get("Customer", [])
responses = []

for customer in customers:
    payload = {
        "billing_address": {
            "address": customer.get("BillAddr", {}).get("Line1", ""),
            "postal_code": customer.get("BillAddr", {}).get("PostalCode", ""),
            "city": customer.get("BillAddr", {}).get("City", ""),
            "country_alpha2": customer.get("BillAddr", {}).get("CountrySubDivisionCode", "")
        },
        "delivery_address": {
            "address": customer.get("ShipAddr", {}).get("Line1", ""),
            "postal_code": customer.get("ShipAddr", {}).get("PostalCode", ""),
            "city": customer.get("ShipAddr", {}).get("City", ""),
            "country_alpha2": customer.get("ShipAddr", {}).get("CountrySubDivisionCode", "")
        } if customer.get("ShipAddr") else None,
        "payment_conditions": "30_days",
        "first_name": customer.get("GivenName", ""),
        "last_name": customer.get("FamilyName", ""),
        "phone": customer.get("PrimaryPhone", {}).get("FreeFormNumber", ""),
        "emails": [customer.get("PrimaryEmailAddr", {}).get("Address", "")]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    responses.append({"customer": f"{customer.get('GivenName', '')} {customer.get('FamilyName', '')}", "response": response.json()})

# Save responses to done.json
with open(done_file_path, "w") as file:
    json.dump(responses, file, indent=4)

print(f"All individual entries processed. Output saved to {done_file_path}")

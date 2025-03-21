import requests

url = "https://app.pennylane.com/api/external/v2/individual_customers"

payload = {
    "billing_address": {
        "address": "4581 Finch St.",
        "postal_code": "94326",
        "city": "Bayshore",
        "country_alpha2": "CA" 
    },
    "delivery_address": {
        "address": "4581 Finch St.",
        "postal_code": "94326",
        "city": "Bayshore",
        "country_alpha2": "CA"  
    },
    "payment_conditions": "30_days",  # Kept default as no info was in JSON
    "first_name": "Amy",  
    "last_name": "Lauterbach",  
    "phone": "(650) 555-3311",
    "emails": ["Birds@Intuit.com"]
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"  
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
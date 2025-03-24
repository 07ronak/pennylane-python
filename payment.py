import requests
import random
from datetime import timedelta, datetime

url = "https://app.pennylane.com/api/external/v2/credit_notes"

def generate_random_date_after_txn_date(txn_date_str):
    txn_date = datetime.strptime(txn_date_str, "%Y-%m-%d").date()
    min_days = 1
    max_days = 30
    random_days = random.randint(min_days, max_days)
    random_date = txn_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

txn_date_from_json = "2025-02-07"

payload = {
    "language": "fr_FR",  # Default value
    "discount": {
        "type": "absolute", #fixed
        "value": str(random.randint(0, 40))  # Random discount value
    },
    "date": "2025-02-07",  # From TxnDate in JSON
    "deadline":  generate_random_date_after_txn_date(txn_date_from_json),
    "customer_id": 8,  # From CustomerRef.value in JSON
    "invoice_lines": [
        {
            "discount": {
                "type": "absolute", #fixed
                "value": str(random.randint(0, 40))  # Random discount value
            },
            "vat_rate": "FR_200",  # default VAT rate
            "label": "QBO", #from JSON
            "quantity": random.randint(1, 100),  # Random quantity
            "raw_currency_unit_price": str(round(random.uniform(1, 100), 2)),  # Random price
            "unit": "piece"
        }
    ],
    "credited_invoice_id": 96,  # From Line[0].LinkedTxn[0].TxnId in JSON
    "currency": "USD"  # From CurrencyRef.value in JSON
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"  
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
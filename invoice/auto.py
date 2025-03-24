import json
import requests
import random
import datetime

# Load data from JSON files
with open("CC.json", "r") as ic_file:
    ic_data = json.load(ic_file)

with open("Invoice.json", "r") as invoice_file:
    invoice_data = json.load(invoice_file)

# Create a mapping between customer names and their IDs from IC.json
customer_name_to_id = {}
customer_id_to_ledger = {}

for entry in ic_data:
    customer_name = entry["response"]["name"]
    customer_id = str(entry["response"]["id"])
    ledger_account_id = entry["response"]["ledger_account"]["id"]
    customer_name_to_id[customer_name] = customer_id
    customer_id_to_ledger[customer_id] = ledger_account_id

# Generate random discount values between 0 and 25
def random_discount():
    return str(round(random.uniform(0, 25)))

# Get today's date and generate a deadline date
today = datetime.date.today().isoformat()
deadline = (datetime.date.today() + datetime.timedelta(days=random.randint(1, 30))).isoformat()

# Pennylane API URL
url = "https://app.pennylane.com/api/external/v2/customer_invoices"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

responses = []

# Logging setup
with open("debug_log.txt", "w") as log_file:
    log_file.write("Starting invoice processing...\n")
    log_file.write(f"Available customer names in IC.json: {list(customer_name_to_id.keys())}\n")

# Process invoices
for invoice in invoice_data.get("QueryResponse", {}).get("Invoice", []):
    customer_name = invoice.get("CustomerRef", {}).get("name", "")
    customer_id = customer_name_to_id.get(customer_name)
    
    with open("debug_log.txt", "a") as log_file:
        log_file.write(f"\nProcessing invoice ID: {invoice.get('Id')} for Customer Name: {customer_name}\n")
    
    if customer_id is None:
        with open("debug_log.txt", "a") as log_file:
            log_file.write(f"Skipping invoice {invoice.get('Id')} - Customer name '{customer_name}' not found in IC.json\n")
        continue
    
    ledger_account_id = customer_id_to_ledger[customer_id]
    
    invoice_lines = []
    for line in invoice.get("Line", []):
        if "SalesItemLineDetail" in line:
            invoice_lines.append({
                "discount": {
                    "type": "absolute",
                    "value": random_discount()
                },
                "vat_rate": "FR_1_05",
                "ledger_account_id": ledger_account_id,
                "raw_currency_unit_price": str(line["SalesItemLineDetail"].get("UnitPrice", 0)),
                "unit": "piece",
                "label": line.get("Description", "No Description"),
                "quantity": line["SalesItemLineDetail"].get("Qty", 1)
            })
    
    if invoice_lines:  # Only create payload if there are valid invoice lines
        payload = {
            "currency": invoice.get("CurrencyRef", {}).get("value", "USD"),
            "language": "fr_FR",
            "discount": {
                "type": "absolute",
                "value": random_discount()
            },
            "invoice_lines": invoice_lines,
            "date": today,
            "deadline": deadline,
            "customer_id": customer_id,
            "pdf_invoice_free_text": invoice.get("CustomerMemo", {}).get("value", "")
        }
        
        with open("debug_log.txt", "a") as log_file:
            log_file.write(f"Sending payload for customer {customer_name} (ID: {customer_id}):\n")
            log_file.write(json.dumps(payload, indent=4) + "\n")
        
        response = requests.post(url, json=payload, headers=headers)
        try:
            response_data = {"invoice_id": invoice.get('Id'), "response": response.json()}
        except json.JSONDecodeError:
            response_data = {"invoice_id": invoice.get('Id'), "response": response.text}
        
        responses.append(response_data)
        with open("debug_log.txt", "a") as log_file:
            log_file.write(f"Response for Invoice {invoice.get('Id')}: {response.text}\n")

# Save responses to a JSON file
with open("invoice_responses.json", "w") as response_file:
    json.dump(responses, response_file, indent=4)

with open("debug_log.txt", "a") as log_file:
    log_file.write("\nInvoice processing completed.\n")
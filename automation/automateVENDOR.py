import json
import requests
import os

# Paths
parent_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(parent_dir, "saved JSON", "Vendor.json")
done_file_path = os.path.join(parent_dir, "done3.json")

# API details
url = "https://app.pennylane.com/api/external/v2/suppliers"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
     "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

# Load vendor data
with open(json_file_path, "r") as file:
    data = json.load(file)

vendors = data.get("QueryResponse", {}).get("Vendor", [])
responses = []

for vendor in vendors:
    payload = {
        "name": vendor.get("DisplayName", "")
    }
    
    response = requests.post(url, json=payload, headers=headers)
    responses.append({"vendor": vendor.get("DisplayName", ""), "response": response.json()})

# Save responses to done.json
with open(done_file_path, "w") as file:
    json.dump(responses, file, indent=4)

print(f"All vendor entries processed. Output saved to {done_file_path}")

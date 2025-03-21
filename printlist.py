import requests
import json

url = "https://app.pennylane.com/api/external/v2/ledger_accounts?page=2&per_page=1000"

headers = {
    "accept": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

response = requests.get(url, headers=headers)

# Save response to a JSON file
with open("try2.json", "w") as file:
    json.dump(response.json(), file, indent=4)

print("Response saved to try2.json")

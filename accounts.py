import requests

url = "https://app.pennylane.com/api/external/v2/ledger_accounts"

payload = {
    "number": "033",
    "label": "Accounts Payable (A/P)",
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
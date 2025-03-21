import requests

url = "https://app.pennylane.com/api/external/v2/suppliers"

payload = { "name": "Bob's Burger Joint" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
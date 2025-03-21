import os
import json
import requests

# API configuration
url = "https://app.pennylane.com/api/external/v2/ledger_accounts"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer -pqhAxQcgRen-FbQx12mHVgyiB73GUU-08WmfwH4tGk"
}

# Define paths
input_folder = "saved JSON"
output_folder = "JSON"
input_file = os.path.join(input_folder, "Accounts.json")
output_file = os.path.join(output_folder, "SavedAccounts.json")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the JSON data
with open(input_file, "r") as file:
    data = json.load(file)

# Check if the JSON is a dictionary with a key holding the list of accounts
if isinstance(data, dict):
    # Adjust this key based on your JSON structure
    data = data.get("accounts", [])
elif not isinstance(data, list):
    raise TypeError("Expected JSON data to be a list of dictionaries or a dictionary with a key holding the list.")

# Extract Id and Name, format Id, and send POST requests
responses = []
for entry in data:
    # Ensure each entry is a dictionary
    if not isinstance(entry, dict):
        print(f"Skipping invalid entry: {entry}")
        continue

    # Extract and format Id
    try:
        formatted_id = f"{int(entry['Id']):03}"
        name = entry["Name"]
    except KeyError as e:
        print(f"Missing key in entry {entry}: {e}")
        continue
    except ValueError as e:
        print(f"Invalid Id value in entry {entry}: {e}")
        continue

    # Prepare the payload
    payload = {
        "Id": formatted_id,
        "Name": name
    }

    # Send POST request
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        responses.append({
            "Id": formatted_id,
            "Name": name,
            "Response": response_data
        })
    except Exception as e:
        responses.append({
            "Id": formatted_id,
            "Name": name,
            "Error": str(e)
        })

# Save the responses to a new JSON file
with open(output_file, "w") as file:
    json.dump(responses, file, indent=4)

print(f"Responses saved to {output_file}")
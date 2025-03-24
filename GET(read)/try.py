from flask import Flask, redirect, request, session, url_for
import requests
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("PERSONAL_SECRET")

CLIENT_ID = os.getenv("UID")
CLIENT_SECRET = os.getenv("Secret")

# Match the registered URI exactly
REDIRECT_URI = "https://localhost:3000/api/callback/pennylane"

# OAuth endpoints provided by Pennylane
AUTHORIZATION_URL = "https://app.pennylane.com/oauth/authorize"
TOKEN_URL = "https://app.pennylane.com/oauth/token"
REVOKE_URL = "https://app.pennylane.com/oauth/revoke"

API_ENDPOINT = "https://app.pennylane.com/api/external/v2/customer_invoices?sort=-id"

@app.route("/")
def index():
    return '<a href="/login">Sign in with Pennylane</a>'

@app.route("/login")
def login():
    # Build the authorization URL with required parameters
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "read",
        "state": "random_state_string"
    }
    auth_url = requests.Request("GET", AUTHORIZATION_URL, params=params).prepare().url
    return redirect(auth_url)

# Change the route to match your registered callback URI
@app.route("/api/callback/pennylane")
def callback():
    # Retrieve authorization code and state from the callback URL
    code = request.args.get("code")
    state = request.args.get("state")

    # Exchange the authorization code for an access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    token_response = requests.post(TOKEN_URL, data=data)
    token_data = token_response.json()

    # Store tokens in the session for later use
    session["access_token"] = token_data.get("access_token")
    session["refresh_token"] = token_data.get("refresh_token")

    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))

    # Use the access token to retrieve data from a protected endpoint
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    api_response = requests.get(API_ENDPOINT, headers=headers)

    return f"<pre>{api_response.text}</pre>"

@app.route("/refresh")
def refresh():
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return redirect(url_for("login"))

    # Request a new access token using the refresh token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    token_response = requests.post(TOKEN_URL, data=data)
    token_data = token_response.json()

    session["access_token"] = token_data.get("access_token")
    session["refresh_token"] = token_data.get("refresh_token")

    return redirect(url_for("profile"))

@app.route("/revoke")
def revoke():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))

    # Revoke the current access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "token": access_token
    }
    revoke_response = requests.post(REVOKE_URL, data=data)

    # Clear the session after revoking the token
    session.clear()
    return "Token revoked. You have been logged out."

if __name__ == "__main__":
    # Configure to run on port 3000 with HTTPS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # You'll need to generate these certificates
    context.load_cert_chain('cert.pem', 'key.pem')

    app.run(host='localhost', port=3000, ssl_context=context, debug=True)
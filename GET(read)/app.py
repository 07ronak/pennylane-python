from flask import Flask, redirect, request, session, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("PERSONAL_SECRET")

CLIENT_ID = os.getenv("UID")
CLIENT_SECRET = os.getenv("Secret")

# For local testing:
REDIRECT_URI = "https://localhost:3000/api/callback/pennylane"
# For production deployment:
# REDIRECT_URI = "https://capia.ai/api/callback/pennylane"

# OAuth endpoints provided by Pennylane
AUTHORIZATION_URL = "https://app.pennylane.com/oauth/authorize"
TOKEN_URL = "https://app.pennylane.com/oauth/token"
REVOKE_URL = "https://app.pennylane.com/oauth/revoke"
API_ENDPOINT = "https://app.pennylane.com/api/external/v1/me"  # Example API endpoint

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
        "state": "random_state_string"  # For CSRF protection; in production, generate a unique value.
    }
    auth_url = requests.Request("GET", AUTHORIZATION_URL, params=params).prepare().url
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Retrieve authorization code and state from the callback URL
    code = request.args.get("code")
    state = request.args.get("state")
    # (Optional) Validate that the returned state matches the one you sent.

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
    app.run(debug=True)

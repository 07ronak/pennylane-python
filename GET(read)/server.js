const express = require("express");
const axios = require("axios");
const session = require("express-session");
const dotenv = require("dotenv");
const { URLSearchParams } = require("url");

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Session configuration
app.use(
  session({
    secret: process.env.PERSONAL_SECRET,
    resave: false,
    saveUninitialized: true,
  })
);

const CLIENT_ID = process.env.UID;
const CLIENT_SECRET = process.env.Secret;

// For local testing:
const REDIRECT_URI = "https://localhost:3000/api/callback/pennylane";
// For production deployment:
// const REDIRECT_URI = "https://capia.ai/api/callback/pennylane";

// OAuth endpoints provided by Pennylane
const AUTHORIZATION_URL = "https://app.pennylane.com/oauth/authorize";
const TOKEN_URL = "https://app.pennylane.com/oauth/token";
const REVOKE_URL = "https://app.pennylane.com/oauth/revoke";

// Example API endpoint
const API_ENDPOINT =
  "https://app.pennylane.com/api/external/v2/customer_invoices?sort=-id";

// Routes
app.get("/", (req, res) => {
  res.send('<a href="/login">Sign in with Pennylane</a>');
});

app.get("/login", (req, res) => {
  // Build the authorization URL with required parameters
  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    response_type: "code",
    scope: "suppliers:readonly",
    /* state: "random_state_string", // For CSRF protection */
  });

  const authUrl = `${AUTHORIZATION_URL}?${params.toString()}`;
  res.redirect(authUrl);
});

/* app.get("/login", (req, res) => {
  // Build the authorization URL with required parameters
  // Using URLSearchParams but ensuring the "+" is properly encoded
  const authUrl = `${AUTHORIZATION_URL}?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(
    REDIRECT_URI
  )}&response_type=code&state=random_state_string`;

  res.redirect(authUrl);
}); */

app.get("/api/callback/pennylane", async (req, res) => {
  // Retrieve authorization code and state from the callback URL
  const code = req.query.code;
  const state = req.query.state;
  // (Optional) Validate that the returned state matches the one you sent.

  try {
    // Exchange the authorization code for an access token
    const params = new URLSearchParams({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      code: code,
      redirect_uri: REDIRECT_URI,
      grant_type: "authorization_code",
    });

    const tokenResponse = await axios.post(TOKEN_URL, params);
    const tokenData = tokenResponse.data;

    // Store tokens in the session for later use
    req.session.access_token = tokenData.access_token;
    req.session.refresh_token = tokenData.refresh_token;

    res.redirect("/profile");
  } catch (error) {
    res.status(500).send(`Error exchanging code for token: ${error.message}`);
  }
});

app.get("/profile", async (req, res) => {
  const accessToken = req.session.access_token;
  if (!accessToken) {
    return res.redirect("/login");
  }

  try {
    // Use the access token to retrieve data from a protected endpoint
    const apiResponse = await axios.get(API_ENDPOINT, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: "application/json",
      },
    });

    res.send(`<pre>${JSON.stringify(apiResponse.data, null, 2)}</pre>`);
  } catch (error) {
    res.status(500).send(`API request error: ${error.message}`);
  }
});

app.get("/refresh", async (req, res) => {
  const refreshToken = req.session.refresh_token;
  if (!refreshToken) {
    return res.redirect("/login");
  }

  try {
    // Request a new access token using the refresh token
    const params = new URLSearchParams({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      refresh_token: refreshToken,
      grant_type: "refresh_token",
    });

    const tokenResponse = await axios.post(TOKEN_URL, params);
    const tokenData = tokenResponse.data;

    req.session.access_token = tokenData.access_token;
    req.session.refresh_token = tokenData.refresh_token;

    res.redirect("/profile");
  } catch (error) {
    res.status(500).send(`Refresh token error: ${error.message}`);
  }
});

app.get("/revoke", async (req, res) => {
  const accessToken = req.session.access_token;
  if (!accessToken) {
    return res.redirect("/login");
  }

  try {
    // Revoke the current access token
    const params = new URLSearchParams({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      token: accessToken,
    });

    await axios.post(REVOKE_URL, params);

    // Clear the session after revoking the token
    req.session.destroy();
    res.send("Token revoked. You have been logged out.");
  } catch (error) {
    res.status(500).send(`Token revocation error: ${error.message}`);
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

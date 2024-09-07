import requests
import webbrowser
from urllib.parse import urlencode

class ZohoBooksIntegration:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = "https://accounts.zoho.com/oauth/v2"
        self.access_token = None
        self.refresh_token = None

    def generate_authorization_url(self):
        params = {
            "scope": "ZohoBooks.fullaccess.all",
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "access_type": "offline",
            "prompt": "consent"
        }
        auth_url = f"{self.base_url}/auth?{urlencode(params)}"
        return auth_url

    def get_tokens(self, code):
        url = f"{self.base_url}/token"
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            return tokens
        else:
            raise Exception(f"Error getting tokens: {response.text}")

    def refresh_access_token(self):
        url = f"{self.base_url}/token"
        data = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "refresh_token"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            return tokens
        else:
            raise Exception(f"Error refreshing access token: {response.text}")

    def make_api_request(self, endpoint, method="GET", data=None):
        url = f"https://books.zoho.com/api/v3/{endpoint}"
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"
        }
        response = requests.request(method, url, headers=headers, json=data)
        return response.json()

# Usage example
if __name__ == "__main__":
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    redirect_uri = "http://localhost:8000/callback"  # Use a valid redirect URI

    zoho_books = ZohoBooksIntegration(client_id, client_secret, redirect_uri)

    # Generate and open the authorization URL
    auth_url = zoho_books.generate_authorization_url()
    print(f"Please visit this URL to authorize the application: {auth_url}")
    webbrowser.open(auth_url)

    # After authorization, you'll be redirected to the redirect_uri with a code parameter
    code = input("Enter the code from the redirect URL: ")

    # Get access and refresh tokens
    tokens = zoho_books.get_tokens(code)
    print("Access token:", zoho_books.access_token)
    print("Refresh token:", zoho_books.refresh_token)

    # Make an API request (e.g., get list of invoices)
    invoices = zoho_books.make_api_request("invoices")
    print("Invoices:", invoices)
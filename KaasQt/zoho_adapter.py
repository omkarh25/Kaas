from pyzohoapi import ZohoBooks
from pyzohoapi.exceptions import ZohoUnauthorized
import time
import requests

class ZohoBooksIntegration:
    def __init__(self, organization_id, region, client_id, client_secret, refresh_token):
        self.organization_id = organization_id
        self.region = region
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.api = self._create_api()

    def _create_api(self):
        return ZohoBooks(
            self.organization_id,
            region=self.region,
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.refresh_token
        )

    def _handle_unauthorized(self, func):
        try:
            return func()
        except ZohoUnauthorized:
            print("Token expired. Refreshing...")
            self.api = self._create_api()  # This will use the refresh token to get a new access token
            time.sleep(1)  # Wait a bit before retrying
            return func()  # Retry the operation

    def get_transactions_list(self, organization_id, account_id, oauth_token):
        url = "https://www.zohoapis.com/books/v2/banktransactions"
        
        headers = {
            "Authorization": f"Zoho-oauthtoken {oauth_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "organization_id": organization_id,
            "account_id": account_id
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.text}"

    def list_chart_of_accounts(self, showbalance=False, filter_by=None, sort_column=None, last_modified_time=None):
        """
        List all chart of accounts along with pagination.

        Args:
            showbalance (bool): Boolean to get current balance of accounts.
            filter_by (str): Filter accounts based on its account type and status.
                Allowed Values: AccountType.All, AccountType.Active, AccountType.Inactive,
                AccountType.Asset, AccountType.Liability, AccountType.Equity,
                AccountType.Income, AccountType.Expense.
            sort_column (str): Sort accounts. Allowed Values: account_name, account_type.
            last_modified_time (str): Last modified time of the accounts.

        Returns:
            dict: JSON response containing the list of chart of accounts.
        """
        def fetch_accounts():
            query_params = []
            
            if showbalance:
                query_params.append("showbalance=true")
            if filter_by:
                query_params.append(f"filter_by={filter_by}")
            if sort_column:
                query_params.append(f"sort_column={sort_column}")
            if last_modified_time:
                query_params.append(f"last_modified_time={last_modified_time}")

            query_string = "&".join(query_params)
            return self.api.get("chartofaccounts", query_string)

        return self._handle_unauthorized(fetch_accounts)

# Usage example
if __name__ == "__main__":
    organization_id = "60029851485"
    region = "in"  # or "eu", "in", "au" depending on your Zoho region
    client_id = "1000.0SQKHCOMCQOBELBGMDTL9K1904GNIX"
    client_secret = "883e9bf021e43cb0b4147a2353319f4be8167138e5"
    refresh_token = "1000.771feed74357afe2ccade1a93468f5e3.4e9988a9b75ff6d743b294cfe80ee43a"
    account_id = "60029851485"

    zoho_books = ZohoBooksIntegration(organization_id, region, client_id, client_secret, refresh_token)


    # List all chart of accounts
    accounts = zoho_books.list_chart_of_accounts()
    print(accounts)

    # List chart of accounts with balance and filtered by active accounts
    active_accounts = zoho_books.list_chart_of_accounts(showbalance=True, filter_by="AccountType.Active")
    print(active_accounts)
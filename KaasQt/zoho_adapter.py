from pyzohoapi import ZohoBooks
from pyzohoapi.exceptions import ZohoUnauthorized
import time

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

    def get_invoices(self):
        return self._handle_unauthorized(lambda: list(self.api.Invoice()))

    def create_invoice(self, invoice_data):
        def create():
            invoice = self.api.Invoice()
            for key, value in invoice_data.items():
                setattr(invoice, key, value)
            invoice.Create()
            return invoice
        return self._handle_unauthorized(create)

    def update_invoice(self, invoice_id, update_data):
        def update():
            invoice = self.api.Invoice(invoice_id)
            for key, value in update_data.items():
                setattr(invoice, key, value)
            invoice.Update()
            return invoice
        return self._handle_unauthorized(update)

    def delete_invoice(self, invoice_id):
        return self._handle_unauthorized(lambda: self.api.Invoice(invoice_id).Delete())

# Usage example
if __name__ == "__main__":
    organization_id = "60029851485"
    region = "in"  # or "eu", "in", "au" depending on your Zoho region
    client_id = "1000.XLGUUGKKJEQXJ9TUD8NFY7STPW96FH"
    client_secret = "71c30889b94a739457057eee7683f546dc2d3b81a5"
    refresh_token = "your_refresh_token"

    zoho_books = ZohoBooksIntegration(organization_id, region, client_id, client_secret, refresh_token)

    # Get all invoices
    invoices = zoho_books.get_invoices()
    for invoice in invoices:
        print(f"Invoice ID: {invoice.ID}, Number: {invoice.Number}")

    # Create a new invoice
    new_invoice_data = {
        "customer_id": "customer_id_here",
        "line_items": [{"item_id": "item_id_here", "quantity": 1}],
        # Add other required fields
    }
    new_invoice = zoho_books.create_invoice(new_invoice_data)
    print(f"New invoice created with ID: {new_invoice.ID}")

    # Update an invoice
    update_data = {"status": "sent"}
    updated_invoice = zoho_books.update_invoice(new_invoice.ID, update_data)
    print(f"Invoice {updated_invoice.ID} updated")

    # Delete an invoice
    if zoho_books.delete_invoice(new_invoice.ID).IsDeleted:
        print(f"Invoice {new_invoice.ID} deleted")
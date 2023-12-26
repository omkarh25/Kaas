import os
from datetime import datetime
import requests
from dotenv import load_dotenv
import excelmodels as em 
import pandas as pd

# Load environment variables from .env file
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Make sure to set this in your .env file

# Function to send message to Discord
def send_discord_message(message: str):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    print(f"Message sent: {message} - Status code: {response.status_code}")

# Function to check for payments due today and send messages
def check_and_alert_payments():
    # Load your data into the RecurringModel list
    
    
    recurring_data = em.load_sheet_into_model(sheet_name, file_path, em.RecurringModel)

    df = em.models_to_dataframe(recurring_data)
    today = datetime.now().date()

    # Filter for payments due today
    messages = []
    for _, row in df.iterrows():
        recurring_payment = em.RecurringModel(**row.to_dict())
        if recurring_payment.nextpayment == today:
            messages.append(f"Payment Alert: {recurring_payment.account} has a payment of {recurring_payment.cost} due today!")

    # Send a message to Discord for each payment
    if messages:
        full_message = "\n".join(messages)
        print(full_message)
        send_discord_message(full_message)
    else:
        print("No payments due today.")

# Run the function
check_and_alert_payments()

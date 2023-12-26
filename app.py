import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
import pandas as pd
from pydantic import BaseModel
import excelmodels as em
from typing import List

# Load environment variables
load_dotenv('credentials.env')

# Fetch credentials from .env file
ADMIN_USERNAME = os.getenv('admin_username')
ADMIN_PASSWORD = os.getenv('admin_password')

# Log file path
log_file_path = 'loginlog.csv'

# Function to verify credentials and log login time
def verify_credentials(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Log login time
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, datetime.now().isoformat()])
        return True
    return False

def get_last_login_time():
    try:
        with open(log_file_path, mode='r') as file:
            last_login = None
            for row in reversed(list(csv.reader(file))):
                if row[0] == ADMIN_USERNAME:
                    last_login = row[1]
                    # Parse the ISO format datetime and reformat it
                    last_login_datetime = datetime.fromisoformat(last_login)
                    last_login_formatted = last_login_datetime.strftime('%d %b %y %I:%M %p')
                    return last_login_formatted
            return last_login
    except FileNotFoundError:
        return None  # File not found or no logins yet

# App main page
def main_page():
    st.title('Excel Data Viewer')
    last_login_time = get_last_login_time()
    if last_login_time:
        st.write(f"Last login time: {last_login_time}")

    # Load data from Excel (you might want to do this part once and cache the results)
    # file_path = 'Kaas.xlsm' # Update with the actual path to your Excel file
    # sheet_names = pd.ExcelFile(file_path).sheet_names

    def load_sheet_into_model(sheet_name: str, file_path: str, model: BaseModel) -> List[BaseModel]:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return [model(**row.to_dict()) for _, row in df.iterrows()]

    # Loading data from each sheet
    accounts_data = load_sheet_into_model(em.sheet_names[0], em.file_path, em.AccountModel)  # Update 'Sheet1' with actual name
    recurring_data = load_sheet_into_model(em.sheet_names[1], em.file_path, em.RecurringModel)
    transactions_data = load_sheet_into_model(em.sheet_names[2], em.file_path, em.TransactionModel)

    # Function to convert Pydantic models to DataFrame
    def models_to_dataframe(models):
        return pd.DataFrame([model.dict() for model in models])

    # Streamlit app
    st.title('Excel Data Viewer')

    # Dropdown to select which sheet to view
    option = st.selectbox(
        'Which data would you like to view?',
        ('Accounts', 'Recurring Payments', 'Transactions')
    )

    # Displaying data based on selection
    if option == 'Accounts':
        st.subheader("Accounts Data")
        st.dataframe(models_to_dataframe(accounts_data))
    elif option == 'Recurring Payments':
        st.subheader("Recurring Payments Data")
        st.dataframe(models_to_dataframe(recurring_data))
    else:
        st.subheader("Transactions Data")
        st.dataframe(models_to_dataframe(transactions_data))
        
def login_page():
    st.title('Login')
    username = st.text_input("Username", "")
    password = st.text_input("Password", "", type="password")
    if st.button('Login'):
        if verify_credentials(username, password):
            st.session_state['authenticated'] = True
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password. Please try again.")

# App routing
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    main_page()
else:
    login_page()
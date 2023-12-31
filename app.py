import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
import pandas as pd
import excelmodels as em
from typing import List
import utils


# Load environment variables
load_dotenv('credentials.env')

# Fetch credentials from .env file
ADMIN_USERNAME = os.getenv('admin_username')
ADMIN_PASSWORD = os.getenv('admin_password')

# Log file path
log_file_path = 'loginlog.csv'

accounts_data = em.load_sheet_into_model(em.acc_file_path, em.AccountModel)  # Update 'Sheet1' with actual name
recurring_data = em.load_sheet_into_model(em.rec_file_path, em.RecurringModel)
transactions_data = em.load_sheet_into_model(em.trn_file_path, em.TransactionModel)

# Function to verify credentials and log login time
def verify_credentials(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Log login time
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, datetime.now().isoformat()])
        return True
    return False

st.set_page_config(
    page_title="Kaas",
    layout="wide"
)

st.title("Kaas")

# App main page
def main_page():
    # Sidebar for navigation
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Accounts Data', 'Recurring Payments Data', 'Transactions Data', 'Transactions Due'])

    # Login details and last login time
    st.title('Excel Data Viewer')
    last_login_time = utils.get_second_last_login_date()
    if last_login_time:
        st.write(f"Last login time: {last_login_time}")

    # Displaying data based on sidebar navigation
    if page == 'Accounts Data':
        st.dataframe(em.models_to_dataframe(accounts_data))
    elif page == 'Recurring Payments Data':
        st.dataframe(em.models_to_dataframe(recurring_data))
    elif page == 'Transactions Data':
        st.dataframe(em.models_to_dataframe(transactions_data))
    elif page == 'Transactions Due':
        st.subheader("Transactions Due")
        # Fetch and display transactions with checkboxes (assuming a function popUp() exists for fetching transactions)
        transactions_due = check_transactions()  # Modify this line to the actual function call that fetches due transactions
        for transaction in transactions_due:
            st.checkbox(transaction, value=False) 
        
def check_transactions():    
    due_transactions = utils.get_rec_due_transactions(utils.last_login_date, utils.recurring_models)
    print(due_transactions)
    
    # Convert due transactions to a format suitable for display and selection
    transaction_options = {
        f"{trans.rec_id}: {trans.account} - {trans.nextpayment}": trans 
        for trans in due_transactions
    }
    
    return transaction_options 
   
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
    # login_page()
    main_page()
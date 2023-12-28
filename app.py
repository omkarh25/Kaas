import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
import pandas as pd
from pydantic import BaseModel
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

# App main page
def main_page():
    st.title('Excel Data Viewer')
    last_login_time = utils.get_second_last_login_date()
    if last_login_time:
        st.write(f"Last login time: {last_login_time}")
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
        st.dataframe(em.models_to_dataframe(accounts_data))
    elif option == 'Recurring Payments':
        st.subheader("Recurring Payments Data")
        st.dataframe(em.models_to_dataframe(recurring_data))
    else:
        st.subheader("Transactions Data")
        st.dataframe(em.models_to_dataframe(transactions_data))
        
def popUp():    
    due_transactions = utils.get_rec_due_transactions(utils.last_login_date, utils.recurring_models)
    print(due_transactions)
    
    # Convert due transactions to a format suitable for display and selection
    transaction_options = {
        f"{trans.rec_id}: {trans.account} - {trans.nextpayment}": trans 
        for trans in due_transactions
    }
    
    # Present transactions to the user
    selected_transactions = st.multiselect(
        "Select transactions to add:",
        options=list(transaction_options.keys())
    )
    
    # Confirm button to add transactions
    if st.button("Add Selected Transactions"):
        # Read existing transactions
        transactions_df = pd.read_csv("Kaas_transactions.csv")
        
        new_rows = []  # A list to collect new rows
        for trans_key in selected_transactions:
            trans = transaction_options[trans_key]
            date_str = trans.nextpayment.strftime('%d-%b-%y')
            new_transaction = em.TransactionModel(
                date=date_str, 
                description=trans.account, 
                amount=trans.cost, 
                area=trans.spend_area.value
            )
            new_rows.append(new_transaction.dict())  # Append new transaction data as a dictionary

        # Convert new_rows to a DataFrame and concatenate with the existing transactions
        new_transactions_df = pd.DataFrame(new_rows)
        transactions_df = pd.concat([transactions_df, new_transactions_df], ignore_index=True)
        
         # Write updated DataFrame back to CSV
        transactions_df.to_csv("Kaas_transactions.csv", index=False)
       
        st.success("Transactions added successfully!")
        
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
    popUp()
    main_page()
else:
    # login_page()
    popUp()
    main_page()
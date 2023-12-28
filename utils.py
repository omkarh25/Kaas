from datetime import datetime
from dotenv import load_dotenv
import excelmodels as em 
import pandas as pd
from pydantic import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta

########################################### util funcs (temp)

# Load the data
loginlog_path = "loginlog.csv"
recurring_path = "Kaas_recurring.csv"

def load_recurring_data(recurring_path):
    df = pd.read_csv(recurring_path)
    models = []
    for _, row in df.iterrows():
        try:
            model = em.RecurringModel(**row)
            models.append(model)
        except ValidationError as e:
            print(f"Error loading data: {e}")
    return models

def get_second_last_login_date():
    loginlog_df = pd.read_csv(loginlog_path)
    second_last_login_str = loginlog_df.iloc[-2, 1]  # Getting the second last entry from the second column
    second_last_login_date = datetime.fromisoformat(second_last_login_str).date()
    return second_last_login_date

def get_rec_due_transactions(last_login, recurring_models):
    transactions_to_add = []
    for model in recurring_models:
        due = False  # Flag to determine if transaction is due

        # Calculate if the transaction should be added based on frequency and last login
        if model.frequency.value == 'yearly':
            due = model.nextpayment <= last_login and model.nextpayment > last_login - relativedelta(years=1)
        elif model.frequency.value == 'quarterly':
            due = model.nextpayment <= last_login and model.nextpayment > last_login - relativedelta(months=3)
        elif model.frequency.value == 'monthly':
            due = model.nextpayment <= last_login and model.nextpayment > last_login - relativedelta(months=1)
        elif model.frequency.value == 'weekly':
            due = model.nextpayment <= last_login and model.nextpayment > last_login - timedelta(days=7)

        if due:
            transactions_to_add.append(model)

    return transactions_to_add


def update_next_payment_dates(models):
    for model in models:
        if model.frequency.value == 'yearly':
            model.nextpayment += relativedelta(years=1)
        elif model.frequency.value == 'quarterly':
            model.nextpayment += relativedelta(months=3)
        elif model.frequency.value == 'monthly':
            model.nextpayment += relativedelta(months=1)
        elif model.frequency.value == 'weekly':
            model.nextpayment += timedelta(days=7)

    return models



# # Determine the last login date
last_login_date = get_second_last_login_date()
# print('lastlogin: ',last_login_date)
# print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# # Find due recurring transactions
recurring_models = load_recurring_data(recurring_path)
# due_transactions = get_rec_due_transactions(last_login_date, recurring_models)
# print(due_transactions)

# print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# # Optionally, update next payment dates
# updated_recurring = update_next_payment_dates(due_transactions)
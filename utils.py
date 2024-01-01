from datetime import datetime
from dotenv import load_dotenv
import excelmodels as em 
import pandas as pd
from pydantic import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


########################################### util funcs (temp)

# Load the data
loginlog_path = em.loginlog_path
recurring_path = em.rec_file_path

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
# last_login_date = get_second_last_login_date()
# print('lastlogin: ',last_login_date)
# print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# # Find due recurring transactions
# recurring_models = load_recurring_data(recurring_path)
# due_transactions = get_rec_due_transactions(last_login_date, recurring_models)
# print(due_transactions)

# print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# # Optionally, update next payment dates
# updated_recurring = update_next_payment_dates(due_transactions)

##############################################################################
# Load the recurring and transactions CSV to use as templates
recurring_df = pd.read_csv(em.rec_file_path)
transactions_template = pd.read_csv(em.trn_file_path).columns

# Function to calculate the next payment date based on the frequency
def calculate_next_payment(start_date, frequency):
    # Handling different frequencies
    if frequency.lower() == 'yearly':
        return start_date.replace(year=start_date.year + 1)
    elif frequency.lower() == 'quarterly':
        months_to_add = 3
    elif frequency.lower() == '6months':
        months_to_add = 6
    elif frequency.lower() == 'monthly':
        months_to_add = 1
    elif frequency.lower() == 'weekly':
        return start_date + timedelta(days=7)
    else:
        return start_date

    # Handling month addition for non-yearly and non-weekly frequencies
    month = start_date.month - 1 + months_to_add
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = min(start_date.day, [31, 29 if year % 4 == 0 and not year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime(year, month, day)

# Function to generate transactions up to a future date
def generate_transactions(future_date):
    # Convert future_date from string to datetime
    future_date = datetime.strptime(future_date, '%Y-%m-%d')

    # List to hold generated transactions
    generated_transactions = []

    # Iterate over each recurring transaction
    for index, row in recurring_df.iterrows():
        # Adjusting the date parsing to accommodate 'month/day/year' format
        next_payment_date = datetime.strptime(row['nextpayment'], '%m/%d/%Y')
        frequency = row['frequency']
        description = row['account']
        amount = row['cost']
        trans_acc = row['trans_acc']
        src_account = row['src_acc']
        
        # Generate transactions until the future date
        while next_payment_date <= future_date:
            transaction = {
                'date': next_payment_date.strftime('%Y-%m-%d'),
                'description': description,
                'amount': amount,
                'trans_acc': trans_acc,
                'src_account': src_account
                # Include other fields from the transactions template as needed
            }
            generated_transactions.append(transaction)
            next_payment_date = calculate_next_payment(next_payment_date, frequency)

    # Convert to DataFrame and sort by date
    transactions_df = pd.DataFrame(generated_transactions)
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    transactions_df = transactions_df.sort_values(by='date')

    return transactions_df

# Example usage: Generate transactions up to a certain future date
future_date = '2025-01-01'
transactions_df = generate_transactions(future_date)
output_path = 'csv/transactions_2025.csv'
transactions_df.to_csv(output_path, index=False)



Finance freedom app

I need a finance management python app with following features:
Core App features

1. Ingest ‘recurring_expenses’,’transactions’ and ‘accounts’ sheets from excel sheet and store it in mongodb.
   2.Remember last visit and unpaid Recurring expenses should be presented as check mark box transactions and should show the expected account balance for each account after deducting the recurring expenses
2. It should compare the expected balance with actual balance and justify difference above 5000 for each account. Justification should be logged in transactions. If less than 5k add it as miscellaneous transaction

Discord Notifications

1. Every day morning at the 830 AM giving a list of days transaction. Alert if expected bank balance is below payment amount for the day
2. Give discord button option to mark paid and log it into transaction
3. Runway alert at 4 weeks

Streamlit User dashboard

1. Main Dashboard with net account value trajectory, ETA to Zero, Last visit, Area of spends pie chart, stats box
2. Ability to view and crud ‘recurring_expenses’,’transactions’ and ‘accounts’ pages
3. Recurring expenses calendar grouped and colour coded

UI Flow:Login — recurring transactions checkbox floating window with skip option — Update account values - Main Dashboard

Function to automatically advance the next due date in  based on last login and generate unattended recurring transaction list. This list of transactions will be presented as floating check boxes and upto checking they should automatically added to list of transactions. This should also change the current \_value accordingly

I need a function to automatically add recurring transactions to the list of transactions based on 'frequency' field. This should be based on the last login date.

I need to present this list into a streamlit pop upbox upon login. If checked these transaction should be automatically added to Kaas_transactions.csv. Analyze app.py and suggest edit to make it work.

Based on the recurring.csv uploaded, can you give me a python program to generate a transactions list based on the recurring transactions columns 'frequency' and 'nextpayment'. the function should take a future date as an arg and generate the transaction list as per the uploaded 'transactions.csv' columns format 



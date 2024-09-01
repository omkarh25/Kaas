import pandas as pd
import os
import requests
from datetime import datetime, timedelta

class PaymentProcessor:
    def __init__(self, excel_file, sheet_name):
        self.df = pd.read_excel(excel_file, sheet_name=sheet_name)
        self.today = datetime.today().date()

    def filter_payments(self):
        self.df['Date'] = pd.to_datetime(self.df['Date']).dt.date
        print("Converted 'Date' to datetime format.")
        self.df['Paid'] = self.df['Paid'].astype(str).str.lower() == 'yes'
        print("Normalized 'Paid' to boolean.")

        self.today_payments = self.df[(self.df['Date'] == self.today) & (~self.df['Paid'])]
        print(f"Filtered today's payments: {len(self.today_payments)} records found.")
        self.past_due_payments = self.df[(self.df['Date'] < self.today) & (~self.df['Paid'])]
        print(f"Filtered past due payments: {len(self.past_due_payments)} records found.")
        self.upcoming_week_payments = self.df[(self.df['Date'] > self.today) & (self.df['Date'] <= self.today + timedelta(days=7)) & (~self.df['Paid'])]
        print(f"Filtered upcoming week payments: {len(self.upcoming_week_payments)} records found.")

    def generate_markdown(self, output_file):
        with open(output_file, 'w') as f:
            f.write("# Transactions\n\n")
            f.write("## Today's Payments\n")
            f.write(self._generate_todo_list(self.today_payments))
            f.write("\n## Past Due Payments\n")
            f.write(self._generate_todo_list(self.past_due_payments))
            f.write("\n## Upcoming Week Payments\n")
            f.write(self._generate_todo_list(self.upcoming_week_payments))

    def _generate_todo_list(self, df):
        todo_list = df.apply(lambda row: f"- [ ] {', '.join(row.astype(str))}", axis=1).tolist()
        return "\n".join(todo_list) + "\n"

def excel_to_markdown(excel_file, sheet_name, output_file):
    processor = PaymentProcessor(excel_file, sheet_name)
    processor.filter_payments()
    processor.generate_markdown(output_file)

# Usage
excel_file = 'Kaas.xlsx'
sheet_name = 'FreedomBlast(Future)'
output_file = '/Users/omkar/Documents/Obsidian Vault/4_DayToDay/31-Aug-24.md'

excel_to_markdown(excel_file, sheet_name, output_file)

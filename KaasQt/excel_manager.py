import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, config):
        self.config = config
        self.excel_file = None
        self.sheets = {}
        self.load_excel(config.get('excel_file', ''))

    def load_excel(self, file_path):
        if file_path and os.path.exists(file_path):
            try:
                self.excel_file = pd.ExcelFile(file_path)
                self.sheets = {sheet: pd.read_excel(self.excel_file, sheet) for sheet in self.excel_file.sheet_names}
                print(f"Loaded Excel file: {file_path}")
                print(f"Available sheets: {self.get_sheet_names()}")
            except Exception as e:
                print(f"Error loading Excel file: {e}")
        else:
            print(f"Excel file not found: {file_path}")
        
        # Ensure 'Freedom(Future)' and 'Transactions(Past)' sheets exist
        if 'Freedom(Future)' not in self.sheets:
            self.sheets['Freedom(Future)'] = pd.DataFrame()
        if 'Transactions(Past)' not in self.sheets:
            self.sheets['Transactions(Past)'] = pd.DataFrame()

    def get_sheet_names(self):
        return list(self.sheets.keys()) if self.excel_file else []

    def get_sheet_data(self, sheet_name):
        return self.sheets.get(sheet_name)

    def process_transactions(self, selected_rows):
        future_sheet = self.sheets['Freedom(Future)']
        past_sheet = self.sheets['Transactions(Past)']

        for index in selected_rows:
            row = future_sheet.iloc[index]
            new_row = {
                'TrNo': past_sheet['TrNo'].max() + 1 if not past_sheet.empty else 1,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Description': row['Description'],
                'Amount': row['Amount'],
                'PaymentMode': row['PaymentMode'],
                'AccID': row['AccID'],
                'Department': row['Department'],
                'Comments': row['Comments'],
                'Category': row['Category'],
                'DeductedReceivedThrough': row['DeductedReceivedThrough'],
                'ExpectedPaymentDate': row['Date']
            }
            past_sheet = pd.concat([past_sheet, pd.DataFrame([new_row])], ignore_index=True)

        future_sheet = future_sheet.drop(selected_rows).reset_index(drop=True)

        self.sheets['Freedom(Future)'] = future_sheet
        self.sheets['Transactions(Past)'] = past_sheet

        # Save changes to Excel file
        with pd.ExcelWriter(self.config['excel_file'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            future_sheet.to_excel(writer, sheet_name='Freedom(Future)', index=False)
            past_sheet.to_excel(writer, sheet_name='Transactions(Past)', index=False)

        print("Transactions processed successfully")
        self.refresh_all_sheets()

    def refresh_all_sheets(self):
        self.load_excel(self.config['excel_file'])
import pandas as pd
import openpyxl
import quantstats as qs

# # Step 1: Load the Excel File
# file_path = r'C:\Users\user\Desktop\Kaas\StrategyAdmin\userexcel\omkar.xlsx'  # Change this to your file path

# # Read the 'DTD' sheet
# dtd_data = pd.read_excel(file_path, sheet_name='DTD', engine='openpyxl')

# # Convert 'Amount' to a numeric value (if needed)
# # This assumes 'Amount' is stored as a string with currency symbols.
# dtd_data['Amount'] = dtd_data['Amount'].replace('[₹,]', '', regex=True).astype(float)

# # Specify the date format for your 'Date' column if known, or leave as None for automatic parsing
# date_format = None  # Update this with your date format, e.g., '%Y-%m-%d' or leave as None

# # Aggregate 'Amount' by 'Date' to calculate 'NetPnL'
# aggregated_data = dtd_data.groupby('Date').agg(NetPnL=('Amount', 'sum')).reset_index()
# aggregated_data['Date'] = pd.to_datetime(aggregated_data['Date'], format=date_format, errors='coerce')
# aggregated_data['Day'] = aggregated_data['Date'].dt.day_name()
# # print(aggregated_data)

# # Write the new data to a 'DTD_Daily' sheet
# # with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
# #     # Load existing book and ensure other sheets remain intact
# #     writer.book = openpyxl.load_workbook(file_path)
# #     # Write new sheet
# #     aggregated_data.to_excel(writer, sheet_name='DTD_Daily', index=False)
# #     writer.save()

# csv_path = 'omkar_dtd.csv'

# aggregated_data.to_csv(csv_path)

# Load the CSV file
csv_file_path = r'C:\Users\user\Desktop\Kaas\omkar_dtd.csv'  # Update this to the actual file path

# Read the CSV file
dtd_data = pd.read_csv(csv_file_path)

# Convert 'Date' to datetime and set as index
dtd_data['Date'] = pd.to_datetime(dtd_data['Date'])
dtd_data.set_index('Date', inplace=True)

# Ensure 'NetPnL' is a float
dtd_data['NetPnL'] = dtd_data['NetPnL'].astype(float)

# Use QuantStats to plot calendar heatmap of 'NetPnL'
qs.plots.histogram(dtd_data['NetPnL'])
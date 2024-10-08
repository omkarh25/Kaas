import xlwings as xw
import pandas as pd
import sys

def process_excel_file():
    # Open the Excel file
    file_path = r'/Users/omkar/Downloads/Kaas (1).xlsx'

    try:
        # Start an instance of Excel and open the workbook
        app = xw.App(visible=False)  # Keep Excel in the background
        wb = xw.Book(file_path)
    except Exception as e:
        print("Error: Unable to open Excel file. Please check permissions.")
        print("You may need to grant permission to Python to control Excel.")
        print("Error details:", str(e))
        sys.exit(1)

    try:
        sheet = wb.sheets['Freedom(Future)']

        # Load the data from the sheet into a pandas DataFrame
        data = sheet.range('A1').expand().options(pd.DataFrame, header=1).value

        # Convert the "Date" column to a datetime object using the specific date format
        data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y')

        # Sort by "Date" column in ascending order
        data_sorted = data.sort_values(by='Date').reset_index(drop=False)

        # Renumber the "TrNo" column sequentially
        data_sorted['TrNo'] = range(1, len(data_sorted) + 1)

        # Convert the "Date" column back to the required format
        data_sorted['Date'] = data_sorted['Date'].dt.strftime('%d-%b-%y')

        # Write the sorted and renumbered data back to the Excel sheet
        sheet.range('A2').value = data_sorted.values

        # Set the date format in Excel explicitly for the "Date" column (B column)
        date_column_range = sheet.range('B2:B' + str(len(data_sorted) + 1))
        date_column_range.number_format = 'DD-MMM-YY'

        # Save the workbook and close
        wb.save()
        # wb.close()
        # app.quit()

        print("Sorting and renumbering complete!")
    except Exception as e:
        print("An error occurred while processing the Excel file:")
        print(str(e))
    finally:
        # Close the workbook and quit Excel, even if an error occurred
        if 'wb' in locals():
            print("Closing the workbook")
            # wb.close()
        if 'app' in locals():
            print("Quitting the Excel application")
            # app.quit()
            

if __name__ == "__main__":
    process_excel_file()
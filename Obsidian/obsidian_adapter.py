import pandas as pd
import os
import requests

def excel_to_markdown(excel_file, sheet_name, output_file):
    # Read the Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Get the first five rows
    df_subset = df.head(5)
    
    # Convert DataFrame to a list of to-do items
    todo_list = df_subset.apply(lambda row: f"- [ ] {', '.join(row.astype(str))}", axis=1).tolist()
    
    # Write the to-do list to the output file
    with open(output_file, 'w') as f:
        f.write("# Transactions\n\n")
        f.write("\n".join(todo_list))
        f.write("\n")
        
# send telegram message
def send_telegram_message(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=data)

    print(f"To-do list has been written to {output_file}")

# Usage
excel_file = 'Kaas.xlsx'
sheet_name = 'FreedomBlast(Future)'
output_file = '/Users/omkar/Documents/Obsidian Vault/4_DayToDay/31-Aug-24.md'

excel_to_markdown(excel_file, sheet_name, output_file)

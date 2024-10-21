# Author: Dhaval Patel. Codebasics Inc.

import openai
import json
import os
import sys
from dotenv import load_dotenv
import xlwings as xw
import pandas as pd

DIR_PATH = os.getcwd()
sys.path.append(DIR_PATH)

ENV_PATH = os.path.join(DIR_PATH, "kaas.env")
# load the kaas.env file
load_dotenv(ENV_PATH)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_big_loans(loan_amt):
    """
    Gets the accounts with "CurrentBalance" greater than or equal to the given loan_amt
    Args:
        df (pd.DataFrame): The input DataFrame
        loan_amt (float): compare this amount with 'CurrentBalance' column
    """
    
    accounts_df = xw.Book(r'Agents/ExcelAgent/Kaas.xlsx').sheets['Accounts(Present)'].range('A1:Z1000').options(pd.DataFrame, index=False).value
    print(accounts_df.head())
    return accounts_df[accounts_df['CurrentBalance'] >= loan_amt]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_big_loans",
            "description": """Function to get the list of big loans from the excel sheet based on the loan amount.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "loanAmount": {
                    "type": "number",
                    "description": "Amount specified by user e.g 10000.00 Rs",
                },
                },
                "required": ["loanAmount"],
                "additionalProperties": False
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
    {"role": "user", "content": "Hi, can you tell me loans above 20000 Rs?"}
]

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print(response.choices[0].message.content)
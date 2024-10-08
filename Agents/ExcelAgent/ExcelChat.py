import os
import sys
import pandas as pd
from pandasai import Agent
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import xlwings as xw

DIR_PATH = os.getcwd()
sys.path.append(DIR_PATH)

ENV_PATH = os.path.join(DIR_PATH, "kaas.env")
# load the kaas.env file
load_dotenv(ENV_PATH)

# use xlwings to read the excel file and load 'Accounts(Present)' sheet into a pandas dataframe
accounts_df = xw.Book(r'Agents/ExcelAgent/Kaas.xlsx').sheets['Accounts(Present)'].range('A1:Z1000').options(pd.DataFrame, index=False).value
print(accounts_df.head())

def get_big_loans(df, loan_amt):
    """
    Gets the accounts with "CurrentBalance" greater than or equal to the given loan_amt
    Args:
        df (pd.DataFrame): The input DataFrame
        loan_amt (float): compare this amount with 'CurrentBalance' column
    """
    return df[df['CurrentBalance'] >= loan_amt]

if __name__ == "__main__":
    # Initialize OpenAI LLM
    llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

    agent = Agent([accounts_df], memory_size=10)
    agent.add_skills(get_big_loans)


    # Chat with the agent
    response = Agent.chat("Get all big loans of more than 10000 Rs")
    print(response)
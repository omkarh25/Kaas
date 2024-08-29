import os
import pandas as pd
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse


# Define the absolute path to the Excel file
file_path = os.path.join(os.path.dirname(__file__), '..', 'E and I Tracker.xlsx')

# Read E and I Tracker.xlsx and load 'Transactions(Past)' sheet
transactions_past_df = pd.read_excel(r'/Users/omkar/Desktop/Kaas/backend/E and I Tracker.xlsx', sheet_name='Transactions(Past)')

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://pandabi.ai (you can also configure it in your .env file)
os.environ["PANDASAI_API_KEY"] = ""

agent = Agent(
    [transactions_past_df],
    config={"verbose": True, "response_parser": StreamlitResponse},
)

print(agent.chat("Plot Department wise income and expense"))
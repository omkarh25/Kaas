import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
from langchain_community.llms import Ollama 


llm = ChatGroq(model_name="llama3-70b-8192", api_key = "")

transactions_past_df = pd.read_excel(r'/Users/omkar/Desktop/Kaas/backend/E and I Tracker.xlsx', sheet_name='Transactions(Past)')

df = SmartDataframe(transactions_past_df, config={"llm": llm})

print( df.chat('What are the deparment wise expenses?'))
print( df.chat('How much did SPY - 008 get till now?'))
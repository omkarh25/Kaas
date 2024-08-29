import pandas as pd
import sqlite3
import chainlit as cl
from openai import AsyncOpenAI
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
from langchain_groq.chat_models import ChatGroq 
import sqlite3
import os

llm = ChatGroq(model_name="llama3-70b-8192", api_key = "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")

@cl.on_chat_start
def start_chat():
    # Set initial message history
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message
async def main(message: cl.Message):
    # Retrieve message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    # Load data
    # df = pd.read_excel('data.xlsx')
    # df = pd.read_csv('data.csv')
    # Read E and I Tracker.xlsx and load 'Transactions(Past)' sheet
    transactions_past_df = pd.read_excel(r'/Users/omkar/Desktop/Kaas/backend/E and I Tracker.xlsx', sheet_name='Transactions(Past)')


    df = SmartDataframe(transactions_past_df, config={"llm": llm})
    
    question = message.content
    response = df.chat(question)
    msg = cl.Message(content=response)
    
    await msg.send()

    # Update message history and send final message
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
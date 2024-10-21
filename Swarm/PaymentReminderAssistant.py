import os
from swarm import Agent
from swarm.repl import run_demo_loop
import dotenv
from openai import OpenAI
import gradio as gr
import pandas as pd
from datetime import datetime
# Load environment variables
dotenv.load_dotenv(dotenv_path="kaas.env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Function to load 'Kaas_1.xlsm' and read 'Freedom(Future)' sheet
def load_kaas_file():
    file_path = r'Swarm/Kaas_1.xlsm'
    if os.path.exists(file_path):
        print('file_path:', file_path)
        return pd.read_excel(file_path, sheet_name='Freedom(Future)')
    else:
        return None
    
def get_past_due_payments():
    """Get past due payments from the DataFrame. The values are in 'Date' column and in the format '5-OCT-24'"""
    df = load_kaas_file()
    today = pd.Timestamp.today().normalize()
    past_due_payments = df[df['Date'] < today]
    print('past_due_payments:', past_due_payments)
    return past_due_payments

def generate_completion(role, task, content):
    """Generate a completion using OpenAI."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Define the User Interface Agent
user_interface_agent = Agent(
    name="User Interface Agent",
    instructions="Use the get_past_due_payments function to get the past due payments and present it to the user in a clear and concise manner.",
    functions=[get_past_due_payments],
)

def chatbot_interface(project_name, user_message):
    """Interface function to interact with the user."""
    past_due_payments = get_past_due_payments()
    
    if past_due_payments.empty:
        response = "There are no past due payments."
    else:
        response = "Here are the past due payments:\n\n"
        for _, row in past_due_payments.iterrows():
            response += f"Date: {row['Date']}, Amount: {row['Amount']}, Description: {row['Description']}\n"
    
    return [[user_message, response]]

# Gradio UI setup
with gr.Blocks() as demo:
    gr.Markdown("## Payment Reminder Assistant")
    
    project_dropdown = gr.Dropdown(
        choices=["Freedom(Future)"],  # List your projects here
        label="Select Project"
    )
    
    user_input = gr.Textbox(label="Your Message")
    
    chatbot_output = gr.Chatbot(label="Chatbot Response")
    
    submit_button = gr.Button("Send")
    
    submit_button.click(
        chatbot_interface,
        inputs=[project_dropdown, user_input],
        outputs=chatbot_output
    )

if __name__ == "__main__":
    demo.launch()

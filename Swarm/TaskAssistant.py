import os
from swarm import Agent
from swarm.repl import run_demo_loop
import dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
dotenv.load_dotenv(dotenv_path="kaas.env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

################### TOOLS ###################

################### Helper Tools ###################
def load_guidelines(project_name):
    """Load project guidelines from a Markdown file."""
    file_path = f'docs/{project_name}.md'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return "Guidelines not found for this project."

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

#################### Main Tool ####################
def provide_guidance(project_name, user_message):
    """Provide guidance based on the selected project and user message."""
    guidelines = load_guidelines(project_name)
    response = generate_completion(
        "task assistant",
        "Analyze the Excel header sheet summary thoroughly and give the user a comprehensive response to help user understand and complete the task.",
        f"{guidelines}\n\nUser: {user_message}"
    )
    
    # Return in the expected format for Gradio Chatbot
    return [[user_message, response]]

################### AGENTS ###################

# Define the User Interface Agent
user_interface_agent = Agent(
    name="User Interface Agent",
    instructions="You are a user interface agent that handles interactions with the user regarding project tasks.",
    functions=[provide_guidance],
)

################### Interface Function ###################
def chatbot_interface(project_name, user_message):
    """Interface function to interact with the user."""
    return provide_guidance(project_name, user_message)

################### Assistant Call Sequence ###################

## 1. chatbot_interface -- project_name, user_message -- provide_guidance -- load_guidelines, generate_completion -- guidelines, response

################### GRADIO UI ###################

# Gradio UI setup
with gr.Blocks() as demo:
    gr.Markdown("## Task Assistant Chatbot")
    
    project_dropdown = gr.Dropdown(
        choices=["AccQTPrd", "FabricKaas", "KaasMainSheetSummary"],  # List your projects here
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
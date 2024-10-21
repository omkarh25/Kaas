from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time

load_dotenv('kaas.env')
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)


# --------------------------------------------------------------
# Upload file
# --------------------------------------------------------------
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = client.files.create(file=open(path, "rb"), purpose="assistants")
    return file


# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------
def create_assistant(file):
    """
    You currently cannot set the temperature for Assistant via the API.
    """
    assistant = client.beta.assistants.create(
        name="WhatsApp AirBnb Assistant",
        instructions="You're a helpful WhatsApp assistant that can assist guests that are staying in our Paris AirBnb. Use your knowledge base to best respond to customer queries. If you don't know the answer, say simply that you cannot help with question and advice to contact the host directly. Be friendly and funny.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id],
    )
    return assistant




# --------------------------------------------------------------
# Thread management
# --------------------------------------------------------------
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread)
    print(f"To {name}:", new_message)
    return new_message


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve("asst_rNfGqSgJfJD6aQjj2EA9mJIF")

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message


# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------

# load technical documentation into string
def load_technical_doc(file_path):
    with open(file_path, "r") as file:
        return file.read()


# function to get all assistants
def get_all_assistants(to_file=False):
    assistants = client.beta.assistants.list(
        order="desc",
        limit="100",
    )
    if to_file:
        with open("assistants.txt", "w") as file:
            for assistant in assistants.data:
                file.write(f"{assistant.id}\n")
    else:
        print(len(assistants.data))
        return assistants

# funtion to get all files
def get_all_files(to_file=False):
    files = client.files.list()
    return files
    
# Retrieve a specific fileid by filename
def get_file_id(filename):
    files = get_all_files()
    for file in files:
        if file.filename == filename:
            print(f"Found file {filename} with id {file.id}")
            return file.id
    return None

# Retrieve a specific assistant by name
def get_assistant_id(name):
    assistants = get_all_assistants()
    for assistant in assistants.data:
        if assistant.name == name:
            print(f"Found assistant {name} with id {assistant.id}")
            return assistant.id
    return None
    
# delete all assistants
def delete_all_assistants():
    my_assistants = get_all_assistants()
    for assistant in my_assistants.data:
        response = client.beta.assistants.delete(assistant.id)
        print(response)
        
# delete all files
def delete_all_files():
    my_files = get_all_files()
    for file in my_files.data:
        response = client.files.delete(file.id)
        print(response)
        
if __name__ == "__main__":
    delete_all_files()
    
    
    # jio_router_config = load_technical_doc("docs/JioRouterConfig.md")
    # user_query = "I am able to access my website from other network but not when I am connected to Jio network. Below are Router settings. Please help."
    # new_message = generate_response(user_query, "123", "Omkar")
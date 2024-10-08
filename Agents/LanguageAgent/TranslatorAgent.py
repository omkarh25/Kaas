from openai import OpenAI
import json
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

DIR_PATH = os.getcwd()
sys.path.append(DIR_PATH)

ENV_PATH = os.path.join(DIR_PATH, "kaas.env")
# load the kaas.env file
load_dotenv(ENV_PATH)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
def transcribe_audio(file_path):
    """
    Transcribes audio from a given file path using the Whisper API.

    Args:
        file_path (str): The path to the audio file to be transcribed.

    Returns:
        str: The transcribed text from the audio file.
    """
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        save_to_json(r'Agents/Transcriptions/08OCT24_translations.json', transcription.text)
    return transcription.text

def translate_audio(file_path):
    """
    Translates audio from a given file path using the Whisper API.

    Args:
        file_path (str): The path to the audio file to be translated.

    Returns:
        str: The translated text from the audio file.
    """
    with open(file_path, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1", 
            file=audio_file
        )
        save_to_json(r'Agents/Transcriptions/08OCT24_translations.json', translation.text)
    return translation.text

def save_to_json(file_path, data):
    """
    Saves data with a timestamp to a JSON file. If the file exists, it appends the data;
    otherwise, it creates a new file and writes the data.

    Args:
        file_path (str): The path to the JSON file where the data will be saved.
        data (str): The data to be saved in the file.

    Raises:
        FileNotFoundError: If the file does not exist and cannot be created.
        json.JSONDecodeError: If the file contains invalid JSON and cannot be parsed.
    """
    timestamp = datetime.now().isoformat()
    entry = {"timestamp": timestamp, "text": data}
    
    try:
        with open(file_path, "r+") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
            
            existing_data.append(entry)
            f.seek(0)
            f.truncate()
            json.dump(existing_data, f, indent=2)
    except FileNotFoundError:
        with open(file_path, "w") as f:
            json.dump([entry], f, indent=2)
            
def generate_bullet_points(text):
    """
    Generates bullet point summaries from a given text using the GPT-4o model.

    Args:
    text (str): The text to be summarized in bullet points.

    Returns:
    str: The summarized text in bullet point format.
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a summarizer. You are given a text and you need to summarize it in numbered bullet points"},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print(completion.choices[0].message.content)
    save_to_json(r'Agents/Summaries/summaries.json', completion.choices[0].message.content)
    return completion.choices[0].message.content

if __name__ == "__main__":
    text = translate_audio(r'Agents/Test.m4a')
    generate_bullet_points(text)
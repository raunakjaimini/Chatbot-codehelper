import requests
import json
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini 2 API key from environment variables
GEMINI2_API_KEY = os.getenv("GEMINI2_API_KEY")

url = "https://api.gemini2.example.com/assist"  # Replace with Gemini 2 endpoint

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {GEMINI2_API_KEY}'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "prompt": final_prompt
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        actual_response = response_data.get('text', 'No response found.')
        return actual_response
    else:
        print("Error:", response.text)
        return "Error occurred while generating response."

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),
    outputs="text"
)
interface.launch()

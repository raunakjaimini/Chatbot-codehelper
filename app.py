import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini 2 API key from environment variables
GEMINI2_API_KEY = os.getenv("GOOGLE_API_KEY")

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
        return "Error occurred while generating response."

# Streamlit app
st.title("Multi-Language Code Assistant")

prompt = st.text_area("Enter your Prompt", "")
if st.button("Submit"):
    response = generate_response(prompt)
    st.text_area("Response", response, height=300)

# Show prompt history
if st.checkbox("Show History"):
    st.write("Prompt History:")
    for p in history:
        st.write(p)

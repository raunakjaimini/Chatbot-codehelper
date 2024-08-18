import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini 2 API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define the Gemini 2 API endpoint
url = "https://api.gemini2.example.com/assist"  # Replace with the actual Gemini 2 endpoint

# Set up headers for the API request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {GOOGLE_API_KEY}'
}

# Initialize history to keep track of prompts
history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "prompt": final_prompt
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses

        response_data = response.json()
        actual_response = response_data.get('text', 'No response found.')
        return actual_response
    except requests.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        return "Connection error: Could not reach the API."
    except requests.Timeout as e:
        print(f"Timeout error occurred: {e}")
        return "Timeout error: The request took too long to complete."
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return f"HTTP error: {e.response.status_code} {e.response.reason}"
    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        return "Error occurred while generating response."

# Streamlit app UI
st.title("Multi-Language Code Assistant")

# User input
prompt = st.text_area("Enter your Prompt", "")

# Button to submit the prompt
if st.button("Submit"):
    response = generate_response(prompt)
    st.text_area("Response", response, height=300)

# Option to display prompt history
if st.checkbox("Show History"):
    st.write("Prompt History:")
    for p in history:
        st.write(p)

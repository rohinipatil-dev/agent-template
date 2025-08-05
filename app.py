import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Create OpenAI client
client = OpenAI()

# Function to get video transcript
def get_transcript(video_id):
    base_url = "https://www.youtube.com/watch?v="
    url = base_url + video_id

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    transcript = soup.find("div", {"class": "cue style-scope ytd-transcript-body-renderer"})

    return transcript.text if transcript else "No transcript available"

# Function to summarize text
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ]
    )

    return response.choices[0].message.content

# Streamlit UI
st.title("YouTube Video Summarizer")
video_id = st.text_input("Enter YouTube Video ID:")

if st.button("Summarize"):
    if video_id:
        transcript = get_transcript(video_id)
        if transcript != "No transcript available":
            summary = summarize_text(transcript)
            st.write(summary)
        else:
            st.write("No transcript available for this video.")
    else:
        st.write("Please enter a valid YouTube Video ID.")
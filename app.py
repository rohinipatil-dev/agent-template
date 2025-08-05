import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

def extract_transcript(video_url):
    # Extract video id from URL
    video_id = video_url.split('=')[1]
    
    # Construct the API URL
    api_url = f"http://video.google.com/timedtext?lang=en&v={video_id}"
    
    # Send GET request and parse the result
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the text from the transcript tags
    transcript = [str(tag.string) for tag in soup.find_all('text')]
    
    return ' '.join(transcript)

def generate_summary(transcript):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("YouTube Video Transcript Extractor and Summarizer")
    
    video_url = st.text_input("Enter YouTube Video URL")
    
    if st.button("Extract and Summarize"):
        if video_url != "":
            with st.spinner("Extracting Transcript..."):
                transcript = extract_transcript(video_url)
            with st.spinner("Generating Summary..."):
                summary = generate_summary(transcript)
            
            st.subheader("Transcript")
            st.write(transcript)
            
            st.subheader("Summary")
            st.write(summary)
        else:
            st.error("Please enter a YouTube video URL.")
            
if __name__ == "__main__":
    main()
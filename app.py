import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_transcript = " ".join([i['text'] for i in transcript])
    return text_transcript

def get_ai_response(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('YouTube Video Speech to Text Converter')
    video_id = st.text_input('Enter YouTube Video ID:')
    if st.button('Convert'):
        with st.spinner('Fetching transcript...'):
            transcript = get_transcript(video_id)
        st.write('Transcript:', transcript)
        with st.spinner('Getting AI response...'):
            ai_response = get_ai_response(transcript)
        st.write('AI Response:', ai_response)

if __name__ == "__main__":
    main()
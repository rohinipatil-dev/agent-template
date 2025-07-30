import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_joke(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly chatbot that tells jokes about programming."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

st.title('Programming Jokes Chatbot')

user_input = st.text_input("Ask me for a programming joke")

if user_input:
    joke = get_joke(user_input)
    st.text(joke)
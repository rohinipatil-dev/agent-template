import openai
import streamlit as st
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_joke(prompt):
    client = openai.OpenAI()
    response = client.chat.models.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly chatbot that tells jokes about programming."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    st.title('Programming Jokes Chatbot')
    user_input = st.text_input("Ask me for a joke!")
    if st.button('Get Joke'):
        joke = get_joke(user_input)
        st.text(joke)

if __name__ == "__main__":
    main()
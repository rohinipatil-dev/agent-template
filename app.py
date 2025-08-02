import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_joke():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a programming joke."},
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('Programming Jokes Chatbot')
    joke_button = st.button('Get a Joke')

    if joke_button:
        joke = get_joke()
        st.write(joke)

if __name__ == "__main__":
    main()
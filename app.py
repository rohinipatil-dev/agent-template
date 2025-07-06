import streamlit as st
from openai import OpenAI, ChatCompletion

openai = OpenAI('your_openai_api_key')

def get_joke():
    message = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ]
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message
    )
    return response.choices[0].message.content

def main():
    st.title("Friendly Joke Bot")
    joke_button = st.button("Tell me a joke")
    if joke_button:
        joke = get_joke()
        st.write(joke)

if __name__ == "__main__":
    main()
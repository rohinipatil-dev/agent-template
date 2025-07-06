import openai
import streamlit as st
import requests

openai.api_key = 'your_openai_api_key'

def get_joke():
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    response = requests.get(url)
    joke = response.json()[0]
    return f"{joke['setup']} - {joke['punchline']}"

def chat_with_bot(message):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=message,
      temperature=0.5,
      max_tokens=100
    )
    return response.choices[0].text.strip()

def main():
    st.title("Programming Joke Bot")
    user_input = st.text_input("You: ", "")
    if st.button("Send"):
        if "joke" in user_input.lower():
            joke = get_joke()
            st.write(f"Bot: {joke}")
        else:
            response = chat_with_bot(user_input)
            st.write(f"Bot: {response}")

if __name__ == "__main__":
    main()
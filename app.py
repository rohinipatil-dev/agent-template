import streamlit as st
from openai import OpenAI, ChatCompletion

openai = OpenAI("your-api-key")

def generate_joke():
    chat_prompt = {
        'messages': [
            {"role": "system", "content": "You are a funny AI that generates jokes."},
            {"role": "user", "content": "Tell me a joke."},
        ]
    }

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=chat_prompt['messages']
    )

    joke = response.choices[0].message.content
    return joke

def main():
    st.title("AI Joke Generator")
    if st.button("Generate Joke"):
        joke = generate_joke()
        st.markdown(joke)

if __name__ == "__main__":
    main()
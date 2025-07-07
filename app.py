import streamlit as st
from openai import OpenAI

def generate_joke(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a funny AI that generates jokes."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title("AI Joke Generator")
    joke_prompt = st.text_input("Enter a topic for the joke:")
    if st.button("Generate Joke"):
        joke = generate_joke(joke_prompt)
        st.text(joke)

if __name__ == "__main__":
    main()
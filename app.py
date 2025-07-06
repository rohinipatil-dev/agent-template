import os
import streamlit as st
from openai import OpenAI

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_cat_fact():
    # Generate a chat message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a random cat fact."},
        ],
    )

    # Extract the assistant's reply
    fact = response['choices'][0]['message']['content']
    return fact

def main():
    st.title("Random Cat Facts")

    if st.button("Generate Fact"):
        fact = get_cat_fact()
        st.write(fact)

if __name__ == "__main__":
    main()
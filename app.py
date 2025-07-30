import streamlit as st
from openai import OpenAI

def get_random_cat_fact():
    client = OpenAI()
    response = client.chat.completions.create(
        model="text-davinci-002",
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable assistant specialized in cat facts."
            },
            {
                "role": "user",
                "content": "Tell me a random fact about cats."
            }
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Random Cat Fact Generator")
    if st.button("Generate"):
        fact = get_random_cat_fact()
        st.write(fact)

if __name__ == "__main__":
    main()
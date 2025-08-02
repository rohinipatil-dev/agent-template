import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_cat_fact():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a cat fact."},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title("Cat Fact Bot")
    st.write("Click the button to get a cat fact!")
    if st.button("Get Cat Fact"):
        fact = get_cat_fact()
        st.write(fact)

if __name__ == "__main__":
    main()
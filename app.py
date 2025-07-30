import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_cat_fact():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant specialized in cat facts."},
            {"role": "user", "content": "Tell me a random fact about cats."},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title('Cat Fact Generator')
    if st.button('Generate Cat Fact'):
        fact = get_cat_fact()
        st.write(fact)

if __name__ == "__main__":
    main()
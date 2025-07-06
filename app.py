import streamlit as st
from openai import OpenAI, ChatCompletion

openai_secret_manager = st.secrets["openai"]
client = OpenAI(openai_secret_manager)

def get_cat_fact():
    prompt = "Tell me a random cat fact."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title("Random Cat Facts")
    if st.button("Generate Fact"):
        fact = get_cat_fact()
        st.write(fact)

if __name__ == "__main__":
    main()
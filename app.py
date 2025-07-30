import streamlit as st
from openai import OpenAI

client = OpenAI()

def translate_to_kannada(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates English to Kannada."},
            {"role": "user", "content": f'Translate "{text}" to Kannada.'}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("English to Kannada Translation")
    user_input = st.text_input("Enter text in English")
    if st.button("Translate"):
        if user_input:
            with st.spinner("Translating..."):
                result = translate_to_kannada(user_input)
                st.success(result)
        else:
            st.warning("Please enter text for translation.")

if __name__ == "__main__":
    main()
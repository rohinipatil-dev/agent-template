import streamlit as st
from openai import OpenAI

def translate_to_kannada(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="text-davinci-003",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that translates English to Kannada."
            },
            {
                "role": "user",
                "content": f"{text}"
            }
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('English to Kannada Translation')
    text = st.text_input('Enter your text in English')
    if st.button('Translate'):
        if text:
            translation = translate_to_kannada(text)
            st.text_area('Translation in Kannada:', translation)
        else:
            st.write('Please enter some text for translation')

if __name__ == "__main__":
    main()
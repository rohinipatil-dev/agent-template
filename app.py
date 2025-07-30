import streamlit as st
from openai import OpenAI

client = OpenAI()

def translate_to_kannada(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'Translate the following English text to Kannada: "{text}"'}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('English to Kannada Translator')
    user_input = st.text_input('Enter your text in English')
    if st.button('Translate'):
        if user_input:
            translated_text = translate_to_kannada(user_input)
            st.text(translated_text)
        else:
            st.warning('Please enter text for translation')

if __name__ == '__main__':
    main()
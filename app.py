import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Define the system message
system_message = {"role": "system", "content": "You are a helpful assistant that translates English to Kannada."}

def translate_to_kannada(text):
    # User message
    user_message = {"role": "user", "content": f'Translate "{text}" to Kannada.'}

    # Get the response from the model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message]
    )

    # Extract the translated text from the response
    translated_text = response.choices[0].message.content

    return translated_text

def main():
    st.title('English to Kannada Translator')

    user_input = st.text_input('Enter your text in English')

    if st.button('Translate'):
        if user_input:
            translated_text = translate_to_kannada(user_input)
            st.write(f'Translated Text: {translated_text}')
        else:
            st.write('Please enter some text to translate.')

if __name__ == '__main__':
    main()
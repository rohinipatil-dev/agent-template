import streamlit as st
from openai import OpenAI, ChatCompletion

def generate_joke(client):
    prompt = {
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant that generates jokes.'},
            {'role': 'user', 'content': 'Tell me a joke.'}
        ]
    }

    response = client.chat_completions.create(model="gpt-3.5-turbo", messages=prompt)
    joke = response.choices[0].message.content
    return joke

def main():
    st.title('AI Joke Generator')

    client = OpenAI(api_key='your-api-key')

    if st.button('Generate Joke'):
        joke = generate_joke(client)
        st.text(joke)

if __name__ == '__main__':
    main()
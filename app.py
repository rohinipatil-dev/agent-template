import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title('Python Programming Assistant')
    st.write('Ask me any Python programming question and I will do my best to provide a helpful answer.')

    user_input = st.text_input('Enter your question here:')
    if st.button('Ask'):
        if user_input:
            st.write('Thinking...')
            response = get_response(user_input)
            st.write(response)
        else:
            st.write('Please enter a question.')

if __name__ == '__main__':
    main()
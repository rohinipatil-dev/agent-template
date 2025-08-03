import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('Python Programming Assistant')
    user_input = st.text_input("Ask your Python programming question here:")
    if st.button('Get Answer'):
        if user_input:
            with st.spinner('Getting AI response...'):
                ai_response = get_ai_response(user_input)
            st.write(ai_response)
        else:
            st.write('Please enter a question.')

if __name__ == '__main__':
    main()
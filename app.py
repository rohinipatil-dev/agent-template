import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_answer(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title('Python Programming Assistant')
    question = st.text_input('Enter your Python programming question here:')
    if st.button('Get Answer'):
        if question:
            answer = get_answer(question)
            st.text(answer)
        else:
            st.warning('Please input a question.')

if __name__ == "__main__":
    main()
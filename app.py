import streamlit as st
from openai import OpenAI

# Create the OpenAI client
client = OpenAI()

def ask_openai(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers Python programming questions."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title('Python Programming Assistant')
    question = st.text_input('Ask your Python programming question here:')
    if st.button('Get Answer'):
        if question:
            answer = ask_openai(question)
            st.markdown(f'**Answer:** {answer}')
        else:
            st.warning('Please input a question.')

if __name__ == "__main__":
    main()
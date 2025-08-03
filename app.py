import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_ai_response(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Python Programming Assistant")
    question = st.text_input("Ask your Python programming question here:")
    if st.button("Get Answer"):
        if question:
            with st.spinner('Getting AI response...'):
                response = get_ai_response(question)
            st.write(response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
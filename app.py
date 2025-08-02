import streamlit as st
from openai import OpenAI

# Create OpenAI client
client = OpenAI()

# Function to communicate with the AI model
def ask_gpt3(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title("Python Programming Assistant")
    question = st.text_input("Ask your Python programming question here:")
    if st.button("Get Answer"):
        if question:
            with st.spinner('Getting the answer...'):
                answer = ask_gpt3(question)
            st.write(answer)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
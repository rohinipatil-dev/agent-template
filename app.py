import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that specializes in dogs health."},
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title("Dog Health Assistant")
    user_input = st.text_input("Please enter your question about dog's health:")
    if st.button("Submit"):
        if user_input:
            response = get_ai_response(user_input)
            st.write(response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
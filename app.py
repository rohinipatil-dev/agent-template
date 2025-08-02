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

def app():
    st.title("AI Agent for Purchasing Used HONDA CRV Hybrid")
    user_input = st.text_input("Enter your query:")
    if st.button("Submit"):
        if user_input:
            response = get_ai_response(user_input)
            st.write(response)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    app()
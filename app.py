import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in the medical and surgical field."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Medical and Surgical Assistant")
    st.write("Hello! I'm an AI assistant specialized in the medical and surgical field. How can I assist you today?")
    
    user_input = st.text_input("Please enter your query:")
    
    if st.button("Submit"):
        if user_input:
            st.write("AI Assistant is generating the response...")
            response = get_ai_response(user_input)
            st.write(response)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    main()
import streamlit as st
from openai import OpenAI, ChatCompletion

# Initialize OpenAI client
client = OpenAI()

# Streamlit UI
st.title("Python Programming Chatbot")
user_input = st.text_input("Ask your Python programming question:")

if st.button("Submit"):
    if user_input:
        # Create a chat model
        model = "gpt-3.5-turbo"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
        response = client.chat_completions.create(
            model=model,
            messages=messages,
        )

        # Get the response content
        chatbot_response = response.choices[0].message.content

        # Display the chatbot response
        st.write(chatbot_response)
    else:
        st.write("Please enter a question.")
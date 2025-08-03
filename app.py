import streamlit as st
from openai import OpenAI

client = OpenAI()

def chat_with_ai(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Zebra Robotics AI Chat Agent")
    user_input = st.text_input("Ask something about Zebra Robotics:")
    if st.button("Send"):
        if user_input:
            response = chat_with_ai(user_input)
            st.markdown(f'**AI:** {response}')
        else:
            st.write("Please enter a question or statement.")

if __name__ == "__main__":
    main()
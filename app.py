import streamlit as st
from openai import OpenAI

def get_ai_response(message):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("AI Assistant")
    user_input = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        response = get_ai_response(user_input)
        st.text_area("Answer:", value=response)

if __name__ == "__main__":
    main()
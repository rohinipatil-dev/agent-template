import streamlit as st
from openai import OpenAI

class PythonChatBot:
    def __init__(self):
        self.client = OpenAI()

    def get_answer(self, question):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content

def main():
    st.title('Python Programming Assistant')
    question = st.text_input('Ask your Python programming question:')
    if st.button('Get Answer'):
        bot = PythonChatBot()
        answer = bot.get_answer(question)
        st.text_area('Answer:', value=answer, height=200, max_chars=None)

if __name__ == "__main__":
    main()
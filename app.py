import streamlit as st
from openai import OpenAI, ChatCompletion
import os

class CatFactsAgent:
    def __init__(self):
        self.client = OpenAI(os.getenv("OPENAI_API_KEY"))

    def get_cat_fact(self):
        prompt = "Tell me a random fact about cats."
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

def main():
    st.title("Cat Facts Agent")
    cat_facts_agent = CatFactsAgent()
    fact_button = st.button("Get a Cat Fact")
    if fact_button:
        cat_fact = cat_facts_agent.get_cat_fact()
        st.markdown(cat_fact)

if __name__ == "__main__":
    main()
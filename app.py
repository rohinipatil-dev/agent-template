import streamlit as st
from openai import OpenAI

client = OpenAI()

def get_cat_fact():
    prompt = "Give me a random fact about cats."
    response = client.chat.completions.create(
        model="text-davinci-002",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    st.title('Cat Facts AI')
    st.image('https://images.unsplash.com/photo-1561948955-570b270e7c36', use_column_width=True)
    st.write('Welcome to Cat Facts AI. Click the button below to get a random fact about cats.')
    if st.button('Get Cat Fact'):
        fact = get_cat_fact()
        st.markdown(f'**Fact:** {fact}')

if __name__ == "__main__":
    main()
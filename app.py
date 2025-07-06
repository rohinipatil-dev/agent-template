import streamlit as st
import openai
from openai.api_resources.completion import Completion

# Initialize OpenAI client
openai.api_key = 'your-openai-api-key'
client = openai.OpenAI()

# Define a function to get a joke from OpenAI
def get_joke():
    prompt = "Tell a programming joke."
    response = client.completions.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    joke = response.choices[0].text.strip()
    return joke

# Streamlit app
def main():
    st.title('Friendly Programming Joke Bot')
    if st.button('Tell me a joke'):
        joke = get_joke()
        st.write(joke)

if __name__ == "__main__":
    main()
import streamlit as st
from openai import OpenAI

# Create the OpenAI client
client = OpenAI()

def get_wellness_suggestion():
    # The system message sets the behavior of the assistant
    system_message = {"role": "system", "content": "You are a helpful assistant that suggests easy practical & scientific tools for daily wellness which can be practiced in minutes."}

    # The user message provides a prompt to the assistant
    user_message = {"role": "user", "content": "Can you suggest a wellness practice for me today?"}

    # Create a conversation with the assistant
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message]
    )

    # Extract the assistant's message from the response
    assistant_message = response.choices[0].message.content

    return assistant_message

def main():
    st.title('Daily Wellness Suggestion Agent')
    st.write('This AI agent will suggest easy practical & scientific tools for daily wellness which can be practiced in minutes.')

    if st.button('Get Wellness Suggestion'):
        with st.spinner('Generating wellness suggestion...'):
            suggestion = get_wellness_suggestion()
        st.success('Suggestion generated successfully!')
        st.write(suggestion)

if __name__ == "__main__":
    main()
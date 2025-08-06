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

def main():
    st.title("AI Resume Creator")
    st.write("Let's create your resume with the help of AI!")

    name = st.text_input("Enter your full name")
    email = st.text_input("Enter your email")
    phone = st.text_input("Enter your phone number")
    education = st.text_input("Enter your education details")
    experience = st.text_input("Enter your work experience")
    skills = st.text_input("Enter your skills")
    projects = st.text_input("Enter your projects")
    certifications = st.text_input("Enter your certifications")

    if st.button("Generate Resume"):
        user_message = f"Create a resume for {name} with email {email} and phone number {phone}. Education details are {education}. Work experience includes {experience}. Skills are {skills}. Projects include {projects}. Certifications include {certifications}."
        ai_response = get_ai_response(user_message)
        st.text_area("Your Resume:", value=ai_response, height=200, max_chars=None)

if __name__ == "__main__":
    main()
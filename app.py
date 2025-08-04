import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfFileReader
from io import BytesIO
import requests

def read_pdf(file):
    pdf = PdfFileReader(file)
    text = ""
    for page in range(pdf.getNumPages()):
        text += pdf.getPage(page).extractText()
    return text

def ask_gpt3(question, document):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": document},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("AI Document Assistant")
    st.write("Upload a PDF document and ask a question based on the document.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        document = read_pdf(uploaded_file)
        question = st.text_input("What is your question?")
        if st.button("Ask"):
            with st.spinner('Generating answer...'):
                answer = ask_gpt3(question, document)
                st.write(answer)

if __name__ == "__main__":
    main()
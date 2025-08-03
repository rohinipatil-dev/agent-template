import streamlit as st
import PyPDF2
from openai import OpenAI

# Create OpenAI client
client = OpenAI()

def extract_text_from_pdf(file):
    pdf_file_obj = open(file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file_obj.close()
    return text

def get_answer_from_ai(pdf_text, question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Here is some information: {pdf_text}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

st.title('AI PDF Assistant')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
question = st.text_input("Enter your question:")

if uploaded_file is not None and question:
    pdf_text = extract_text_from_pdf(uploaded_file)
    answer = get_answer_from_ai(pdf_text, question)
    st.write(answer)
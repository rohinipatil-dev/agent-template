import streamlit as st
from openai import OpenAI
import PyPDF2
from io import BytesIO

# Create the OpenAI client
client = OpenAI()

def extract_text_from_pdf(file):
    pdf_file_obj = BytesIO(file.getbuffer())
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    return text

def get_answer_from_ai(document_text, user_query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": document_text},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message.content

st.title("AI Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    document_text = extract_text_from_pdf(uploaded_file)
    user_query = st.text_input("Enter your query:")
    if user_query:
        answer = get_answer_from_ai(document_text, user_query)
        st.write(answer)
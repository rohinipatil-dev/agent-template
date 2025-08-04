import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from chromadb import ChromaDB
import numpy as np

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB
db = ChromaDB(dimensions=768)

def extract_pdf_text(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            text=chunk
        )
        embeddings.append(response.embeddings[0])
    return embeddings

def store_embeddings(embeddings, chunks):
    for embedding, chunk in zip(embeddings, chunks):
        db.insert(np.array(embedding), chunk)

def retrieve_chunks(query):
    query_embedding = generate_embeddings([query])[0]
    results = db.query(np.array(query_embedding), num_results=3)
    return [result[1] for result in results]

def generate_response(chunks, query):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for chunk in chunks:
        messages.append({"role": "document", "content": chunk})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

st.title("AI Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
if uploaded_file is not None:
    text = extract_pdf_text(uploaded_file)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    store_embeddings(embeddings, chunks)
    st.success("Document uploaded and processed successfully!")

query = st.text_input("Enter your query:")
if st.button("Ask"):
    if uploaded_file is None:
        st.error("Please upload a document first.")
    else:
        chunks = retrieve_chunks(query)
        response = generate_response(chunks, query)
        st.write(response)
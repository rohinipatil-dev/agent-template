import streamlit as st
from openai import OpenAI
from PyPDF2.pdf import PdfReader
import faiss
import numpy as np
from tiktoken import Tokenizer

# Initialize OpenAI client
client = OpenAI()

# Initialize tokenizer
tokenizer = Tokenizer()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to generate embeddings
def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embed_text.create(model="text-embedding-3-small", text=chunk)
        embeddings.append(response.embedding)
    return embeddings

# Function to create FAISS index
def create_faiss_index(embeddings):
    index = faiss.IndexFlatL2(len(embeddings[0]))
    faiss.normalize_L2(embeddings)
    index.add(np.array(embeddings))
    return index

# Function to retrieve top chunks
def retrieve_top_chunks(query, chunks, index, top_k=3):
    query_embedding = generate_embeddings([query])[0]
    faiss.normalize_L2(np.array([query_embedding]))
    distances, indices = index.search(np.array([query_embedding]), top_k)
    top_chunks = [chunks[i] for i in indices[0]]
    return top_chunks

# Function to generate answer
def generate_answer(query, top_chunks):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for chunk in top_chunks:
        messages.append({"role": "assistant", "content": chunk})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content

# Streamlit app
st.title("AI Agent with RAG model")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)

    query = st.text_input("Enter your question")
    if query:
        top_chunks = retrieve_top_chunks(query, chunks, index)
        answer = generate_answer(query, top_chunks)
        st.write(answer)
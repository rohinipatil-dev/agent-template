import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
import tiktoken
import numpy as np

# Create OpenAI client
client = OpenAI()

# Create ChromaDB client
db = chromadb.PersistentClient(path="./chroma_db")

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
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
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

def store_embeddings(chunks, embeddings):
    for i in range(len(chunks)):
        db.insert(chunks[i], embeddings[i])

def retrieve_chunks(query):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding
    results = db.search(query_embedding, k=3)
    return [result[0] for result in results]

def generate_answer(context, query):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for chunk in context:
        messages.append({"role": "user", "content": chunk})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    st.title("AI Agent with RAG")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)
        store_embeddings(chunks, embeddings)
        query = st.text_input("Enter your question")
        if st.button("Answer"):
            context = retrieve_chunks(query)
            answer = generate_answer(context, query)
            st.write(answer)

if __name__ == "__main__":
    main()
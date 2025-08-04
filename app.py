import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from chromadb import PersistentClient
from tiktoken import Tokenizer
import numpy as np

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB client
chroma_db = PersistentClient(path="./chroma_db")

# Define the tokenizer
tokenizer = Tokenizer()

# Define the text embedding model
text_embedding_model = "text-embedding-3-small"

def extract_text_from_pdf(file):
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
            model=text_embedding_model,
            text=chunk
        )
        embeddings.append(response.embedding)
    return embeddings

def store_embeddings(embeddings, chunks):
    for embedding, chunk in zip(embeddings, chunks):
        chroma_db.add_document(embedding, chunk)

def retrieve_chunks(query):
    query_embedding = client.embeddings.create(
        model=text_embedding_model,
        text=query
    ).embedding
    top_chunks = chroma_db.get_nearest(query_embedding, k=3)
    return [chunk for _, chunk in top_chunks]

def generate_answer(query, chunks):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    st.title("AI Document Assistant")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)
        store_embeddings(embeddings, chunks)
        st.success("Document processed and ready for queries.")
        query = st.text_input("Enter your query")
        if st.button("Get Answer"):
            chunks = retrieve_chunks(query)
            answer = generate_answer(query, chunks)
            st.write(answer)

if __name__ == "__main__":
    main()
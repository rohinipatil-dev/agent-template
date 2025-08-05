import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
from tiktoken import Tokenizer, models
import openai

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB
db = chromadb.PersistentClient(path="./chroma_db")

# Initialize Tokenizer
tokenizer = Tokenizer(models.WordLevel())

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
            model="text-embedding-3-small",
            documents=[{"text": chunk}]
        )
        embeddings.append(response.embeddings[0].embedding)
    return embeddings

def store_embeddings(embeddings, chunks):
    for i, embedding in enumerate(embeddings):
        db.add_document(embedding, chunks[i])

def process_pdf(file):
    text = extract_text_from_pdf(file)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    store_embeddings(embeddings, chunks)

def retrieve_chunks(query):
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        documents=[{"text": query}]
    ).embeddings[0].embedding
    return db.search(query_embedding, top_k=3)

def generate_answer(query, chunks):
    prompt = "\n".join(chunks) + "\n" + query
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("AI Agent with RAG Model")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        process_pdf(uploaded_file)
        query = st.text_input("Enter your query:")
        if query:
            chunks = retrieve_chunks(query)
            answer = generate_answer(query, chunks)
            st.text(answer)

if __name__ == "__main__":
    main()
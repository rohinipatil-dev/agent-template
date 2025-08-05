import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
import tiktoken

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB client
chroma_db = chromadb.PersistentClient(path="./chroma_db")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
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
        response = client.text_embedding.create(
            model="text-embedding-3-small",
            text=chunk
        )
        embeddings.append(response.embedding)
    return embeddings

# Function to store embeddings in ChromaDB
def store_embeddings(chunks, embeddings):
    for chunk, embedding in zip(chunks, embeddings):
        chroma_db.add_document(embedding, chunk)

# Function to retrieve relevant chunks
def retrieve_chunks(query_embedding):
    results = chroma_db.search(query_embedding, k=3)
    return [result[1] for result in results]

# Function to generate answer
def generate_answer(context, query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title("AI Agent")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)
        store_embeddings(chunks, embeddings)

        query = st.text_input("Enter your query")
        if st.button("Submit"):
            query_embedding = generate_embeddings([query])[0]
            context = retrieve_chunks(query_embedding)
            answer = generate_answer(context, query)
            st.write(answer)

if __name__ == "__main__":
    main()